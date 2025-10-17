"""
Comparative Analysis Components
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Phase 4: Enhanced comparison features
- Residue comparison (multiple residues side by side)
- Scenario progression analysis
- Top residues ranking
- Residue potential vs availability analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
from src.data.residue_registry import RESIDUES_REGISTRY, CATEGORIES


def get_top_residues(scenario: str = "Realista", limit: int = 15, category: Optional[str] = None) -> List[Dict]:
    """
    Get top residues by biogas potential.

    Args:
        scenario: Which scenario to analyze
        limit: Number of residues to return
        category: Filter by category (None = all)

    Returns:
        List of residue dictionaries sorted by potential descending
    """
    residues = []

    for residue_name, residue_data in RESIDUES_REGISTRY.items():
        if category and residue_data.category != category:
            continue

        residues.append({
            'name': residue_name,
            'icon': residue_data.icon,
            'category': residue_data.category,
            'ch4_potential': residue_data.scenarios.get(scenario, 0.0),
            'availability': residue_data.availability.final_availability,
            'generation': residue_data.generation[:50] + '...' if len(residue_data.generation) > 50 else residue_data.generation
        })

    # Sort by potential descending
    residues.sort(key=lambda x: x['ch4_potential'], reverse=True)

    return residues[:limit]


def render_top_residues_table(scenario: str = "Realista", limit: int = 15, category: Optional[str] = None) -> None:
    """
    Render table of top residues by potential.

    Args:
        scenario: Which scenario to show
        limit: Number of residues to display
        category: Filter by category (None = all)
    """
    residues = get_top_residues(scenario, limit, category)

    if not residues:
        st.info("Sem dados disponíveis")
        return

    # Create dataframe
    df = pd.DataFrame([{
        'Rank': idx + 1,
        'Residuo': f"{r['icon']} {r['name']}",
        'Categoria': r['category'],
        'Potencial CH4': f"{r['ch4_potential']:,.0f}",
        'Disponibilidade': f"{r['availability']:.1f}%"
    } for idx, r in enumerate(residues)])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Rank': st.column_config.NumberColumn(width='small'),
            'Residuo': st.column_config.TextColumn(width='large'),
            'Categoria': st.column_config.TextColumn(width='medium'),
            'Potencial CH4': st.column_config.TextColumn(width='medium'),
            'Disponibilidade': st.column_config.TextColumn(width='medium')
        }
    )


def render_top_residues_chart(scenario: str = "Realista", limit: int = 15, category: Optional[str] = None) -> None:
    """
    Render bar chart of top residues.

    Args:
        scenario: Which scenario to show
        limit: Number of residues to display
        category: Filter by category (None = all)
    """
    residues = get_top_residues(scenario, limit, category)

    if not residues:
        st.info("Sem dados disponíveis")
        return

    names = [f"{r['icon']} {r['name'][:30]}" for r in residues]
    values = [r['ch4_potential'] for r in residues]
    colors = ['#059669' if r['category'] == 'Agricultura' else
              '#ea580c' if r['category'] == 'Pecuária' else
              '#7c3aed' if r['category'] == 'Urbano' else
              '#8b5cf6' for r in residues]

    fig = go.Figure(data=[
        go.Bar(
            y=names,
            x=values,
            orientation='h',
            marker_color=colors,
            text=[f'{v:,.0f}' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Potencial: %{x:,.0f} Mi m³/ano<extra></extra>'
        )
    ])

    fig.update_layout(
        title=f'Top {limit} Resíduos - Cenário {scenario}',
        xaxis_title='Potencial CH₄ (Mi m³/ano)',
        yaxis_title='',
        height=600,
        margin=dict(l=200),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def render_residue_potential_vs_availability(scenario: str = "Realista") -> None:
    """
    Render scatter plot of residue potential vs availability.

    Args:
        scenario: Which scenario to show
    """
    data = []

    for residue_name, residue_data in RESIDUES_REGISTRY.items():
        potential = residue_data.scenarios.get(scenario, 0.0)
        if potential > 0:  # Only include residues with potential
            data.append({
                'name': f"{residue_data.icon} {residue_name}",
                'potential': potential,
                'availability': residue_data.availability.final_availability,
                'category': residue_data.category
            })

    if not data:
        st.info("Sem dados disponíveis")
        return

    df = pd.DataFrame(data)

    # Color mapping
    color_map = {
        'Agricultura': '#059669',
        'Pecuária': '#ea580c',
        'Urbano': '#7c3aed',
        'Industrial': '#8b5cf6'
    }

    fig = px.scatter(
        df,
        x='availability',
        y='potential',
        size='potential',
        color='category',
        hover_name='name',
        color_discrete_map=color_map,
        title=f'Potencial vs Disponibilidade - Cenário {scenario}',
        labels={
            'availability': 'Disponibilidade Final (%)',
            'potential': 'Potencial CH₄ (Mi m³/ano)',
            'category': 'Setor'
        }
    )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def render_scenario_progression(residue_name: str) -> None:
    """
    Render scenario progression for a specific residue.

    Args:
        residue_name: Name of residue to analyze
    """
    if residue_name not in RESIDUES_REGISTRY:
        st.error(f"Resíduo '{residue_name}' não encontrado")
        return

    residue = RESIDUES_REGISTRY[residue_name]
    scenarios = ['Pessimista', 'Realista', 'Otimista', 'Teórico (100%)']
    values = [residue.scenarios.get(s, 0.0) for s in scenarios]

    fig = go.Figure(data=[
        go.Scatter(
            x=scenarios,
            y=values,
            mode='lines+markers',
            line=dict(color='#059669', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            text=[f'{v:,.0f} Mi m³/ano' for v in values],
            textposition='top center',
            hovertemplate='<b>%{x}</b><br>Potencial: %{y:,.0f} Mi m³/ano<extra></extra>'
        )
    ])

    fig.update_layout(
        title=f'Progressão de Cenários - {residue.icon} {residue_name}',
        xaxis_title='Cenário',
        yaxis_title='Potencial CH₄ (Mi m³/ano)',
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


def render_residue_comparison(residue_names: List[str], scenario: str = "Realista") -> None:
    """
    Compare multiple residues side by side.

    Args:
        residue_names: List of residue names to compare
        scenario: Which scenario to show
    """
    comparison_data = []

    for residue_name in residue_names:
        if residue_name in RESIDUES_REGISTRY:
            residue = RESIDUES_REGISTRY[residue_name]
            comparison_data.append({
                'name': residue_name,
                'icon': residue.icon,
                'ch4_potential': residue.scenarios.get(scenario, 0.0),
                'availability': residue.availability.final_availability,
                'bmp': residue.chemical_params.bmp,
                'moisture': residue.chemical_params.moisture
            })

    if not comparison_data:
        st.warning("Nenhum resíduo válido para comparação")
        return

    # Create comparison chart
    names = [f"{r['icon']} {r['name']}" for r in comparison_data]
    ch4_values = [r['ch4_potential'] for r in comparison_data]
    availability_values = [r['availability'] for r in comparison_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names,
        y=ch4_values,
        name='Potencial CH₄ (Mi m³/ano)',
        yaxis='y',
        marker_color='#059669',
        text=[f'{v:,.0f}' for v in ch4_values],
        textposition='auto'
    ))

    fig.add_trace(go.Scatter(
        x=names,
        y=availability_values,
        name='Disponibilidade (%)',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#ea580c', width=3),
        marker=dict(size=10),
        text=[f'{v:.1f}%' for v in availability_values],
        textposition='top center'
    ))

    fig.update_layout(
        title=f'Comparação de Resíduos - Cenário {scenario}',
        yaxis=dict(title='Potencial CH₄ (Mi m³/ano)'),
        yaxis2=dict(title='Disponibilidade (%)', overlaying='y', side='right'),
        hovermode='x unified',
        height=400,
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed comparison table
    st.markdown("### Detalhes da Comparação")
    df = pd.DataFrame([{
        'Resíduo': f"{r['icon']} {r['name']}",
        'Potencial CH₄': f"{r['ch4_potential']:,.0f} Mi m³/ano",
        'Disponibilidade': f"{r['availability']:.1f}%",
        'BMP': f"{r['bmp']:.1f}",
        'Umidade': f"{r['moisture']:.1f}%"
    } for r in comparison_data])

    st.dataframe(df, use_container_width=True, hide_index=True)


def render_comparative_analysis_dashboard(scenario: str = "Realista") -> None:
    """
    Render complete comparative analysis dashboard.

    Args:
        scenario: Which scenario to visualize
    """
    st.markdown(f"## 📈 Análise Comparativa - Cenário {scenario}")

    # Section 1: Top residues
    st.markdown("### Top Resíduos por Potencial")
    st.markdown("**Ranking dos 15 resíduos com maior potencial de biogas**")

    col1, col2 = st.columns([1, 2])

    with col1:
        chart_type = st.radio(
            "Tipo de visualização:",
            ["Tabela", "Gráfico"],
            key="top_residues_view"
        )

    if chart_type == "Tabela":
        render_top_residues_table(scenario, limit=20)
    else:
        render_top_residues_chart(scenario, limit=20)

    st.divider()

    # Section 2: Potential vs Availability scatter
    st.markdown("### Análise de Potencial vs Disponibilidade")
    st.markdown("**Relação entre potencial de biogás e disponibilidade final**")
    render_residue_potential_vs_availability(scenario)

    st.divider()

    # Section 3: Top by category
    st.markdown("### Top Resíduos por Setor")

    category_tabs = st.tabs(["Agricultura", "Pecuária", "Urbano", "Industrial"])

    for tab, category in zip(category_tabs, ["Agricultura", "Pecuária", "Urbano", "Industrial"]):
        with tab:
            render_top_residues_table(scenario, limit=10, category=category)


__all__ = [
    'get_top_residues',
    'render_top_residues_table',
    'render_top_residues_chart',
    'render_residue_potential_vs_availability',
    'render_scenario_progression',
    'render_residue_comparison',
    'render_comparative_analysis_dashboard'
]
