"""
Page 4: Análise de Setores - Database-Driven Sector Analysis
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Features:
- Sector potential comparison
- Sector metrics and statistics
- Top residues by sector
- Sector contribution analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Database integration
from src.data_handler import get_all_residues_with_params

from src.ui.main_navigation import render_main_navigation, render_navigation_divider

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Análise de Setores - CP2B",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render page header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 50%, #8b5cf6 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🏭 Análise de Setores
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Comparação Setorial • Dados Validados do Banco de Dados
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            🌾 Agricultura • 🐄 Pecuária • 🏙️ Urbano • 🏭 Industrial
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
            key="sector_scenario"
        )

        st.markdown("---")
        st.markdown("### 🔍 Filtros")

        show_top_n = st.slider(
            "Top resíduos por setor:",
            min_value=3,
            max_value=10,
            value=5,
            step=1
        )

        return scenario, show_top_n


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sector_label(sector_code):
    """Convert sector code to label with emoji"""
    labels = {
        'AG_AGRICULTURA': '🌾 Agricultura',
        'PC_PECUARIA': '🐄 Pecuária',
        'UR_URBANO': '🏙️ Urbano',
        'IN_INDUSTRIAL': '🏭 Industrial'
    }
    return labels.get(sector_code, sector_code)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def render_sector_metrics(df, scenario):
    """Render sector overview metrics"""
    st.markdown(f"### 📊 Visão Geral dos Setores - Cenário {scenario}")

    # Map scenario to column
    scenario_col_map = {
        "Pessimista": "fator_pessimista",
        "Realista": "fator_realista",
        "Otimista": "fator_otimista"
    }
    fde_col = scenario_col_map[scenario]

    # Calculate sector statistics
    sector_stats = df.groupby('setor').agg({
        'nome': 'count',
        fde_col: 'mean',
        'bmp_medio': 'mean'
    }).reset_index()

    sector_stats.columns = ['setor', 'count', 'saf_medio', 'bmp_medio']
    sector_stats['fde_pct'] = sector_stats['saf_medio'] * 100

    # Display metrics
    cols = st.columns(4)

    sector_order = ['AG_AGRICULTURA', 'PC_PECUARIA', 'UR_URBANO', 'IN_INDUSTRIAL']
    sector_colors = {
        'AG_AGRICULTURA': '#10b981',
        'PC_PECUARIA': '#f59e0b',
        'UR_URBANO': '#3b82f6',
        'IN_INDUSTRIAL': '#8b5cf6'
    }

    for idx, sector_code in enumerate(sector_order):
        sector_data = sector_stats[sector_stats['setor'] == sector_code]

        if not sector_data.empty:
            with cols[idx]:
                label = get_sector_label(sector_code)
                count = int(sector_data['count'].values[0])
                saf = sector_data['fde_pct'].values[0]

                st.markdown(f"""
                <div style='background-color: {sector_colors[sector_code]}; padding: 1.5rem;
                            border-radius: 10px; color: white; text-align: center;'>
                    <h2 style='margin: 0; font-size: 2.5rem;'>{count}</h2>
                    <p style='margin: 5px 0; font-size: 0.9rem; opacity: 0.9;'>Resíduos</p>
                    <hr style='margin: 10px 0; opacity: 0.3;'>
                    <p style='margin: 0; font-size: 1.3rem; font-weight: bold;'>{saf:.1f}%</p>
                    <p style='margin: 0; font-size: 0.8rem; opacity: 0.8;'>FDE Médio</p>
                </div>
                <p style='text-align: center; margin-top: 10px; font-weight: 500;'>{label}</p>
                """, unsafe_allow_html=True)


def render_sector_distribution(df, scenario):
    """Render sector distribution charts"""
    st.markdown("### 📈 Distribuição Setorial")

    scenario_col_map = {
        "Pessimista": "fator_pessimista",
        "Realista": "fator_realista",
        "Otimista": "fator_otimista"
    }
    fde_col = scenario_col_map[scenario]

    col1, col2 = st.columns(2)

    with col1:
        # Residue count by sector
        sector_counts = df.groupby('setor').size().reset_index(name='count')
        sector_counts['label'] = sector_counts['setor'].apply(get_sector_label)

        fig = px.pie(
            sector_counts,
            values='count',
            names='label',
            title="Distribuição de Resíduos por Setor",
            color='setor',
            color_discrete_map={
                'AG_AGRICULTURA': '#10b981',
                'PC_PECUARIA': '#f59e0b',
                'UR_URBANO': '#3b82f6',
                'IN_INDUSTRIAL': '#8b5cf6'
            },
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Average FDE by sector
        sector_saf = df.groupby('setor')[fde_col].mean().reset_index()
        sector_saf['fde_pct'] = sector_saf[fde_col] * 100
        sector_saf['label'] = sector_saf['setor'].apply(get_sector_label)

        fig = px.bar(
            sector_saf,
            x='label',
            y='fde_pct',
            title=f"FDE Médio por Setor - {scenario}",
            labels={'fde_pct': 'FDE Médio (%)', 'label': 'Setor'},
            color='setor',
            text='fde_pct',
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


def render_top_residues_by_sector(df, scenario, top_n=5):
    """Render top residues for each sector"""
    st.markdown(f"### 🏆 Top {top_n} Resíduos por Setor")

    scenario_col_map = {
        "Pessimista": "fator_pessimista",
        "Realista": "fator_realista",
        "Otimista": "fator_otimista"
    }
    fde_col = scenario_col_map[scenario]

    # Create tabs for each sector
    sector_order = ['AG_AGRICULTURA', 'PC_PECUARIA', 'UR_URBANO', 'IN_INDUSTRIAL']
    tab_labels = [get_sector_label(s) for s in sector_order]

    tabs = st.tabs(tab_labels)

    for idx, sector_code in enumerate(sector_order):
        with tabs[idx]:
            sector_df = df[df['setor'] == sector_code].nlargest(top_n, fde_col)

            if not sector_df.empty:
                # Create horizontal bar chart
                sector_df_plot = sector_df[['nome', fde_col, 'bmp_medio']].copy()
                sector_df_plot['fde_pct'] = sector_df_plot[fde_col] * 100

                fig = px.bar(
                    sector_df_plot,
                    x='fde_pct',
                    y='nome',
                    orientation='h',
                    title=f"Top {top_n} - {get_sector_label(sector_code)}",
                    labels={'fde_pct': 'FDE (%)', 'nome': 'Resíduo'},
                    text='fde_pct',
                    color_discrete_sequence=['#f59e0b']
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    height=300,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)

                # Show data table
                display_df = sector_df[['nome', 'bmp_medio', fde_col]].copy()
                display_df['FDE (%)'] = display_df[fde_col] * 100
                display_df = display_df[['nome', 'bmp_medio', 'FDE (%)']].copy()
                display_df.columns = ['Resíduo', 'BMP (mL CH₄/g VS)', 'FDE (%)']
                display_df['BMP (mL CH₄/g VS)'] = display_df['BMP (mL CH₄/g VS)'].round(1)
                display_df['FDE (%)'] = display_df['FDE (%)'].round(2)

                st.dataframe(display_df, use_container_width=True)
            else:
                st.info(f"Nenhum resíduo encontrado para {get_sector_label(sector_code)}")


def render_sector_comparison_table(df, scenario):
    """Render detailed sector comparison table"""
    st.markdown("### 📋 Tabela Comparativa Detalhada")

    scenario_col_map = {
        "Pessimista": "fator_pessimista",
        "Realista": "fator_realista",
        "Otimista": "fator_otimista"
    }
    fde_col = scenario_col_map[scenario]

    # Create summary table
    summary = df.groupby('setor').agg({
        'nome': 'count',
        fde_col: ['mean', 'min', 'max'],
        'bmp_medio': ['mean', 'min', 'max']
    }).reset_index()

    # Flatten column names
    summary.columns = ['setor', 'count', 'fde_mean', 'fde_min', 'fde_max', 'bmp_mean', 'bmp_min', 'bmp_max']

    # Convert to percentages
    for col in ['fde_mean', 'fde_min', 'fde_max']:
        summary[col] = summary[col] * 100

    # Add labels
    summary['Setor'] = summary['setor'].apply(get_sector_label)

    # Prepare display dataframe
    display_df = pd.DataFrame({
        'Setor': summary['Setor'],
        'N° Resíduos': summary['count'],
        'FDE Médio (%)': summary['fde_mean'].round(2),
        'FDE Min (%)': summary['fde_min'].round(2),
        'FDE Max (%)': summary['fde_max'].round(2),
        'BMP Médio': summary['bmp_mean'].round(1),
        'BMP Min': summary['bmp_min'].round(1),
        'BMP Max': summary['bmp_max'].round(1)
    })

    st.dataframe(display_df, use_container_width=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""

    # Render header
    render_header()

    # Main navigation
    render_main_navigation(current_page="analise_setores")
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

    # Sector metrics
    render_sector_metrics(df, scenario)

    st.markdown("---")

    # Sector distribution
    render_sector_distribution(df, scenario)

    st.markdown("---")

    # Top residues by sector
    render_top_residues_by_sector(df, scenario, top_n)

    st.markdown("---")

    # Comparison table
    render_sector_comparison_table(df, scenario)

    st.markdown("---")

    # Methodology note
    st.markdown("### ℹ️ Metodologia")

    st.info("""
    **Análise Setorial:**

    Os setores foram definidos com base na origem dos resíduos:

    - **🌾 Agricultura**: Resíduos de culturas agrícolas (cana, citros, café, milho, soja, eucalipto)
    - **🐄 Pecuária**: Dejetos animais (aves, bovinos, suínos)
    - **🏙️ Urbano**: Resíduos sólidos urbanos e lodo de esgoto
    - **🏭 Industrial**: Efluentes e resíduos de processamento industrial

    **Cálculo de FDE:**
    FDE = FC × FCp × FS × FL

    **BMP**: Potencial Metanogênico em **mL CH₄/g VS** (valores validados por literatura científica)

    Todos os valores são baseados em **dados atualizados do banco de dados**.
    """)


if __name__ == "__main__":
    main()
