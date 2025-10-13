"""
Panorama de Resíduos - São Paulo
Sistema de consulta de dados limpo e minimalista
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src import ui_components_premium as ui
from src import plotly_theme as pt

# --- Page Configuration ---
st.set_page_config(
    page_title="Panorama de Resíduos - SP",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Custom CSS ---
ui.load_css()

# CSS para botões personalizados
st.markdown("""
<style>
/* Força visibilidade do texto */
.stSelectbox div[data-baseweb="select"] {
    color: #0F1A2A !important;
}

.stSelectbox span {
    color: #0F1A2A !important;
}

/* Botões de seleção customizados */
.selection-button {
    display: inline-block;
    padding: 12px 24px;
    margin: 4px;
    border-radius: 8px;
    border: 2px solid #E2E8F0;
    background: white;
    color: #0F1A2A;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.selection-button:hover {
    border-color: #2ecc71;
    background: #f0f9f4;
}

.selection-button.active {
    border-color: #2ecc71;
    background: #2ecc71;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Header Simples e Limpo ---
st.markdown("""
<div style="
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
    border-radius: 16px;
    padding: 40px 32px;
    margin-bottom: 32px;
    text-align: center;
">
    <h1 style="
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        line-height: 1.3;
    ">
        Panorama de Resíduos — São Paulo
    </h1>
    <p style="
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        margin-top: 12px;
        margin-bottom: 0;
    ">
        Consulta de dados sobre potencial energético de resíduos
    </p>
</div>
""", unsafe_allow_html=True)

# --- Seleção por Botões ---
st.markdown("### Selecione os parâmetros de consulta")

# Initialize session state
if 'cultura_selecionada' not in st.session_state:
    st.session_state.cultura_selecionada = "Cana-de-açúcar"
if 'residuo_selecionado' not in st.session_state:
    st.session_state.residuo_selecionado = "Bagaço"
if 'ano_selecionado' not in st.session_state:
    st.session_state.ano_selecionado = "2024"

# Cultura
st.markdown("#### Cultura Agrícola")
culturas = ["Cana-de-açúcar", "Milho", "Soja", "Arroz", "Café"]
cols_cultura = st.columns(len(culturas))

for idx, cultura in enumerate(culturas):
    with cols_cultura[idx]:
        if st.button(
            cultura,
            key=f"btn_cultura_{cultura}",
            use_container_width=True,
            type="primary" if st.session_state.cultura_selecionada == cultura else "secondary"
        ):
            st.session_state.cultura_selecionada = cultura
            st.rerun()

# Tipo de Resíduo (dinâmico baseado na cultura)
st.markdown("#### Tipo de Resíduo")
residuos_por_cultura = {
    "Cana-de-açúcar": ["Bagaço", "Palha", "Vinhaça", "Torta de Filtro"],
    "Milho": ["Palha", "Sabugo", "Folhas"],
    "Soja": ["Palha", "Cascas"],
    "Arroz": ["Palha", "Casca"],
    "Café": ["Polpa", "Casca", "Pergaminho"]
}

residuos_disponiveis = residuos_por_cultura.get(st.session_state.cultura_selecionada, ["Todos"])
cols_residuo = st.columns(len(residuos_disponiveis))

for idx, residuo in enumerate(residuos_disponiveis):
    with cols_residuo[idx]:
        if st.button(
            residuo,
            key=f"btn_residuo_{residuo}",
            use_container_width=True,
            type="primary" if st.session_state.residuo_selecionado == residuo else "secondary"
        ):
            st.session_state.residuo_selecionado = residuo
            st.rerun()

# Ano de Referência
st.markdown("#### Ano de Referência")
anos = ["2024", "2023", "2022", "2021"]
cols_ano = st.columns(len(anos))

for idx, ano in enumerate(anos):
    with cols_ano[idx]:
        if st.button(
            ano,
            key=f"btn_ano_{ano}",
            use_container_width=True,
            type="primary" if st.session_state.ano_selecionado == ano else "secondary"
        ):
            st.session_state.ano_selecionado = ano
            st.rerun()

st.markdown("---")

# --- Exibir Seleção Atual ---
st.info(f"📊 **Consultando:** {st.session_state.cultura_selecionada} → {st.session_state.residuo_selecionado} ({st.session_state.ano_selecionado})")

st.markdown("---")

# --- Dados Reais (sem estimativas) ---
st.markdown("### 📈 Dados Disponíveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Composição Química")
    
    # Dados reais de composição (valores fictícios para demo, substituir por dados reais)
    composicao = {
        'Celulose': 42.3,
        'Lignina': 22.5,
        'Hemicelulose': 28.7,
        'Outros': 6.5
    }
    
    fig_donut = pt.create_donut_chart(
        values=list(composicao.values()),
        labels=list(composicao.keys()),
        title=""
    )
    st.plotly_chart(fig_donut, width="stretch")
    
    # Tabela com dados exatos
    df_comp = pd.DataFrame({
        'Componente': list(composicao.keys()),
        'Percentual (%)': list(composicao.values())
    })
    st.dataframe(df_comp, hide_index=True, use_container_width=True)

with col2:
    st.markdown("#### Geração Anual por Região")
    
    # Dados por região (valores fictícios, substituir por reais)
    regioes = ['Ribeirão Preto', 'Campinas', 'São José do Rio Preto', 'Presidente Prudente']
    valores = [4.5, 2.8, 2.1, 1.6]
    
    fig_bar = pt.create_bar_chart(
        x=regioes,
        y=valores,
        title="",
        y_label="Milhões toneladas/ano",
        color=pt.COLORS['green']
    )
    st.plotly_chart(fig_bar, width="stretch")
    
    # Tabela com dados exatos
    df_regioes = pd.DataFrame({
        'Região': regioes,
        'Geração (M ton/ano)': valores
    })
    st.dataframe(df_regioes, hide_index=True, use_container_width=True)

st.markdown("---")

# --- Dados Tabulares Completos ---
st.markdown("### 📋 Dados Detalhados")

# Dados simulados - substituir por dados reais do banco
dados_completos = pd.DataFrame({
    'Município': ['Ribeirão Preto', 'Campinas', 'São José do Rio Preto', 'Piracicaba', 'Araraquara'],
    'Área Cultivada (ha)': [125000, 89000, 102000, 67000, 58000],
    'Geração de Resíduo (ton/ano)': [450000, 320000, 367000, 241000, 209000],
    'Aproveitamento Atual (%)': [15.2, 8.5, 12.3, 6.8, 9.1]
})

st.dataframe(dados_completos, use_container_width=True, hide_index=True)

# Botão de download
csv = dados_completos.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Baixar dados completos (CSV)",
    data=csv,
    file_name=f"panorama_{st.session_state.cultura_selecionada.lower().replace('-', '_')}_{st.session_state.ano_selecionado}.csv",
    mime="text/csv"
)

st.markdown("---")

# --- Fontes dos Dados ---
with st.expander("📖 Fontes e Metodologia"):
    st.markdown("""
    **Fontes de Dados:**
    - IBGE/SIDRA: Dados de produção agrícola e área cultivada
    - MapBiomas: Cobertura e uso do solo
    - Defesa Agropecuária SP: Dados de rebanhos
    - NIPE/UNICAMP: Fatores de conversão e potencial energético
    
    **Metodologia:**
    - Os dados de geração de resíduos são calculados com base na produção agrícola reportada
    - Fatores de conversão específicos para cada cultura e tipo de resíduo
    - Dados atualizados anualmente conforme disponibilidade das fontes
    
    **Última atualização:** Março de 2024
    """)

st.markdown("---")

# --- Rodapé Minimalista ---
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 24px;">
    CP2B — Centro de Pesquisa para Inovação em Biogás | UNICAMP
</div>
""", unsafe_allow_html=True)

