"""
Reference Data Models - SOLID SRP (Single Responsibility Principle)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

This module contains immutable dataclass definitions for scientific references
and parameter sources with full traceability.

Phase 2 - Database Integration
Connects to cp2b_panorama.db (674 papers, 7,648 parameters)
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path


class AttributeDict(dict):
    """
    Dictionary subclass that allows attribute-style access.

    Enables both dict-style and attribute-style access:
        d['key'] and d.key both work

    This is used by ParameterSource.reference property to support
    Page 2 UI code that expects object attribute access (source.reference.citation_short)
    while maintaining dict compatibility.

    Examples:
        >>> d = AttributeDict({'name': 'test', 'value': 123})
        >>> d['name']
        'test'
        >>> d.name
        'test'
        >>> d.value
        123
    """
    def __getattr__(self, key: str) -> Any:
        """Allow attribute-style access to dict keys"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            )

    def __setattr__(self, key: str, value: Any) -> None:
        """Allow attribute-style assignment to dict keys"""
        self[key] = value

    def __delattr__(self, key: str) -> None:
        """Allow attribute-style deletion of dict keys"""
        try:
            del self[key]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{key}'"
            )


@dataclass(frozen=True)
class ScientificReference:
    """
    Immutable scientific paper reference with citation generation.

    Represents a single scientific paper from the cp2b_panorama.db database.
    Provides methods for citation formatting and metadata access.
    """
    # Primary keys
    id: int
    paper_id: Optional[int]  # Link to validation database

    # Systematic identification
    codename: str  # P0001_AG_CANA_2003
    codename_short: Optional[str]  # AG_CANA_001

    # File management
    pdf_filename: str  # P0001_AG_CANA_2003.pdf
    pdf_path: str  # Full path to PDF
    original_filename: Optional[str]

    # Classification
    sector: Optional[str]  # AG_CANA, PEC_SUINO, etc.
    sector_full: Optional[str]  # Agricultura - Cana-de-açúcar
    primary_residue: Optional[str]
    query_folder: Optional[str]

    # Bibliographic metadata
    authors: Optional[str]
    publication_year: Optional[int]
    journal: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]
    doi: Optional[str]
    title: Optional[str]
    abstract: Optional[str]
    keywords: Optional[str]  # JSON array

    # Additional identifiers
    scopus_id: Optional[str]
    pubmed_id: Optional[str]
    google_scholar_link: Optional[str]

    # Quality tracking
    data_quality: str = "Validated"
    extraction_complete: bool = True
    metadata_complete: bool = False
    verified_by: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    # Notes
    notes: Optional[str] = None

    @property
    def citation_short(self) -> str:
        """
        Generate short citation format: First Author et al. (Year)

        Returns:
            str: Short citation, e.g., "Silva et al. (2020)"

        Examples:
            >>> ref.citation_short
            'Silva et al. (2020)'
            >>> ref_no_metadata.citation_short
            'P0001_AG_CANA_2003'
        """
        if not self.authors or not self.publication_year:
            # Fallback to codename if metadata incomplete
            return self.codename

        # Extract first author's last name
        first_author = self.authors.split(';')[0].strip()
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip()
        else:
            # If no comma, assume last word is last name
            last_name = first_author.split()[-1]

        # Check if multiple authors
        if ';' in self.authors or ' and ' in self.authors.lower():
            return f"{last_name} et al. ({self.publication_year})"
        else:
            return f"{last_name} ({self.publication_year})"

    @property
    def citation_apa(self) -> str:
        """
        Generate APA-style citation.

        Returns:
            str: APA citation format

        Examples:
            >>> ref.citation_apa
            'Silva, J., Santos, M. (2020). Biogas production from vinasse. Bioresource Technology, 280, 123-130.'
        """
        if not self.has_metadata:
            return f"{self.codename} (metadata incomplete)"

        parts = []

        # Authors (Year)
        if self.authors:
            authors_formatted = self.authors.replace(';', ',')
            parts.append(f"{authors_formatted} ({self.publication_year}).")
        elif self.publication_year:
            parts.append(f"({self.publication_year}).")

        # Title
        if self.title:
            parts.append(f"{self.title}.")

        # Journal, volume, issue, pages
        if self.journal:
            journal_part = self.journal
            if self.volume:
                journal_part += f", {self.volume}"
            if self.issue:
                journal_part += f"({self.issue})"
            if self.pages:
                journal_part += f", {self.pages}"
            parts.append(f"{journal_part}.")

        # DOI
        if self.doi:
            parts.append(f"https://doi.org/{self.doi}")

        return " ".join(parts)

    @property
    def has_metadata(self) -> bool:
        """
        Check if paper has complete bibliographic metadata.

        Returns:
            bool: True if authors, year, and title are present
        """
        return all([
            self.authors is not None,
            self.publication_year is not None,
            self.title is not None
        ])

    @property
    def pdf_exists(self) -> bool:
        """
        Check if PDF file exists at specified path.

        Returns:
            bool: True if PDF file exists
        """
        return Path(self.pdf_path).exists()

    @property
    def external_url(self) -> Optional[str]:
        """
        Get external URL for paper (DOI or Google Scholar).

        Returns:
            Optional[str]: URL string or None
        """
        if self.doi:
            return f"https://doi.org/{self.doi}"
        elif self.google_scholar_link:
            return self.google_scholar_link
        return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dict: All fields as dictionary (complete for reconstruction)
        """
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'codename': self.codename,
            'codename_short': self.codename_short,
            'pdf_filename': self.pdf_filename,
            'pdf_path': self.pdf_path,
            'original_filename': self.original_filename,
            'sector': self.sector,
            'sector_full': self.sector_full,
            'primary_residue': self.primary_residue,
            'query_folder': self.query_folder,
            'authors': self.authors,
            'publication_year': self.publication_year,
            'journal': self.journal,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'doi': self.doi,
            'title': self.title,
            'abstract': self.abstract,
            'keywords': self.keywords,
            'scopus_id': self.scopus_id,
            'pubmed_id': self.pubmed_id,
            'google_scholar_link': self.google_scholar_link,
            'data_quality': self.data_quality,
            'extraction_complete': self.extraction_complete,
            'metadata_complete': self.metadata_complete,
            'verified_by': self.verified_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'notes': self.notes
        }


@dataclass(frozen=True)
class ParameterSource:
    """
    Parameter value with full source traceability.

    Represents a single parameter measurement (BMP, TS, VS, etc.)
    with complete traceability to source paper and page number.

    NOTE: Reference fields are FLATTENED (not nested dataclass) to avoid
    Streamlit serialization issues with frozen nested dataclasses.
    """
    # Parameter identification
    parameter_name: str  # BMP, TS, VS, pH, COD, etc.
    parameter_category: Optional[str]  # Chemical, Operational, Physical

    # Value information
    value_min: Optional[float]
    value_mean: Optional[float]
    value_max: Optional[float]
    unit: str

    # Sample statistics
    n_samples: Optional[int]
    std_deviation: Optional[float]

    # Source traceability - FLATTENED (primitive types only)
    reference_id: int
    reference_codename: str
    reference_citation_short: str
    reference_title: Optional[str]
    reference_authors: Optional[str]
    reference_publication_year: Optional[int]
    reference_doi: Optional[str]
    reference_pdf_path: str
    reference_sector_full: Optional[str]
    reference_data_quality: str
    reference_metadata_complete: bool
    page_number: Optional[int]  # Page where value was found

    # Quality indicators
    data_quality: str  # High, Medium, Low
    extraction_method: Optional[str]  # Pass1, Pass2, etc.
    confidence_score: Optional[float]  # 0.0 to 1.0

    # Measurement context
    measurement_conditions: Optional[str]
    substrate_type: Optional[str]

    @property
    def value_display(self) -> str:
        """
        Format value for display with unit.

        Returns:
            str: Formatted value string

        Examples:
            >>> source.value_display
            '250 ± 30 ml CH₄/g VS'
            >>> source_range.value_display
            '200-300 ml CH₄/g VS (mean: 250)'
        """
        if self.value_min is not None and self.value_max is not None and self.value_mean is not None:
            # Full range with mean
            return f"{self.value_min:.1f}-{self.value_max:.1f} {self.unit} (média: {self.value_mean:.1f})"
        elif self.value_mean is not None and self.std_deviation is not None:
            # Mean with standard deviation
            return f"{self.value_mean:.1f} ± {self.std_deviation:.1f} {self.unit}"
        elif self.value_mean is not None:
            # Mean only
            return f"{self.value_mean:.1f} {self.unit}"
        elif self.value_min is not None and self.value_max is not None:
            # Range without mean
            return f"{self.value_min:.1f}-{self.value_max:.1f} {self.unit}"
        else:
            return f"N/A {self.unit}"

    @property
    def reference(self) -> AttributeDict:
        """
        Return reference info as AttributeDict for full compatibility.

        This property allows BOTH access styles:
        - Dict-style: source.reference['citation_short']
        - Attribute-style: source.reference.citation_short (required by Page 2 UI)

        Returns:
            AttributeDict: Reference information with all fields,
                          supports both dict and attribute access

        Examples:
            >>> source.reference['citation_short']
            'Silva et al. (2020)'
            >>> source.reference.citation_short  # Same thing!
            'Silva et al. (2020)'
        """
        return AttributeDict({
            'id': self.reference_id,
            'codename': self.reference_codename,
            'citation_short': self.reference_citation_short,
            'title': self.reference_title,
            'authors': self.reference_authors,
            'publication_year': self.reference_publication_year,
            'doi': self.reference_doi,
            'pdf_path': self.reference_pdf_path,
            'sector_full': self.reference_sector_full,
            'data_quality': self.reference_data_quality,
            'metadata_complete': self.reference_metadata_complete
        })

    @property
    def source_citation(self) -> str:
        """
        Get formatted source citation with page number.

        Returns:
            str: Citation with page reference

        Examples:
            >>> source.source_citation
            'Silva et al. (2020), p. 15'
        """
        citation = self.reference_citation_short
        if self.page_number:
            return f"{citation}, p. {self.page_number}"
        return citation

    @property
    def quality_badge(self) -> str:
        """
        Get emoji badge for data quality.

        Returns:
            str: Emoji representing quality level
        """
        quality_map = {
            'high': '⭐⭐⭐',
            'medium': '⭐⭐',
            'low': '⭐'
        }
        return quality_map.get(self.data_quality.lower(), '⚠️')

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dict: All fields as dictionary
        """
        return {
            'parameter_name': self.parameter_name,
            'parameter_category': self.parameter_category,
            'value_min': self.value_min,
            'value_mean': self.value_mean,
            'value_max': self.value_max,
            'unit': self.unit,
            'value_display': self.value_display,
            'n_samples': self.n_samples,
            'std_deviation': self.std_deviation,
            # Flattened reference fields
            'reference_id': self.reference_id,
            'reference_codename': self.reference_codename,
            'reference_citation_short': self.reference_citation_short,
            'reference_title': self.reference_title,
            'reference_authors': self.reference_authors,
            'reference_publication_year': self.reference_publication_year,
            'reference_doi': self.reference_doi,
            'reference_pdf_path': self.reference_pdf_path,
            'reference_sector_full': self.reference_sector_full,
            'reference_data_quality': self.reference_data_quality,
            'reference_metadata_complete': self.reference_metadata_complete,
            'source_citation': self.source_citation,
            'page_number': self.page_number,
            'data_quality': self.data_quality,
            'quality_badge': self.quality_badge,
            'extraction_method': self.extraction_method,
            'confidence_score': self.confidence_score,
            'measurement_conditions': self.measurement_conditions,
            'substrate_type': self.substrate_type
        }


@dataclass(frozen=True)
class ResidueReferenceSummary:
    """
    Summary statistics for references of a specific residue.

    Provides overview of literature coverage for a residue,
    including paper count, parameter count, and completeness metrics.
    """
    # Residue identification
    residue_codigo: str
    residue_name: str
    sector: str

    # Reference statistics
    paper_count: int  # Total papers linked to this residue
    parameter_count: int  # Total parameter measurements
    primary_sources_count: int  # Papers providing 3+ parameters

    # Parameter coverage
    parameters_available: List[str]  # List of available parameters (BMP, TS, VS, etc.)
    parameters_missing: List[str]  # List of expected but missing parameters

    # Quality metrics
    high_quality_count: int  # Papers with high quality data
    medium_quality_count: int
    low_quality_count: int

    # Metadata completeness
    papers_with_metadata: int  # Papers with complete bibliographic info

    @property
    def coverage_score(self) -> float:
        """
        Calculate coverage score (0-100) based on parameters available.

        Expected parameters: BMP, TS, VS, pH, COD, C:N ratio

        Returns:
            float: Coverage percentage
        """
        expected_params = ['BMP', 'TS', 'VS', 'pH', 'COD', 'CN_RATIO']
        available_count = sum(1 for p in expected_params if p in self.parameters_available)
        return (available_count / len(expected_params)) * 100

    @property
    def completeness_percentage(self) -> float:
        """
        Calculate metadata completeness percentage.

        Returns:
            float: Percentage of papers with complete metadata
        """
        if self.paper_count == 0:
            return 0.0
        return (self.papers_with_metadata / self.paper_count) * 100

    @property
    def quality_distribution(self) -> Dict[str, int]:
        """
        Get quality distribution as dictionary.

        Returns:
            Dict: Quality counts by level
        """
        return {
            'High': self.high_quality_count,
            'Medium': self.medium_quality_count,
            'Low': self.low_quality_count
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dict: All fields and computed properties
        """
        return {
            'residue_codigo': self.residue_codigo,
            'residue_name': self.residue_name,
            'sector': self.sector,
            'paper_count': self.paper_count,
            'parameter_count': self.parameter_count,
            'primary_sources_count': self.primary_sources_count,
            'parameters_available': self.parameters_available,
            'parameters_missing': self.parameters_missing,
            'coverage_score': self.coverage_score,
            'completeness_percentage': self.completeness_percentage,
            'quality_distribution': self.quality_distribution
        }
