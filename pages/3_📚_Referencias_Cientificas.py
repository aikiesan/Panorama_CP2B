"""
Page 3: Referências Científicas
CP2B - Scientific references with DOI, Scopus links, and detailed bibliographic data
"""

import streamlit as st
import pandas as pd
from typing import List

from src.research_data import (
    get_available_residues,
    get_residue_data,
    get_residue_icon,
    ScientificReference
)
from src.ui_components import render_full_selector


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
            📚 Referências Científicas Validadas
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Base de Dados • DOI • Scopus • Revisão Sistemática
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📄 Literatura Revisada • 🔍 Busca Sistemática • ✅ Dados Validados • 📊 Alta Relevância
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# REFERENCE EXPORT UTILITIES
# ============================================================================

def export_bibtex(references: List[ScientificReference], residue_name: str) -> str:
    """Export references as BibTeX format"""
    bibtex_entries = []

    for i, ref in enumerate(references, 1):
        # Generate citation key
        first_author = ref.authors.split(',')[0].split()[-1].lower()
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


def export_ris(references: List[ScientificReference], residue_name: str) -> str:
    """Export references as RIS format"""
    ris_entries = []

    for ref in references:
        # Format authors with line breaks
        authors_formatted = ref.authors.replace(',', '\nAU  - ')
        
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

def render_references_table(references: List[ScientificReference], residue_name: str):
    """Render interactive references table"""
    st.markdown("### 📄 Base de Referências Bibliográficas")

    if not references:
        st.info("ℹ️ Nenhuma referência disponível para este resíduo ainda")
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
        avg_year = sum(r.year for r in references) / len(references) if references else 0
        st.metric("📅 Ano Médio", f"{avg_year:.0f}")

    st.markdown("---")

    # Convert to DataFrame
    refs_data = []
    for ref in references:
        # Create clickable links
        doi_link = f"[🔗 DOI]({ref.doi})" if ref.doi else "—"
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
                default=['Very High', 'High', 'Medium', 'Low']
            )

        with col2:
            year_min = st.number_input("Ano Mínimo", min_value=1990, max_value=2025, value=2000)

        with col3:
            year_max = st.number_input("Ano Máximo", min_value=1990, max_value=2025, value=2025)

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
        bibtex_data = export_bibtex(references, residue_name)
        st.download_button(
            label="📄 Exportar BibTeX",
            data=bibtex_data,
            file_name=f"referencias_{residue_name.lower().replace(' ', '_')}.bib",
            mime="text/plain"
        )

    with col2:
        ris_data = export_ris(references, residue_name)
        st.download_button(
            label="📋 Exportar RIS",
            data=ris_data,
            file_name=f"referencias_{residue_name.lower().replace(' ', '_')}.ris",
            mime="text/plain"
        )

    with col3:
        csv_data = export_csv(filtered_df)
        st.download_button(
            label="📊 Exportar CSV",
            data=csv_data,
            file_name=f"referencias_{residue_name.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )


# ============================================================================
# METHODOLOGY SECTION
# ============================================================================

def render_methodology():
    """Render methodology and validation approach"""
    st.markdown("### 📖 Metodologia de Revisão")

    with st.expander("ℹ️ Abordagem PRISMA e Critérios de Seleção", expanded=False):
        st.markdown("""
        **Metodologia de Revisão Sistemática:**

        Este banco de dados foi construído seguindo princípios da metodologia PRISMA
        (Preferred Reporting Items for Systematic Reviews and Meta-Analyses).

        **Critérios de Inclusão:**
        - ✅ Artigos revisados por pares (peer-reviewed)
        - ✅ Dados empíricos de BMP e composição química
        - ✅ Contextualização brasileira ou clima tropical/subtropical
        - ✅ Publicações em periódicos indexados (Scopus, Web of Science)
        - ✅ Dados operacionais de plantas reais ou experimentos controlados

        **Critérios de Exclusão:**
        - ❌ Dados não verificáveis ou sem metodologia clara
        - ❌ Estudos puramente teóricos sem validação experimental
        - ❌ Dados de contextos climáticos incompatíveis

        **Bases de Dados Consultadas:**
        - 🔍 Scopus
        - 🔍 Web of Science
        - 🔍 Google Scholar
        - 🔍 SciELO

        **Classificação de Relevância:**
        - **Very High**: Dados primários de experimentos brasileiros com metodologia robusta
        - **High**: Dados relevantes de contextos similares (América Latina, clima tropical)
        - **Medium**: Revisões de literatura e meta-análises
        - **Low**: Dados secundários ou de contextos distantes

        **Classificação de Tipo de Dado:**
        - **Literatura Científica**: Artigos peer-reviewed
        - **Dados Primários**: Experimentos originais
        - **Sensoriamento Remoto**: Dados de satélite e geoprocessamento
        - **Normas e Regulamentação**: CONAMA, ABNT, legislação
        """)


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

    # New parallel sector + residue selector
    selected_residue = render_full_selector(key_prefix="referencias")

    if not selected_residue:
        return

    st.markdown("---")

    # Gather references
    if selected_residue == 'Todos os Resíduos':
        # Collect all references from all residues
        all_references = []
        for residue_name in get_available_residues():
            residue_data = get_residue_data(residue_name)
            if residue_data and residue_data.references:
                all_references.extend(residue_data.references)

        references = all_references
        display_name = "Todos os Resíduos"
    else:
        # Get specific residue references
        residue_data = get_residue_data(selected_residue)

        if not residue_data:
            st.error("⚠️ Dados não encontrados")
            return

        references = residue_data.references
        display_name = selected_residue

    # Render sections
    if references:
        render_key_papers(references)

        st.markdown("---")

        render_references_table(references, display_name)
    else:
        st.info(f"📚 Nenhuma referência disponível para **{display_name}** no momento.")

    st.markdown("---")

    render_methodology()


if __name__ == "__main__":
    main()
