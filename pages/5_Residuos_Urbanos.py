"""
Resíduos Urbanos - Análise Detalhada
Página especializada em resíduos sólidos urbanos e resíduos de poda.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import data_handler as dh
from src import plotter as pl
from src import ui_components as ui

# --- Page Configuration ---
st.set_page_config(
    page_title="Resíduos Urbanos - Panorama de Resíduos SP",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium design system
ui.load_css()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🏭 Resíduos Urbanos</h1>
    <p class="hero-subtitle">Análise de RSU (Resíduos Sólidos Urbanos) e Resíduos de Poda em SP</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
df_municipios = dh.load_all_municipalities()

# --- Info Box ---
st.info("""
📌 **Sobre esta seção**: Explore os dados de resíduos urbanos do Estado de São Paulo,
incluindo Resíduos Sólidos Urbanos (RSU) e Resíduos de Poda e Capina (RPO). Os dados
mostram o potencial de aproveitamento energético destes resíduos.
""")

st.markdown("---")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_urbano = df_municipios['total_urbano_m_ano'].sum()
    st.metric("🏙️ Total Urbano", f"{total_urbano/1_000_000:.1f}M m³/ano")

with col2:
    total_rsu = df_municipios['rsu_potencial_m_ano'].sum()
    st.metric("🗑️ RSU", f"{total_rsu/1_000_000:.1f}M m³/ano")

with col3:
    total_rpo = df_municipios['rpo_potencial_m_ano'].sum()
    st.metric("🍂 RPO (Poda)", f"{total_rpo/1_000:.1f}K m³/ano")

with col4:
    municipios_urbano = (df_municipios['total_urbano_m_ano'] > 0).sum()
    st.metric("📍 Municípios", municipios_urbano)

st.markdown("---")

# --- Main Content: Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "👥 Relação com População",
    "🗺️ Distribuição Espacial",
    "🔍 Análise por Município"
])

# Tab 1: Overview
with tab1:
    st.subheader("📊 Visão Geral - Resíduos Urbanos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🗑️ Composição dos Resíduos Urbanos")

        df_urbano = pd.DataFrame({
            'tipo': ['RSU (Resíduos Sólidos)', 'RPO (Poda e Capina)'],
            'potencial_m3_ano': [
                df_municipios['rsu_potencial_m_ano'].sum(),
                df_municipios['rpo_potencial_m_ano'].sum()
            ]
        })

        fig_barras = px.bar(
            df_urbano,
            x='tipo',
            y='potencial_m3_ano',
            title="Potencial de Biogás - Resíduos Urbanos",
            labels={'tipo': 'Tipo de Resíduo', 'potencial_m3_ano': 'Potencial (m³/ano)'},
            color='potencial_m3_ano',
            color_continuous_scale='Blues'
        )

        fig_barras.update_layout(showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)

        # Stats
        percentual_rsu = (df_urbano.iloc[0]['potencial_m3_ano'] / df_urbano['potencial_m3_ano'].sum() * 100)
        st.info(f"🗑️ RSU representa **{percentual_rsu:.1f}%** do potencial urbano total")

    with col2:
        st.markdown("### 🎯 Distribuição por Categoria de Município")

        # Classify by population
        df_municipios['categoria_pop'] = pd.cut(
            df_municipios['populacao_2022'],
            bins=[0, 20000, 100000, 500000, float('inf')],
            labels=['Pequeno (<20K)', 'Médio (20-100K)', 'Grande (100-500K)', 'Metrópole (>500K)']
        )

        df_por_categoria = df_municipios.groupby('categoria_pop')['total_urbano_m_ano'].sum().reset_index()

        fig_pizza = px.pie(
            df_por_categoria,
            values='total_urbano_m_ano',
            names='categoria_pop',
            title="Potencial Urbano por Tamanho de Município",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        st.plotly_chart(fig_pizza, use_container_width=True)

    st.markdown("---")

    # Top municipalities
    st.markdown("### 🏆 Top 15 Municípios - Potencial de Resíduos Urbanos")

    df_top_urb = df_municipios.nlargest(15, 'total_urbano_m_ano')[
        ['nome_municipio', 'total_urbano_m_ano', 'rsu_potencial_m_ano', 'rpo_potencial_m_ano', 'populacao_2022']
    ].copy()

    fig_top = go.Figure()

    fig_top.add_trace(go.Bar(
        y=df_top_urb['nome_municipio'],
        x=df_top_urb['rsu_potencial_m_ano'],
        name='RSU',
        orientation='h',
        marker=dict(color='#3498db')
    ))

    fig_top.add_trace(go.Bar(
        y=df_top_urb['nome_municipio'],
        x=df_top_urb['rpo_potencial_m_ano'],
        name='RPO (Poda)',
        orientation='h',
        marker=dict(color='#2ecc71')
    ))

    fig_top.update_layout(
        barmode='stack',
        title='Top 15 Municípios - Composição do Potencial Urbano',
        xaxis_title='Potencial de Biogás (m³/ano)',
        yaxis_title='',
        height=600,
        showlegend=True
    )

    st.plotly_chart(fig_top, use_container_width=True)

# Tab 2: Population Relation
with tab2:
    st.subheader("👥 Relação entre População e Geração de Resíduos")

    st.markdown("### 📊 População vs Potencial de RSU")

    fig_scatter = px.scatter(
        df_municipios[df_municipios['total_urbano_m_ano'] > 0],
        x='populacao_2022',
        y='rsu_potencial_m_ano',
        size='rsu_potencial_m_ano',
        hover_data=['nome_municipio'],
        title='População vs Potencial RSU',
        labels={'populacao_2022': 'População (2022)', 'rsu_potencial_m_ano': 'Potencial RSU (m³/ano)'},
        color='rsu_potencial_m_ano',
        color_continuous_scale='Blues',
        trendline="ols"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("""
💡 **Correlação**: Como esperado, existe forte correlação entre população e geração de RSU.
Municípios mais populosos geram mais resíduos urbanos e, consequentemente, têm maior potencial
de aproveitamento energético.
    """)

    # Per capita analysis
    st.markdown("### 📊 Geração Per Capita de RSU")

    # Calculate per capita RSU (approximation)
    df_per_capita = df_municipios[df_municipios['populacao_2022'] > 1000].copy()
    df_per_capita['rsu_per_capita_m3_ano'] = df_per_capita['rsu_potencial_m_ano'] / df_per_capita['populacao_2022']
    df_per_capita = df_per_capita.sort_values('rsu_per_capita_m3_ano', ascending=False).head(20)

    fig_per_capita = px.bar(
        df_per_capita,
        x='nome_municipio',
        y='rsu_per_capita_m3_ano',
        title='Top 20 - Potencial RSU Per Capita',
        labels={'nome_municipio': 'Município', 'rsu_per_capita_m3_ano': 'RSU Per Capita (m³/ano/hab)'},
        color='rsu_per_capita_m3_ano',
        color_continuous_scale='Blues'
    )

    fig_per_capita.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_per_capita, use_container_width=True)

# Tab 3: Spatial
with tab3:
    st.subheader("🗺️ Distribuição Espacial - Resíduos Urbanos")

    st.info("🗺️ **Análise Espacial**: Visualize a distribuição geográfica do potencial de resíduos urbanos.")

    # Scatter: Density vs Urban Potential
    st.markdown("### 📍 Densidade Demográfica vs Potencial Urbano")

    fig_densidade = px.scatter(
        df_municipios[(df_municipios['total_urbano_m_ano'] > 0) & (df_municipios['densidade_demografica'] > 0)],
        x='densidade_demografica',
        y='total_urbano_m_ano',
        size='populacao_2022',
        hover_data=['nome_municipio'],
        title='Densidade Demográfica vs Potencial Urbano',
        labels={'densidade_demografica': 'Densidade (hab/km²)', 'total_urbano_m_ano': 'Potencial Urbano (m³/ano)'},
        color='total_urbano_m_ano',
        color_continuous_scale='Blues',
        log_x=True
    )

    st.plotly_chart(fig_densidade, use_container_width=True)

    st.markdown("""
💡 **Insight**: Municípios com maior densidade demográfica tendem a ter maior concentração
de resíduos urbanos, mas o volume absoluto depende também da população total.
    """)

# Tab 4: By Municipality
with tab4:
    st.subheader("🔍 Análise Detalhada por Município")

    # Municipality selector
    municipios_urbano = df_municipios[df_municipios['total_urbano_m_ano'] > 0]['nome_municipio'].sort_values().tolist()

    municipio_selecionado = st.selectbox(
        "Selecione um município:",
        options=municipios_urbano
    )

    if municipio_selecionado:
        mun_data = df_municipios[df_municipios['nome_municipio'] == municipio_selecionado].iloc[0]

        # KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 População", f"{mun_data['populacao_2022']:,.0f}")

        with col2:
            st.metric("🏙️ Total Urbano", f"{mun_data['total_urbano_m_ano']:,.0f} m³/ano")

        with col3:
            st.metric("🗑️ RSU", f"{mun_data['rsu_potencial_m_ano']:,.0f} m³/ano")

        with col4:
            st.metric("🍂 RPO", f"{mun_data['rpo_potencial_m_ano']:,.0f} m³/ano")

        st.markdown("---")

        # Comparison with state average
        st.markdown(f"### 📊 Comparação: {municipio_selecionado} vs Média Estadual")

        media_estadual_rsu = df_municipios[df_municipios['rsu_potencial_m_ano'] > 0]['rsu_potencial_m_ano'].mean()
        media_estadual_rpo = df_municipios[df_municipios['rpo_potencial_m_ano'] > 0]['rpo_potencial_m_ano'].mean()

        df_comp = pd.DataFrame({
            'Indicador': ['RSU (m³/ano)', 'RPO (m³/ano)'],
            'Município': [mun_data['rsu_potencial_m_ano'], mun_data['rpo_potencial_m_ano']],
            'Média Estadual': [media_estadual_rsu, media_estadual_rpo]
        })

        fig_comp = go.Figure()

        fig_comp.add_trace(go.Bar(
            x=df_comp['Indicador'],
            y=df_comp['Município'],
            name=municipio_selecionado,
            marker=dict(color='#3498db')
        ))

        fig_comp.add_trace(go.Bar(
            x=df_comp['Indicador'],
            y=df_comp['Média Estadual'],
            name='Média Estadual',
            marker=dict(color='#95a5a6')
        ))

        fig_comp.update_layout(
            title=f'Comparação: {municipio_selecionado} vs Média Estadual',
            barmode='group',
            yaxis_title='Potencial (m³/ano)'
        )

        st.plotly_chart(fig_comp, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <h3 style="color: #3498db;">🏭 Resíduos Urbanos</h3>
    <p><strong>Análise de RSU e resíduos de poda urbana</strong></p>
    <p>Fontes: SNIS, NIPE/UNICAMP</p>
</div>
""", unsafe_allow_html=True)
