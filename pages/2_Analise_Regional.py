"""
Análise Regional - Página 2
Comparative analysis focusing on municipality-level details.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src import data_handler as dh
from src import plotter as pl
from src import ui_components as ui


# --- Page Configuration ---
st.set_page_config(
    page_title="Análise Regional - Biogás SP",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium design system
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
    st.stop()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🔍 Análise Regional Detalhada</h1>
    <p class="hero-subtitle">Comparação e Detalhamento por Município</p>
</div>
""", unsafe_allow_html=True)

# --- Municipality Selection ---
st.sidebar.header("🏙️ Seleção de Município")

# Search bar for municipality
municipios_ordenados = sorted(df_completo['nome_municipio'].unique().tolist())
municipio_selecionado = st.sidebar.selectbox(
    "Selecione um município:",
    options=municipios_ordenados,
    help="Digite para buscar ou selecione da lista"
)

# Get municipality data
mun_data = dh.get_municipality_details(municipio_selecionado)

# Calculate state averages for comparison
state_avg = {
    'total_final_m_ano': df_completo['total_final_m_ano'].mean(),
    'populacao_2022': df_completo['populacao_2022'].mean(),
    'densidade_demografica': df_completo['densidade_demografica'].mean(),
    'total_agricola_m_ano': df_completo['total_agricola_m_ano'].mean(),
    'total_pecuaria_m_ano': df_completo['total_pecuaria_m_ano'].mean(),
    'total_urbano_m_ano': df_completo['total_urbano_m_ano'].mean()
}

# --- Municipality Overview ---
st.header(f"📍 {municipio_selecionado}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="População (2022)",
        value=f"{mun_data['populacao_2022']:,.0f}",
        help="População estimada para 2022"
    )

with col2:
    st.metric(
        label="Área",
        value=f"{mun_data['area_km2']:,.1f} km²",
        help="Área total do município"
    )

with col3:
    st.metric(
        label="Densidade Demográfica",
        value=f"{mun_data['densidade_demografica']:.1f} hab/km²",
        help="Habitantes por quilômetro quadrado"
    )

with col4:
    st.metric(
        label="Categoria de Potencial",
        value=mun_data['categoria_potencial'],
        help="Classificação do potencial de biogás"
    )

st.markdown("---")

# --- Comparison with State Average ---
ui.render_comparison_metrics(mun_data, state_avg)

st.markdown("---")

# --- Detailed Breakdown ---
st.header("📊 Detalhamento por Setor e Substrato")

col1, col2 = st.columns(2)

with col1:
    # Sector breakdown
    st.subheader("Por Setor")
    setores_mun = {
        'Agricultura': mun_data['total_agricola_m_ano'],
        'Pecuária': mun_data['total_pecuaria_m_ano'],
        'Urbano': mun_data['total_urbano_m_ano']
    }
    
    df_setores_mun = pd.DataFrame(list(setores_mun.items()), columns=['setor', 'volume'])
    df_setores_mun = df_setores_mun[df_setores_mun['volume'] > 0]
    
    if not df_setores_mun.empty:
        fig_setores = pl.criar_grafico_donut_setor(df_setores_mun)
        st.plotly_chart(fig_setores, use_container_width=True)
    else:
        st.info("Sem dados de setores para este município.")

with col2:
    # Radar chart
    st.subheader("Composição de Substratos")
    fig_radar = pl.criar_grafico_radar_municipio(mun_data)
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# --- Substrate Details Table ---
st.subheader("🌾 Detalhamento de Substratos")

substratos_detalhados = {
    'Substrato': [
        'Cana-de-açúcar', 'Soja', 'Milho', 'Café', 'Citros',
        'Bovinos', 'Suínos', 'Aves', 'Piscicultura',
        'Silvicultura', 'RSU', 'RPO'
    ],
    'Potencial (m³/ano)': [
        mun_data['biogas_cana_m_ano'],
        mun_data['biogas_soja_m_ano'],
        mun_data['biogas_milho_m_ano'],
        mun_data['biogas_cafe_m_ano'],
        mun_data['biogas_citros_m_ano'],
        mun_data['biogas_bovinos_m_ano'],
        mun_data['biogas_suino_m_ano'],
        mun_data['biogas_aves_m_ano'],
        mun_data['biogas_piscicultura_m_ano'],
        mun_data['biogas_silvicultura_m_ano'],
        mun_data['rsu_potencial_m_ano'],
        mun_data['rpo_potencial_m_ano']
    ],
    'Setor': [
        'Agricultura', 'Agricultura', 'Agricultura', 'Agricultura', 'Agricultura',
        'Pecuária', 'Pecuária', 'Pecuária', 'Pecuária',
        'Agricultura', 'Urbano', 'Urbano'
    ]
}

df_substratos_det = pd.DataFrame(substratos_detalhados)
df_substratos_det = df_substratos_det[df_substratos_det['Potencial (m³/ano)'] > 0].sort_values(
    'Potencial (m³/ano)', ascending=False
)

# Display as table with formatting
st.dataframe(
    df_substratos_det.style.format({'Potencial (m³/ano)': '{:,.0f}'}),
    use_container_width=True,
    height=400
)

st.markdown("---")

# --- Comparison with Similar Municipalities ---
st.header("🔄 Comparação com Municípios Similares")

# Find similar municipalities (by population range)
pop_margem = mun_data['populacao_2022'] * 0.3  # ±30%
df_similares = df_completo[
    (df_completo['populacao_2022'] >= mun_data['populacao_2022'] - pop_margem) &
    (df_completo['populacao_2022'] <= mun_data['populacao_2022'] + pop_margem) &
    (df_completo['nome_municipio'] != municipio_selecionado)
].head(10)

if not df_similares.empty:
    st.info(f"Comparando {municipio_selecionado} com municípios de população similar (±30%)")
    
    # Add the selected municipality to the comparison
    df_comparacao = pd.concat([
        pd.DataFrame([mun_data]),
        df_similares
    ]).reset_index(drop=True)
    
    # Highlight selected municipality
    df_comparacao['destaque'] = df_comparacao['nome_municipio'] == municipio_selecionado
    
    # Create comparison chart
    fig_comp = pl.criar_grafico_top_municipios(df_comparacao, top_n=len(df_comparacao))
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rank_potencial = (df_comparacao['total_final_m_ano'] > mun_data['total_final_m_ano']).sum() + 1
        st.metric(
            "Posição no Grupo",
            f"{rank_potencial}º de {len(df_comparacao)}",
            help="Ranking por potencial total de biogás"
        )
    
    with col2:
        media_grupo = df_comparacao['total_final_m_ano'].mean()
        diff_media = ((mun_data['total_final_m_ano'] - media_grupo) / media_grupo * 100)
        st.metric(
            "vs Média do Grupo",
            f"{diff_media:+.1f}%",
            help="Diferença percentual em relação à média do grupo"
        )
    
    with col3:
        max_grupo = df_comparacao['total_final_m_ano'].max()
        diff_max = ((mun_data['total_final_m_ano'] - max_grupo) / max_grupo * 100)
        st.metric(
            "vs Melhor do Grupo",
            f"{diff_max:+.1f}%",
            help="Diferença percentual em relação ao maior potencial do grupo"
        )
else:
    st.info("Não foram encontrados municípios similares para comparação.")

st.markdown("---")

# --- Regional Context ---
st.header("🗺️ Contexto no Estado")

st.subheader("Ranking Estadual")

# Calculate state ranking
df_ranking = df_completo[['nome_municipio', 'total_final_m_ano']].sort_values(
    'total_final_m_ano', ascending=False
).reset_index(drop=True)
df_ranking.index += 1

posicao_estado = df_ranking[df_ranking['nome_municipio'] == municipio_selecionado].index[0]
total_municipios_estado = len(df_ranking)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Posição no Estado",
        f"{posicao_estado}º",
        help=f"Ranking entre {total_municipios_estado} municípios"
    )

with col2:
    percentil = (1 - (posicao_estado / total_municipios_estado)) * 100
    st.metric(
        "Percentil",
        f"{percentil:.1f}%",
        help="Percentual de municípios com potencial menor"
    )

with col3:
    contrib_estado = (mun_data['total_final_m_ano'] / df_completo['total_final_m_ano'].sum() * 100)
    st.metric(
        "Contribuição Estadual",
        f"{contrib_estado:.2f}%",
        help="Percentual do potencial total do estado"
    )

# Show top and bottom 5 for context
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 5 do Estado")
    top5 = df_ranking.head(5)[['nome_municipio', 'total_final_m_ano']]
    top5.columns = ['Município', 'Potencial (m³/ano)']
    st.dataframe(
        top5.style.format({'Potencial (m³/ano)': '{:,.0f}'}),
        use_container_width=True
    )

with col2:
    st.subheader("📍 Municípios Próximos no Ranking")
    # Show municipalities around the selected one
    start_idx = max(0, posicao_estado - 3)
    end_idx = min(total_municipios_estado, posicao_estado + 2)
    proximos = df_ranking.iloc[start_idx:end_idx][['nome_municipio', 'total_final_m_ano']]
    proximos.columns = ['Município', 'Potencial (m³/ano)']
    
    # Highlight the selected municipality
    def highlight_selected(row):
        if row['Município'] == municipio_selecionado:
            return ['background-color: #d4edda'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        proximos.style.format({'Potencial (m³/ano)': '{:,.0f}'}).apply(highlight_selected, axis=1),
        use_container_width=True
    )

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p><strong>Análise Regional - Biogás SP</strong></p>
    <p>Use a barra lateral para selecionar outro município</p>
</div>
""", unsafe_allow_html=True)

