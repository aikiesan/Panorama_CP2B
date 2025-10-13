"""
Panorama de Resíduos - Estado de São Paulo
Plataforma de visualização de dados de resíduos de múltiplas fontes.
Main application page following SOLID principles.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import custom modules
from src import data_handler as dh
from src import plotter as pl
from src import ui_components as ui


# --- Page Configuration ---
st.set_page_config(
    page_title="Panorama de Resíduos - SP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the premium design system
ui.load_css()

# --- Load Data ---
@st.cache_data
def load_data():
    """Load and cache the municipality data."""
    return dh.load_all_municipalities()

try:
    df_completo = load_data()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados do banco: {e}")
    st.info("Verifique se o arquivo de banco de dados está no caminho correto em .streamlit/secrets.toml")
    st.stop()

# --- Sidebar Filters ---
filtros = ui.render_filters_sidebar(df_completo)

# --- Apply Filters ---
df_filtrado = dh.filter_dataframe(df_completo, **filtros)

if df_filtrado.empty:
    st.warning("⚠️ Nenhum município encontrado com os filtros selecionados. Ajuste os filtros.")
    st.stop()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">📊 Panorama de Resíduos - Estado de São Paulo</h1>
    <p class="hero-subtitle">Plataforma de Visualização de Dados de Resíduos e Potencial Energético</p>
</div>
""", unsafe_allow_html=True)

# --- About Section ---
ui.show_about_section()

st.markdown("---")

# --- Data Summary ---
st.header("📊 Resumo dos Dados")
st.markdown("Visualize os dados de potencial de biogás dos municípios selecionados")

kpis = dh.get_kpis_totais(df_filtrado)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Municípios no Filtro",
        value=f"{kpis['total_municipios']:,}",
        help="Número de municípios considerados com os filtros atuais"
    )

with col2:
    st.metric(
        label="Volume Total Registrado",
        value=f"{kpis['total_biogas']:,.0f} m³/ano",
        help="Somatório dos volumes registrados"
    )

with col3:
    if kpis['top_municipio']:
        st.metric(
            label="Maior Volume Individual",
            value=kpis['top_municipio'],
            delta=f"{kpis['top_municipio_valor']:,.0f} m³/ano",
            help="Município com maior volume registrado"
        )

st.markdown("---")

# --- Sector Data Distribution ---
st.subheader("Distribuição por Setor")
ui.render_sector_kpis(kpis)

st.markdown("---")

# --- Info Section: About Biogas ---
with st.expander("ℹ️ Sobre Biogás", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **O que é Biogás?**

        Gás combustível produzido pela decomposição anaeróbia de matéria orgânica.

        **Composição típica:**
        - 🔥 Metano (CH₄): 50-75%
        - 💨 CO₂: 25-45%
        - Outros gases: traços

        **Fontes de Resíduos:**
        - ♻️ Resíduos agrícolas
        - 🐄 Resíduos pecuários
        - 🏭 Resíduos urbanos
        """)
    with col2:
        st.markdown("""
        **Dados deste Sistema**

        Os dados apresentados são baseados em:

        1. **🌾 Agricultura**: Dados de produção agrícola (SIDRA/IBGE)
        2. **🐄 Pecuária**: Dados de rebanhos (SIDRA/IBGE, Defesa Agropecuária SP)
        3. **🏭 Urbano**: Dados de resíduos urbanos (estimativas baseadas em população)

        **Fontes**: NIPE/UNICAMP, SIDRA/IBGE
        """)

st.markdown("---")

# --- Main Visualizations: Sector Distribution ---
st.header("📊 Distribuição do Potencial por Setor")

col1, col2 = st.columns(2)

with col1:
    df_setor = dh.get_volume_por_setor(df_filtrado)
    fig_donut = pl.criar_grafico_donut_setor(df_setor)
    st.plotly_chart(fig_donut, use_container_width=True)
    
    # Educational insights
    if not df_setor.empty:
        setor_dominante = df_setor.loc[df_setor['volume'].idxmax(), 'setor']
        pct_dominante = (df_setor.loc[df_setor['volume'].idxmax(), 'volume'] / df_setor['volume'].sum() * 100)
        st.info(f"🎯 **Setor dominante**: {setor_dominante} representa {pct_dominante:.1f}% do potencial total!")

with col2:
    # Category distribution
    fig_categoria = pl.criar_grafico_evolucao_categoria(df_filtrado)
    st.plotly_chart(fig_categoria, use_container_width=True)
    
    # Educational insights
    alto_potencial = len(df_filtrado[df_filtrado['categoria_potencial'] == 'ALTO'])
    if alto_potencial > 0:
        st.success(f"✨ {alto_potencial} municípios têm **ALTO** potencial de biogás!")

st.markdown("---")

# --- Substrate Breakdown with Educational Content ---
st.header("🌾 Explorando os Substratos - De onde vem o Biogás?")

df_substrato = dh.get_volume_por_substrato(df_filtrado)

if not df_substrato.empty:
    # Main substrate chart
    fig_substrato = pl.criar_grafico_barras_substrato(df_substrato)
    st.plotly_chart(fig_substrato, use_container_width=True)
    
    # Educational cards about top substrates
    st.subheader("📚 Conheça os Principais Substratos")
    
    # Get top 3 substrates
    top_3_substratos = df_substrato.head(3)
    
    # Educational information about each substrate
    substrate_info = {
        'Silvicultura': {
            'icon': '🌲',
            'descricao': 'Resíduos de florestas plantadas (eucalipto, pinus). Incluem cascas, galhos e serragem.',
            'curiosidade': 'O Brasil é o 2º maior produtor de celulose do mundo!'
        },
        'Soja': {
            'icon': '🫘',
            'descricao': 'Palha e restos da colheita de soja. São Paulo é um grande produtor.',
            'curiosidade': 'Cada hectare de soja gera cerca de 3-4 toneladas de palha!'
        },
        'Milho': {
            'icon': '🌽',
            'descricao': 'Palha, sabugo e restos da planta após a colheita do milho.',
            'curiosidade': 'A palha de milho pode produzir até 300m³ de biogás por tonelada!'
        },
        'Cana-de-açúcar': {
            'icon': '🎋',
            'descricao': 'Bagaço, palha e vinhaça da produção de açúcar e etanol.',
            'curiosidade': 'SP é o maior produtor de cana do Brasil, com mais de 50% da produção nacional!'
        },
        'Bovinos': {
            'icon': '🐄',
            'descricao': 'Esterco de gado bovino, rico em matéria orgânica para digestão anaeróbia.',
            'curiosidade': 'Uma vaca pode produzir 10-15 kg de esterco por dia!'
        },
        'Suínos': {
            'icon': '🐷',
            'descricao': 'Dejetos de suínos, altamente eficientes para produção de biogás.',
            'curiosidade': 'Dejetos de suínos produzem 3x mais biogás que esterco bovino!'
        },
        'Aves': {
            'icon': '🐔',
            'descricao': 'Cama de frango e dejetos de aves, ricos em nitrogênio.',
            'curiosidade': 'SP tem o 3º maior plantel de aves do Brasil!'
        },
        'RSU': {
            'icon': '🗑️',
            'descricao': 'Resíduos Sólidos Urbanos - a fração orgânica do lixo das cidades.',
            'curiosidade': 'Cerca de 50% do lixo urbano é matéria orgânica que pode gerar biogás!'
        },
        'Citros': {
            'icon': '🍊',
            'descricao': 'Cascas e bagaço de laranja, limão e outras frutas cítricas.',
            'curiosidade': 'SP produz 80% da laranja do Brasil e é líder mundial em suco!'
        },
        'RPO': {
            'icon': '🍂',
            'descricao': 'Resíduos de Poda e Capina urbana - galhos, folhas e grama.',
            'curiosidade': 'Representam 5-10% dos resíduos urbanos em cidades arborizadas!'
        },
        'Café': {
            'icon': '☕',
            'descricao': 'Cascas e polpa do café, subprodutos do beneficiamento.',
            'curiosidade': 'Cada tonelada de café gera 1 tonelada de casca!'
        },
        'Piscicultura': {
            'icon': '🐟',
            'descricao': 'Resíduos de criação de peixes, incluindo ração não consumida.',
            'curiosidade': 'A piscicultura paulista cresce 10% ao ano!'
        }
    }
    
    cols = st.columns(3)
    for idx, (_, row) in enumerate(top_3_substratos.iterrows()):
        with cols[idx % 3]:
            substrato = row['substrato']
            volume = row['volume']
            info = substrate_info.get(substrato, {'icon': '📦', 'descricao': 'Substrato orgânico', 'curiosidade': ''})
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 20px;
                border-radius: 15px;
                border-left: 5px solid #27ae60;
                margin: 10px 0;
                min-height: 200px;
            ">
                <h3 style="margin-top: 0;">{info['icon']} {substrato}</h3>
                <p style="font-size: 1.1em; color: #27ae60; font-weight: bold;">
                    {volume:,.0f} m³/ano
                </p>
                <p style="font-size: 0.9em; color: #555;">
                    {info['descricao']}
                </p>
                <p style="font-size: 0.85em; color: #7f8c8d; font-style: italic;">
                    💡 {info['curiosidade']}
                </p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Nenhum substrato com potencial maior que zero nos municípios filtrados.")

st.markdown("---")

# --- Top Municipalities ---
st.header("🏆 Municípios Destaque em Potencial de Biogás")

df_top = dh.get_top_municipios(df_filtrado, n=10)
fig_top = pl.criar_grafico_top_municipios(df_top, top_n=10)
st.plotly_chart(fig_top, use_container_width=True)

# Insights about top municipalities
if not df_top.empty:
    top_mun = df_top.iloc[0]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🥇 Líder em Potencial",
            top_mun['nome_municipio'],
            f"{top_mun['total_final_m_ano']:,.0f} m³/ano"
        )
    
    with col2:
        # Find which sector dominates in the top municipality
        setores_top = {
            'Agricultura': top_mun['total_agricola_m_ano'],
            'Pecuária': top_mun['total_pecuaria_m_ano'],
            'Urbano': top_mun['total_urbano_m_ano']
        }
        setor_dominante_top = max(setores_top, key=setores_top.get)
        st.metric(
            "🎯 Setor Principal",
            setor_dominante_top,
            f"{setores_top[setor_dominante_top]:,.0f} m³/ano"
        )
    
    with col3:
        # Population of top municipality
        st.metric(
            "👥 População",
            f"{top_mun['populacao_2022']:,.0f}",
            "habitantes (2022)"
        )

st.markdown("---")

# --- Interactive Exploration ---
st.header("🔍 Explore as Relações entre Dados")

st.markdown("""
<div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <p style="margin: 0; color: #2e7d32;">
    💡 <strong>Dica:</strong> Use os gráficos abaixo para explorar como diferentes fatores se relacionam 
    com o potencial de biogás. Cada ponto representa um município!
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👥 População", "📏 Área Territorial", "🗺️ Mapa Geográfico"])

with tab1:
    st.subheader("População vs Potencial de Biogás")
    fig_pop_biogas = pl.criar_grafico_dispersao(
        df_filtrado,
        x_col='populacao_2022',
        y_col='total_final_m_ano',
        labels={
            'populacao_2022': 'População (2022)',
            'total_final_m_ano': 'Potencial de Biogás (m³/ano)'
        }
    )
    st.plotly_chart(fig_pop_biogas, use_container_width=True)
    
    st.markdown("""
    **💭 O que observar:**
    - Municípios mais populosos tendem a ter maior potencial? (principalmente resíduos urbanos)
    - Há municípios pequenos com alto potencial? (provavelmente por agricultura/pecuária)
    - A relação é linear ou existem outliers interessantes?
    """)

with tab2:
    st.subheader("Área Territorial vs Potencial de Biogás")
    fig_area_biogas = pl.criar_grafico_dispersao(
        df_filtrado,
        x_col='area_km2',
        y_col='total_final_m_ano',
        labels={
            'area_km2': 'Área (km²)',
            'total_final_m_ano': 'Potencial de Biogás (m³/ano)'
        }
    )
    st.plotly_chart(fig_area_biogas, use_container_width=True)
    
    st.markdown("""
    **💭 O que observar:**
    - Municípios maiores têm mais potencial agrícola?
    - A densidade de produção varia significativamente?
    - Alguns municípios pequenos podem ter alta produtividade por km²!
    """)

with tab3:
    st.subheader("Visualização Geográfica")
    
    # Check if GeoJSON exists
    geojson_path = Path(__file__).parent / "data" / "processed" / "sp_municipios_simplified_0_001.geojson"
    
    if geojson_path.exists():
        try:
            fig_mapa = pl.criar_mapa_coropleth_sp(df_filtrado, str(geojson_path))
            st.plotly_chart(fig_mapa, use_container_width=True)
            
            st.markdown("""
            **💭 O que observar:**
            - Existem regiões com maior concentração de potencial?
            - O interior tem maior potencial agrícola/pecuário?
            - Regiões metropolitanas destacam-se em resíduos urbanos?
            """)
        except Exception as e:
            st.warning("⚠️ Mapa temporariamente indisponível. Use as outras visualizações para explorar os dados.")
    else:
        st.info("📊 Mapa geográfico será adicionado em breve. Por enquanto, explore os gráficos de dispersão acima!")

st.markdown("---")

# --- Data Table ---
with st.expander("📋 Ver Tabela de Dados Completa"):
    colunas_exibir = [
        'nome_municipio',
        'populacao_2022',
        'total_final_m_ano',
        'total_agricola_m_ano',
        'total_pecuaria_m_ano',
        'total_urbano_m_ano',
        'categoria_potencial'
    ]
    
    formato = {
        'populacao_2022': '{:,.0f}',
        'total_final_m_ano': '{:,.0f}',
        'total_agricola_m_ano': '{:,.0f}',
        'total_pecuaria_m_ano': '{:,.0f}',
        'total_urbano_m_ano': '{:,.0f}'
    }
    
    ui.render_data_table(
        df_filtrado,
        title="Dados dos Municípios",
        columns=colunas_exibir,
        format_dict=formato
    )

st.markdown("---")

# --- Data Sources and Methodology ---
st.header("📚 Fontes de Dados e Metodologia")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 Fontes de Dados Primárias

    **SIDRA/IBGE**
    - Produção Agrícola Municipal (PAM)
    - Pesquisa Pecuária Municipal (PPM)
    - Dados demográficos e territoriais

    **Defesa Agropecuária - SP**
    - Cadastro de propriedades rurais
    - Dados de rebanhos registrados

    **MapBiomas**
    - Cobertura e uso do solo
    - Dados geográficos
    """)

with col2:
    st.markdown("""
    ### 🔬 Metodologia

    **Cálculo de Volumes**
    - Baseado em fatores de conversão específicos por tipo de resíduo
    - Dados de produção agrícola e efetivo de rebanhos
    - Estimativas para resíduos urbanos (população)

    **Referências Técnicas**
    - NIPE/UNICAMP: Fatores de conversão
    - Literatura técnica especializada
    - Normas e padrões internacionais (VDI 4630)
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <h3 style="color: #27ae60;">📊 Panorama de Resíduos - São Paulo</h3>
    <p><strong>Plataforma de visualização de dados de resíduos e potencial energético</strong></p>
    <p>Fontes: SIDRA/IBGE, MapBiomas, Defesa Agropecuária SP, NIPE/UNICAMP</p>
    <p style="font-size: 0.9em; margin-top: 15px;">
        💡 Navegue pelas páginas à esquerda para explorar diferentes tipos de resíduos e análises
    </p>
</div>
""", unsafe_allow_html=True)

