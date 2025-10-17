"""
Municipality Ranking Component
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Display municipality rankings and geographic analysis

Renders tables and visualizations showing:
- Top N municipalities by CH4 potential
- Electricity generation capacity by municipality
- Geographic distribution (map optional)
- Municipal ranking tables with sortable columns

SOLID Compliance:
- Single Responsibility: Only renders municipality rankings
- No data calculation: Uses pre-ranked data
- Reusable across residues
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Optional
from src.utils.formatters import format_biogas_potential, format_electricity_potential


def render_top_municipalities_table(
    municipalities: List[Dict[str, any]],
    top_n: int = 10,
    title: str = "Top Municípios Produtores",
    show_rank: bool = True,
    show_state: bool = True
) -> None:
    """
    Render table with top N municipalities by CH4 potential.

    Displays ranking table with columns:
    - Rank
    - Municipality name
    - CH4 potential (Mi Nm³)
    - Electricity generation (GWh)
    - % of top 10 total
    - State (optional)

    Args:
        municipalities: List of municipality dicts from ContributionAnalyzer
        top_n: Number of municipalities to display (default 10)
        title: Table title
        show_rank: Display rank column (default True)
        show_state: Display state column (default True)

    Returns:
        None (renders to Streamlit)

    Example:
        >>> from src.services import ContributionAnalyzer
        >>> from src.data.agricultura.cana import CANA_DE_ACUCAR_DATA
        >>> municipalities = ContributionAnalyzer.rank_municipalities(
        ...     CANA_DE_ACUCAR_DATA,
        ...     top_n=10
        ... )
        >>> render_top_municipalities_table(municipalities)
    """
    if not municipalities:
        st.warning("Sem dados de municípios disponíveis")
        return

    # Limit to top_n
    top_municipalities = municipalities[:top_n]

    # Prepare dataframe
    data = []
    for munic in top_municipalities:
        row = {}

        if show_rank:
            row['Rank'] = f"#{munic['rank']}"

        row['Município'] = munic['name']
        row['CH₄ Potencial'] = f"{munic['ch4']:.1f} Mi Nm³"
        row['Eletricidade'] = f"{munic['electricity']:.2f} GWh"
        row['% do Top 10'] = f"{munic['percentage']:.1f}%"

        if show_state and munic.get('state'):
            row['Estado'] = munic['state']

        data.append(row)

    df = pd.DataFrame(data)

    st.markdown(f"### {title}")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={col: st.column_config.TextColumn() for col in df.columns}
        )

    with col2:
        total_ch4 = sum(m['ch4'] for m in top_municipalities)
        st.metric("Total CH₄ (Top 10)", f"{total_ch4:.1f} Mi Nm³")

    with col3:
        total_electricity = sum(m['electricity'] for m in top_municipalities)
        st.metric("Total Eletricidade", f"{total_electricity:.2f} GWh")


def render_municipality_bar_chart(
    municipalities: List[Dict[str, any]],
    metric: str = 'ch4',
    top_n: int = 15,
    title: str = "Municípios Produtores",
    height: int = 500
) -> None:
    """
    Render horizontal bar chart of municipalities by potential.

    Args:
        municipalities: List of municipality dicts
        metric: 'ch4' or 'electricity'
        top_n: Show top N municipalities
        title: Chart title
        height: Chart height in pixels

    Returns:
        None (renders to Streamlit via Plotly)

    Example:
        >>> render_municipality_bar_chart(
        ...     municipalities,
        ...     metric='ch4',
        ...     top_n=15
        ... )
    """
    if not municipalities:
        st.warning("Sem dados de municípios")
        return

    # Get top N
    top_municipalities = municipalities[:top_n]

    # Prepare data
    names = [m['name'] for m in top_municipalities]
    values = [m[metric] for m in top_municipalities]

    # Determine title and label
    if metric == 'ch4':
        axis_title = "CH₄ Potencial (Mi Nm³)"
        hover_title = f"{top_municipalities[0]['name']}: CH₄ = "
    else:
        axis_title = "Eletricidade (GWh)"
        hover_title = f"{top_municipalities[0]['name']}: Energia = "

    # Create chart
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
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title=axis_title)
                ),
                hovertemplate='<b>%{y}</b><br>' + axis_title + ': %{x:.1f}<extra></extra>'
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title=axis_title,
        yaxis_title="Município",
        height=height,
        margin=dict(l=200, r=20, t=40, b=20),
        font=dict(size=11)
    )

    st.plotly_chart(fig, width="stretch")


def render_municipality_pie_chart(
    municipalities: List[Dict[str, any]],
    top_n: int = 10,
    title: str = "Distribuição de Potencial por Município"
) -> None:
    """
    Render pie chart showing % contribution of top municipalities.

    Args:
        municipalities: List of municipality dicts
        top_n: Number of municipalities to show
        title: Chart title

    Returns:
        None (renders to Streamlit via Plotly)
    """
    if not municipalities:
        st.warning("Sem dados de municípios")
        return

    top_municipalities = municipalities[:top_n]

    names = [m['name'] for m in top_municipalities]
    values = [m['ch4'] for m in top_municipalities]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=names,
                values=values,
                textposition='auto',
                textinfo='percent+label',
                hovertext=[
                    f"{m['name']}<br>"
                    f"CH₄: {m['ch4']:.1f} Mi Nm³<br>"
                    f"Eletricidade: {m['electricity']:.2f} GWh"
                    for m in top_municipalities
                ],
                hoverinfo='text'
            )
        ]
    )

    fig.update_layout(
        title=title,
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, width="stretch")


def render_municipality_metrics(municipalities: List[Dict[str, any]]) -> None:
    """
    Render key metrics about municipalities in a row.

    Args:
        municipalities: List of municipality dicts

    Returns:
        None (renders to Streamlit)
    """
    if not municipalities:
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Top Município",
            municipalities[0]['name'][:20],
            municipalities[0]['ch4']
        )

    with col2:
        total_ch4 = sum(m['ch4'] for m in municipalities[:10])
        st.metric(
            "Total (Top 10)",
            f"{total_ch4:.1f} Mi Nm³"
        )

    with col3:
        avg_ch4 = sum(m['ch4'] for m in municipalities[:10]) / min(10, len(municipalities))
        st.metric(
            "Média (Top 10)",
            f"{avg_ch4:.1f} Mi Nm³"
        )

    with col4:
        total_electricity = sum(m['electricity'] for m in municipalities[:10])
        st.metric(
            "Eletricidade (Top 10)",
            f"{total_electricity:.2f} GWh"
        )


def render_municipality_comparison(
    municipalities1: List[Dict[str, any]],
    municipalities2: List[Dict[str, any]],
    label1: str = "Cenário 1",
    label2: str = "Cenário 2",
    top_n: int = 10
) -> None:
    """
    Render side-by-side comparison of municipalities in two scenarios.

    Args:
        municipalities1: First list of municipalities
        municipalities2: Second list of municipalities
        label1: Label for first scenario
        label2: Label for second scenario
        top_n: Number of municipalities to compare

    Returns:
        None (renders to Streamlit)
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {label1}")
        if municipalities1:
            render_top_municipalities_table(
                municipalities1,
                top_n=top_n,
                title="",
                show_rank=False,
                show_state=False
            )
        else:
            st.info("Sem dados disponíveis")

    with col2:
        st.markdown(f"### {label2}")
        if municipalities2:
            render_top_municipalities_table(
                municipalities2,
                top_n=top_n,
                title="",
                show_rank=False,
                show_state=False
            )
        else:
            st.info("Sem dados disponíveis")


def render_municipality_detail_card(
    municipality: Dict[str, any],
    show_icon: bool = True
) -> None:
    """
    Render detailed card for a single municipality.

    Args:
        municipality: Municipality dict
        show_icon: Display state icon

    Returns:
        None (renders to Streamlit)
    """
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 8, 1])

        with col1:
            if show_icon and municipality.get('state'):
                st.markdown("📍")

        with col2:
            st.markdown(f"## {municipality['name']}")
            if municipality.get('state'):
                st.caption(f"Estado: {municipality['state']}")

        with col3:
            st.metric("Rank", f"#{municipality['rank']}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "CH₄ Potencial",
                f"{municipality['ch4']:.1f} Mi Nm³"
            )

        with col2:
            st.metric(
                "Eletricidade",
                f"{municipality['electricity']:.2f} GWh"
            )

        with col3:
            st.metric(
                "% do Top 10",
                f"{municipality['percentage']:.1f}%"
            )

        with col4:
            if municipality.get('production'):
                st.metric(
                    "Produção",
                    f"{municipality['production']:.0f} ton/ano"
                )


def render_municipality_distribution_map_placeholder() -> None:
    """
    Render placeholder for interactive municipality map.

    Future: Can be replaced with actual Plotly map when geographic data available.

    Returns:
        None (renders to Streamlit)
    """
    st.info(
        "🗺️ **Mapa Interativo** disponível em futuras versões com dados geográficos detalhados"
    )
