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
    get_residue_icon,
    get_residues_by_sector
)
from src.ui.tabs import render_sector_tabs
from src.ui.horizontal_nav import render_horizontal_nav

# Import Phase 2 UI components
from src.ui.availability_card import render_availability_card
from src.ui.contribution_chart import render_sector_contribution_chart, render_sector_bar_chart
from src.ui.municipality_ranking import render_top_municipalities_table
from src.ui.validation_panel import render_data_validation

# Import Phase 5 SAF helpers
from src.utils.saf_helpers import (
    get_high_priority_residues,
    get_viable_residues,
    get_saf_tier_color,
    create_saf_badge,
    sort_residues_by_saf
)


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
    """Initialize session state for scenario selection and SAF filter"""
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = "Realista"
    if "saf_filter" not in st.session_state:
        st.session_state.saf_filter = "All"


def render_sidebar_controls():
    """Render sidebar controls: scenario selector and SAF priority filter"""
    with st.sidebar:
        st.markdown("### 🎭 Cenário")

        scenario_options = ["Pessimista", "Realista", "Otimista", "Teórico (100%)"]
        scenario_index = scenario_options.index(st.session_state.selected_scenario) \
                         if st.session_state.selected_scenario in scenario_options else 1

        selected_scenario = st.radio(
            "Escolha o cenário:",
            options=scenario_options,
            index=scenario_index,
            key="scenario_sidebar",
            help="Selecione o cenário de potencial para análise"
        )
        st.session_state.selected_scenario = selected_scenario

        st.markdown("---")
        st.markdown("### 🚀 Filtro de Prioridade (SAF)")

        saf_filter_options = ["All", "High Priority (SAF > 8%)", "Viable (SAF > 4%)"]
        saf_filter_index = saf_filter_options.index(st.session_state.saf_filter) \
                          if st.session_state.saf_filter in saf_filter_options else 0

        selected_saf_filter = st.radio(
            "Mostrar resíduos por prioridade:",
            options=saf_filter_options,
            index=saf_filter_index,
            key="saf_filter_sidebar",
            help="Filtrar resíduos por disponibilidade real (SAF)"
        )
        st.session_state.saf_filter = selected_saf_filter

        return selected_scenario, selected_saf_filter


def main():
    """Main page render function - Phase 4 with integrated UI components"""

    # Initialize session state
    initialize_session_state()

    render_header()

    # Render sidebar controls (scenario selector and SAF filter)
    selected_scenario, selected_saf_filter = render_sidebar_controls()

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

    # Display SAF Priority Badge if available
    if hasattr(residue_data, 'saf_real') and residue_data.saf_real is not None:
        badge_html = create_saf_badge(residue_data)
        tier_color = get_saf_tier_color(residue_data.priority_tier) if hasattr(residue_data, 'priority_tier') else "#666"
        st.markdown(f"<p style='color:{tier_color};font-weight:bold;'>{badge_html}</p>", unsafe_allow_html=True)

    # ========================================================================
    # SECTION 1: AVAILABILITY CARD (Full Width)
    # ========================================================================

    st.markdown("### 📋 Informações do Resíduo")
    render_availability_card(residue_data)

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
        st.markdown("### 🎭 Comparação entre Cenários")

        # Create scenario comparison chart
        scenario_names = list(residue_data.scenarios.keys())
        ch4_values = list(residue_data.scenarios.values())

        # Calculate deltas from realistic
        realistic_value = residue_data.scenarios.get('Realista', 0)
        delta_values = [
            ((v - realistic_value) / realistic_value * 100) if realistic_value > 0 else 0
            for v in ch4_values
        ]

        # CH4 potential comparison chart
        fig_ch4 = go.Figure(data=[
            go.Bar(
                x=scenario_names,
                y=ch4_values,
                text=[f"{v:,.0f}" for v in ch4_values],
                textposition='auto',
                marker_color=['#dc2626', '#059669', '#f59e0b', '#6b7280']
            )
        ])
        fig_ch4.update_layout(
            title='Potencial de Biogás (Mi m³ CH₄/ano)',
            yaxis_title='CH₄ (Mi m³/ano)',
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_ch4, width="stretch")

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

    # Get municipalities from residue data
    municipalities = residue_data.top_municipalities if hasattr(residue_data, 'top_municipalities') else []
    if municipalities:
        # Format municipalities with required fields
        formatted_municipalities = []
        for idx, munic in enumerate(municipalities):
            formatted_municipalities.append({
                'rank': idx + 1,
                'name': munic.get('name', 'N/A'),
                'ch4': munic.get('ch4_potential', 0),
                'electricity': munic.get('ch4_potential', 0) * 0.143,  # 1 Mi m³ CH₄ ≈ 0.143 GWh
                'percentage': munic.get('percentage', 0),
                'state': 'SP'  # Default to SP
            })
        render_top_municipalities_table(formatted_municipalities)
    else:
        st.info("ℹ️ Sem dados de municípios disponíveis para este resíduo")

    st.markdown("---")

    # ========================================================================
    # SECTION 5: DATA VALIDATION PANEL
    # ========================================================================

    st.markdown("### ✓ Validação de Dados")
    render_data_validation(residue_data)

    st.markdown("---")

    # ========================================================================
    # SECTION 6: TECHNICAL JUSTIFICATION
    # ========================================================================

    st.markdown("### 📝 Justificativa Técnica")

    with st.expander("📖 Metodologia e Fundamentação", expanded=False):
        st.markdown(residue_data.justification)

    st.markdown("---")

    # Footer
    st.caption("📊 CP2B - PanoramaCP2B | Dados validados e cenários conservadores | Phase 4 Enhanced UI")


if __name__ == "__main__":
    main()
