"""
Precision Database Adapter
Adapts CP2B_Precision_Biogas.db to PanoramaCP2B webapp ParameterSource model

Maps validated scientific data to the existing ParameterSource dataclass
with flattened reference fields for Streamlit compatibility.
"""

import sqlite3
from typing import List, Optional
from pathlib import Path

from src.models.reference_models import ParameterSource


class PrecisionDatabaseAdapter:
    """
    Adapter for CP2B Precision Biogas validation database.

    Converts validated parameters from CP2B_Precision_Biogas.db
    to ParameterSource objects expected by Page 2 UI.

    Database Schema:
        - chemical_parameters: Validated parameter measurements
        - scientific_papers: Source paper metadata
        - residue_types: Residue definitions with webapp code mapping
    """

    # Path to validated precision database
    DB_PATH = Path(__file__).parent.parent.parent / "data" / "CP2B_Precision_Biogas.db"

    # Webapp residue codes → Precision DB residue_id mapping
    RESIDUE_MAPPING = {
        'VINHACA': 4,           # Legacy code
        'CANA_VINHACA': 4,      # Standard webapp code
        'BAGACO': 6,            # Webapp code for sugarcane bagasse
        'CANA_BAGACO': 6,       # Alternative code
        'PALHA': 5,             # Webapp code for sugarcane straw
        'CANA_PALHA': 5,        # Alternative code
        'TORTA': 7,             # Webapp code for filter cake
        'CANA_TORTA_FILTRO': 7, # Alternative code
        'CASCAS_CITROS': 8,     # Webapp code for citrus peel
        'CITRUS_CASCA': 8,      # Precision DB code
        'BAGACO_CITROS': 9,     # Webapp code for citrus bagasse
        'CITRUS_BAGACO': 9,     # Precision DB code
        'POLPA_CITROS': 8,      # Webapp code (map to peel for now)
        'EUCALIPTO': 1,
        'EUCALIPTO_CASCA': 1,
        'CAMA_FRANGO': 2,
        'AVES_CAMA': 2,         # Legacy code
        'DEJETOS_SUINO': 3,
        'SUINO_DEJETO': 3,      # Legacy code
        # Future residues will be added as validated
    }

    # Parameter categories for webapp display
    PARAMETER_CATEGORIES = {
        'BMP': 'Biogas',
        'METHANE_CONTENT': 'Biogas',
        'METHANE_YIELD': 'Biogas',
        'COD': 'Chemical',
        'BOD': 'Chemical',
        'TAN': 'Chemical',
        'NITROGEN': 'Chemical',
        'CARBON': 'Chemical',
        'CN_RATIO': 'Chemical',
        'PHOSPHORUS': 'Chemical',
        'POTASSIUM': 'Chemical',
        'PROTEIN': 'Chemical',
        'LIPIDS': 'Chemical',
        'CARBOHYDRATES': 'Chemical',
        'pH': 'Physical',
        'TS': 'Physical',
        'VS': 'Physical',
        'MOISTURE': 'Physical',
        'DENSITY': 'Physical',
        'CELLULOSE': 'Structural',
        'HEMICELLULOSE': 'Structural',
        'LIGNIN': 'Structural',
        'FIBER': 'Structural',
        'ASH': 'Chemical',
    }

    @classmethod
    def load_parameter_sources(
        cls,
        residue_code: str,
        parameter_name: str
    ) -> List[ParameterSource]:
        """
        Load validated parameter sources in ParameterSource format.

        Queries precision database and converts rows to ParameterSource objects
        with all required fields properly mapped.

        Args:
            residue_code: Webapp residue code (e.g., 'CANA_VINHACA', 'VINHACA')
            parameter_name: Parameter name (e.g., 'COD', 'pH', 'BMP', 'TS')

        Returns:
            List[ParameterSource]: List of validated parameter measurements
                                   with full source traceability.
                                   Returns empty list if residue not in DB
                                   or no validated data found.

        Examples:
            >>> sources = PrecisionDatabaseAdapter.load_parameter_sources('VINHACA', 'COD')
            >>> len(sources)
            55  # 55 validated COD measurements for vinasse
            >>> sources[0].reference_citation_short
            'España-Gamboa et al. (2012)'
            >>> sources[0].value_mean
            46.12
        """
        # Map webapp code to database residue_id
        residue_id = cls.RESIDUE_MAPPING.get(residue_code)

        if residue_id is None:
            # Residue not yet validated in precision database
            return []

        # Connect to precision database
        conn = sqlite3.connect(cls.DB_PATH)
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()

        # Query validated parameters with full paper metadata
        # UPDATED: Use COALESCE to prefer standardized values with fallback
        query = """
            SELECT
                -- Parameter fields (use standardized if available, fallback to original)
                cp.param_id,
                cp.parameter_name,
                cp.value_min,
                COALESCE(cp.value_standardized, cp.value_mean) as value_mean,
                cp.value_max,
                COALESCE(cp.unit_standardized, cp.unit) as unit,
                cp.page_number,
                cp.context_excerpt,
                cp.validation_classification,

                -- Paper metadata fields
                sp.paper_id,
                sp.codename,
                sp.authors,
                sp.publication_year,
                sp.title,
                sp.doi,
                sp.sector,
                sp.pdf_path,
                sp.validation_status

            FROM chemical_parameters cp
            JOIN scientific_papers sp ON cp.paper_id = sp.paper_id
            WHERE cp.residue_id = ?
              AND cp.parameter_name = ?
              AND cp.is_validated = 1
            ORDER BY sp.publication_year DESC, sp.authors ASC
        """

        cursor.execute(query, (residue_id, parameter_name))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        # Convert database rows to ParameterSource objects
        sources = []

        for row in rows:
            # Generate citation short (format: "Authors (Year)")
            authors = row['authors'] or 'Unknown'
            year = row['publication_year'] or 0
            citation_short = f"{authors} ({year})"

            # Map database row to ParameterSource with EXACT field names
            source = ParameterSource(
                # === PARAMETER IDENTIFICATION ===
                parameter_name=row['parameter_name'],
                parameter_category=cls.PARAMETER_CATEGORIES.get(
                    row['parameter_name'],
                    'Other'
                ),

                # === VALUE INFORMATION (STANDARDIZED) ===
                value_min=row['value_min'],
                value_mean=row['value_mean'],  # Already COALESCE'd in query
                value_max=row['value_max'],
                unit=row['unit'] or 'unitless',  # Already COALESCE'd in query

                # === SAMPLE STATISTICS ===
                n_samples=1,  # Each row is one measurement
                std_deviation=None,  # Not stored in precision DB

                # === FLATTENED REFERENCE FIELDS ===
                reference_id=row['paper_id'],
                reference_codename=row['codename'],
                reference_citation_short=citation_short,
                reference_title=row['title'],
                reference_authors=row['authors'],
                reference_publication_year=row['publication_year'],
                reference_doi=row['doi'],
                reference_pdf_path=row['pdf_path'] or '',
                reference_sector_full=cls._get_sector_full(row['sector']),
                reference_data_quality=row['validation_status'] or 'High',
                reference_metadata_complete=True,

                # === SOURCE TRACEABILITY ===
                page_number=row['page_number'],

                # === QUALITY INDICATORS ===
                data_quality='High',  # All validated data is high quality
                extraction_method=row['validation_classification'],  # Manual, Automated, etc.
                confidence_score=1.0,  # All validated = 100% confidence

                # === MEASUREMENT CONTEXT ===
                measurement_conditions=row['context_excerpt'],  # Text context from paper
                substrate_type=None  # Not stored separately
            )

            sources.append(source)

        return sources

    @classmethod
    def _get_sector_full(cls, sector_code: Optional[str]) -> str:
        """
        Convert sector code to full display name.

        Args:
            sector_code: Short code like 'Cana', 'AG_CANA_VINHACA', 'Eucalipto', etc.

        Returns:
            str: Full sector name for display
        """
        if not sector_code:
            return 'Unknown'

        # Handle both short codes and full webapp codes
        sector_map = {
            'Cana': 'Agricultura - Cana-de-açúcar',
            'AG_CANA_VINHACA': 'Agricultura - Cana-de-açúcar',
            'AG_CANA': 'Agricultura - Cana-de-açúcar',
            'Eucalipto': 'Florestal - Eucalipto',
            'FL_EUCALIPTO': 'Florestal - Eucalipto',
            'Frango': 'Pecuária - Avicultura',
            'PEC_AVES': 'Pecuária - Avicultura',
            'PEC_FRANGO': 'Pecuária - Avicultura',
            'Suino': 'Pecuária - Suinocultura',
            'PEC_SUINO': 'Pecuária - Suinocultura',
        }
        return sector_map.get(sector_code, sector_code)

    @classmethod
    def get_available_parameters(cls, residue_code: str) -> List[str]:
        """
        Get list of validated parameters available for a residue.

        Args:
            residue_code: Webapp residue code

        Returns:
            List[str]: List of parameter names with validated data
                       e.g., ['COD', 'pH', 'TS', 'VS', 'NITROGEN', ...]

        Examples:
            >>> params = PrecisionDatabaseAdapter.get_available_parameters('VINHACA')
            >>> len(params)
            18  # 18 different parameter types validated for vinasse
            >>> 'COD' in params
            True
        """
        residue_id = cls.RESIDUE_MAPPING.get(residue_code)

        if residue_id is None:
            return []

        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()

        query = """
            SELECT DISTINCT parameter_name
            FROM chemical_parameters
            WHERE residue_id = ? AND is_validated = 1
            ORDER BY parameter_name ASC
        """

        cursor.execute(query, (residue_id,))
        params = [row[0] for row in cursor.fetchall()]
        conn.close()

        return params

    @classmethod
    def get_parameter_count(cls, residue_code: str, parameter_name: str) -> int:
        """
        Count how many validated measurements exist for a parameter.

        Args:
            residue_code: Webapp residue code
            parameter_name: Parameter name

        Returns:
            int: Number of validated measurements
        """
        residue_id = cls.RESIDUE_MAPPING.get(residue_code)

        if residue_id is None:
            return 0

        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*)
            FROM chemical_parameters
            WHERE residue_id = ?
              AND parameter_name = ?
              AND is_validated = 1
        """

        cursor.execute(query, (residue_id, parameter_name))
        count = cursor.fetchone()[0]
        conn.close()

        return count

    @classmethod
    def get_database_stats(cls) -> dict:
        """
        Get statistics about the precision database.

        Returns:
            dict: Database statistics including total parameters,
                  papers, and breakdown by residue
        """
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()

        stats = {}

        # Total validated parameters
        cursor.execute("""
            SELECT COUNT(*)
            FROM chemical_parameters
            WHERE is_validated = 1
        """)
        stats['total_validated_parameters'] = cursor.fetchone()[0]

        # Total papers
        cursor.execute("SELECT COUNT(*) FROM scientific_papers")
        stats['total_papers'] = cursor.fetchone()[0]

        # Total residues
        cursor.execute("SELECT COUNT(*) FROM residue_types")
        stats['total_residues'] = cursor.fetchone()[0]

        # Parameters by residue
        cursor.execute("""
            SELECT rt.residue_code, COUNT(*) as count
            FROM chemical_parameters cp
            JOIN residue_types rt ON cp.residue_id = rt.residue_id
            WHERE cp.is_validated = 1
            GROUP BY rt.residue_code
            ORDER BY count DESC
        """)
        stats['parameters_by_residue'] = dict(cursor.fetchall())

        # Parameters by type
        cursor.execute("""
            SELECT parameter_name, COUNT(*) as count
            FROM chemical_parameters
            WHERE is_validated = 1
            GROUP BY parameter_name
            ORDER BY count DESC
            LIMIT 10
        """)
        stats['top_parameters'] = dict(cursor.fetchall())

        conn.close()
        return stats
