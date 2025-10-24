"""
Parameter Service - SOLID SRP (Single Responsibility Principle)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Service layer for parameter queries with full source traceability.
Every parameter value traces back to source paper + page number.

Phase 2 - Database Integration

NOTE: Caching is handled at data_handler.py level to avoid Engine serialization issues.
"""

import streamlit as st  # Only for error messages (st.warning, st.error)
import pandas as pd
from sqlalchemy.engine import Engine
from typing import List, Dict, Optional
from collections import defaultdict

from src.models.reference_models import ParameterSource, ScientificReference, ResidueReferenceSummary
from src.services.reference_service import ReferenceService


class ParameterService:
    """
    Service for querying parameter ranges with source traceability.

    Provides access to 7,648 chemical parameters with full traceability
    to source papers and page numbers.

    Architecture:
    - Constructor injection (DB connection)
    - Returns ParameterSource dataclasses with ScientificReference linkage
    - Full traceability: parameter → paper → page number
    - Cached queries for performance
    """

    def __init__(self, db_connection: Engine):
        """
        Initialize service with database connection.

        Args:
            db_connection: SQLAlchemy engine for cp2b_panorama.db
        """
        self.conn = db_connection
        self.ref_service = ReferenceService(db_connection)

    def _row_to_parameter_source(self, row: pd.Series, value_type: str = 'mean') -> Optional[ParameterSource]:
        """
        Convert database row to ParameterSource dataclass with FLATTENED reference fields.

        Args:
            row: Pandas Series from query result
            value_type: Which value to use ('min', 'mean', 'max')

        Returns:
            Optional[ParameterSource]: Parameter source or None if reference missing
        """
        # Determine which reference ID and page number to use
        ref_id_col = f'{value_type}_reference_id'
        page_col = f'{value_type}_page_number'

        ref_id = row.get(ref_id_col)
        page_number = row.get(page_col)

        if pd.isna(ref_id):
            return None

        # Load reference to extract its fields
        reference = self.ref_service.get_reference_by_id(int(ref_id))
        if not reference:
            return None

        return ParameterSource(
            parameter_name=str(row['parameter_name']),
            parameter_category=str(row['parameter_category']) if pd.notna(row.get('parameter_category')) else None,
            value_min=float(row['value_min']) if pd.notna(row.get('value_min')) else None,
            value_mean=float(row['value_mean']) if pd.notna(row.get('value_mean')) else None,
            value_max=float(row['value_max']) if pd.notna(row.get('value_max')) else None,
            unit=str(row['unit']),
            n_samples=int(row['n_samples']) if pd.notna(row.get('n_samples')) else None,
            std_deviation=float(row['std_deviation']) if pd.notna(row.get('std_deviation')) else None,
            # FLATTENED reference fields (extract from reference object)
            reference_id=reference.id,
            reference_codename=reference.codename,
            reference_citation_short=reference.citation_short,
            reference_title=reference.title,
            reference_authors=reference.authors,
            reference_publication_year=reference.publication_year,
            reference_doi=reference.doi,
            reference_pdf_path=reference.pdf_path,
            reference_sector_full=reference.sector_full,
            reference_data_quality=reference.data_quality,
            reference_metadata_complete=reference.metadata_complete,
            page_number=int(page_number) if pd.notna(page_number) else None,
            data_quality=str(row.get('data_quality', 'Medium')),
            extraction_method=str(row['extraction_method']) if pd.notna(row.get('extraction_method')) else None,
            confidence_score=float(row['confidence_score']) if pd.notna(row.get('confidence_score')) else None,
            measurement_conditions=str(row['measurement_conditions']) if pd.notna(row.get('measurement_conditions')) else None,
            substrate_type=str(row['substrate_type']) if pd.notna(row.get('substrate_type')) else None
        )

    def get_parameter_sources(
        self,
        residue_codigo: str,
        parameter_name: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[ParameterSource]:
        """
        Get all sources for a specific parameter of a residue.

        Returns all measurements for a parameter (e.g., all BMP values for Vinhaça)
        with complete source traceability. Supports pagination for large result sets.

        Args:
            residue_codigo: Residue code (e.g., 'CANA_VINHACA')
            parameter_name: Parameter name (e.g., 'BMP', 'TS', 'VS')
            limit: Maximum number of results to return (None = all)
            offset: Number of results to skip (for pagination)

        Returns:
            List[ParameterSource]: All sources with references and page numbers

        Example:
            >>> # Get all sources
            >>> sources = service.get_parameter_sources('CANA_VINHACA', 'BMP')
            >>>
            >>> # Get first 10 sources (pagination)
            >>> sources_page1 = service.get_parameter_sources('CANA_VINHACA', 'BMP', limit=10, offset=0)
            >>> sources_page2 = service.get_parameter_sources('CANA_VINHACA', 'BMP', limit=10, offset=10)
        """
        try:
            query = """
                SELECT * FROM parameter_ranges
                WHERE residue_codigo = ?
                  AND parameter_name = ?
                ORDER BY data_quality DESC, value_mean DESC
            """

            # Add pagination if requested
            if limit is not None:
                query += f" LIMIT {limit} OFFSET {offset}"

            df = pd.read_sql_query(query, self.conn, params=[residue_codigo, parameter_name])

            sources = []
            for _, row in df.iterrows():
                # Create source for mean value (most common case)
                if pd.notna(row.get('mean_reference_id')):
                    source = self._row_to_parameter_source(row, value_type='mean')
                    if source:
                        sources.append(source)

            return sources
        except Exception as e:
            st.warning(f"Erro ao carregar fontes de {parameter_name} para {residue_codigo}: {str(e)}")
            return []

    def get_parameters_by_residue(
        self,
        residue_codigo: str,
        include_all_values: bool = False
    ) -> Dict[str, List[ParameterSource]]:
        """
        Get all parameters for a residue, grouped by parameter name.

        Args:
            residue_codigo: Residue code
            include_all_values: If True, include min/max sources in addition to mean

        Returns:
            Dict[str, List[ParameterSource]]: Parameter name → list of sources

        Example:
            >>> params = service.get_parameters_by_residue('CANA_VINHACA')
            >>> params.keys()
            dict_keys(['BMP', 'TS', 'VS', 'pH', 'COD', 'TAN'])
            >>> len(params['BMP'])
            15  # 15 different BMP measurements from various papers
        """
        try:
            query = """
                SELECT * FROM parameter_ranges
                WHERE residue_codigo = ?
                ORDER BY parameter_name, data_quality DESC
            """
            df = pd.read_sql_query(query, self.conn, params=[residue_codigo])

            params_dict = defaultdict(list)

            for _, row in df.iterrows():
                param_name = str(row['parameter_name'])

                # Always include mean value
                if pd.notna(row.get('mean_reference_id')):
                    source = self._row_to_parameter_source(row, value_type='mean')
                    if source:
                        params_dict[param_name].append(source)

                if include_all_values:
                    # Also include min and max if different references
                    if pd.notna(row.get('min_reference_id')) and row['min_reference_id'] != row.get('mean_reference_id'):
                        source = self._row_to_parameter_source(row, value_type='min')
                        if source:
                            params_dict[param_name].append(source)

                    if pd.notna(row.get('max_reference_id')) and row['max_reference_id'] != row.get('mean_reference_id'):
                        source = self._row_to_parameter_source(row, value_type='max')
                        if source:
                            params_dict[param_name].append(source)

            return dict(params_dict)
        except Exception as e:
            st.error(f"Erro ao carregar parâmetros para {residue_codigo}: {str(e)}")
            return {}

    def get_parameter_statistics(self, residue_codigo: str) -> Dict[str, Dict]:
        """
        Get statistical summary for all parameters of a residue.

        Useful for Page 2 parameter overview.

        Args:
            residue_codigo: Residue code

        Returns:
            Dict[str, Dict]: Parameter name → statistics dict
                Statistics dict contains:
                - paper_count: Number of papers
                - min_value: Minimum across all sources
                - mean_value: Average across all sources
                - max_value: Maximum across all sources
                - unit: Measurement unit
                - avg_quality: Average quality score (High=3, Medium=2, Low=1)

        Example:
            >>> stats = service.get_parameter_statistics('CANA_VINHACA')
            >>> stats['BMP']
            {
                'paper_count': 15,
                'min_value': 180.0,
                'mean_value': 260.5,
                'max_value': 350.0,
                'unit': 'ml CH₄/g VS',
                'avg_quality': 2.7
            }
        """
        try:
            query = """
                SELECT
                    pr.parameter_name,
                    COUNT(DISTINCT pr.mean_reference_id) as paper_count,
                    MIN(pr.value_mean) as min_value,
                    AVG(pr.value_mean) as mean_value,
                    MAX(pr.value_mean) as max_value,
                    pr.unit,
                    AVG(CASE pr.data_quality
                        WHEN 'high' THEN 3
                        WHEN 'High' THEN 3
                        WHEN 'medium' THEN 2
                        WHEN 'Medium' THEN 2
                        ELSE 1 END) as avg_quality
                FROM parameter_ranges pr
                WHERE pr.residue_codigo = ?
                GROUP BY pr.parameter_name, pr.unit
                ORDER BY pr.parameter_name
            """
            df = pd.read_sql_query(query, self.conn, params=[residue_codigo])

            stats_dict = {}
            for _, row in df.iterrows():
                param_name = str(row['parameter_name'])
                stats_dict[param_name] = {
                    'paper_count': int(row['paper_count']),
                    'min_value': float(row['min_value']) if pd.notna(row['min_value']) else None,
                    'mean_value': float(row['mean_value']) if pd.notna(row['mean_value']) else None,
                    'max_value': float(row['max_value']) if pd.notna(row['max_value']) else None,
                    'unit': str(row['unit']),
                    'avg_quality': float(row['avg_quality']) if pd.notna(row['avg_quality']) else 2.0
                }

            return stats_dict
        except Exception as e:
            st.warning(f"Erro ao carregar estatísticas de parâmetros para {residue_codigo}: {str(e)}")
            return {}

    def compare_parameters_across_residues(
        self,
        parameter_name: str,
        residue_list: List[str]
    ) -> pd.DataFrame:
        """
        Compare a parameter across multiple residues.

        Args:
            parameter_name: Parameter to compare (e.g., 'BMP')
            residue_list: List of residue codes

        Returns:
            pd.DataFrame: Comparison table with columns:
                - residue_codigo
                - residue_name (if available)
                - min_value
                - mean_value
                - max_value
                - paper_count
                - unit

        Example:
            >>> df = service.compare_parameters_across_residues(
            ...     'BMP',
            ...     ['CANA_VINHACA', 'SUINO_DEJETO', 'CAFE_CASCA']
            ... )
        """
        if not residue_list:
            return pd.DataFrame()

        placeholders = ','.join(['?'] * len(residue_list))
        query = f"""
            SELECT
                pr.residue_codigo,
                MIN(pr.value_mean) as min_value,
                AVG(pr.value_mean) as mean_value,
                MAX(pr.value_mean) as max_value,
                COUNT(DISTINCT pr.mean_reference_id) as paper_count,
                pr.unit
            FROM parameter_ranges pr
            WHERE pr.parameter_name = ?
              AND pr.residue_codigo IN ({placeholders})
            GROUP BY pr.residue_codigo, pr.unit
            ORDER BY mean_value DESC
        """

        params = [parameter_name] + residue_list
        df = pd.read_sql_query(query, self.conn, params=params)

        return df

    def get_residue_reference_summary(self, residue_codigo: str) -> Optional[ResidueReferenceSummary]:
        """
        Get comprehensive reference summary for a residue.

        Args:
            residue_codigo: Residue code

        Returns:
            Optional[ResidueReferenceSummary]: Summary or None if residue not found

        Example:
            >>> summary = service.get_residue_reference_summary('SUINO_DEJETO')
            >>> summary.paper_count
            78
            >>> summary.parameter_count
            1246
            >>> summary.coverage_score
            100.0  # Has all expected parameters
        """
        # Get basic counts
        count_query = """
            SELECT
                COUNT(DISTINCT rr.reference_id) as paper_count,
                COUNT(DISTINCT pr.id) as parameter_count
            FROM residue_references rr
            LEFT JOIN parameter_ranges pr ON rr.residue_codigo = pr.residue_codigo
            WHERE rr.residue_codigo = ?
        """
        counts = pd.read_sql_query(count_query, self.conn, params=[residue_codigo])

        if counts.empty or counts.iloc[0]['paper_count'] == 0:
            return None

        paper_count = int(counts.iloc[0]['paper_count'])
        parameter_count = int(counts.iloc[0]['parameter_count'])

        # Get primary sources (papers providing 3+ parameters)
        primary_query = """
            SELECT COUNT(DISTINCT rr.reference_id) as primary_count
            FROM residue_references rr
            WHERE rr.residue_codigo = ?
              AND rr.parameter_count >= 3
        """
        primary_df = pd.read_sql_query(primary_query, self.conn, params=[residue_codigo])
        primary_count = int(primary_df.iloc[0]['primary_count']) if not primary_df.empty else 0

        # Get available parameters
        params_query = """
            SELECT DISTINCT parameter_name
            FROM parameter_ranges
            WHERE residue_codigo = ?
        """
        params_df = pd.read_sql_query(params_query, self.conn, params=[residue_codigo])
        parameters_available = params_df['parameter_name'].tolist()

        # Expected parameters (standard set)
        expected_params = ['BMP', 'TS', 'VS', 'pH', 'COD', 'CN_RATIO']
        parameters_missing = [p for p in expected_params if p not in parameters_available]

        # Get quality distribution
        quality_query = """
            SELECT
                sr.data_quality,
                COUNT(DISTINCT sr.id) as count
            FROM residue_references rr
            JOIN scientific_references sr ON rr.reference_id = sr.id
            WHERE rr.residue_codigo = ?
            GROUP BY sr.data_quality
        """
        quality_df = pd.read_sql_query(quality_query, self.conn, params=[residue_codigo])

        high_quality_count = 0
        medium_quality_count = 0
        low_quality_count = 0

        for _, row in quality_df.iterrows():
            quality = str(row['data_quality']).lower()
            count = int(row['count'])
            if 'high' in quality or 'validated' in quality:
                high_quality_count += count
            elif 'medium' in quality:
                medium_quality_count += count
            else:
                low_quality_count += count

        # Get metadata completeness
        metadata_query = """
            SELECT COUNT(DISTINCT sr.id) as metadata_count
            FROM residue_references rr
            JOIN scientific_references sr ON rr.reference_id = sr.id
            WHERE rr.residue_codigo = ?
              AND sr.metadata_complete = 1
        """
        metadata_df = pd.read_sql_query(metadata_query, self.conn, params=[residue_codigo])
        papers_with_metadata = int(metadata_df.iloc[0]['metadata_count']) if not metadata_df.empty else 0

        # Get residue name and sector (from residuos table if available)
        residue_info_query = """
            SELECT nome, setor
            FROM residuos
            WHERE codigo = ?
        """
        residue_info = pd.read_sql_query(residue_info_query, self.conn, params=[residue_codigo])

        residue_name = residue_codigo  # Fallback
        sector = "Unknown"

        if not residue_info.empty:
            residue_name = str(residue_info.iloc[0]['nome'])
            sector = str(residue_info.iloc[0]['setor'])

        return ResidueReferenceSummary(
            residue_codigo=residue_codigo,
            residue_name=residue_name,
            sector=sector,
            paper_count=paper_count,
            parameter_count=parameter_count,
            primary_sources_count=primary_count,
            parameters_available=parameters_available,
            parameters_missing=parameters_missing,
            high_quality_count=high_quality_count,
            medium_quality_count=medium_quality_count,
            low_quality_count=low_quality_count,
            papers_with_metadata=papers_with_metadata
        )


# ============================================================================
# WRAPPER FUNCTIONS FOR STREAMLIT
# Note: Caching happens at data_handler.py level, not here
# ============================================================================

def load_parameter_sources(
    _conn: Engine,
    residue_codigo: str,
    parameter_name: str
) -> List[ParameterSource]:
    """
    Wrapper for getting parameter sources.

    NOTE: This function is NOT cached. Caching happens in data_handler.py
    to avoid double-caching and Engine serialization issues.

    Args:
        _conn: Database connection
        residue_codigo: Residue code
        parameter_name: Parameter name

    Returns:
        List[ParameterSource]: Sources with traceability
    """
    service = ParameterService(_conn)
    return service.get_parameter_sources(residue_codigo, parameter_name)


def load_parameters_by_residue(
    _conn: Engine,
    residue_codigo: str
) -> Dict[str, List[ParameterSource]]:
    """
    Wrapper for getting all parameters of a residue.

    NOTE: This function is NOT cached. Caching happens in data_handler.py
    to avoid double-caching and Engine serialization issues.

    Args:
        _conn: Database connection
        residue_codigo: Residue code

    Returns:
        Dict: Parameter name → list of sources
    """
    service = ParameterService(_conn)
    return service.get_parameters_by_residue(residue_codigo)


def load_parameter_statistics(
    _conn: Engine,
    residue_codigo: str
) -> Dict[str, Dict]:
    """
    Wrapper for parameter statistics.

    NOTE: This function is NOT cached. Caching happens in data_handler.py
    to avoid double-caching and Engine serialization issues.

    Args:
        _conn: Database connection
        residue_codigo: Residue code

    Returns:
        Dict: Parameter statistics
    """
    service = ParameterService(_conn)
    return service.get_parameter_statistics(residue_codigo)
