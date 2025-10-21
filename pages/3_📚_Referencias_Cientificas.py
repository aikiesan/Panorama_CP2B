"""
Page 3: Referências Científicas (Culture-Grouped Version)
CP2B - Scientific references organized by CULTURE, not by individual residue

Key Change: References are deduplicated and shown once per culture
Example: All Cana-de-Açúcar references shown together for Palha, Bagaço, Vinhaça, Torta
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Set
from collections import defaultdict

from src.data.residue_registry import (
    get_available_residues,
    get_residue_data,
    RESIDUES_REGISTRY
)
from src.models.residue_models import ScientificReference
from src.ui.tabs import render_sector_tabs, render_hierarchical_dropdowns
from src.ui.main_navigation import render_main_navigation, render_navigation_divider


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Referências Científicas - CP2B",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# SECTOR AND CULTURE MAPPING
# ============================================================================

# Maps residue names to their sector (primary grouping)
def get_sector_for_residue(residue_name: str) -> str:
    """Get sector for a residue based on its category"""
    residue_data = get_residue_data(residue_name)
    if residue_data:
        return residue_data.category
    return 'Outros'


# Maps agricultural residues to specific culture sub-groups
AGRICULTURE_CULTURE_GROUPS = {
    # Cana-de-Açúcar
    'Palha de Cana-de-açúcar (Palhiço)': 'Agricultura - Cana-de-Açúcar',
    'Bagaço de cana': 'Agricultura - Cana-de-Açúcar',
    'Vinhaça de Cana-de-açúcar': 'Agricultura - Cana-de-Açúcar',
    'Torta de Filtro (Filter Cake)': 'Agricultura - Cana-de-Açúcar',

    # Milho
    'Palha de milho': 'Agricultura - Milho',
    'Sabugo de milho': 'Agricultura - Milho',

    # Soja
    'Palha de soja': 'Agricultura - Soja',
    'Vagens vazias': 'Agricultura - Soja',
    'Casca de soja': 'Agricultura - Soja',

    # Café
    'Casca de café (pergaminho)': 'Agricultura - Café',
    'Polpa de café': 'Agricultura - Café',
    'Mucilagem fermentada': 'Agricultura - Café',

    # Eucalipto
    'Casca de eucalipto': 'Agricultura - Eucalipto',
    'Galhos e ponteiros': 'Agricultura - Eucalipto',
    'Folhas de eucalipto': 'Agricultura - Eucalipto',

    # Citros
    'Bagaço de citros': 'Agricultura - Citros',
    'Cascas de citros': 'Agricultura - Citros',
    'Polpa de citros': 'Agricultura - Citros',
}


def get_group_for_residue(residue_name: str) -> str:
    """
    Get the grouping category for a residue.
    For agricultura: returns specific culture (e.g., 'Agricultura - Cana-de-Açúcar')
    For other sectors: returns sector name (e.g., 'Pecuária', 'Industrial', 'Urbano')
    """
    # Check if it's an agricultural residue with specific culture
    if residue_name in AGRICULTURE_CULTURE_GROUPS:
        return AGRICULTURE_CULTURE_GROUPS[residue_name]
    
    # Otherwise return the sector
    sector = get_sector_for_residue(residue_name)
    return sector if sector else 'Outros'


def gather_references_by_group() -> Dict[str, List[ScientificReference]]:
    """
    Gather all references organized by sector/culture group.
    - Agricultura residues are grouped by culture (Cana, Milho, Soja, etc.)
    - Other sectors are grouped by sector (Pecuária, Industrial, Urbano)
    Deduplicates references within each group.
    """
    group_refs = defaultdict(list)
    seen_refs_per_group = defaultdict(set)

    for residue_name in get_available_residues():
        residue_data = get_residue_data(residue_name)

        if not residue_data or not residue_data.references:
            continue

        group = get_group_for_residue(residue_name)

        for ref in residue_data.references:
            # Create unique key for deduplication
            ref_key = (ref.title, ref.year, ref.authors[:50])  # Use first 50 chars of authors

            if ref_key not in seen_refs_per_group[group]:
                seen_refs_per_group[group].add(ref_key)
                group_refs[group].append(ref)

    return dict(group_refs)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render orange/amber gradient header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #ea580c 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            📚 Referências Científicas por Setor
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Base de Dados Organizada • DOI • Scopus • Sem Duplicações
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            🌾 Agricultura • 🐄 Pecuária • 🏭 Industrial • 🏙️ Urbano • 🔍 Referências Únicas
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# REFERENCE EXPORT UTILITIES
# ============================================================================

def export_bibtex(references: List[ScientificReference], group_name: str) -> str:
    """Export references as BibTeX format"""
    bibtex_entries = []

    for i, ref in enumerate(references, 1):
        # Generate citation key
        first_author = ref.authors.split(',')[0].split()[-1].lower() if ref.authors else 'unknown'
        key = f"{first_author}{ref.year}"

        entry = f"""@article{{{key},
    title = {{{ref.title}}},
    author = {{{ref.authors}}},
    year = {{{ref.year}}},"""

        if ref.journal:
            entry += f"\n    journal = {{{ref.journal}}},"
        if ref.doi:
            entry += f"\n    doi = {{{ref.doi}}},"

        entry += "\n}\n"
        bibtex_entries.append(entry)

    return "\n".join(bibtex_entries)


def export_ris(references: List[ScientificReference], group_name: str) -> str:
    """Export references as RIS format"""
    ris_entries = []

    for ref in references:
        # Format authors with line breaks
        authors_formatted = ref.authors.replace(',', '\nAU  - ') if ref.authors else 'Unknown'

        entry = f"""TY  - JOUR
TI  - {ref.title}
AU  - {authors_formatted}
PY  - {ref.year}"""

        if ref.journal:
            entry += f"\nJO  - {ref.journal}"
        if ref.doi:
            entry += f"\nDO  - {ref.doi}"

        entry += "\nER  -\n"
        ris_entries.append(entry)

    return "\n".join(ris_entries)


def export_csv(df: pd.DataFrame) -> bytes:
    """Export references as CSV"""
    return df.to_csv(index=False).encode('utf-8-sig')


# ============================================================================
# REFERENCES TABLE
# ============================================================================

def render_references_table(references: List[ScientificReference], group_name: str):
    """Render interactive references table"""
    st.markdown(f"### 📄 Referências de {group_name}")

    if not references:
        st.info(f"ℹ️ Nenhuma referência disponível para {group_name} ainda")
        return

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total de Artigos", len(references))

    with col2:
        high_rel = sum(1 for r in references if r.relevance == "High" or r.relevance == "Very High")
        st.metric("⭐ Alta Relevância", high_rel)

    with col3:
        with_doi = sum(1 for r in references if r.doi)
        st.metric("🔗 Com DOI", with_doi)

    with col4:
        avg_year = sum(r.year for r in references if r.year) / len(references) if references else 0
        st.metric("📅 Ano Médio", f"{avg_year:.0f}" if avg_year > 0 else "—")

    st.markdown("---")

    # Convert to DataFrame
    refs_data = []
    for ref in references:
        # Create clickable links
        doi_link = f"[🔗 DOI](https://doi.org/{ref.doi})" if ref.doi else "—"
        scopus_link = f"[📊 Scopus]({ref.scopus_link})" if ref.scopus_link else "—"

        # Format key findings
        findings_text = "\n".join([f"• {finding}" for finding in ref.key_findings]) if ref.key_findings else "—"

        refs_data.append({
            'Título': ref.title,
            'Autores': ref.authors,
            'Ano': ref.year,
            'Revista': ref.journal if ref.journal else "—",
            'DOI': doi_link,
            'Scopus': scopus_link,
            'Relevância': ref.relevance,
            'Tipo': ref.data_type,
            'Principais Achados': findings_text
        })

    df = pd.DataFrame(refs_data)

    # Filters
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            relevance_filter = st.multiselect(
                "Relevância",
                options=['Very High', 'High', 'Medium', 'Low'],
                default=['Very High', 'High', 'Medium', 'Low'],
                key=f"relevance_filter_{group_name}"
            )

        with col2:
            year_min = st.number_input("Ano Mínimo", min_value=1990, max_value=2025, value=2000, key=f"year_min_{group_name}")

        with col3:
            year_max = st.number_input("Ano Máximo", min_value=1990, max_value=2025, value=2025, key=f"year_max_{group_name}")

    # Apply filters
    filtered_df = df[
        (df['Relevância'].isin(relevance_filter)) &
        (df['Ano'] >= year_min) &
        (df['Ano'] <= year_max)
    ]

    st.markdown(f"**{len(filtered_df)} de {len(df)} referências exibidas**")

    # Display table
    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            'Título': st.column_config.TextColumn('Título', width='large'),
            'Autores': st.column_config.TextColumn('Autores', width='medium'),
            'Ano': st.column_config.NumberColumn('Ano', width='small'),
            'Revista': st.column_config.TextColumn('Revista', width='medium'),
            'DOI': st.column_config.LinkColumn('DOI', width='small'),
            'Scopus': st.column_config.LinkColumn('Scopus', width='small'),
            'Relevância': st.column_config.TextColumn('Relevância', width='small'),
            'Tipo': st.column_config.TextColumn('Tipo de Dado', width='medium'),
            'Principais Achados': st.column_config.TextColumn('Principais Achados', width='large')
        }
    )

    # Export buttons
    st.markdown("---")
    st.markdown("### 📥 Exportar Referências")

    col1, col2, col3 = st.columns(3)

    with col1:
        bibtex_data = export_bibtex(references, group_name)
        st.download_button(
            label="📄 Exportar BibTeX",
            data=bibtex_data,
            file_name=f"referencias_{group_name.lower().replace(' ', '_').replace('-', '_')}.bib",
            mime="text/plain",
            key=f"bibtex_{group_name}"
        )

    with col2:
        ris_data = export_ris(references, group_name)
        st.download_button(
            label="📋 Exportar RIS",
            data=ris_data,
            file_name=f"referencias_{group_name.lower().replace(' ', '_').replace('-', '_')}.ris",
            mime="text/plain",
            key=f"ris_{group_name}"
        )

    with col3:
        csv_data = export_csv(filtered_df)
        st.download_button(
            label="📊 Exportar CSV",
            data=csv_data,
            file_name=f"referencias_{group_name.lower().replace(' ', '_').replace('-', '_')}.csv",
            mime="text/csv",
            key=f"csv_{group_name}"
        )


# ============================================================================
# KEY PAPERS HIGHLIGHT
# ============================================================================

def render_key_papers(references: List[ScientificReference]):
    """Highlight top-tier references"""
    high_rel_refs = [r for r in references if r.relevance in ["Very High", "High"]]

    if not high_rel_refs:
        return

    st.markdown("### ⭐ Artigos de Destaque")

    for ref in high_rel_refs[:3]:  # Show top 3
        with st.container():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                        padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;
                        border-left: 5px solid #f59e0b;'>
                <h4 style='margin: 0 0 10px 0; color: #1f2937;'>{ref.title}</h4>
                <p style='margin: 5px 0; color: #4b5563;'><strong>Autores:</strong> {ref.authors}</p>
                <p style='margin: 5px 0; color: #4b5563;'><strong>Ano:</strong> {ref.year} | <strong>Revista:</strong> {ref.journal or "—"}</p>
            </div>
            """, unsafe_allow_html=True)

            if ref.key_findings:
                st.markdown("**Principais Achados:**")
                for finding in ref.key_findings:
                    st.markdown(f"• {finding}")

            col1, col2 = st.columns(2)
            with col1:
                if ref.doi:
                    st.markdown(f"[🔗 Acessar via DOI](https://doi.org/{ref.doi})")
            with col2:
                if ref.scopus_link:
                    st.markdown(f"[📊 Ver no Scopus]({ref.scopus_link})")

            st.markdown("---")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function"""
    render_header()

    # Main navigation bar
    render_main_navigation(current_page="referencias")
    render_navigation_divider()

    # Show database-backed residue list instead
    from src.data_handler import get_all_residues_with_params

    st.info("""
    📚 **Referências Científicas - Database Integrado**

    As referências estão sendo reorganizadas. Por enquanto, veja os resíduos catalogados no banco de dados validado.
    Para detalhes técnicos completos, consulte as Páginas 1 (Disponibilidade) e 2 (Parâmetros Químicos).
    """)

    df = get_all_residues_with_params()

    st.markdown("### 📊 Resíduos Catalogados (38 total)")

    # Group by sector
    for setor in ['AG_AGRICULTURA', 'PC_PECUARIA', 'UR_URBANO', 'IN_INDUSTRIAL']:
        df_setor = df[df['setor'] == setor]
        if len(df_setor) > 0:
            sector_names = {'AG_AGRICULTURA': '🌾 Agricultura', 'PC_PECUARIA': '🐄 Pecuária',
                          'UR_URBANO': '🏙️ Urbano', 'IN_INDUSTRIAL': '🏭 Industrial'}
            with st.expander(f"{sector_names[setor]} ({len(df_setor)} resíduos)", expanded=True):
                st.dataframe(df_setor[['nome', 'bmp_medio', 'fator_realista']],
                           hide_index=True, use_container_width=True,
                           column_config={'nome': 'Resíduo', 'bmp_medio': 'BMP (m³/kg VS)',
                                        'fator_realista': st.column_config.NumberColumn('SAF (%)', format="%.1f%%")})

    return

    # Group selection dropdown
    selected_group = st.selectbox(
        "Setor / Cultura Agrícola",
        options=['Todos os Setores'] + groups,
        key="group_selector"
    )

    st.markdown("---")

    if selected_group == 'Todos os Setores':
        # Show all groups organized by main sector
        sector_order = ['Agricultura', 'Pecuária', 'Industrial', 'Urbano', 'Outros']
        
        for sector in sector_order:
            # Get all groups for this sector
            sector_groups = [g for g in groups if g.startswith(sector) or g == sector]
            
            if not sector_groups:
                continue
            
            # Sector header
            sector_icons = {
                'Agricultura': '🌾',
                'Pecuária': '🐄',
                'Industrial': '🏭',
                'Urbano': '🏙️',
                'Outros': '📊'
            }
            icon = sector_icons.get(sector, '📊')
            st.markdown(f"## {icon} {sector}")
            
            for group in sorted(sector_groups):
                refs = group_refs[group]
                with st.expander(f"📚 {group} ({len(refs)} referências)", expanded=False):
                    render_key_papers(refs)
                    render_references_table(refs, group)
            
            st.markdown("---")
    else:
        # Show selected group
        refs = group_refs[selected_group]
        render_key_papers(refs)
        render_references_table(refs, selected_group)


if __name__ == "__main__":
    main()
