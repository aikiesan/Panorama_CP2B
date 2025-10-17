"""
Page 1: Disponibilidade de Resíduos - Enhanced with Phase 2 UI Components
CP2B - Main page for residue availability factors and validation
Phase 4: Integrated AvailabilityCard, ScenarioSelector, ContributionChart, MunicipalityRanking, ValidationPanel
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data.residue_registry import (
    get_available_residues,
    get_residue_data,
    get_residue_icon
)
from src.ui.tabs import render_sector_tabs
from src.ui.horizontal_nav import render_horizontal_nav

# Import Phase 2 UI components
from src.ui.availability_card import render_availability_card
from src.ui.scenario_selector import render_scenario_selector
from src.ui.contribution_chart import render_sector_contribution_chart, render_sector_bar_chart
from src.ui.municipality_ranking import render_top_municipalities_table
from src.ui.validation_panel import render_data_validation


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
            🔬 Metodologia Conservadora • 📊 Dados Validados • 🌾 Agricultura • 🐄 Pecuária • 🏙️ RSU
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN RENDER - PHASE 4 ENHANCED
# ============================================================================

def initialize_session_state():
    """Initialize session state for scenario selection"""
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = "Realista"


def main():
    """Main page render function - Phase 4 with integrated UI components"""

    # Initialize session state
    initialize_session_state()

    render_header()

    # Horizontal navigation tabs
    render_horizontal_nav("Disponibilidade")

    # Sector and residue selection
    selected_sector, selected_residue = render_sector_tabs(key_prefix="disponibilidade")

    if not selected_residue:
        st.info("👆 Selecione um setor e resíduo acima para visualizar os dados")
        return

    st.markdown("---")

    # Load residue data
    residue_data = get_residue_data(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados para este resíduo")
        return

    # ========================================================================
    # SECTION 1: AVAILABILITY CARD + SCENARIO SELECTOR (Side by Side)
    # ========================================================================

    col_card, col_scenario = st.columns([2, 1])

    with col_card:
        st.markdown("### 📋 Informações do Resíduo")
        render_availability_card(residue_data)

    with col_scenario:
        st.markdown("### 🎭 Selecione Cenário")
        selected_scenario = render_scenario_selector(key="disponibilidade_scenario", default="Realista")
        st.session_state.selected_scenario = selected_scenario

    st.markdown("---")

    # ========================================================================
    # SECTION 2: MAIN RESULTS METRICS (Dynamic based on selected scenario)
    # ========================================================================

    st.markdown("### 📊 Principais Resultados")

    scenarios = residue_data.scenarios
    availability = residue_data.availability
    realistic_potential = scenarios.get(st.session_state.selected_scenario, 0)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            f"💨 Potencial ({st.session_state.selected_scenario})",
            f"{realistic_potential:,.1f} Mi m³/ano",
            help=f"Cenário {st.session_state.selected_scenario} de CH₄"
        )

    with col2:
        theoretical = scenarios.get('Teórico (100%)', 0)
        reduction = ((theoretical - realistic_potential) / theoretical * 100) if theoretical > 0 else 0
        st.metric(
            "📉 Redução vs Teórico",
            f"{reduction:.1f}%",
            delta=f"vs. {theoretical:,.0f} Mi m³/ano",
            delta_color="normal",
            help="Redução do potencial teórico"
        )

    with col3:
        st.metric(
            "✅ Disponibilidade Final",
            f"{availability.final_availability:.1f}%",
            help="Disponibilidade real após fatores"
        )

    with col4:
        electricity = realistic_potential * 1.43
        st.metric(
            "⚡ Energia Equivalente",
            f"{electricity:,.0f} GWh/ano",
            help="Potencial de geração elétrica"
        )

    st.markdown("---")

    # ========================================================================
    # SECTION 3: SCENARIO COMPARISON + CONTRIBUTION CHARTS (Side by Side)
    # ========================================================================

    col_scenario_comp, col_contrib = st.columns(2)

    with col_scenario_comp:
        render_scenario_comparison(residue_data.scenarios)

    with col_contrib:
        st.markdown("### 📈 Análise de Contribuição")
        if residue_data.has_sub_residues():
            render_sector_contribution_chart(residue_data, st.session_state.selected_scenario)
        else:
            st.info("ℹ️ Este resíduo não possui sub-componentes")

    st.markdown("---")

    # ========================================================================
    # SECTION 4: MUNICIPALITY RANKING
    # ========================================================================

    st.markdown("### 🏆 Análise Geográfica - Top Municípios")
    render_top_municipalities_table(residue_data)

    st.markdown("---")

    # ========================================================================
    # SECTION 5: AVAILABILITY FACTORS TABLE (Updated layout)
    # ========================================================================

    st.markdown("### 🔢 Fatores de Disponibilidade (Literatura Validada)")

    st.info("""
    **📊 Como interpretar a tabela:**
    - **Mínimo**: Valor mínimo encontrado na literatura revisada
    - **Valor Adotado**: Valor conservador utilizado no cálculo ✅
    - **Máximo**: Valor máximo encontrado na literatura
    - **Justificativa**: Explicação de cada fator
    """)

    ranges_data = availability.to_range_table()

    if ranges_data:
        df_factors = pd.DataFrame(ranges_data)
        st.dataframe(
            df_factors,
            hide_index=True,
            width="stretch",
            height=300,
            column_config={
                'Fator': st.column_config.TextColumn('Fator de Correção', width='medium'),
                'Mínimo': st.column_config.TextColumn('Mínimo', width='small'),
                'Valor Adotado': st.column_config.TextColumn('Valor Adotado ✅', width='small'),
                'Máximo': st.column_config.TextColumn('Máximo', width='small'),
                'Justificativa': st.column_config.TextColumn('Justificativa', width='large')
            }
        )
    else:
        factors_dict = availability.to_dict()
        df_factors = pd.DataFrame([
            {'Fator': k, 'Valor': v} for k, v in factors_dict.items()
        ])
        st.dataframe(df_factors, hide_index=True, width="stretch")

    with st.expander("ℹ️ Metodologia de Cálculo", expanded=False):
        st.markdown("""
        **Fórmula da Disponibilidade Final:**

        ```
        Disponibilidade Final (SAF) = FC × (1 - FCp) × FS × FL × 100%
        ```

        **Descrição dos Fatores:**

        - **FC (Fator de Coleta)**: Eficiência técnica de recolhimento do resíduo
        - **FCp (Fator de Competição)**: Percentual competido por usos prioritários
        - **FS (Fator Sazonal)**: Variação sazonal da disponibilidade
        - **FL (Fator Logístico)**: Restrição por distância econômica

        **Valores Conservadores:** Os ranges MIN/MEAN/MAX mostram a variabilidade,
        e o "Valor Adotado" é escolhido de forma conservadora para garantir estimativas realistas.
        """)

    st.markdown("---")

    # ========================================================================
    # SECTION 6: DATA VALIDATION PANEL
    # ========================================================================

    st.markdown("### ✓ Validação de Dados")
    render_data_validation(residue_data)

    st.markdown("---")

    # ========================================================================
    # SECTION 7: TECHNICAL JUSTIFICATION
    # ========================================================================

    st.markdown("### 📝 Justificativa Técnica")

    with st.expander("📖 Metodologia e Fundamentação", expanded=False):
        st.markdown(residue_data.justification)

    st.markdown("---")

    # Footer
    st.caption("📊 CP2B - PanoramaCP2B | Dados validados e cenários conservadores | Phase 4 Enhanced UI")


if __name__ == "__main__":
    main()
