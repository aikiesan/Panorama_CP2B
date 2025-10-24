"""
Export Helpers - Utility functions for exporting references and parameters
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Supports BibTeX, CSV, and formatted report exports.
Phase 2 - Database Integration
"""

import pandas as pd
from typing import List
from io import StringIO

from src.models.reference_models import ScientificReference, ParameterSource


def generate_bibtex(references: List[ScientificReference]) -> str:
    """
    Generate BibTeX formatted string from references.

    Args:
        references: List of ScientificReference objects

    Returns:
        str: BibTeX formatted citations

    Example:
        >>> bibtex = generate_bibtex(refs)
        >>> print(bibtex)
        @article{Silva2020,
            author = {Silva, J. and Santos, M.},
            title = {Biogas production from vinasse},
            journal = {Bioresource Technology},
            year = {2020},
            volume = {280},
            pages = {123-130},
            doi = {10.1016/j.biortech.2020.123456}
        }
    """
    bibtex_entries = []

    for ref in references:
        # Skip if no metadata
        if not ref.has_metadata:
            continue

        # Generate citation key: FirstAuthorYear
        citation_key = _generate_citation_key(ref)

        # Build BibTeX entry
        entry_lines = [f"@article{{{citation_key},"]

        # Author
        if ref.authors:
            authors_formatted = _format_bibtex_authors(ref.authors)
            entry_lines.append(f"    author = {{{authors_formatted}}},")

        # Title
        if ref.title:
            entry_lines.append(f"    title = {{{ref.title}}},")

        # Journal
        if ref.journal:
            entry_lines.append(f"    journal = {{{ref.journal}}},")

        # Year
        if ref.publication_year:
            entry_lines.append(f"    year = {{{ref.publication_year}}},")

        # Volume
        if ref.volume:
            entry_lines.append(f"    volume = {{{ref.volume}}},")

        # Issue/Number
        if ref.issue:
            entry_lines.append(f"    number = {{{ref.issue}}},")

        # Pages
        if ref.pages:
            entry_lines.append(f"    pages = {{{ref.pages}}},")

        # DOI
        if ref.doi:
            entry_lines.append(f"    doi = {{{ref.doi}}},")

        # Keywords (if available)
        if ref.keywords:
            entry_lines.append(f"    keywords = {{{ref.keywords}}},")

        # Note with codename for traceability
        entry_lines.append(f"    note = {{CP2B Database: {ref.codename}}}")

        entry_lines.append("}")
        entry_lines.append("")  # Blank line between entries

        bibtex_entries.append("\n".join(entry_lines))

    return "\n".join(bibtex_entries)


def _generate_citation_key(ref: ScientificReference) -> str:
    """
    Generate citation key for BibTeX entry.

    Format: FirstAuthorLastNameYear
    Example: Silva2020

    Args:
        ref: ScientificReference

    Returns:
        str: Citation key
    """
    if not ref.authors or not ref.publication_year:
        # Fallback to codename
        return ref.codename.replace('_', '')

    # Extract first author's last name
    first_author = ref.authors.split(';')[0].strip()
    if ',' in first_author:
        last_name = first_author.split(',')[0].strip()
    else:
        # Assume last word is last name
        last_name = first_author.split()[-1]

    # Remove special characters
    last_name = ''.join(c for c in last_name if c.isalnum())

    return f"{last_name}{ref.publication_year}"


def _format_bibtex_authors(authors_str: str) -> str:
    """
    Format author string for BibTeX.

    Converts semicolon-separated or 'and'-separated authors to BibTeX format.

    Args:
        authors_str: Author string (e.g., "Silva, J.; Santos, M.")

    Returns:
        str: BibTeX formatted authors (e.g., "Silva, J. and Santos, M.")
    """
    # Replace semicolons with ' and '
    authors_formatted = authors_str.replace(';', ' and')
    return authors_formatted.strip()


def generate_csv_references(references: List[ScientificReference]) -> str:
    """
    Generate CSV formatted string from references.

    Args:
        references: List of ScientificReference objects

    Returns:
        str: CSV formatted string

    Example:
        >>> csv = generate_csv_references(refs)
        >>> # Can be saved to file or downloaded via Streamlit
    """
    # Convert to list of dicts
    data = []
    for ref in references:
        data.append({
            'Codename': ref.codename,
            'Authors': ref.authors if ref.authors else '',
            'Year': ref.publication_year if ref.publication_year else '',
            'Title': ref.title if ref.title else '',
            'Journal': ref.journal if ref.journal else '',
            'Volume': ref.volume if ref.volume else '',
            'Issue': ref.issue if ref.issue else '',
            'Pages': ref.pages if ref.pages else '',
            'DOI': ref.doi if ref.doi else '',
            'Sector': ref.sector_full if ref.sector_full else ref.sector,
            'PDF_Path': ref.pdf_path,
            'Has_Metadata': 'Yes' if ref.has_metadata else 'No'
        })

    # Convert to DataFrame and then CSV
    df = pd.DataFrame(data)
    return df.to_csv(index=False)


def generate_parameter_report(
    residue_codigo: str,
    residue_name: str,
    parameters_dict: dict
) -> pd.DataFrame:
    """
    Generate comprehensive parameter report for a residue.

    Creates a detailed table with all parameters and their sources.

    Args:
        residue_codigo: Residue code
        residue_name: Residue display name
        parameters_dict: Dict from ParameterService.get_parameters_by_residue()

    Returns:
        pd.DataFrame: Report table with columns:
            - Parameter
            - Value
            - Unit
            - Source
            - Page
            - Quality

    Example:
        >>> params = parameter_service.get_parameters_by_residue('CANA_VINHACA')
        >>> report = generate_parameter_report('CANA_VINHACA', 'Vinhaça', params)
        >>> report.to_excel('vinhaca_parameters.xlsx')
    """
    rows = []

    for param_name, sources in parameters_dict.items():
        for source in sources:
            rows.append({
                'Residue_Code': residue_codigo,
                'Residue_Name': residue_name,
                'Parameter': param_name,
                'Value_Min': source.value_min if source.value_min is not None else '',
                'Value_Mean': source.value_mean if source.value_mean is not None else '',
                'Value_Max': source.value_max if source.value_max is not None else '',
                'Unit': source.unit,
                'Source_Paper': source.reference.codename,
                'Source_Citation': source.reference.citation_short,
                'Page_Number': source.page_number if source.page_number else '',
                'Data_Quality': source.data_quality,
                'Quality_Badge': source.quality_badge,
                'N_Samples': source.n_samples if source.n_samples else '',
                'Measurement_Conditions': source.measurement_conditions if source.measurement_conditions else ''
            })

    df = pd.DataFrame(rows)
    return df


def generate_residue_summary_csv(summary_dict: dict) -> str:
    """
    Generate CSV summary of residue reference statistics.

    Args:
        summary_dict: Dict of {residue_codigo: ResidueReferenceSummary}

    Returns:
        str: CSV formatted string
    """
    rows = []

    for codigo, summary in summary_dict.items():
        rows.append({
            'Residue_Code': summary.residue_codigo,
            'Residue_Name': summary.residue_name,
            'Sector': summary.sector,
            'Paper_Count': summary.paper_count,
            'Parameter_Count': summary.parameter_count,
            'Primary_Sources': summary.primary_sources_count,
            'High_Quality_Papers': summary.high_quality_count,
            'Medium_Quality_Papers': summary.medium_quality_count,
            'Low_Quality_Papers': summary.low_quality_count,
            'Papers_With_Metadata': summary.papers_with_metadata,
            'Coverage_Score': f"{summary.coverage_score:.1f}%",
            'Completeness': f"{summary.completeness_percentage:.1f}%",
            'Parameters_Available': ', '.join(summary.parameters_available),
            'Parameters_Missing': ', '.join(summary.parameters_missing) if summary.parameters_missing else 'None'
        })

    df = pd.DataFrame(rows)
    return df.to_csv(index=False)


def format_reference_table_for_display(references: List[ScientificReference]) -> pd.DataFrame:
    """
    Format references for display in Streamlit table.

    Args:
        references: List of ScientificReference objects

    Returns:
        pd.DataFrame: Formatted table ready for st.dataframe()
    """
    data = []

    for ref in references:
        # Format year
        year_display = str(ref.publication_year) if ref.publication_year else 'N/A'

        # Format authors (truncate if too long)
        authors_display = ref.authors if ref.authors else 'N/A'
        if len(authors_display) > 50:
            authors_display = authors_display[:47] + '...'

        # Format title
        title_display = ref.title if ref.title else 'N/A'
        if len(title_display) > 60:
            title_display = title_display[:57] + '...'

        data.append({
            'Código': ref.codename,
            'Ano': year_display,
            'Autores': authors_display,
            'Título': title_display,
            'Journal': ref.journal if ref.journal else 'N/A',
            'DOI': ref.doi if ref.doi else 'N/A',
            'Setor': ref.sector_full if ref.sector_full else ref.sector,
            'Qualidade': ref.data_quality,
            'Metadata': '✅' if ref.has_metadata else '⏳'
        })

    return pd.DataFrame(data)


def format_parameter_sources_table(sources: List[ParameterSource]) -> pd.DataFrame:
    """
    Format parameter sources for display in Streamlit table.

    Args:
        sources: List of ParameterSource objects

    Returns:
        pd.DataFrame: Formatted table
    """
    data = []

    for source in sources:
        data.append({
            'Valor': source.value_display,
            'Fonte': source.reference.citation_short,
            'Página': source.page_number if source.page_number else 'N/A',
            'Qualidade': source.quality_badge,
            'Amostras': source.n_samples if source.n_samples else 'N/A',
            'Condições': source.measurement_conditions if source.measurement_conditions else 'N/A'
        })

    return pd.DataFrame(data)


def generate_ris_format(references: List[ScientificReference]) -> str:
    """
    Generate RIS format for Mendeley/Zotero import.

    RIS (Research Information Systems) is a standardized tag format
    for bibliographic citations, widely supported by reference managers.

    Args:
        references: List of ScientificReference objects

    Returns:
        str: RIS formatted string

    Example:
        >>> ris = generate_ris_format(refs)
        >>> # Save to file or offer for download
        >>> with open('references.ris', 'w') as f:
        ...     f.write(ris)
    """
    ris_entries = []

    for ref in references:
        # Skip if no metadata
        if not ref.has_metadata:
            continue

        entry = []
        entry.append("TY  - JOUR")  # Type: Journal article

        # Title
        if ref.title:
            entry.append(f"TI  - {ref.title}")

        # Authors (split multiple authors)
        if ref.authors:
            authors_list = ref.authors.replace(';', ',').split(',')
            for author in authors_list[:10]:  # Limit to 10 authors
                author_clean = author.strip()
                if author_clean:
                    entry.append(f"AU  - {author_clean}")

        # Publication year
        if ref.publication_year:
            entry.append(f"PY  - {ref.publication_year}")
            entry.append(f"Y1  - {ref.publication_year}")  # Alternate year tag

        # Journal
        if ref.journal:
            entry.append(f"JO  - {ref.journal}")
            entry.append(f"T2  - {ref.journal}")  # Alternate journal tag

        # Volume
        if ref.volume:
            entry.append(f"VL  - {ref.volume}")

        # Issue
        if ref.issue:
            entry.append(f"IS  - {ref.issue}")

        # Pages
        if ref.pages:
            entry.append(f"SP  - {ref.pages}")

        # DOI
        if ref.doi:
            entry.append(f"DO  - {ref.doi}")

        # Abstract
        if ref.abstract:
            # RIS format requires multi-line abstracts to continue with "  - "
            abstract_clean = ref.abstract.replace('\n', ' ').strip()
            if len(abstract_clean) > 0:
                entry.append(f"AB  - {abstract_clean}")

        # Keywords
        if ref.keywords:
            entry.append(f"KW  - {ref.keywords}")

        # URL (for DOI or Google Scholar)
        if ref.external_url:
            entry.append(f"UR  - {ref.external_url}")

        # Database/Archive (CP2B specific)
        entry.append("DB  - CP2B Panorama Database")

        # Custom ID (codename for traceability)
        entry.append(f"ID  - {ref.codename}")

        # Notes (sector and quality info)
        notes_parts = []
        if ref.sector_full:
            notes_parts.append(f"Sector: {ref.sector_full}")
        if ref.data_quality:
            notes_parts.append(f"Quality: {ref.data_quality}")

        if notes_parts:
            entry.append(f"N1  - {' | '.join(notes_parts)}")

        # End of record
        entry.append("ER  -")
        entry.append("")  # Blank line between entries

        ris_entries.append("\n".join(entry))

    return "\n".join(ris_entries)
