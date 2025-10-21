"""
Page 3: Análise Comparativa - Database-Driven Analytics
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Features:
- Top residues ranking by SAF
- Scenario comparison (Pessimista/Realista/Otimista)
- BMP distribution analysis
- Sector-wise comparisons
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Database integration
from src.data_handler import (
    get_all_residues_with_params,
    get_sector_summary,
    get_bmp_distribution
)

from src.ui.main_navigation import render_main_navigation, render_navigation_divider

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Análise Comparativa - CP2B",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render page header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #ec4899 50%, #f59e0b 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            📈 Análise Comparativa de Resíduos
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Ranking e Comparações • Dados Validados do Banco de Dados
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Top Resíduos • 🎯 Comparação Cenários • 🔬 Análise BMP
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

def render_sidebar():
    """Render sidebar controls"""
    with st.sidebar:
        st.markdown("### 🎭 Cenário")

        scenario = st.radio(
            "Escolha o cenário:",
            options=["Pessimista", "Realista", "Otimista"],
            index=1,  # Default to Realista
            key="comparative_scenario"
        )

        st.markdown("---")
        st.markdown("### 🔍 Filtros")

        top_n = st.slider(
            "Número de resíduos no ranking:",
            min_value=5,
            max_value=20,
            value=10,
            step=1
        )

        return scenario, top_n


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def render_top_residues_chart(df, scenario, top_n=10):
    """Render top residues ranking chart"""
    st.markdown(f"### 🏆 Top {top_n} Resíduos - Cenário {scenario}")

    # Select scenario column
    scenario_col_map = {
        "Pessimista": "fator_pessimista",
        "Realista": "fator_realista",
        "Otimista": "fator_otimista"
    }

    saf_col = scenario_col_map[scenario]

    # Get top N residues
    top_residues = df.nlargest(top_n, saf_col)[['nome', saf_col, 'setor', 'bmp_medio']].copy()
    top_residues['saf_pct'] = top_residues[saf_col] * 100

    # Create bar chart
    fig = px.bar(
        top_residues,
        x='saf_pct',
        y='nome',
        orientation='h',
        color='setor',
        title=f"Disponibilidade Final (SAF) - Cenário {scenario}",
        labels={'saf_pct': 'SAF (%)', 'nome': 'Resíduo', 'setor': 'Setor'},
        text='saf_pct',
        color_discrete_map={
            'AG_AGRICULTURA': '#10b981',
            'PC_PECUARIA': '#f59e0b',
            'UR_URBANO': '#3b82f6',
            'IN_INDUSTRIAL': '#8b5cf6'
        }
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        height=500,
        showlegend=True,
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show data table
    with st.expander("📊 Ver dados detalhados"):
        display_df = top_residues[['nome', 'setor', 'bmp_medio', 'saf_pct']].copy()
        display_df.columns = ['Resíduo', 'Setor', 'BMP (mL CH₄/g VS)', 'SAF (%)']
        display_df['SAF (%)'] = display_df['SAF (%)'].round(2)
        display_df['BMP (mL CH₄/g VS)'] = display_df['BMP (mL CH₄/g VS)'].round(1)
        st.dataframe(display_df, use_container_width=True)


def render_scenario_comparison(df, top_n=10):
    """Render comparison of all three scenarios"""
    st.markdown("### 🔄 Comparação de Cenários")

    st.info("""
    **Como interpretar:**
    - **Pessimista**: Considera fatores limitantes (baixa coleta, alta competição)
    - **Realista**: Cenário médio baseado em dados reais
    - **Otimista**: Condições favoráveis (alta eficiência, baixa competição)
    """)

    # Get top residues in Realista scenario
    top_residues = df.nlargest(top_n, 'fator_realista')['nome'].tolist()

    # Filter for these residues
    comparison_df = df[df['nome'].isin(top_residues)][['nome', 'fator_pessimista', 'fator_realista', 'fator_otimista']].copy()

    # Convert to percentages
    comparison_df['Pessimista'] = comparison_df['fator_pessimista'] * 100
    comparison_df['Realista'] = comparison_df['fator_realista'] * 100
    comparison_df['Otimista'] = comparison_df['fator_otimista'] * 100

    # Create grouped bar chart
    fig = go.Figure()

    for scenario, color in [('Pessimista', '#ef4444'), ('Realista', '#f59e0b'), ('Otimista', '#10b981')]:
        fig.add_trace(go.Bar(
            name=scenario,
            x=comparison_df['nome'],
            y=comparison_df[scenario],
            marker_color=color
        ))

    fig.update_layout(
        title=f"SAF (%) - Comparação dos 3 Cenários (Top {top_n})",
        xaxis_title="Resíduo",
        yaxis_title="SAF (%)",
        barmode='group',
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def render_bmp_analysis(df):
    """Render BMP distribution analysis"""
    st.markdown("### 🔬 Análise de BMP (Potencial Metanogênico)")

    col1, col2 = st.columns(2)

    with col1:
        # BMP distribution by sector
        fig = px.box(
            df,
            x='setor',
            y='bmp_medio',
            color='setor',
            title="Distribuição de BMP por Setor",
            labels={'bmp_medio': 'BMP (mL CH₄/g VS)', 'setor': 'Setor'},
            color_discrete_map={
                'AG_AGRICULTURA': '#10b981',
                'PC_PECUARIA': '#f59e0b',
                'UR_URBANO': '#3b82f6',
                'IN_INDUSTRIAL': '#8b5cf6'
            }
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # BMP histogram
        fig = px.histogram(
            df,
            x='bmp_medio',
            nbins=20,
            title="Distribuição de BMP - Todos os Resíduos",
            labels={'bmp_medio': 'BMP (mL CH₄/g VS)', 'count': 'Número de Resíduos'},
            color_discrete_sequence=['#f59e0b']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Statistics
    st.markdown("#### 📊 Estatísticas de BMP")
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

    with stats_col1:
        st.metric("Média", f"{df['bmp_medio'].mean():.1f} mL/g VS")
    with stats_col2:
        st.metric("Mediana", f"{df['bmp_medio'].median():.1f} mL/g VS")
    with stats_col3:
        st.metric("Mínimo", f"{df['bmp_medio'].min():.1f} mL/g VS")
    with stats_col4:
        st.metric("Máximo", f"{df['bmp_medio'].max():.1f} mL/g VS")


def render_sector_distribution(df):
    """Render sector distribution analysis"""
    st.markdown("### 🏭 Distribuição por Setor")

    col1, col2 = st.columns(2)

    with col1:
        # Count by sector
        sector_counts = df.groupby('setor').size().reset_index(name='count')

        fig = px.pie(
            sector_counts,
            values='count',
            names='setor',
            title="Número de Resíduos por Setor",
            color='setor',
            color_discrete_map={
                'AG_AGRICULTURA': '#10b981',
                'PC_PECUARIA': '#f59e0b',
                'UR_URBANO': '#3b82f6',
                'IN_INDUSTRIAL': '#8b5cf6'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Average SAF by sector
        sector_saf = df.groupby('setor')['fator_realista'].mean().reset_index()
        sector_saf['saf_pct'] = sector_saf['fator_realista'] * 100

        fig = px.bar(
            sector_saf,
            x='setor',
            y='saf_pct',
            title="SAF Médio por Setor (Cenário Realista)",
            labels={'saf_pct': 'SAF Médio (%)', 'setor': 'Setor'},
            color='setor',
            text='saf_pct',
            color_discrete_map={
                'AG_AGRICULTURA': '#10b981',
                'PC_PECUARIA': '#f59e0b',
                'UR_URBANO': '#3b82f6',
                'IN_INDUSTRIAL': '#8b5cf6'
            }
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""

    # Render header
    render_header()

    # Main navigation
    render_main_navigation(current_page="analise_comparativa")
    render_navigation_divider()

    # Sidebar controls
    scenario, top_n = render_sidebar()

    # Load data from database
    try:
        df = get_all_residues_with_params()

        if df.empty:
            st.error("❌ Nenhum dado encontrado no banco de dados")
            return

        st.success(f"✅ {len(df)} resíduos carregados do banco de dados")

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return

    # Main content
    st.markdown("---")

    # Top residues ranking
    render_top_residues_chart(df, scenario, top_n)

    st.markdown("---")

    # Scenario comparison
    render_scenario_comparison(df, top_n)

    st.markdown("---")

    # BMP analysis
    render_bmp_analysis(df)

    st.markdown("---")

    # Sector distribution
    render_sector_distribution(df)

    st.markdown("---")

    # Methodology note
    st.markdown("### ℹ️ Metodologia")

    st.info("""
    **Cálculo de SAF (Sistema de Availabilidade Final):**

    SAF = FC × FCp × FS × FL

    Onde:
    - **FC** (Fator de Coleta): Eficiência técnica de coleta
    - **FCp** (Fator de Competição): Percentual disponível (não competindo)
    - **FS** (Fator de Sazonalidade): Variação ao longo do ano
    - **FL** (Fator Logístico): Restrição econômica por distância

    **BMP** (Potencial Metanogênico): Agora em **mL CH₄/g VS** (conversão ×1000 de m³/ton)

    *Nota: BMP agora em mL CH₄/g VS (conversão: ÷ 1000 para m³/ton)*

    Todos os valores são baseados em **dados validados do banco de dados** com referências científicas.
    """)


if __name__ == "__main__":
    main()
