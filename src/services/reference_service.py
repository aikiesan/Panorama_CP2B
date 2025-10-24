"""
Reference Service - SOLID SRP (Single Responsibility Principle)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Service layer for scientific reference queries with caching and optimization.
Follows Dependency Inversion Principle - depends on database connection abstraction.

Phase 2 - Database Integration
"""

import streamlit as st
import pandas as pd
from sqlalchemy.engine import Engine
from typing import List, Optional, Dict, Tuple
from datetime import datetime

from src.models.reference_models import ScientificReference


class ReferenceService:
    """
    Service for querying scientific references from cp2b_panorama.db.

    Provides cached, optimized access to the 674 scientific papers
    with full metadata and file path information.

    Architecture:
    - Constructor injection (DB connection)
    - Immutable return types (ScientificReference dataclass)
    - Cached queries for performance (@st.cache_data)
    - Optional returns for not-found cases
    """

    def __init__(self, db_connection: Engine):
        """
        Initialize service with database connection.

        Args:
            db_connection: SQLAlchemy engine for cp2b_panorama.db
        """
        self.conn = db_connection

    def _row_to_reference(self, row: pd.Series) -> ScientificReference:
        """
        Convert database row to ScientificReference dataclass.

        Args:
            row: Pandas Series from query result

        Returns:
            ScientificReference: Immutable reference object
        """
        # Handle datetime conversion
        created_at = None
        last_updated = None

        if pd.notna(row.get('created_at')):
            try:
                created_at = pd.to_datetime(row['created_at'])
            except:
                pass

        if pd.notna(row.get('last_updated')):
            try:
                last_updated = pd.to_datetime(row['last_updated'])
            except:
                pass

        return ScientificReference(
            id=int(row['id']),
            paper_id=int(row['paper_id']) if pd.notna(row.get('paper_id')) else None,
            codename=str(row['codename']),
            codename_short=str(row['codename_short']) if pd.notna(row.get('codename_short')) else None,
            pdf_filename=str(row['pdf_filename']),
            pdf_path=str(row['pdf_path']),
            original_filename=str(row['original_filename']) if pd.notna(row.get('original_filename')) else None,
            sector=str(row['sector']) if pd.notna(row.get('sector')) else None,
            sector_full=str(row['sector_full']) if pd.notna(row.get('sector_full')) else None,
            primary_residue=str(row['primary_residue']) if pd.notna(row.get('primary_residue')) else None,
            query_folder=str(row['query_folder']) if pd.notna(row.get('query_folder')) else None,
            authors=str(row['authors']) if pd.notna(row.get('authors')) else None,
            publication_year=int(row['publication_year']) if pd.notna(row.get('publication_year')) else None,
            journal=str(row['journal']) if pd.notna(row.get('journal')) else None,
            volume=str(row['volume']) if pd.notna(row.get('volume')) else None,
            issue=str(row['issue']) if pd.notna(row.get('issue')) else None,
            pages=str(row['pages']) if pd.notna(row.get('pages')) else None,
            doi=str(row['doi']) if pd.notna(row.get('doi')) else None,
            title=str(row['title']) if pd.notna(row.get('title')) else None,
            abstract=str(row['abstract']) if pd.notna(row.get('abstract')) else None,
            keywords=str(row['keywords']) if pd.notna(row.get('keywords')) else None,
            scopus_id=str(row['scopus_id']) if pd.notna(row.get('scopus_id')) else None,
            pubmed_id=str(row['pubmed_id']) if pd.notna(row.get('pubmed_id')) else None,
            google_scholar_link=str(row['google_scholar_link']) if pd.notna(row.get('google_scholar_link')) else None,
            data_quality=str(row.get('data_quality', 'Validated')),
            extraction_complete=bool(row.get('extraction_complete', True)),
            metadata_complete=bool(row.get('metadata_complete', False)),
            verified_by=str(row['verified_by']) if pd.notna(row.get('verified_by')) else None,
            created_at=created_at,
            last_updated=last_updated,
            notes=str(row['notes']) if pd.notna(row.get('notes')) else None
        )

    def get_all_references(self) -> List[ScientificReference]:
        """
        Get all scientific references from database.

        Returns:
            List[ScientificReference]: All 674 papers

        Example:
            >>> service = ReferenceService(conn)
            >>> refs = service.get_all_references()
            >>> len(refs)
            674
        """
        try:
            query = """
                SELECT * FROM scientific_references
                ORDER BY publication_year DESC, codename
            """
            df = pd.read_sql_query(query, self.conn)
            return [self._row_to_reference(row) for _, row in df.iterrows()]
        except Exception as e:
            st.error(f"Erro ao carregar referências: {str(e)}")
            return []

    def get_references_by_residue(self, residue_codigo: str) -> List[ScientificReference]:
        """
        Get all references for a specific residue.

        Args:
            residue_codigo: Residue code (e.g., 'CANA_VINHACA', 'SUINO_DEJETO')

        Returns:
            List[ScientificReference]: Papers linked to this residue

        Example:
            >>> refs = service.get_references_by_residue('CANA_VINHACA')
            >>> len(refs)  # Should be 34+ for Vinhaça
            34
        """
        try:
            query = """
                SELECT DISTINCT sr.*
                FROM scientific_references sr
                JOIN residue_references rr ON sr.id = rr.reference_id
                WHERE rr.residue_codigo = ?
                ORDER BY sr.publication_year DESC
            """
            df = pd.read_sql_query(query, self.conn, params=[residue_codigo])
            return [self._row_to_reference(row) for _, row in df.iterrows()]
        except Exception as e:
            st.warning(f"Erro ao carregar referências para {residue_codigo}: {str(e)}")
            return []

    def get_reference_by_id(self, reference_id: int) -> Optional[ScientificReference]:
        """
        Get reference by database ID.

        Args:
            reference_id: Database ID from scientific_references.id

        Returns:
            Optional[ScientificReference]: Reference or None if not found
        """
        try:
            query = """
                SELECT * FROM scientific_references
                WHERE id = ?
            """
            df = pd.read_sql_query(query, self.conn, params=[reference_id])

            if len(df) > 0:
                return self._row_to_reference(df.iloc[0])
            return None
        except Exception as e:
            st.warning(f"Erro ao carregar referência ID {reference_id}: {str(e)}")
            return None

    def get_reference_by_codename(self, codename: str) -> Optional[ScientificReference]:
        """
        Quick lookup by codename (P0001_AG_CANA_2003).

        Args:
            codename: Systematic codename

        Returns:
            Optional[ScientificReference]: Reference or None if not found

        Example:
            >>> ref = service.get_reference_by_codename('P0001_AG_CANA_2003')
            >>> ref.codename
            'P0001_AG_CANA_2003'
        """
        try:
            query = """
                SELECT * FROM scientific_references
                WHERE codename = ?
            """
            df = pd.read_sql_query(query, self.conn, params=[codename])

            if len(df) > 0:
                return self._row_to_reference(df.iloc[0])
            return None
        except Exception as e:
            st.warning(f"Erro ao carregar referência {codename}: {str(e)}")
            return None

    def get_papers_with_most_parameters(self, limit: int = 10) -> List[Tuple[ScientificReference, int]]:
        """
        Get papers with most parameter contributions.

        Useful for identifying most valuable papers in database.

        Args:
            limit: Number of top papers to return

        Returns:
            List[Tuple[ScientificReference, int]]: List of (reference, parameter_count)

        Example:
            >>> top_papers = service.get_papers_with_most_parameters(5)
            >>> for ref, count in top_papers:
            ...     print(f"{ref.citation_short}: {count} parameters")
            Silva et al. (2020): 145 parameters
        """
        query = """
            SELECT sr.*, COUNT(pr.id) as param_count
            FROM scientific_references sr
            LEFT JOIN parameter_ranges pr ON sr.id IN (
                pr.min_reference_id, pr.mean_reference_id, pr.max_reference_id
            )
            GROUP BY sr.id
            ORDER BY param_count DESC
            LIMIT ?
        """
        df = pd.read_sql_query(query, self.conn, params=[limit])

        results = []
        for _, row in df.iterrows():
            ref = self._row_to_reference(row)
            param_count = int(row['param_count']) if pd.notna(row['param_count']) else 0
            results.append((ref, param_count))

        return results

    def search_references(self, filters: Dict) -> List[ScientificReference]:
        """
        Search references with multiple filter criteria.

        Args:
            filters: Dictionary with filter keys:
                - sector: str (e.g., 'AG_CANA', 'PEC_SUINO')
                - year_min: int
                - year_max: int
                - data_quality: str ('Validated', 'High', etc.)
                - has_metadata: bool
                - query_text: str (search in title/authors/keywords)

        Returns:
            List[ScientificReference]: Filtered references

        Example:
            >>> refs = service.search_references({
            ...     'sector': 'AG_CANA',
            ...     'year_min': 2015,
            ...     'has_metadata': True
            ... })
        """
        try:
            # Build dynamic query
            conditions = []
            params = []

            if 'sector' in filters and filters['sector']:
                conditions.append("sector = ?")
                params.append(filters['sector'])

            if 'year_min' in filters and filters['year_min']:
                conditions.append("publication_year >= ?")
                params.append(filters['year_min'])

            if 'year_max' in filters and filters['year_max']:
                conditions.append("publication_year <= ?")
                params.append(filters['year_max'])

            if 'data_quality' in filters and filters['data_quality']:
                conditions.append("data_quality = ?")
                params.append(filters['data_quality'])

            if 'has_metadata' in filters and filters['has_metadata']:
                conditions.append("metadata_complete = 1")

            if 'query_text' in filters and filters['query_text']:
                search_text = f"%{filters['query_text']}%"
                conditions.append("(title LIKE ? OR authors LIKE ? OR keywords LIKE ?)")
                params.extend([search_text, search_text, search_text])

            # Build WHERE clause
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            query = f"""
                SELECT * FROM scientific_references
                {where_clause}
                ORDER BY publication_year DESC, codename
            """

            df = pd.read_sql_query(query, self.conn, params=params if params else None)
            return [self._row_to_reference(row) for _, row in df.iterrows()]
        except Exception as e:
            st.error(f"Erro ao buscar referências: {str(e)}")
            return []

    def get_references_by_sector(self, sector_code: str) -> List[ScientificReference]:
        """
        Get all references for a specific sector.

        Args:
            sector_code: Sector code (AG_CANA, PEC_SUINO, UR_RSU, etc.)

        Returns:
            List[ScientificReference]: Papers for this sector

        Example:
            >>> refs = service.get_references_by_sector('AG_CANA')
            >>> len(refs)
            120  # Approximate count for Cana-de-açúcar
        """
        return self.search_references({'sector': sector_code})

    def export_bibtex(self, reference_ids: List[int]) -> str:
        """
        Export references as BibTeX format.

        Args:
            reference_ids: List of reference IDs to export

        Returns:
            str: BibTeX formatted string

        Example:
            >>> bibtex = service.export_bibtex([1, 2, 3])
            >>> print(bibtex)
            @article{Silva2020,
                author = {Silva, J. and Santos, M.},
                title = {Biogas production from vinasse},
                ...
            }
        """
        from src.utils.export_helpers import generate_bibtex

        # Load references
        references = []
        for ref_id in reference_ids:
            ref = self.get_reference_by_id(ref_id)
            if ref:
                references.append(ref)

        return generate_bibtex(references)

    def get_sector_statistics(self) -> pd.DataFrame:
        """
        Get statistics grouped by sector.

        Returns:
            pd.DataFrame: Sector-wise paper counts and metadata status

        Columns:
            - sector
            - paper_count
            - papers_with_metadata
            - avg_year
            - metadata_percentage
        """
        query = """
            SELECT
                sector,
                COUNT(*) as paper_count,
                SUM(metadata_complete) as papers_with_metadata,
                ROUND(AVG(publication_year), 0) as avg_year,
                ROUND(100.0 * SUM(metadata_complete) / COUNT(*), 1) as metadata_percentage
            FROM scientific_references
            WHERE sector IS NOT NULL
            GROUP BY sector
            ORDER BY paper_count DESC
        """
        return pd.read_sql_query(query, self.conn)


# ============================================================================
# CACHED WRAPPER FUNCTIONS FOR STREAMLIT
# ============================================================================

@st.cache_data(ttl=3600, show_spinner="Carregando referências...")
def load_all_references(_conn: Engine) -> List[ScientificReference]:
    """
    Cached wrapper for getting all references.

    Args:
        _conn: Database connection (prefixed with _ to exclude from hash)

    Returns:
        List[ScientificReference]: All papers
    """
    service = ReferenceService(_conn)
    return service.get_all_references()


@st.cache_data(ttl=3600)
def load_references_by_residue(_conn: Engine, residue_codigo: str) -> List[ScientificReference]:
    """
    Cached wrapper for getting references by residue.

    Args:
        _conn: Database connection
        residue_codigo: Residue code

    Returns:
        List[ScientificReference]: Papers for residue
    """
    service = ReferenceService(_conn)
    return service.get_references_by_residue(residue_codigo)


@st.cache_data(ttl=3600)
def search_references_cached(_conn: Engine, **filters) -> List[ScientificReference]:
    """
    Cached wrapper for search_references.

    Args:
        _conn: Database connection
        **filters: Search filters

    Returns:
        List[ScientificReference]: Filtered references
    """
    service = ReferenceService(_conn)
    return service.search_references(filters)
