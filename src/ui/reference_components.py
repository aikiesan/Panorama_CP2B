"""
Reference UI Components - Reusable Streamlit components for displaying references
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Provides UI components for:
- Reference cards with PDF links
- Parameter source traceability
- BibTeX export
- Reference tables

Phase 2 - Database Integration
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List, Optional
import os

from src.models.reference_models import ScientificReference, ParameterSource
from src.utils.export_helpers import (
    generate_bibtex,
    generate_ris_format,
    format_reference_table_for_display,
    format_parameter_sources_table
)


def render_reference_card(reference: ScientificReference, show_pdf_link: bool = True):
    """
    Render a single reference as an expandable card.

    Args:
        reference: ScientificReference object
        show_pdf_link: Whether to show PDF/DOI links

    Example:
        >>> for ref in references:
        ...     render_reference_card(ref)
    """
    with st.expander(f"📄 {reference.citation_short}"):
        # Title
        if reference.title:
            st.markdown(f"**{reference.title}**")
        else:
            st.markdown(f"**{reference.codename}** *(metadata incomplete)*")

        # Authors and year
        col1, col2 = st.columns([3, 1])
        with col1:
            if reference.authors:
                st.caption(f"👤 {reference.authors}")
            else:
                st.caption("👤 *Authors not available*")

        with col2:
            if reference.publication_year:
                st.caption(f"📅 {reference.publication_year}")

        # Journal information
        if reference.journal:
            journal_info = reference.journal
            if reference.volume:
                journal_info += f", Vol. {reference.volume}"
            if reference.issue:
                journal_info += f"({reference.issue})"
            if reference.pages:
                journal_info += f", pp. {reference.pages}"
            st.caption(f"📖 {journal_info}")

        # Quality and sector
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"🏷️ {reference.data_quality}")
        with col2:
            if reference.sector_full:
                st.caption(f"📂 {reference.sector_full}")
        with col3:
            metadata_icon = "✅" if reference.has_metadata else "⏳"
            st.caption(f"{metadata_icon} Metadata")

        # Links
        if show_pdf_link:
            st.markdown("---")
            render_pdf_link(reference)

        # Abstract (if available)
        if reference.abstract:
            with st.expander("📝 Abstract"):
                st.write(reference.abstract)


def render_pdf_link(reference: ScientificReference):
    """
    Render clickable links to PDF or external sources.

    Handles Windows file paths and provides fallback to DOI.

    Args:
        reference: ScientificReference object
    """
    links_html = []

    # Check if PDF exists
    pdf_path = Path(reference.pdf_path)

    if pdf_path.exists():
        # Convert Windows path to file:// URL
        file_url = pdf_path.as_uri()
        links_html.append(f'<a href="{file_url}" target="_blank">📄 Abrir PDF Local</a>')
    else:
        links_html.append('📄 <span style="color: gray;">PDF não disponível localmente</span>')

    # DOI link
    if reference.doi:
        doi_url = f"https://doi.org/{reference.doi}"
        links_html.append(f'<a href="{doi_url}" target="_blank">🔗 Ver via DOI</a>')

    # Google Scholar link
    if reference.google_scholar_link:
        links_html.append(f'<a href="{reference.google_scholar_link}" target="_blank">🌐 Google Scholar</a>')

    # Display all links
    if links_html:
        st.markdown(" | ".join(links_html), unsafe_allow_html=True)
    else:
        st.caption("⚠️ Nenhum link disponível")


def render_reference_table(
    references: List[ScientificReference],
    show_filters: bool = True,
    allow_selection: bool = False
) -> Optional[List[int]]:
    """
    Render references as a sortable, filterable table.

    Args:
        references: List of ScientificReference objects
        show_filters: Whether to show filter controls
        allow_selection: Whether to allow row selection

    Returns:
        Optional[List[int]]: Selected reference IDs if allow_selection=True

    Example:
        >>> selected_ids = render_reference_table(refs, allow_selection=True)
        >>> if selected_ids:
        ...     bibtex = generate_bibtex_for_ids(selected_ids)
    """
    if not references:
        st.info("📭 Nenhuma referência disponível")
        return None

    # Convert to DataFrame
    df = format_reference_table_for_display(references)

    # Filters
    selected_ids = None

    if show_filters:
        col1, col2, col3 = st.columns(3)

        with col1:
            # Sector filter
            sectors = ['Todos'] + sorted(df['Setor'].unique().tolist())
            selected_sector = st.selectbox('Filtrar por Setor:', sectors, key='ref_table_sector')

        with col2:
            # Year filter
            years = ['Todos'] + sorted([y for y in df['Ano'].unique() if y != 'N/A'], reverse=True)
            selected_year = st.selectbox('Filtrar por Ano:', years, key='ref_table_year')

        with col3:
            # Metadata filter
            metadata_filter = st.selectbox(
                'Filtrar por Metadata:',
                ['Todos', 'Completo ✅', 'Incompleto ⏳'],
                key='ref_table_metadata'
            )

        # Apply filters
        if selected_sector != 'Todos':
            df = df[df['Setor'] == selected_sector]

        if selected_year != 'Todos':
            df = df[df['Ano'] == selected_year]

        if metadata_filter == 'Completo ✅':
            df = df[df['Metadata'] == '✅']
        elif metadata_filter == 'Incompleto ⏳':
            df = df[df['Metadata'] == '⏳']

    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        height=400,
        hide_index=True
    )

    # Selection (if enabled)
    if allow_selection:
        st.markdown("---")
        st.caption("💡 Selecione referências para exportar")

        # Use multiselect based on codenames
        codenames = df['Código'].tolist()
        selected_codenames = st.multiselect(
            'Referências selecionadas:',
            codenames,
            key='ref_table_selection'
        )

        if selected_codenames:
            # Get IDs for selected references
            selected_ids = [
                ref.id for ref in references
                if ref.codename in selected_codenames
            ]

    return selected_ids


def render_parameter_with_sources(
    parameter_name: str,
    sources: List[ParameterSource],
    show_all: bool = False
):
    """
    Render parameter value with expandable source list.

    Shows parameter value and allows user to expand to see all contributing sources.

    Args:
        parameter_name: Display name (e.g., "BMP", "TS")
        sources: List of ParameterSource objects
        show_all: If True, show all sources; if False, show top 3 + expander

    Example:
        >>> sources = parameter_service.get_parameter_sources('CANA_VINHACA', 'BMP')
        >>> render_parameter_with_sources('BMP', sources)
    """
    if not sources:
        st.caption(f"**{parameter_name}**: *Não disponível*")
        return

    # Summary statistics
    values = [s.value_mean for s in sources if s.value_mean is not None]
    if values:
        min_val = min(values)
        max_val = max(values)
        mean_val = sum(values) / len(values)

        # Display summary
        st.markdown(f"**{parameter_name}**: {mean_val:.1f} ({min_val:.1f} - {max_val:.1f}) {sources[0].unit}")
        st.caption(f"📊 {len(sources)} fonte(s) | {len(values)} medições")

        # Source details
        with st.expander(f"📄 Ver Fontes para {parameter_name}"):
            if show_all or len(sources) <= 5:
                # Show all sources
                for source in sources:
                    render_source_traceability_badge(source)
            else:
                # Show top 3 + expander for rest
                for source in sources[:3]:
                    render_source_traceability_badge(source)

                with st.expander(f"Ver mais {len(sources) - 3} fonte(s)"):
                    for source in sources[3:]:
                        render_source_traceability_badge(source)

            # Export sources table
            st.markdown("---")
            df_sources = format_parameter_sources_table(sources)
            st.dataframe(df_sources, use_container_width=True, hide_index=True)


def render_source_traceability_badge(source: ParameterSource):
    """
    Render a single source with quality badge and citation.

    Args:
        source: ParameterSource object

    Example:
        >>> render_source_traceability_badge(source)
        ⭐⭐⭐ 260.0 ml CH₄/g VS | Silva et al. (2020), p. 15
    """
    # Build display string
    quality = source.quality_badge
    value = source.value_display
    citation = source.source_citation

    st.markdown(f"{quality} **{value}** | {citation}")

    # Additional details (if available)
    details = []
    if source.n_samples:
        details.append(f"{source.n_samples} amostras")
    if source.measurement_conditions:
        details.append(source.measurement_conditions)

    if details:
        st.caption(" • ".join(details))


def render_bibtex_export_button(references: List[ScientificReference], filename: str = "references.bib"):
    """
    Render download button for BibTeX export.

    Args:
        references: List of ScientificReference objects
        filename: Output filename

    Example:
        >>> render_bibtex_export_button(selected_refs, "vinhaca_refs.bib")
    """
    if not references:
        st.warning("⚠️ Nenhuma referência para exportar")
        return

    # Generate BibTeX
    bibtex_content = generate_bibtex(references)

    if not bibtex_content.strip():
        st.warning("⚠️ Nenhuma referência com metadata completa para exportar")
        return

    # Download button
    st.download_button(
        label=f"📥 Exportar {len(references)} referência(s) em BibTeX",
        data=bibtex_content,
        file_name=filename,
        mime="application/x-bibtex"
    )


def render_export_buttons(references: List[ScientificReference], base_filename: str = "references"):
    """
    Render multiple export format buttons (BibTeX, RIS, CSV).

    Args:
        references: List of ScientificReference objects
        base_filename: Base filename without extension

    Example:
        >>> render_export_buttons(selected_refs, "vinhaca_refs")
        # Shows buttons for .bib, .ris, .csv
    """
    if not references:
        st.warning("⚠️ Nenhuma referência para exportar")
        return

    st.markdown("### 📥 Exportar Referências")

    col1, col2, col3 = st.columns(3)

    with col1:
        # BibTeX export
        bibtex_content = generate_bibtex(references)
        if bibtex_content.strip():
            st.download_button(
                label="📄 BibTeX (.bib)",
                data=bibtex_content,
                file_name=f"{base_filename}.bib",
                mime="application/x-bibtex",
                help="Para LaTeX, Overleaf"
            )
        else:
            st.button("📄 BibTeX (.bib)", disabled=True, help="Nenhuma referência com metadata completa")

    with col2:
        # RIS export
        ris_content = generate_ris_format(references)
        if ris_content.strip():
            st.download_button(
                label="📚 RIS (.ris)",
                data=ris_content,
                file_name=f"{base_filename}.ris",
                mime="application/x-research-info-systems",
                help="Para Mendeley, Zotero, EndNote"
            )
        else:
            st.button("📚 RIS (.ris)", disabled=True, help="Nenhuma referência com metadata completa")

    with col3:
        # CSV export
        from src.utils.export_helpers import generate_csv_references
        csv_content = generate_csv_references(references)
        st.download_button(
            label="📊 CSV (.csv)",
            data=csv_content,
            file_name=f"{base_filename}.csv",
            mime="text/csv",
            help="Para Excel, análise de dados"
        )

    # Summary
    with_metadata = sum(1 for ref in references if ref.has_metadata)
    st.caption(f"💡 {len(references)} referências total | {with_metadata} com metadata completa")


def render_reference_statistics(references: List[ScientificReference]):
    """
    Render statistics cards for a list of references.

    Args:
        references: List of ScientificReference objects

    Example:
        >>> render_reference_statistics(refs)
        Shows: Total papers, papers with metadata, year range, sectors
    """
    if not references:
        return

    # Calculate statistics
    total_papers = len(references)
    papers_with_metadata = sum(1 for ref in references if ref.has_metadata)
    papers_with_doi = sum(1 for ref in references if ref.doi)

    years = [ref.publication_year for ref in references if ref.publication_year]
    year_range = f"{min(years)}-{max(years)}" if years else "N/A"

    sectors = {}
    for ref in references:
        sector = ref.sector_full or ref.sector or "Unknown"
        sectors[sector] = sectors.get(sector, 0) + 1

    # Display as metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 Total de Papers", total_papers)

    with col2:
        metadata_pct = (papers_with_metadata / total_papers * 100) if total_papers > 0 else 0
        st.metric("✅ Com Metadata", f"{papers_with_metadata} ({metadata_pct:.0f}%)")

    with col3:
        doi_pct = (papers_with_doi / total_papers * 100) if total_papers > 0 else 0
        st.metric("🔗 Com DOI", f"{papers_with_doi} ({doi_pct:.0f}%)")

    with col4:
        st.metric("📅 Período", year_range)

    # Sector distribution
    if len(sectors) > 1:
        st.markdown("#### 📂 Distribuição por Setor")
        sector_df = pd.DataFrame([
            {"Setor": sector, "Papers": count}
            for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(sector_df, use_container_width=True, hide_index=True)


def render_search_interface() -> dict:
    """
    Render search and filter interface for references.

    Returns:
        dict: Filter parameters for ReferenceService.search_references()

    Example:
        >>> filters = render_search_interface()
        >>> refs = reference_service.search_references(filters)
    """
    st.markdown("### 🔍 Buscar Referências")

    filters = {}

    col1, col2 = st.columns(2)

    with col1:
        # Sector filter
        sector = st.selectbox(
            'Setor:',
            ['Todos', 'AG_CANA', 'AG_SOJA', 'AG_CAFE', 'AG_CITROS', 'PEC_SUINO',
             'PEC_BOVINO', 'PEC_AVES', 'UR_RSU', 'UR_RPO', 'IND_GERAL'],
            key='search_sector'
        )
        if sector != 'Todos':
            filters['sector'] = sector

    with col2:
        # Year range
        col_year1, col_year2 = st.columns(2)
        with col_year1:
            year_min = st.number_input('Ano mínimo:', min_value=1990, max_value=2025, value=2000, key='search_year_min')
            filters['year_min'] = year_min

        with col_year2:
            year_max = st.number_input('Ano máximo:', min_value=1990, max_value=2025, value=2025, key='search_year_max')
            filters['year_max'] = year_max

    # Text search
    query_text = st.text_input('🔎 Buscar em título, autores ou palavras-chave:', key='search_query')
    if query_text:
        filters['query_text'] = query_text

    # Quality filter
    col1, col2 = st.columns(2)

    with col1:
        quality = st.selectbox(
            'Qualidade dos dados:',
            ['Todos', 'Validated', 'High', 'Medium', 'Low'],
            key='search_quality'
        )
        if quality != 'Todos':
            filters['data_quality'] = quality

    with col2:
        has_metadata = st.checkbox('Apenas com metadata completa', key='search_metadata')
        if has_metadata:
            filters['has_metadata'] = True

    return filters
