"""
Sector Analysis Visualization Components
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Phase 4: Enhanced visualization for sector-level biogas potential analysis

Single Responsibility: Render aggregated sector analysis visualizations
- Sector potential comparison (pie chart, bar chart)
- Scenario distribution across sectors
- Top residues by sector
- Sector contribution to total potential
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
from src.data.residue_registry import RESIDUES_REGISTRY, SECTORS


def get_sector_statistics(scenario: str = "Realista") -> Dict[str, dict]:
    """
    Calculate aggregated statistics for each sector.

    Args:
        scenario: Which scenario to analyze ('Pessimista', 'Realista', 'Otimista', 'Teórico (100%)')

    Returns:
        Dictionary with sector stats: {sector_name: {'total_ch4': float, 'count': int, 'residues': list}}
    """
    stats = {}

    for sector_name, sector_info in SECTORS.items():
        sector_residues = sector_info.get("residues", [])
        total_ch4 = 0.0
        residue_details = []

        for residue_name in sector_residues:
            if residue_name in RESIDUES_REGISTRY:
                residue = RESIDUES_REGISTRY[residue_name]
                ch4_potential = residue.scenarios.get(scenario, 0.0)

                # Skip residues with no calculated scenario data (TODO: calculate from generation data)
                if ch4_potential == 0.0:
                    continue

                total_ch4 += ch4_potential

                residue_details.append({
                    'name': residue_name,
                    'ch4': ch4_potential,
                    'availability': residue.availability.final_availability,
                    'icon': residue.icon
                })

        # Sort residues by potential
        residue_details.sort(key=lambda x: x['ch4'], reverse=True)

        stats[sector_name] = {
            'total_ch4': total_ch4,
            'count': len(sector_residues),
            'residues': residue_details
        }

    return stats


def render_sector_potential_pie(scenario: str = "Realista") -> None:
    """
    Render pie chart showing sector contribution to total biogas potential.

    Args:
        scenario: Which scenario to visualize
    """
    stats = get_sector_statistics(scenario)

    sectors = list(stats.keys())
    values = [stats[s]['total_ch4'] for s in sectors]
    colors = ['#059669', '#ea580c', '#7c3aed', '#8b5cf6']  # Agricultura, Pecuária, Urbano, Industrial

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=sectors,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>Potencial: %{value:.0f} Mi m³/ano<br>Percentual: %{percent}<extra></extra>',
        textinfo='label+percent',
        textposition='auto'
    )])

    fig.update_layout(
        title=f'Distribuição de Potencial de Biogás por Setor - Cenário {scenario}',
        height=400,
        showlegend=True,
        font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True, key="sector_pie_chart")


def render_sector_comparison_bars(scenario: str = "Realista") -> None:
    """
    Render bar chart comparing sector potentials.

    Args:
        scenario: Which scenario to visualize
    """
    stats = get_sector_statistics(scenario)

    sectors = list(stats.keys())
    values = [stats[s]['total_ch4'] for s in sectors]
    colors = ['#059669', '#ea580c', '#7c3aed', '#8b5cf6']

    fig = go.Figure(data=[
        go.Bar(
            x=sectors,
            y=values,
            text=[f'{v:,.0f}' for v in values],
            textposition='auto',
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Potencial: %{y:,.0f} Mi m³/ano<extra></extra>'
        )
    ])

    fig.update_layout(
        title=f'Potencial de Biogás por Setor - Cenário {scenario}',
        yaxis_title='Potencial CH₄ (Mi m³/ano)',
        xaxis_title='Setor',
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, key="sector_bar_chart")


def render_sector_metrics(scenario: str = "Realista") -> None:
    """
    Render sector statistics as metric cards.

    Args:
        scenario: Which scenario to visualize
    """
    stats = get_sector_statistics(scenario)
    total_potential = sum([s['total_ch4'] for s in stats.values()])

    cols = st.columns(4)

    sector_names = ["Agricultura", "Pecuária", "Urbano", "Industrial"]
    sector_icons = ["🌾", "🐄", "🏙️", "🏭"]

    for col, sector_name, icon in zip(cols, sector_names, sector_icons):
        with col:
            sector_stats = stats[sector_name]
            potential = sector_stats['total_ch4']
            percentage = (potential / total_potential * 100) if total_potential > 0 else 0

            st.metric(
                f"{icon} {sector_name}",
                f"{potential:,.0f} Mi m³",
                f"{percentage:.1f}% do total",
                delta_color="off"
            )


def render_sector_top_residues(sector_name: str = "Agricultura", scenario: str = "Realista", top_n: int = 5) -> None:
    """
    Render table of top residues in a specific sector.

    Args:
        sector_name: Which sector to analyze
        scenario: Which scenario to visualize
        top_n: Number of top residues to show
    """
    stats = get_sector_statistics(scenario)
    sector_stats = stats.get(sector_name, {})
    residue_details = sector_stats.get('residues', [])[:top_n]

    if not residue_details:
        st.info(f"Sem dados disponíveis para {sector_name}")
        return

    # Create dataframe
    df = pd.DataFrame([{
        'Residuo': f"{r['icon']} {r['name']}",
        'Potencial CH4': f"{r['ch4']:,.0f} Mi m³/ano",
        'Disponibilidade': f"{r['availability']:.1f}%"
    } for r in residue_details])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Residuo': st.column_config.TextColumn(width='large'),
            'Potencial CH4': st.column_config.TextColumn(width='medium'),
            'Disponibilidade': st.column_config.TextColumn(width='medium')
        }
    )


def render_scenario_comparison_all_sectors(scenario_1: str = "Pessimista", scenario_2: str = "Realista") -> None:
    """
    Render comparison of two scenarios across all sectors.

    Args:
        scenario_1: First scenario to compare
        scenario_2: Second scenario to compare
    """
    stats_1 = get_sector_statistics(scenario_1)
    stats_2 = get_sector_statistics(scenario_2)

    sectors = list(stats_1.keys())
    values_1 = [stats_1[s]['total_ch4'] for s in sectors]
    values_2 = [stats_2[s]['total_ch4'] for s in sectors]

    fig = go.Figure(data=[
        go.Bar(name=scenario_1, x=sectors, y=values_1, marker_color='#dc2626'),
        go.Bar(name=scenario_2, x=sectors, y=values_2, marker_color='#059669')
    ])

    fig.update_layout(
        title=f'Comparação de Cenários: {scenario_1} vs {scenario_2}',
        yaxis_title='Potencial CH₄ (Mi m³/ano)',
        xaxis_title='Setor',
        barmode='group',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True, key="scenario_comparison_chart")


def render_sector_electricity_potential(scenario: str = "Realista", key_suffix: str = "") -> None:
    """
    Render electricity generation potential by sector.

    Args:
        scenario: Which scenario to visualize
        key_suffix: Optional suffix to make chart key unique when used multiple times
    """
    stats = get_sector_statistics(scenario)

    sectors = []
    gwh_values = []

    for sector_name, sector_stats in stats.items():
        # Convert Mi m³ CH₄ to GWh (1 Nm³ CH₄ ≈ 1 kWh ≈ 0.001 MWh)
        # 1 Mi m³ = 1,000,000 Nm³
        ch4_million = sector_stats['total_ch4']
        gwh = (ch4_million * 1_000_000 * 1.43) / 1_000_000  # Using 1.43 conversion factor

        sectors.append(sector_name)
        gwh_values.append(gwh)

    colors = ['#059669', '#ea580c', '#7c3aed', '#8b5cf6']

    fig = go.Figure(data=[
        go.Bar(
            x=sectors,
            y=gwh_values,
            text=[f'{v:.0f}' for v in gwh_values],
            textposition='auto',
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Eletricidade: %{y:.0f} GWh/ano<extra></extra>'
        )
    ])

    fig.update_layout(
        title=f'Potencial de Geração Elétrica por Setor - Cenário {scenario}',
        yaxis_title='Energia (GWh/ano)',
        xaxis_title='Setor',
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, key=f"electricity_potential_chart{key_suffix}")


def render_full_sector_dashboard(scenario: str = "Realista") -> None:
    """
    Render complete sector analysis dashboard.

    Args:
        scenario: Which scenario to visualize
    """
    st.markdown(f"## 📊 Análise de Setores - Cenário {scenario}")

    # Metrics row
    st.markdown("### Potencial por Setor")
    render_sector_metrics(scenario)

    st.divider()

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Distribuição de Potencial")
        render_sector_potential_pie(scenario)

    with col2:
        st.markdown("### Comparação entre Setores")
        render_sector_comparison_bars(scenario)

    st.divider()

    # Electricity potential
    st.markdown("### Potencial de Geração Elétrica")
    render_sector_electricity_potential(scenario, key_suffix="_dashboard")

    st.divider()

    # Top residues by sector
    st.markdown("### Principais Resíduos por Setor")

    sector_tabs = st.tabs(["Agricultura", "Pecuária", "Urbano", "Industrial"])

    for tab, sector_name in zip(sector_tabs, ["Agricultura", "Pecuária", "Urbano", "Industrial"]):
        with tab:
            render_sector_top_residues(sector_name, scenario, top_n=7)


__all__ = [
    'get_sector_statistics',
    'render_sector_potential_pie',
    'render_sector_comparison_bars',
    'render_sector_metrics',
    'render_sector_top_residues',
    'render_scenario_comparison_all_sectors',
    'render_sector_electricity_potential',
    'render_full_sector_dashboard'
]
