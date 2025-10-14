"""
Page 1: Disponibilidade de Resíduos
CP2B - Main page for residue availability factors and validation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.research_data import (
    get_available_residues,
    get_residue_data,
    get_residue_icon
)
from src.ui_components import render_full_selector


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
# MAIN RESULTS CARDS
# ============================================================================

def render_main_results(residue_data):
    """Render key metrics cards"""
    st.markdown("### 📊 Principais Resultados")

    scenarios = residue_data.scenarios
    availability = residue_data.availability

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        realistic_potential = scenarios.get('Realista', 0)
        st.metric(
            "💨 Potencial Realista",
            f"{realistic_potential:,.1f} Mi m³/ano",
            help="Cenário realista validado com CH₄"
        )

    with col2:
        theoretical = scenarios.get('Teórico (100%)', 0)
        reduction = ((theoretical - realistic_potential) / theoretical * 100) if theoretical > 0 else 0
        st.metric(
            "📉 Redução do Teórico",
            f"{reduction:.1f}%",
            delta=f"vs. {theoretical:,.0f} Mi m³/ano",
            delta_color="normal",
            help="Redução do potencial teórico devido a fatores de competição"
        )

    with col3:
        st.metric(
            "✅ Disponibilidade Final",
            f"{availability.final_availability:.1f}%",
            help="Disponibilidade real após todos os fatores de correção"
        )

    with col4:
        # Electricity equivalent (assuming 1.43 kWh/m³ CH₄)
        electricity = realistic_potential * 1.43
        st.metric(
            "⚡ Energia Equivalente",
            f"{electricity:,.0f} GWh/ano",
            help="Potencial de geração elétrica"
        )


# ============================================================================
# AVAILABILITY FACTORS TABLE
# ============================================================================

def render_availability_factors(availability):
    """Render availability factors table"""
    st.markdown("### 🔢 Fatores de Disponibilidade")

    factors_dict = availability.to_dict()

    # Create DataFrame
    df_factors = pd.DataFrame([
        {'Fator': k, 'Valor': v} for k, v in factors_dict.items()
    ])

    # Display as table
    st.dataframe(
        df_factors,
        hide_index=True,
        use_container_width=True,
        column_config={
            'Fator': st.column_config.TextColumn('Fator de Correção', width='large'),
            'Valor': st.column_config.TextColumn('Valor', width='medium')
        }
    )

    # Legend
    with st.expander("ℹ️ Legenda dos Fatores", expanded=False):
        st.markdown("""
        **Fatores de Correção Aplicados:**

        - **FC (Fator de Coleta)**: Eficiência técnica de recolhimento do resíduo
        - **FCp (Fator de Competição)**: Percentual competido por usos prioritários estabelecidos
        - **FS (Fator Sazonal)**: Variação sazonal da disponibilidade ao longo do ano
        - **FL (Fator Logístico)**: Restrição por distância econômica de transporte (tipicamente 20-30 km)

        **Metodologia:**
        Disponibilidade Final = FC × (1 - FCp) × FS × FL × 100%

        Valores conservadores baseados em dados de usinas reais, literatura científica e normas ambientais.
        """)


# ============================================================================
# SCENARIO COMPARISON
# ============================================================================

def render_scenario_comparison(scenarios):
    """Render scenario comparison charts"""
    st.markdown("### 🎭 Comparação entre Cenários")

    st.info("""
    **Metodologia de Cenários:**

    - **Pessimista**: Fatores conservadores máximos (maior competição)
    - **Realista**: Fatores calibrados com dados reais (base para planejamento)
    - **Otimista**: Fatores otimistas (menor competição, maior eficiência)
    - **Teórico (100%)**: Disponibilidade total sem competições (não operacional)
    """)

    scenario_names = list(scenarios.keys())
    ch4_values = list(scenarios.values())

    # Calculate deltas from realistic
    realistic_value = scenarios.get('Realista', 0)
    delta_values = [((v - realistic_value) / realistic_value * 100) if realistic_value > 0 else 0 for v in ch4_values]

    col1, col2 = st.columns(2)

    with col1:
        # CH4 potential comparison
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
            height=400
        )
        st.plotly_chart(fig_ch4, use_container_width=True)

    with col2:
        # Delta comparison
        fig_delta = go.Figure(data=[
            go.Bar(
                x=scenario_names,
                y=delta_values,
                text=[f"{v:+.1f}%" for v in delta_values],
                textposition='auto',
                marker_color=['#dc2626', '#6b7280', '#f59e0b', '#2563eb']
            )
        ])
        fig_delta.update_layout(
            title='Variação vs Cenário Realista (%)',
            yaxis_title='Delta (%)',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_delta, use_container_width=True)


# ============================================================================
# TECHNICAL JUSTIFICATION
# ============================================================================

def render_justification(residue_data):
    """Render technical justification section"""
    st.markdown("### 📝 Justificativa Técnica")

    with st.expander("📖 Metodologia e Fundamentação", expanded=False):
        st.markdown(residue_data.justification)


# ============================================================================
# TOP MUNICIPALITIES (BACKGROUND)
# ============================================================================

def render_top_municipalities(residue_data):
    """Render top municipalities if available"""
    if not residue_data.top_municipalities:
        return

    st.markdown("### 🏆 Top 5 Municípios Produtores (Referência)")

    df_top = pd.DataFrame(residue_data.top_municipalities[:5])

    st.dataframe(
        df_top,
        hide_index=True,
        use_container_width=True,
        column_config={
            'rank': '#',
            'name': 'Município',
            'ch4': st.column_config.NumberColumn('CH₄ (Mi m³/ano)', format="%.1f"),
            'electricity': st.column_config.NumberColumn('Eletricidade (GWh/ano)', format="%.0f")
        }
    )

    st.caption("💡 Dados geográficos disponíveis como referência para planejamento regional")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function"""
    render_header()

    # New parallel sector + residue selector
    selected_residue = render_full_selector(key_prefix="disponibilidade")

    if not selected_residue:
        return

    st.markdown("---")

    # Load residue data
    residue_data = get_residue_data(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados para este resíduo")
        return

    # Render all sections
    render_main_results(residue_data)

    st.markdown("---")

    render_availability_factors(residue_data.availability)

    st.markdown("---")

    render_scenario_comparison(residue_data.scenarios)

    st.markdown("---")

    render_justification(residue_data)

    st.markdown("---")

    render_top_municipalities(residue_data)


if __name__ == "__main__":
    main()
