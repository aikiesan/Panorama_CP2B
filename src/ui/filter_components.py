"""
Filter Components Module - Single Responsibility Principle
Reusable filter UI components for data exploration.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional


def render_filters_sidebar(df: pd.DataFrame) -> Dict:
    """
    Creates clean, intuitive filter controls in the sidebar.

    Args:
        df: Source DataFrame with all available data

    Returns:
        dict: Dictionary with selected filter values
    """
    st.sidebar.header("🔍 Filtros de Visualização")
    st.sidebar.markdown("Ajuste os filtros para explorar os dados")
    st.sidebar.markdown("---")

    # Sector filter - simplified
    st.sidebar.subheader("Por Setor")
    setores_selecionados = []
    if st.sidebar.checkbox("🌾 Agricultura", value=True):
        setores_selecionados.append('Agricultura')
    if st.sidebar.checkbox("🐄 Pecuária", value=True):
        setores_selecionados.append('Pecuária')
    if st.sidebar.checkbox("🏭 Urbano", value=True):
        setores_selecionados.append('Urbano')

    st.sidebar.markdown("---")

    # Potential category filter - simplified
    st.sidebar.subheader("Por Categoria de Potencial")
    categorias_selecionadas = []
    if st.sidebar.checkbox("🔴 Alto Potencial", value=True):
        categorias_selecionadas.append('ALTO')
    if st.sidebar.checkbox("🟡 Médio Potencial", value=True):
        categorias_selecionadas.append('MÉDIO')
    if st.sidebar.checkbox("🟢 Baixo Potencial", value=True):
        categorias_selecionadas.append('BAIXO')

    st.sidebar.markdown("---")

    # Population range filter - simplified
    st.sidebar.subheader("Por População")
    pop_min = int(df['populacao_2022'].min())
    pop_max = int(df['populacao_2022'].max())

    use_pop_filter = st.sidebar.checkbox("Filtrar por faixa populacional", value=False)

    if use_pop_filter:
        pop_range = st.sidebar.slider(
            "População (habitantes):",
            min_value=pop_min,
            max_value=pop_max,
            value=(pop_min, pop_max),
            format="%d"
        )
    else:
        pop_range = (pop_min, pop_max)

    st.sidebar.markdown("---")

    # Municipality search - simplified
    with st.sidebar.expander("🔎 Buscar Município Específico"):
        municipios_disponiveis = sorted(df['nome_municipio'].unique().tolist())
        municipio_busca = st.selectbox(
            "Digite ou selecione:",
            options=["Todos"] + municipios_disponiveis,
            index=0
        )
        municipios_selecionados = None if municipio_busca == "Todos" else [municipio_busca]

    return {
        'categorias': categorias_selecionadas if categorias_selecionadas else ['ALTO', 'MÉDIO', 'BAIXO'],
        'setores': setores_selecionados if setores_selecionados else ['Agricultura', 'Pecuária', 'Urbano'],
        'pop_range': pop_range,
        'municipios': municipios_selecionados
    }


def render_bmp_range_filter(min_bmp: float = 0, max_bmp: float = 800) -> tuple[float, float]:
    """
    Renders a BMP (Biochemical Methane Potential) range filter.

    Args:
        min_bmp: Minimum BMP value in dataset
        max_bmp: Maximum BMP value in dataset

    Returns:
        tuple: (min_selected, max_selected) BMP range
    """
    st.sidebar.subheader("Por Potencial Metanogênico (BMP)")

    bmp_range = st.sidebar.slider(
        "Faixa de BMP (mL CH₄/g VS):",
        min_value=float(min_bmp),
        max_value=float(max_bmp),
        value=(float(min_bmp), float(max_bmp)),
        step=10.0,
        help="Filtre resíduos por potencial metanogênico bioquímico"
    )

    return bmp_range


def render_residue_search(available_residues: List[str], key: str = "residue_search") -> Optional[str]:
    """
    Renders a residue search/select component.

    Args:
        available_residues: List of available residue names
        key: Unique key for the component

    Returns:
        str: Selected residue name or None
    """
    st.markdown("### 🔍 Buscar Resíduo")

    selected = st.selectbox(
        "**Digite ou selecione um resíduo:**",
        options=[""] + sorted(available_residues),
        format_func=lambda x: "Selecione um resíduo..." if x == "" else x,
        key=key
    )

    return selected if selected != "" else None


__all__ = [
    'render_filters_sidebar',
    'render_bmp_range_filter',
    'render_residue_search'
]
