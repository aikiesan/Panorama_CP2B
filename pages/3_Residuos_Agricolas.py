"""
Resíduos Agrícolas - Análise Detalhada
Página especializada em resíduos da agricultura paulista.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import data_handler as dh
from src import plotter as pl
from src import ui_components as ui
from src.data_sources import sidra_handler as sidra

# --- Page Configuration ---
st.set_page_config(
    page_title="Resíduos Agrícolas - Panorama de Resíduos SP",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium design system
ui.load_css()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🌾 Resíduos Agrícolas</h1>
    <p class="hero-subtitle">Análise Detalhada da Produção e Potencial de Resíduos Agrícolas em SP</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
df_municipios = dh.load_all_municipalities()
df_agricola = sidra.load_sidra_agricola()

# --- Info Box ---
st.info("""
📌 **Sobre esta seção**: Explore os dados de resíduos agrícolas provenientes das principais
culturas do Estado de São Paulo. Os dados incluem área plantada, produção, geração de resíduos
e potencial de biogás por município e cultura.
""")

st.markdown("---")

# --- KPIs ---
if not df_agricola.empty:
    totais = sidra.get_total_residuos_agricola()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌾 Produção Total",
            f"{totais['total_producao_ton']/1_000_000:.2f}M ton",
            help="Produção agrícola total em toneladas"
        )

    with col2:
        st.metric(
            "♻️ Resíduos Gerados",
            f"{totais['total_residuos_ton']/1_000_000:.2f}M ton",
            help="Total de resíduos agrícolas gerados"
        )

    with col3:
        st.metric(
            "⚡ Potencial Biogás",
            f"{totais['total_potencial_biogas_m3']/1_000_000:.1f}M m³",
            help="Potencial de produção de biogás"
        )

    with col4:
        st.metric(
            "🌱 Culturas",
            f"{totais['culturas_count']}",
            help="Número de culturas analisadas"
        )
else:
    st.warning("""
⚠️ **Dados não disponíveis**: As tabelas de dados agrícolas ainda não foram populadas.

Para visualizar esta seção completamente, importe seus dados para a tabela `residuos_agricolas` no banco de dados.
    """)

    # Show data from existing municipalities table
    col1, col2, col3 = st.columns(3)

    with col1:
        total_cana = df_municipios['biogas_cana_m_ano'].sum()
        st.metric("🎋 Cana-de-açúcar", f"{total_cana/1_000_000:.1f}M m³/ano")

    with col2:
        total_soja = df_municipios['biogas_soja_m_ano'].sum()
        st.metric("🫘 Soja", f"{total_soja/1_000_000:.1f}M m³/ano")

    with col3:
        total_milho = df_municipios['biogas_milho_m_ano'].sum()
        st.metric("🌽 Milho", f"{total_milho/1_000_000:.1f}M m³/ano")

st.markdown("---")

# --- Sidebar: Filters ---
st.sidebar.header("🔍 Filtros")

if not df_agricola.empty and 'cultura' in df_agricola.columns:
    culturas_disponiveis = sidra.get_culturas_disponiveis()
    cultura_selecionada = st.sidebar.selectbox(
        "Selecione a cultura:",
        options=["Todas"] + culturas_disponiveis
    )
else:
    # Use data from municipalities table
    culturas_disponiveis = ['Cana-de-açúcar', 'Soja', 'Milho', 'Café', 'Citros', 'Silvicultura']
    cultura_selecionada = st.sidebar.selectbox(
        "Selecione a cultura:",
        options=["Todas"] + culturas_disponiveis
    )

# --- Main Content: Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "🗺️ Análise Espacial",
    "📈 Séries Temporais",
    "🔍 Análise por Cultura"
])

# Tab 1: Overview
with tab1:
    st.subheader("📊 Visão Geral - Resíduos Agrícolas")

    # Use municipalities data as fallback
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌾 Potencial por Substrato Agrícola")

        df_substrato_agri = pd.DataFrame({
            'cultura': ['Cana-de-açúcar', 'Soja', 'Milho', 'Café', 'Citros', 'Silvicultura'],
            'potencial_m3_ano': [
                df_municipios['biogas_cana_m_ano'].sum(),
                df_municipios['biogas_soja_m_ano'].sum(),
                df_municipios['biogas_milho_m_ano'].sum(),
                df_municipios['biogas_cafe_m_ano'].sum(),
                df_municipios['biogas_citros_m_ano'].sum(),
                df_municipios['biogas_silvicultura_m_ano'].sum()
            ]
        })

        df_substrato_agri = df_substrato_agri[df_substrato_agri['potencial_m3_ano'] > 0].sort_values('potencial_m3_ano', ascending=False)

        fig_barras = px.bar(
            df_substrato_agri,
            x='cultura',
            y='potencial_m3_ano',
            title="Potencial de Biogás por Cultura Agrícola",
            labels={'cultura': 'Cultura', 'potencial_m3_ano': 'Potencial (m³/ano)'},
            color='potencial_m3_ano',
            color_continuous_scale='Greens'
        )

        fig_barras.update_layout(showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Distribuição Percentual")

        fig_pizza = px.pie(
            df_substrato_agri,
            values='potencial_m3_ano',
            names='cultura',
            title="Distribuição do Potencial Agrícola",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_pizza, use_container_width=True)

    st.markdown("---")

    # Top municipalities
    st.markdown("### 🏆 Top 15 Municípios - Potencial Agrícola")

    df_top_agri = df_municipios.nlargest(15, 'total_agricola_m_ano')[
        ['nome_municipio', 'total_agricola_m_ano', 'biogas_cana_m_ano', 'biogas_soja_m_ano', 'biogas_milho_m_ano']
    ].copy()

    fig_top = go.Figure()

    fig_top.add_trace(go.Bar(
        y=df_top_agri['nome_municipio'],
        x=df_top_agri['biogas_cana_m_ano'],
        name='Cana',
        orientation='h',
        marker=dict(color='#27ae60')
    ))

    fig_top.add_trace(go.Bar(
        y=df_top_agri['nome_municipio'],
        x=df_top_agri['biogas_soja_m_ano'],
        name='Soja',
        orientation='h',
        marker=dict(color='#f39c12')
    ))

    fig_top.add_trace(go.Bar(
        y=df_top_agri['nome_municipio'],
        x=df_top_agri['biogas_milho_m_ano'],
        name='Milho',
        orientation='h',
        marker=dict(color='#e74c3c')
    ))

    fig_top.update_layout(
        barmode='stack',
        title='Top 15 Municípios - Composição do Potencial Agrícola',
        xaxis_title='Potencial de Biogás (m³/ano)',
        yaxis_title='',
        height=600,
        showlegend=True
    )

    st.plotly_chart(fig_top, use_container_width=True)

# Tab 2: Spatial Analysis
with tab2:
    st.subheader("🗺️ Análise Espacial - Distribuição Geográfica")

    st.info("🗺️ **Mapa**: A visualização geográfica permite identificar regiões com maior concentração de potencial agrícola.")

    # Create a choropleth map if geojson is available
    from pathlib import Path
    geojson_path = Path(__file__).parent.parent / "data" / "processed" / "sp_municipios_simplified_0_001.geojson"

    if geojson_path.exists():
        try:
            fig_mapa = pl.criar_mapa_coropleth_sp(df_municipios, str(geojson_path), 'total_agricola_m_ano')
            st.plotly_chart(fig_mapa, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Mapa temporariamente indisponível: {e}")
    else:
        st.info("📊 Mapa geográfico será adicionado em breve.")

    # Scatter plot: Area vs Production
    st.markdown("### 📍 Relação: Área Territorial vs Potencial Agrícola")

    fig_scatter = px.scatter(
        df_municipios[df_municipios['total_agricola_m_ano'] > 0],
        x='area_km2',
        y='total_agricola_m_ano',
        size='total_agricola_m_ano',
        hover_data=['nome_municipio'],
        title='Área Territorial vs Potencial Agrícola',
        labels={'area_km2': 'Área (km²)', 'total_agricola_m_ano': 'Potencial Biogás (m³/ano)'},
        color='total_agricola_m_ano',
        color_continuous_scale='Greens'
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# Tab 3: Time Series
with tab3:
    st.subheader("📈 Séries Temporais")

    if not df_agricola.empty and 'ano' in df_agricola.columns:
        st.markdown("### 📊 Evolução da Produção e Resíduos ao Longo dos Anos")

        # Group by year
        df_evolucao = df_agricola.groupby('ano').agg({
            'producao_ton': 'sum',
            'residuo_gerado_ton': 'sum',
            'potencial_biogas_m3': 'sum'
        }).reset_index()

        fig_line = go.Figure()

        fig_line.add_trace(go.Scatter(
            x=df_evolucao['ano'],
            y=df_evolucao['producao_ton'],
            name='Produção (ton)',
            mode='lines+markers',
            line=dict(color='#27ae60', width=3)
        ))

        fig_line.add_trace(go.Scatter(
            x=df_evolucao['ano'],
            y=df_evolucao['residuo_gerado_ton'],
            name='Resíduos (ton)',
            mode='lines+markers',
            line=dict(color='#e67e22', width=3)
        ))

        fig_line.update_layout(
            title='Evolução Temporal - Produção e Resíduos Agrícolas',
            xaxis_title='Ano',
            yaxis_title='Toneladas',
            hovermode='x unified'
        )

        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("""
📊 **Análise temporal**: Para visualizar séries temporais, os dados precisam incluir
informações de múltiplos anos na tabela `residuos_agricolas`.
        """)

        st.markdown("### 📌 Dados Disponíveis (Snapshot Atual)")
        st.metric("Total Agrícola Atual", f"{df_municipios['total_agricola_m_ano'].sum()/1_000_000:.1f}M m³/ano")

# Tab 4: By Crop Analysis
with tab4:
    st.subheader(f"🔍 Análise Detalhada: {cultura_selecionada}")

    if cultura_selecionada == "Todas":
        st.info("Selecione uma cultura específica no filtro lateral para ver análise detalhada.")

        # Show summary table
        st.markdown("### 📊 Resumo Geral por Cultura")

        col_map = {
            'Cana-de-açúcar': 'biogas_cana_m_ano',
            'Soja': 'biogas_soja_m_ano',
            'Milho': 'biogas_milho_m_ano',
            'Café': 'biogas_cafe_m_ano',
            'Citros': 'biogas_citros_m_ano',
            'Silvicultura': 'biogas_silvicultura_m_ano'
        }

        summary_data = []
        for cultura, col in col_map.items():
            if col in df_municipios.columns:
                total = df_municipios[col].sum()
                municipios_com_producao = (df_municipios[col] > 0).sum()
                media = df_municipios[df_municipios[col] > 0][col].mean() if municipios_com_producao > 0 else 0

                summary_data.append({
                    'Cultura': cultura,
                    'Potencial Total (m³/ano)': f"{total:,.0f}",
                    'Municípios Produtores': municipios_com_producao,
                    'Média por Município (m³/ano)': f"{media:,.0f}"
                })

        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)

    else:
        # Detailed analysis for selected crop
        col_map = {
            'Cana-de-açúcar': 'biogas_cana_m_ano',
            'Soja': 'biogas_soja_m_ano',
            'Milho': 'biogas_milho_m_ano',
            'Café': 'biogas_cafe_m_ano',
            'Citros': 'biogas_citros_m_ano',
            'Silvicultura': 'biogas_silvicultura_m_ano'
        }

        coluna = col_map.get(cultura_selecionada)

        if coluna and coluna in df_municipios.columns:
            df_cultura = df_municipios[df_municipios[coluna] > 0][['nome_municipio', coluna, 'populacao_2022', 'area_km2']].copy()
            df_cultura = df_cultura.sort_values(coluna, ascending=False)

            # KPIs for this crop
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🌾 Potencial Total", f"{df_cultura[coluna].sum()/1_000_000:.2f}M m³/ano")

            with col2:
                st.metric("📍 Municípios Produtores", len(df_cultura))

            with col3:
                st.metric("📊 Média por Município", f"{df_cultura[coluna].mean():,.0f} m³/ano")

            st.markdown(f"### 📊 Top 20 Municípios Produtores - {cultura_selecionada}")

            fig_crop = px.bar(
                df_cultura.head(20),
                x='nome_municipio',
                y=coluna,
                title=f'Top 20 Municípios - {cultura_selecionada}',
                labels={'nome_municipio': 'Município', coluna: 'Potencial (m³/ano)'},
                color=coluna,
                color_continuous_scale='Greens'
            )

            fig_crop.update_layout(xaxis={'categoryorder': 'total descending'}, showlegend=False)
            st.plotly_chart(fig_crop, use_container_width=True)

            # Data table
            with st.expander("📋 Ver Dados Completos"):
                df_display = df_cultura.copy()
                df_display.columns = ['Município', 'Potencial Biogás (m³/ano)', 'População (2022)', 'Área (km²)']
                st.dataframe(df_display, use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <h3 style="color: #27ae60;">🌾 Resíduos Agrícolas</h3>
    <p><strong>Análise detalhada da produção agrícola e geração de resíduos</strong></p>
    <p>Fontes: SIDRA/IBGE, NIPE/UNICAMP</p>
</div>
""", unsafe_allow_html=True)
