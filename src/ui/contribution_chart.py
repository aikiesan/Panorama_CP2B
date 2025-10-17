"""
Contribution Chart Component
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Render visualizations of residue/sector contributions

Provides interactive charts showing:
- Pie chart of % contribution by sub-residue
- Bar chart comparing sub-residues
- Horizontal bar for sector breakdown
- Sankey diagram for flows (optional)

SOLID Compliance:
- Single Responsibility: Only renders contribution charts
- No data processing: Uses pre-calculated contributions
- Reusable across pages
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
from src.utils.formatters import format_biogas_potential


def render_contribution_pie_chart(
    contributions: List[Dict[str, any]],
    title: str = "Contribuição por Sub-Resíduo",
    show_legend: bool = True,
    height: int = 500
) -> None:
    """
    Render interactive pie chart showing % contribution of each component.

    Args:
        contributions: List of dicts with 'name', 'ch4', 'percentage', 'icon'
        title: Chart title
        show_legend: Show legend (default True)
        height: Chart height in pixels

    Returns:
        None (renders to Streamlit via Plotly)

    Example:
        >>> from src.services import ContributionAnalyzer
        >>> from src.data.agricultura.cana import CANA_DE_ACUCAR_DATA
        >>> contributions = ContributionAnalyzer.calculate_contributions(
        ...     CANA_DE_ACUCAR_DATA.sub_residues
        ... )
        >>> render_contribution_pie_chart(contributions)
    """
    if not contributions:
        st.warning("Sem dados de contribuição disponíveis")
        return

    # Filter out zero contributions
    valid_contributions = [c for c in contributions if c['ch4'] > 0 or c == contributions[0]]

    # Prepare data
    labels = [f"{c['icon']} {c['name']}" for c in valid_contributions]
    values = [c['ch4'] for c in valid_contributions]
    percentages = [c['percentage'] for c in valid_contributions]
    hover_text = [
        f"{valid_contributions[i]['name']}<br>"
        f"CH₄: {format_biogas_potential(valid_contributions[i]['ch4'])}<br>"
        f"Contribuição: {valid_contributions[i]['percentage']:.1f}%"
        for i in range(len(valid_contributions))
    ]

    # Create pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textposition='auto',
                textinfo='percent+label',
                hovertext=hover_text,
                hoverinfo='text',
                marker=dict(
                    line=dict(color='white', width=2)
                )
            )
        ]
    )

    fig.update_layout(
        title=title,
        height=height,
        showlegend=show_legend,
        font=dict(size=12),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, width="stretch")


def render_contribution_bar_chart(
    contributions: List[Dict[str, any]],
    title: str = "Potencial CH₄ por Sub-Resíduo",
    metric: str = 'ch4',
    orientation: str = 'vertical',
    height: int = 400
) -> None:
    """
    Render bar chart comparing sub-residues by CH4 or other metric.

    Args:
        contributions: List of contribution dicts
        title: Chart title
        metric: Which metric to plot ('ch4' default, or 'percentage')
        orientation: 'vertical' or 'horizontal' bars
        height: Chart height in pixels

    Returns:
        None (renders to Streamlit via Plotly)

    Example:
        >>> render_contribution_bar_chart(
        ...     contributions,
        ...     title="CH₄ Potencial",
        ...     orientation='horizontal'
        ... )
    """
    if not contributions:
        st.warning("Sem dados de contribuição disponíveis")
        return

    valid_contributions = [c for c in contributions if c['ch4'] > 0]

    if not valid_contributions:
        st.warning("Sem contribuições positivas para exibir")
        return

    # Prepare data
    names = [f"{c['icon']} {c['name']}" for c in valid_contributions]
    values = [c[metric] for c in valid_contributions]

    # Determine y-axis label
    y_label = "CH₄ Potencial (Mi Nm³)" if metric == 'ch4' else "Contribuição (%)"

    # Create bar chart
    if orientation == 'vertical':
        fig = go.Figure(
            data=[
                go.Bar(
                    x=names,
                    y=values,
                    text=[f"{v:.1f}" for v in values],
                    textposition='auto',
                    marker=dict(
                        color=values,
                        colorscale='Viridis',
                        showscale=False,
                        line=dict(color='darkgray', width=1)
                    ),
                    hovertemplate='<b>%{x}</b><br>' + y_label + ': %{y:.1f}<extra></extra>'
                )
            ]
        )
        fig.update_layout(
            title=title,
            xaxis_title="Sub-Resíduo",
            yaxis_title=y_label,
            height=height,
            margin=dict(l=60, r=20, t=40, b=60)
        )
    else:  # horizontal
        fig = go.Figure(
            data=[
                go.Bar(
                    y=names,
                    x=values,
                    orientation='h',
                    text=[f"{v:.1f}" for v in values],
                    textposition='auto',
                    marker=dict(
                        color=values,
                        colorscale='Viridis',
                        showscale=False,
                        line=dict(color='darkgray', width=1)
                    ),
                    hovertemplate='<b>%{y}</b><br>' + y_label + ': %{x:.1f}<extra></extra>'
                )
            ]
        )
        fig.update_layout(
            title=title,
            xaxis_title=y_label,
            yaxis_title="Sub-Resíduo",
            height=height,
            margin=dict(l=200, r=20, t=40, b=20)
        )

    st.plotly_chart(fig, width="stretch")


def render_contribution_comparison(
    contributions: List[Dict[str, any]],
    show_pie: bool = True,
    show_bar: bool = True
) -> None:
    """
    Render side-by-side pie and bar charts for comprehensive contribution analysis.

    Args:
        contributions: List of contribution dicts
        show_pie: Display pie chart (default True)
        show_bar: Display bar chart (default True)

    Returns:
        None (renders to Streamlit)

    Example:
        >>> render_contribution_comparison(contributions, show_pie=True, show_bar=True)
    """
    if not show_pie and not show_bar:
        st.warning("Selecione pelo menos um tipo de gráfico")
        return

    if show_pie and show_bar:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Distribuição (%)")
            render_contribution_pie_chart(
                contributions,
                title="",
                show_legend=True,
                height=400
            )

        with col2:
            st.markdown("### Potencial Absoluto")
            render_contribution_bar_chart(
                contributions,
                title="",
                metric='ch4',
                orientation='horizontal',
                height=400
            )
    elif show_pie:
        render_contribution_pie_chart(contributions)
    else:
        render_contribution_bar_chart(contributions)


def render_sector_contribution_chart(
    sector_aggregation: Dict[str, Dict[str, float]],
    title: str = "Distribuição de Potencial por Setor",
    show_values: bool = True
) -> None:
    """
    Render pie chart showing % contribution by sector (Agricultura, Pecuária, etc.).

    Args:
        sector_aggregation: Dict from ContributionAnalyzer.aggregate_by_sector()
        title: Chart title
        show_values: Show percentage labels

    Returns:
        None (renders to Streamlit via Plotly)

    Example:
        >>> sectors = {
        ...     'Agricultura': {...},
        ...     'Pecuária': {...}
        ... }
        >>> aggregation = ContributionAnalyzer.aggregate_by_sector(sectors)
        >>> render_sector_contribution_chart(aggregation)
    """
    if not sector_aggregation:
        st.warning("Sem dados de setores disponíveis")
        return

    # Calculate total for percentages
    total_ch4 = sum(s['total_ch4'] for s in sector_aggregation.values())

    if total_ch4 == 0:
        st.warning("Sem potencial de CH₄ calculado para os setores")
        return

    # Prepare data
    sector_icons = {
        'Agricultura': '🌾',
        'Pecuária': '🐄',
        'Urbano': '🏙️',
        'Industrial': '🏭'
    }

    labels = []
    values = []
    percentages = []

    for sector_name, data in sector_aggregation.items():
        icon = sector_icons.get(sector_name, '📊')
        labels.append(f"{icon} {sector_name}")
        values.append(data['total_ch4'])
        pct = (data['total_ch4'] / total_ch4 * 100) if total_ch4 > 0 else 0
        percentages.append(pct)

    # Create pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textposition='auto',
                textinfo='percent+label' if show_values else 'label',
                hovertext=[
                    f"{labels[i]}<br>"
                    f"CH₄: {format_biogas_potential(values[i])}<br>"
                    f"Contribuição: {percentages[i]:.1f}%"
                    for i in range(len(labels))
                ],
                hoverinfo='text',
                marker=dict(line=dict(color='white', width=2))
            )
        ]
    )

    fig.update_layout(
        title=title,
        height=500,
        font=dict(size=12),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, width="stretch")


def render_sector_bar_chart(
    sector_aggregation: Dict[str, Dict[str, float]],
    title: str = "Potencial CH₄ por Setor"
) -> None:
    """
    Render horizontal bar chart comparing sectors.

    Args:
        sector_aggregation: Dict from aggregate_by_sector()
        title: Chart title

    Returns:
        None (renders to Streamlit)
    """
    if not sector_aggregation:
        st.warning("Sem dados de setores")
        return

    sector_icons = {
        'Agricultura': '🌾',
        'Pecuária': '🐄',
        'Urbano': '🏙️',
        'Industrial': '🏭'
    }

    labels = [
        f"{sector_icons.get(s, '📊')} {s}"
        for s in sector_aggregation.keys()
    ]
    values = [s['total_ch4'] for s in sector_aggregation.values()]

    fig = go.Figure(
        data=[
            go.Bar(
                y=labels,
                x=values,
                orientation='h',
                text=[format_biogas_potential(v) for v in values],
                textposition='auto',
                marker=dict(
                    color=values,
                    colorscale='Plasma',
                    showscale=False
                )
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="CH₄ Potencial (Mi Nm³)",
        height=300,
        margin=dict(l=150, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, width="stretch")


def render_contribution_metrics_row(contributions: List[Dict[str, any]]) -> None:
    """
    Render contribution data as metric cards in a row.

    Args:
        contributions: List of contribution dicts

    Returns:
        None (renders to Streamlit)
    """
    if not contributions:
        return

    # Show top 4 contributors
    top_contributions = sorted(contributions, key=lambda x: x['ch4'], reverse=True)[:4]

    cols = st.columns(len(top_contributions))

    for col, contrib in zip(cols, top_contributions):
        with col:
            st.metric(
                f"{contrib['icon']} {contrib['name'][:20]}",
                f"{contrib['percentage']:.1f}%",
                f"{format_biogas_potential(contrib['ch4'])}"
            )
