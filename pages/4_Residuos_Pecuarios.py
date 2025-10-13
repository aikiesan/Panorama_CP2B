"""
Resíduos Pecuários - Análise Detalhada
Página especializada em resíduos da pecuária paulista.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src import data_handler as dh
from src import plotter as pl
from src import ui_components as ui
from src.data_sources import agro_handler as agro

# --- Page Configuration ---
st.set_page_config(
    page_title="Resíduos Pecuários - Panorama de Resíduos SP",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium design system
ui.load_css()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🐄 Resíduos Pecuários</h1>
    <p class="hero-subtitle">Análise Detalhada da Produção Pecuária e Geração de Resíduos em SP</p>
</div>
""", unsafe_allow_html=True)

# --- Load Data ---
df_municipios = dh.load_all_municipalities()
df_pecuaria = agro.load_residuos_pecuarios()

# --- Info Box ---
st.info("""
📌 **Sobre esta seção**: Explore os dados de resíduos pecuários provenientes da criação
de bovinos, suínos, aves e piscicultura no Estado de São Paulo. Os dados incluem rebanhos,
geração de resíduos e potencial de biogás por município.
""")

st.markdown("---")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_bovinos = df_municipios['biogas_bovinos_m_ano'].sum()
    st.metric("🐄 Bovinos", f"{total_bovinos/1_000_000:.1f}M m³/ano")

with col2:
    total_suinos = df_municipios['biogas_suino_m_ano'].sum()
    st.metric("🐷 Suínos", f"{total_suinos/1_000_000:.1f}M m³/ano")

with col3:
    total_aves = df_municipios['biogas_aves_m_ano'].sum()
    st.metric("🐔 Aves", f"{total_aves/1_000_000:.1f}M m³/ano")

with col4:
    total_peixes = df_municipios['biogas_piscicultura_m_ano'].sum()
    st.metric("🐟 Piscicultura", f"{total_peixes/1_000:.1f}K m³/ano")

st.markdown("---")

# --- Main Content: Tabs ---
tab1, tab2, tab3 = st.tabs([
    "📊 Visão Geral",
    "🗺️ Distribuição Geográfica",
    "🔍 Análise por Criação"
])

# Tab 1: Overview
with tab1:
    st.subheader("📊 Visão Geral - Resíduos Pecuários")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐄 Potencial por Tipo de Criação")

        df_pecuario = pd.DataFrame({
            'tipo_criacao': ['Bovinos', 'Suínos', 'Aves', 'Piscicultura'],
            'potencial_m3_ano': [
                df_municipios['biogas_bovinos_m_ano'].sum(),
                df_municipios['biogas_suino_m_ano'].sum(),
                df_municipios['biogas_aves_m_ano'].sum(),
                df_municipios['biogas_piscicultura_m_ano'].sum()
            ]
        })

        df_pecuario = df_pecuario[df_pecuario['potencial_m3_ano'] > 0].sort_values('potencial_m3_ano', ascending=False)

        fig_barras = px.bar(
            df_pecuario,
            x='tipo_criacao',
            y='potencial_m3_ano',
            title="Potencial de Biogás por Tipo de Criação",
            labels={'tipo_criacao': 'Tipo de Criação', 'potencial_m3_ano': 'Potencial (m³/ano)'},
            color='potencial_m3_ano',
            color_continuous_scale='Oranges'
        )

        fig_barras.update_layout(showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Distribuição Percentual")

        fig_pizza = px.pie(
            df_pecuario,
            values='potencial_m3_ano',
            names='tipo_criacao',
            title="Distribuição do Potencial Pecuário",
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )

        st.plotly_chart(fig_pizza, use_container_width=True)

    st.markdown("---")

    # Top municipalities
    st.markdown("### 🏆 Top 15 Municípios - Potencial Pecuário")

    df_top_pec = df_municipios.nlargest(15, 'total_pecuaria_m_ano')[
        ['nome_municipio', 'total_pecuaria_m_ano', 'biogas_bovinos_m_ano', 'biogas_suino_m_ano', 'biogas_aves_m_ano']
    ].copy()

    fig_top = go.Figure()

    fig_top.add_trace(go.Bar(
        y=df_top_pec['nome_municipio'],
        x=df_top_pec['biogas_bovinos_m_ano'],
        name='Bovinos',
        orientation='h',
        marker=dict(color='#e67e22')
    ))

    fig_top.add_trace(go.Bar(
        y=df_top_pec['nome_municipio'],
        x=df_top_pec['biogas_suino_m_ano'],
        name='Suínos',
        orientation='h',
        marker=dict(color='#e74c3c')
    ))

    fig_top.add_trace(go.Bar(
        y=df_top_pec['nome_municipio'],
        x=df_top_pec['biogas_aves_m_ano'],
        name='Aves',
        orientation='h',
        marker=dict(color='#f39c12')
    ))

    fig_top.update_layout(
        barmode='stack',
        title='Top 15 Municípios - Composição do Potencial Pecuário',
        xaxis_title='Potencial de Biogás (m³/ano)',
        yaxis_title='',
        height=600,
        showlegend=True
    )

    st.plotly_chart(fig_top, use_container_width=True)

# Tab 2: Spatial
with tab2:
    st.subheader("🗺️ Distribuição Geográfica - Pecuária")

    st.info("🗺️ **Análise Espacial**: Identifique as regiões com maior concentração de atividade pecuária.")

    # Scatter plot: Pop vs Pecuaria
    st.markdown("### 📍 Relação: População vs Potencial Pecuário")

    fig_scatter = px.scatter(
        df_municipios[df_municipios['total_pecuaria_m_ano'] > 0],
        x='populacao_2022',
        y='total_pecuaria_m_ano',
        size='total_pecuaria_m_ano',
        hover_data=['nome_municipio'],
        title='População vs Potencial Pecuário',
        labels={'populacao_2022': 'População (2022)', 'total_pecuaria_m_ano': 'Potencial Biogás (m³/ano)'},
        color='total_pecuaria_m_ano',
        color_continuous_scale='Oranges'
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("""
💡 **Insight**: Municípios com menor população mas alta atividade pecuária destacam-se
como importantes produtores rurais com potencial significativo de aproveitamento de resíduos.
    """)

# Tab 3: By Type
with tab3:
    st.subheader("🔍 Análise por Tipo de Criação")

    tipo_criacao = st.selectbox(
        "Selecione o tipo de criação:",
        options=['Bovinos', 'Suínos', 'Aves', 'Piscicultura']
    )

    col_map = {
        'Bovinos': 'biogas_bovinos_m_ano',
        'Suínos': 'biogas_suino_m_ano',
        'Aves': 'biogas_aves_m_ano',
        'Piscicultura': 'biogas_piscicultura_m_ano'
    }

    coluna = col_map[tipo_criacao]

    df_tipo = df_municipios[df_municipios[coluna] > 0][['nome_municipio', coluna, 'populacao_2022', 'area_km2']].copy()
    df_tipo = df_tipo.sort_values(coluna, ascending=False)

    # KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🐄 Potencial Total", f"{df_tipo[coluna].sum()/1_000_000:.2f}M m³/ano")

    with col2:
        st.metric("📍 Municípios Criadores", len(df_tipo))

    with col3:
        st.metric("📊 Média por Município", f"{df_tipo[coluna].mean():,.0f} m³/ano")

    st.markdown(f"### 📊 Top 20 Municípios - {tipo_criacao}")

    fig_tipo = px.bar(
        df_tipo.head(20),
        x='nome_municipio',
        y=coluna,
        title=f'Top 20 Municípios - {tipo_criacao}',
        labels={'nome_municipio': 'Município', coluna: 'Potencial (m³/ano)'},
        color=coluna,
        color_continuous_scale='Oranges'
    )

    fig_tipo.update_layout(xaxis={'categoryorder': 'total descending'}, showlegend=False)
    st.plotly_chart(fig_tipo, use_container_width=True)

    # Data table
    with st.expander("📋 Ver Dados Completos"):
        df_display = df_tipo.copy()
        df_display.columns = ['Município', f'Potencial {tipo_criacao} (m³/ano)', 'População (2022)', 'Área (km²)']
        st.dataframe(df_display, use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <h3 style="color: #e67e22;">🐄 Resíduos Pecuários</h3>
    <p><strong>Análise detalhada da pecuária e geração de resíduos</strong></p>
    <p>Fontes: SIDRA/IBGE, Defesa Agropecuária SP, NIPE/UNICAMP</p>
</div>
""", unsafe_allow_html=True)
