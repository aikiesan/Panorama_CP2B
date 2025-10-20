"""
Page 3: Análise Comparativa - Phase 4 Enhanced Analytics
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Features:
- Top residues ranking
- Residue potential vs availability analysis
- Scenario progression comparison
- Multi-residue comparison tool
"""

import streamlit as st
from src.ui.comparative_analysis import (
    render_comparative_analysis_dashboard,
    render_scenario_progression,
    render_residue_comparison,
    get_top_residues
)
from src.data.residue_registry import get_available_residues

# Import Phase 5 SAF helpers
from src.utils.saf_helpers import (
    sort_residues_by_saf,
    get_saf_tier_color,
    create_saf_badge,
    PRIORITY_COLORS
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Análise Comparativa - CP2B",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render page header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #ec4899 50%, #f59e0b 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            📈 Análise Comparativa de Resíduos
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Ranking, Comparações e Análises Avançadas
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Top Resíduos • 🔍 Potencial vs Disponibilidade • 🎯 Comparação Cenários
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

def render_sidebar_controls():
    """Render sidebar scenario selector and SAF priority filter"""
    with st.sidebar:
        st.markdown("### 🎭 Cenário")

        scenario_options = ["Pessimista", "Realista", "Otimista", "Teórico (100%)"]
        selected_scenario = st.radio(
            "Escolha o cenário:",
            options=scenario_options,
            index=1,  # Default to Realista
            key="comparative_scenario",
            help="Selecione o cenário para análise"
        )

        st.markdown("---")
        st.markdown("### 🚀 Filtro por Prioridade (SAF)")

        priority_options = ["All", "EXCEPCIONAL", "EXCELENTE", "MUITO BOM", "BOM", "RAZOÁVEL", "REGULAR", "BAIXO", "CRÍTICO", "INVIÁVEL"]
        selected_priority = st.selectbox(
            "Filtrar por tier de prioridade:",
            options=priority_options,
            index=0,
            key="comparative_priority",
            help="Filtrar resíduos por nível de prioridade SAF"
        )

        return selected_scenario, selected_priority


# ============================================================================
# MAIN CONTENT
# ============================================================================

def main():
    """Main page render"""

    # Header
    render_header()

    # Sidebar controls
    selected_scenario, selected_priority = render_sidebar_controls()

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Dashboard Comparativo",
        "📊 Progressão de Cenários",
        "🔄 Comparar Resíduos",
        "ℹ️ Metodologia"
    ])

    # ========================================================================
    # TAB 1: COMPARATIVE ANALYSIS DASHBOARD
    # ========================================================================

    with tab1:
        render_comparative_analysis_dashboard(selected_scenario)

    # ========================================================================
    # TAB 2: SCENARIO PROGRESSION
    # ========================================================================

    with tab2:
        st.markdown("## 📊 Progressão de Cenários por Resíduo")
        st.markdown("""
        Visualize como o potencial de um resíduo varia nos diferentes cenários de disponibilidade.
        """)

        # Residue selector
        available_residues = get_available_residues()
        selected_residue = st.selectbox(
            "Selecione um resíduo para análise:",
            options=available_residues,
            key="scenario_progression_selector",
            help="Escolha um resíduo para ver a progressão entre cenários"
        )

        if selected_residue:
            render_scenario_progression(selected_residue)

            # Add explanation
            st.markdown("### 📝 Interpretação")
            st.info("""
            A progressão entre cenários mostra:
            - **Pessimista:** Menor disponibilidade (fatores de competição altos)
            - **Realista:** Cenário intermediário com pressupostos conservadores
            - **Otimista:** Maior disponibilidade com melhor infraestrutura
            - **Teórico (100%):** Potencial máximo teórico sem restrições
            """)

    # ========================================================================
    # TAB 3: RESIDUE COMPARISON TOOL
    # ========================================================================

    with tab3:
        st.markdown("## 🔄 Ferramenta de Comparação de Resíduos")
        st.markdown("""
        Selecione múltiplos resíduos para comparação lado a lado.
        """)

        # Multi-select for residues
        available_residues = get_available_residues()
        selected_residues = st.multiselect(
            "Selecione resíduos para comparar (máximo 5):",
            options=available_residues,
            max_selections=5,
            key="residue_comparison_selector",
            help="Escolha até 5 resíduos para comparação detalhada"
        )

        if selected_residues:
            render_residue_comparison(selected_residues, selected_scenario)
        else:
            st.info("Selecione pelo menos um resíduo para começar a comparação")

    # ========================================================================
    # TAB 4: METHODOLOGY
    # ========================================================================

    with tab4:
        st.markdown("## ℹ️ Metodologia de Análise")

        st.markdown("""
        ### Ranking de Resíduos

        Os resíduos são classificados pelo seu **potencial de biogás** no cenário selecionado.

        O potencial é calculado como:
        ```
        Potencial (Mi m³/ano) = Geração (ton/ano) × BMP (m³/ton) × Disponibilidade Final (%)
        ```

        ### Disponibilidade Final

        A disponibilidade é determinada por:
        ```
        Disponibilidade = FC × (1 - FCp) × FS × FL × 100%
        ```

        Onde:
        - **FC:** Fator de Coleta (infraestrutura)
        - **FCp:** Fator de Competição
        - **FS:** Fator de Sazonalidade
        - **FL:** Fator de Logística

        ### Cenários

        - **Pessimista:** Fatores conservadores, restrições significativas
        - **Realista:** Pressupostos equilibrados, estado atual de desenvolvimento
        - **Otimista:** Cenário com melhorias de infraestrutura
        - **Teórico (100%):** Potencial máximo sem restrições (referência apenas)

        ### Potencial Elétrico

        Conversão de biogás para eletricidade:
        ```
        Eletricidade (GWh/ano) = CH₄ (Mi m³/ano) × 1.43
        ```

        Com base em 1 Nm³ CH₄ ≈ 1 kWh eletricidade (40% eficiência de motor)
        """)

        st.markdown("---")

        st.markdown("""
        ### Interpretação dos Gráficos

        **Potencial vs Disponibilidade:**
        - Bolhas maiores = maior potencial
        - Posição horizontal = disponibilidade final
        - Posição vertical = potencial de biogás
        - Resíduos no canto superior direito são ideais (alto potencial + alta disponibilidade)

        **Progressão de Cenários:**
        - Mostra como o potencial varia com os pressupostos
        - Inclinação acentuada = sensibilidade a fatores de disponibilidade
        - Linha plana = resíduo pouco sensível a mudanças de cenário
        """)

        st.divider()

        st.markdown("### Dados Utilizados")

        # Show data summary
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            residues_count = len(available_residues)
            st.metric("Total de Resíduos", residues_count)

        with col2:
            st.metric("Setores", 4)

        with col3:
            st.metric("Cenários", 4)

        with col4:
            st.metric("Data da Análise", "2025-10-17")

        st.caption("""
        Análise baseada em dados da CP2B com 43 resíduos catalogados
        e validação científica de 100+ referências bibliográficas.
        """)


if __name__ == "__main__":
    main()
