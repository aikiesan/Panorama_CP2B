"""
Page 1: Disponibilidade de Resíduos
CP2B - Main page for residue availability factors and validation
DATABASE INTEGRATED - Phase 1.2 Complete
Shows ALL 38 residues (Agricultura, Pecuária, Urbano, Industrial)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Database integration (replaces residue_registry)
from src.data_handler import (
    get_all_residues_with_params,
    get_residue_by_name,
    get_residues_for_dropdown,
    calculate_saf
)

# New visualization components
from src.ui.chart_components import create_waterfall_chart

from src.ui.main_navigation import render_main_navigation, render_navigation_divider


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Disponibilidade de Resíduos - CP2B",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render blue/green gradient header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2563eb 0%, #059669 50%, #0d9488 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            📊 Disponibilidade de Resíduos para Biogás
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Fatores de Disponibilidade Real e Cenários de Potencial
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            🔬 Metodologia Conservadora • 📊 Dados Validados • 🗄️ Database: 38 Resíduos (4 setores)
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# DATABASE-DRIVEN RESIDUE SELECTOR
# ============================================================================

def render_residue_selector():
    """Render dropdown selector using database - shows ALL 38 residues"""
    st.markdown("### 🎯 Selecione o Resíduo")

    residues_by_sector = get_residues_for_dropdown()

    # Sector icons and names
    sector_icons = {
        'AG_AGRICULTURA': '🌾',
        'PC_PECUARIA': '🐄',
        'UR_URBANO': '🏙️',
        'IN_INDUSTRIAL': '🏭'
    }

    sector_names = {
        'AG_AGRICULTURA': 'Agricultura',
        'PC_PECUARIA': 'Pecuária',
        'UR_URBANO': 'Urbano',
        'IN_INDUSTRIAL': 'Industrial'
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        # Sector selector
        sector_options = list(residues_by_sector.keys())
        sector_labels = [f"{sector_icons.get(s, '')} {sector_names.get(s, s)}" for s in sector_options]

        selected_sector_idx = st.selectbox(
            "Setor:",
            range(len(sector_options)),
            format_func=lambda x: sector_labels[x],
            key="disp_sector_selector"
        )

        selected_sector = sector_options[selected_sector_idx]

    with col2:
        # Residue selector for chosen sector
        sector_residues = residues_by_sector[selected_sector]

        if sector_residues:
            selected_residue = st.selectbox(
                "Resíduo:",
                sector_residues,
                key="disp_residue_selector"
            )
        else:
            st.warning(f"Nenhum resíduo disponível no setor {sector_names.get(selected_sector, selected_sector)}")
            selected_residue = None

    return selected_residue


# ============================================================================
# AVAILABILITY CARD (DATABASE VERSION)
# ============================================================================

def render_availability_card_from_db(residue_data):
    """Display availability card from database dict structure"""
    st.markdown("### 📋 Informações do Resíduo")

    # Residue name and sector
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"**Nome:** {residue_data.get('nome', 'N/A')}")

    with col2:
        sector_names = {
            'AG_AGRICULTURA': '🌾 Agricultura',
            'PC_PECUARIA': '🐄 Pecuária',
            'UR_URBANO': '🏙️ Urbano',
            'IN_INDUSTRIAL': '🏭 Industrial'
        }
        st.markdown(f"**Setor:** {sector_names.get(residue_data.get('setor', ''), 'N/A')}")

    st.markdown("---")

    # Availability factors
    st.markdown("#### 📊 Fatores de Disponibilidade (SAF)")

    col1, col2, col3, col4 = st.columns(4)

    fc = residue_data.get('fc_medio', 0)
    fcp = residue_data.get('fcp_medio', 0)
    fs = residue_data.get('fs_medio', 0)
    fl = residue_data.get('fl_medio', 0)

    with col1:
        st.metric("FC (Coleta)", f"{fc:.0%}", help="Fator de Coleta - Eficiência técnica de coleta")

    with col2:
        st.metric("FCp (Competição)", f"{fcp:.0%}", help="Fator de Competição - Usos alternativos do resíduo")

    with col3:
        st.metric("FS (Sazonalidade)", f"{fs:.0%}", help="Fator de Sazonalidade - Variação ao longo do ano")

    with col4:
        st.metric("FL (Logística)", f"{fl:.0%}", help="Fator Logístico - Restrição por distância")

    # Calculate SAF
    saf = calculate_saf(fc, fcp, fs, fl)

    st.markdown("---")
    st.markdown(f"### ✅ Disponibilidade Final (SAF): **{saf:.1f}%**")

    st.info(f"""
    **Fórmula:** SAF = FC × FCp × FS × FL × 100%

    **Interpretação:**
    - SAF = {fc:.0%} (coleta) × {fcp:.0%} (disponível após competição) × {fs:.0%} (sazonal) × {fl:.0%} (logística) × 100%
    - SAF = {saf:.1f}%

    **Nota:** FCp={fcp:.0%} significa que **{fcp:.0%} está disponível** para biogás após {(1-fcp):.0%} ir para usos competitivos.

    Este resíduo tem **{saf:.1f}% de disponibilidade real** considerando todos os fatores técnicos, logísticos e de competição.
    """)


# ============================================================================
# SCENARIO COMPARISON (FROM DATABASE)
# ============================================================================

def render_scenario_comparison(residue_data):
    """Render scenario comparison using database scenario factors"""
    st.markdown("### 🎭 Comparação entre Cenários")

    # Get scenario factors from database
    fator_pessimista = residue_data.get('fator_pessimista', 0)
    fator_realista = residue_data.get('fator_realista', 0)
    fator_otimista = residue_data.get('fator_otimista', 0)
    fator_teorico = 1.0  # Theoretical is always 100%

    scenarios = {
        "Pessimista": fator_pessimista * 100,
        "Realista": fator_realista * 100,
        "Otimista": fator_otimista * 100,
        "Teórico (100%)": fator_teorico * 100
    }

    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(scenarios.keys()),
            y=list(scenarios.values()),
            text=[f"{v:.1f}%" for v in scenarios.values()],
            textposition='outside',
            marker_color=['#dc2626', '#059669', '#f59e0b', '#6b7280']
        )
    ])

    fig.update_layout(
        title='Disponibilidade por Cenário (%)',
        yaxis_title='Disponibilidade (%)',
        xaxis_title='Cenário',
        showlegend=False,
        height=400,
        yaxis=dict(range=[0, max(scenarios.values()) * 1.2])
    )

    st.plotly_chart(fig, use_container_width=True)

    # Scenario explanation
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pessimista", f"{fator_pessimista:.0%}", help="Cenário conservador - restrições significativas")

    with col2:
        st.metric("Realista", f"{fator_realista:.0%}", help="Cenário intermediário - estado atual")

    with col3:
        st.metric("Otimista", f"{fator_otimista:.0%}", help="Cenário otimista - melhorias de infraestrutura")

    with col4:
        st.metric("Teórico", "100%", help="Potencial máximo - sem restrições (referência)")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function - Database Integrated"""

    render_header()

    # Main navigation bar
    render_main_navigation(current_page="disponibilidade")
    render_navigation_divider()

    # Residue selection
    selected_residue = render_residue_selector()

    if not selected_residue:
        st.info("👆 Selecione um setor e resíduo acima para visualizar os dados")

        # Show database stats
        st.markdown("---")
        st.markdown("### 📊 Estatísticas do Banco de Dados")

        df_all = get_all_residues_with_params()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total de Resíduos", len(df_all), help="Resíduos catalogados no banco de dados")

        with col2:
            ag_count = len(df_all[df_all['setor'] == 'AG_AGRICULTURA'])
            st.metric("🌾 Agricultura", ag_count)

        with col3:
            pc_count = len(df_all[df_all['setor'] == 'PC_PECUARIA'])
            st.metric("🐄 Pecuária", pc_count)

        with col4:
            ur_count = len(df_all[df_all['setor'] == 'UR_URBANO'])
            st.metric("🏙️ Urbano", ur_count)

        # Show Industrial count separately
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            in_count = len(df_all[df_all['setor'] == 'IN_INDUSTRIAL'])
            st.metric("🏭 Industrial", in_count)

        with col2:
            valid_bmp = len(df_all[df_all['bmp_medio'] > 0])
            st.metric("Resíduos com BMP válido", valid_bmp, help="BMP > 0")

        with col3:
            valid_saf = len(df_all[df_all['fator_realista'] > 0])
            st.metric("Resíduos com SAF válido", valid_saf, help="SAF realista > 0")

        with col4:
            completeness = (valid_bmp / len(df_all)) * 100 if len(df_all) > 0 else 0
            st.metric("Completude do DB", f"{completeness:.0f}%")

        st.markdown("---")
        st.markdown("### 📚 Sobre a Disponibilidade")

        st.markdown("""
        **Fatores de Disponibilidade (SAF):**

        A disponibilidade real de um resíduo para biogás é determinada por 4 fatores principais:

        1. **FC (Fator de Coleta)**: Eficiência técnica de coleta (0.30-0.95)
           - Quão fácil é coletar o resíduo tecnicamente

        2. **FCp (Fator de Competição)**: % DISPONÍVEL após usos competitivos (0.10-0.90)
           - FCp = 0.70 significa 70% disponível, 30% vai para outros usos
           - FCp = 0.20 significa 20% disponível, 80% vai para usos estabelecidos
           - Exemplos de competição: cogeração, ração animal, fertilizante, indústria química

        3. **FS (Fator de Sazonalidade)**: Variação ao longo do ano (0.50-1.0)
           - Safra concentrada reduz disponibilidade anual

        4. **FL (Fator Logístico)**: Viabilidade de transporte/operação (0.50-0.95)
           - Distância econômica, custos operacionais

        **Fórmula Corrigida:**
        ```
        SAF = FC × FCp × FS × FL × 100%
        ```

        **Exemplo - Bagaço de Cana (alta competição):**
        - FC=0.95 (coleta excelente), FCp=0.20 (só 20% disponível, 80% vai para cogeração)
        - FS=0.90, FL=0.90
        - SAF = 0.95 × 0.20 × 0.90 × 0.90 = **15.4%** (conservador, reflete realidade)

        **Cenários:**
        - **Pessimista:** Fatores conservadores, restrições significativas
        - **Realista:** Pressupostos equilibrados, estado atual
        - **Otimista:** Melhorias de infraestrutura e logística
        - **Teórico (100%):** Potencial máximo sem restrições (referência apenas)
        """)

        return

    st.markdown("---")

    # Load residue data from database
    residue_data = get_residue_by_name(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados para este resíduo")
        return

    # ========================================================================
    # SECTION 1: AVAILABILITY CARD
    # ========================================================================

    render_availability_card_from_db(residue_data)

    st.markdown("---")

    # ========================================================================
    # SECTION 2: SAF WATERFALL CHART (NEW!)
    # ========================================================================

    st.markdown("### 📊 Breakdown de Disponibilidade (SAF) - Waterfall Chart")

    st.info("""
    **Nova visualização:** O gráfico waterfall mostra o impacto progressivo de cada fator na disponibilidade final.

    Começamos com o potencial teórico (100%) e aplicamos cada fator sequencialmente até chegar à disponibilidade real.
    """)

    fc = residue_data.get('fc_medio', 0)
    fcp = residue_data.get('fcp_medio', 0)
    fs = residue_data.get('fs_medio', 0)
    fl = residue_data.get('fl_medio', 0)

    try:
        fig_waterfall = create_waterfall_chart(fc, fcp, fs, fl, residue_data.get('nome', 'Resíduo'))
        st.plotly_chart(fig_waterfall, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar waterfall chart: {e}")

    st.markdown("---")

    # ========================================================================
    # SECTION 3: SCENARIO COMPARISON
    # ========================================================================

    render_scenario_comparison(residue_data)

    st.markdown("---")

    # ========================================================================
    # SECTION 4: TECHNICAL JUSTIFICATION
    # ========================================================================

    st.markdown("### 📝 Informações Adicionais")

    with st.expander("🔍 Ver Código e Categoria", expanded=False):
        st.markdown(f"**Código:** {residue_data.get('codigo', 'N/A')}")
        st.markdown(f"**Categoria:** {residue_data.get('categoria_codigo', 'N/A')}")
        st.markdown(f"**ID no banco:** {residue_data.get('id', 'N/A')}")

    # Footer
    st.markdown("---")
    st.caption("📊 CP2B - PanoramaCP2B | Database Integrado | Todos os 38 resíduos disponíveis (Agricultura, Pecuária, Urbano, Industrial)")


if __name__ == "__main__":
    main()
