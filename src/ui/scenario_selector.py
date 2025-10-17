"""
Scenario Selector Component
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Provide UI for selecting availability scenarios

Renders horizontal radio buttons for selecting one of 4 scenarios:
- Pessimista (conservative, max competition)
- Realista (realistic, baseline)
- Otimista (optimistic, min competition)
- Teórico (theoretical, no constraints)

SOLID Compliance:
- Single Responsibility: Only renders scenario selection
- No business logic: Pure UI component
- Reusable across pages
"""

import streamlit as st
from typing import Literal


def render_scenario_selector(
    key: str = 'scenario_selector',
    default: str = 'Realista',
    horizontal: bool = True,
    show_descriptions: bool = True
) -> str:
    """
    Render horizontal/vertical scenario selector radio buttons.

    Provides user-friendly way to select one of 4 scenarios for
    availability analysis and visualization.

    Args:
        key: Unique key for Streamlit session state (required)
        default: Default selected scenario ('Realista' default)
        horizontal: Use horizontal layout (True) or vertical (False)
        show_descriptions: Show scenario descriptions (True) or names only (False)

    Returns:
        Selected scenario name: 'Pessimista', 'Realista', 'Otimista', or 'Teórico (100%)'

    Example:
        >>> scenario = render_scenario_selector(key='main_page_scenario')
        >>> st.write(f"Selected: {scenario}")
        Selected: Realista

    Visual Output:
        ┌─────────────────────────────────────────────┐
        │ 🎭 Cenários de Disponibilidade              │
        ├─────────────────────────────────────────────┤
        │ ( ) Pessimista  ( ) Realista  (•) Otimista │
        │ ( ) Teórico 100%                            │
        └─────────────────────────────────────────────┘
    """
    # Scenario definitions
    scenarios = {
        'Pessimista': {
            'label': '😟 Pessimista',
            'description': 'Cenário conservador com máxima competição'
        },
        'Realista': {
            'label': '📊 Realista',
            'description': 'Cenário calibrado com fatores reais'
        },
        'Otimista': {
            'label': '😊 Otimista',
            'description': 'Cenário otimista com mínima competição'
        },
        'Teórico (100%)': {
            'label': '🎯 Teórico (100%)',
            'description': 'Máximo teórico sem restrições'
        }
    }

    # Container with title
    st.markdown("### 🎭 Cenários de Disponibilidade")

    if show_descriptions:
        st.markdown("**Selecione um cenário para análise:**")

    # Radio button selection
    col1, col2 = st.columns([3, 1])

    with col1:
        options = list(scenarios.keys())
        selected = st.radio(
            label="Cenário",
            options=options,
            index=options.index(default) if default in options else 1,
            horizontal=horizontal,
            key=key,
            label_visibility="collapsed"
        )

    with col2:
        if show_descriptions and selected in scenarios:
            st.info(
                f"ℹ️ {scenarios[selected]['description']}",
                icon="ℹ️"
            )

    return selected


def render_scenario_tabs(
    key: str = 'scenario_tabs',
    default_index: int = 1
) -> str:
    """
    Render scenarios as tabs (alternative to radio buttons).

    Args:
        key: Unique key for Streamlit component
        default_index: Index of default selected tab

    Returns:
        Selected scenario name

    Example:
        >>> scenario = render_scenario_tabs(key='tabs_scenario')
    """
    scenario_names = ['Pessimista', 'Realista', 'Otimista', 'Teórico (100%)']
    scenario_icons = ['😟', '📊', '😊', '🎯']

    tabs = st.tabs([f"{icon} {name}" for icon, name in zip(scenario_icons, scenario_names)])

    # Create hidden radio to track selection
    selected = st.radio(
        "Scenario",
        scenario_names,
        index=default_index,
        key=key,
        label_visibility="collapsed"
    )

    return selected


def render_scenario_comparison_header(
    scenario: str,
    show_chart_button: bool = True
) -> None:
    """
    Render header showing current scenario with comparison option.

    Args:
        scenario: Currently selected scenario name
        show_chart_button: Show "Compare Scenarios" button

    Returns:
        None (renders to Streamlit)

    Example:
        >>> render_scenario_comparison_header('Realista')
    """
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        emoji = {
            'Pessimista': '😟',
            'Realista': '📊',
            'Otimista': '😊',
            'Teórico (100%)': '🎯'
        }.get(scenario, '❓')
        st.markdown(f"## {emoji} Cenário: **{scenario}**")

    with col2:
        descriptions = {
            'Pessimista': 'Máxima competição, fatores mínimos',
            'Realista': 'Calibrado com dados reais',
            'Otimista': 'Mínima competição, fatores máximos',
            'Teórico (100%)': 'Sem restrições externas'
        }
        st.caption(descriptions.get(scenario, ''))

    with col3:
        if show_chart_button and st.button("📈 Comparar", key=f"compare_{scenario}"):
            st.session_state.show_scenario_comparison = True
            st.rerun()


def render_scenario_info_box(scenario: str) -> None:
    """
    Render informational box about the selected scenario.

    Args:
        scenario: Scenario name to display info for

    Returns:
        None (renders to Streamlit)
    """
    scenario_info = {
        'Pessimista': {
            'color': 'red',
            'title': 'Cenário Pessimista',
            'description': 'Assume máxima concorrência por recursos alternativos',
            'details': [
                '• FC: Valor mínimo (menor eficiência de coleta)',
                '• FCp: Valor máximo (máxima competição)',
                '• FS: Valor mínimo (sazonalidade forte)',
                '• FL: Valor mínimo (maiores restrições logísticas)',
                '• Resultado: Disponibilidade muito baixa',
                '• Uso: Análise de caso pessimista, planejamento conservador'
            ]
        },
        'Realista': {
            'color': 'blue',
            'title': 'Cenário Realista',
            'description': 'Representa condições reais calibradas com dados experimentais',
            'details': [
                '• FC: Valor médio (eficiência típica)',
                '• FCp: Valor médio (competição típica)',
                '• FS: Valor médio (sazonalidade média)',
                '• FL: Valor médio (distância típica)',
                '• Resultado: Disponibilidade realista',
                '• Uso: Planejamento padrão, tomada de decisão'
            ]
        },
        'Otimista': {
            'color': 'green',
            'title': 'Cenário Otimista',
            'description': 'Assume melhorias operacionais e mercado em desenvolvimento',
            'details': [
                '• FC: Valor máximo (melhor eficiência de coleta)',
                '• FCp: Valor mínimo (redução de competição)',
                '• FS: Valor máximo (menor sazonalidade)',
                '• FL: Valor máximo (melhor logística)',
                '• Resultado: Disponibilidade elevada',
                '• Uso: Análise de potencial, planejamento ambicioso'
            ]
        },
        'Teórico (100%)': {
            'color': 'orange',
            'title': 'Cenário Teórico',
            'description': 'Máximo teórico sem nenhuma restrição externa',
            'details': [
                '• FC = 1.0 (coleta perfeita)',
                '• FCp = 0.0 (sem competição)',
                '• FS = 1.0 (disponível ano inteiro)',
                '• FL = 1.0 (logística perfeita)',
                '• Resultado: 100% teórico',
                '• Uso: Benchmark, estabelecer limites superiores'
            ]
        }
    }

    if scenario in scenario_info:
        info = scenario_info[scenario]
        st.markdown(f"### {info['title']}")
        st.markdown(info['description'])

        with st.expander("📋 Detalhes dos Fatores", expanded=False):
            for detail in info['details']:
                st.markdown(detail)


def render_scenario_selector_simple(
    key: str = 'simple_scenario'
) -> Literal['Pessimista', 'Realista', 'Otimista', 'Teórico (100%)']:
    """
    Render simple compact scenario selector (minimal space).

    Args:
        key: Unique session state key

    Returns:
        Selected scenario

    Example:
        >>> scenario = render_scenario_selector_simple()
    """
    return st.selectbox(
        label="Cenário",
        options=['Pessimista', 'Realista', 'Otimista', 'Teórico (100%)'],
        index=1,  # Default to Realista
        key=key,
        help="Selecione um cenário de disponibilidade"
    )


def render_scenario_with_metrics(
    scenario: str,
    availability_pct: float,
    ch4_potential: float,
    electricity_gwh: float = None
) -> None:
    """
    Render scenario display with key metrics.

    Args:
        scenario: Scenario name
        availability_pct: Availability percentage
        ch4_potential: CH4 potential in millions Nm³
        electricity_gwh: Electricity potential in GWh

    Returns:
        None (renders to Streamlit)
    """
    emoji = {
        'Pessimista': '😟',
        'Realista': '📊',
        'Otimista': '😊',
        'Teórico (100%)': '🎯'
    }.get(scenario, '❓')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(f"{emoji} Cenário", scenario)

    with col2:
        st.metric("Disponibilidade", f"{availability_pct:.1f}%")

    with col3:
        st.metric("CH₄ Potencial", f"{ch4_potential:.1f} Mi Nm³")

    with col4:
        if electricity_gwh:
            st.metric("Eletricidade", f"{electricity_gwh:.2f} GWh")
