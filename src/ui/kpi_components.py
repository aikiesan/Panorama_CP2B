"""
KPI Components Module - Single Responsibility Principle
Reusable KPI and metric card components for the biogas dashboard.
"""

import streamlit as st
from typing import Dict


def render_kpi_cards(kpis: Dict) -> None:
    """
    Renders KPI metrics in a row of columns.

    Args:
        kpis: Dictionary with KPI values
            - total_biogas: Total biogas potential
            - total_municipios: Number of municipalities
            - top_municipio: Name of top municipality
            - top_municipio_valor: Biogas value of top municipality
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🌱 Potencial Total de Biogás",
            value=f"{kpis['total_biogas']:,.0f} m³/ano",
            help="Somatório do potencial de biogás de todos os municípios filtrados"
        )

    with col2:
        st.metric(
            label="🏙️ Municípios",
            value=f"{kpis['total_municipios']:,}",
            help="Número de municípios considerados na análise"
        )

    with col3:
        st.metric(
            label="⭐ Maior Potencial",
            value=kpis['top_municipio'],
            delta=f"{kpis['top_municipio_valor']:,.0f} m³/ano",
            help="Município com maior potencial de biogás"
        )


def render_sector_kpis(kpis: Dict) -> None:
    """
    Renders sector-specific KPI metrics.

    Args:
        kpis: Dictionary with sector KPI values
            - total_agricola: Agricultural biogas
            - total_pecuaria: Livestock biogas
            - total_urbano: Urban biogas
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🌾 Agricultura",
            value=f"{kpis['total_agricola']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos agrícolas"
        )

    with col2:
        st.metric(
            label="🐄 Pecuária",
            value=f"{kpis['total_pecuaria']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos pecuários"
        )

    with col3:
        st.metric(
            label="🏭 Urbano",
            value=f"{kpis['total_urbano']:,.0f} m³/ano",
            help="Potencial de biogás de resíduos urbanos (RSU e RPO)"
        )


def render_comparison_metrics(mun_data, state_avg: Dict) -> None:
    """
    Renders comparison metrics between a municipality and state average.

    Args:
        mun_data: Series with municipality data
        state_avg: Dictionary with state average values
    """
    st.subheader("📊 Comparação com Média Estadual")

    col1, col2, col3 = st.columns(3)

    with col1:
        mun_total = mun_data.get('total_final_m_ano', 0)
        avg_total = state_avg.get('total_final_m_ano', 0)
        delta_pct = ((mun_total - avg_total) / avg_total * 100) if avg_total > 0 else 0

        st.metric(
            label="Potencial Total",
            value=f"{mun_total:,.0f} m³/ano",
            delta=f"{delta_pct:+.1f}% vs média",
            help="Comparado com a média estadual"
        )

    with col2:
        mun_pop = mun_data.get('populacao_2022', 0)
        avg_pop = state_avg.get('populacao_2022', 0)
        delta_pop_pct = ((mun_pop - avg_pop) / avg_pop * 100) if avg_pop > 0 else 0

        st.metric(
            label="População",
            value=f"{mun_pop:,.0f}",
            delta=f"{delta_pop_pct:+.1f}% vs média"
        )

    with col3:
        mun_dens = mun_data.get('densidade_demografica', 0)
        avg_dens = state_avg.get('densidade_demografica', 0)
        delta_dens_pct = ((mun_dens - avg_dens) / avg_dens * 100) if avg_dens > 0 else 0

        st.metric(
            label="Densidade Demográfica",
            value=f"{mun_dens:.1f} hab/km²",
            delta=f"{delta_dens_pct:+.1f}% vs média"
        )


__all__ = [
    'render_kpi_cards',
    'render_sector_kpis',
    'render_comparison_metrics'
]
