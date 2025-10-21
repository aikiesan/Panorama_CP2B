"""
Page 4: Análise de Setores - Phase 4 Sector Analysis
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Features:
- Sector potential comparison
- Sector contribution to total biogas
- Electricity generation by sector
- Top residues by sector
"""

import streamlit as st
from src.ui.sector_analysis import (
    render_full_sector_dashboard,
    render_sector_potential_pie,
    render_sector_comparison_bars,
    render_sector_metrics,
    render_sector_top_residues,
    render_scenario_comparison_all_sectors,
    render_sector_electricity_potential,
    get_sector_statistics
)
from src.ui.main_navigation import render_main_navigation, render_navigation_divider

# Import Phase 5 SAF helpers
from src.utils.saf_helpers import (
    get_high_priority_residues,
    get_viable_residues,
    get_saf_tier_color,
    PRIORITY_COLORS
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Análise de Setores - CP2B",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render page header"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🏭 Análise de Setores
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Potencial de Biogás por Setor Econômico
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            🌾 Agricultura • 🐄 Pecuária • 🏙️ Urbano • 🏭 Industrial
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

def render_sidebar_controls():
    """Render sidebar controls"""
    with st.sidebar:
        st.markdown("### 🎭 Cenário")

        scenario_options = ["Pessimista", "Realista", "Otimista", "Teórico (100%)"]
        selected_scenario = st.radio(
            "Escolha o cenário:",
            options=scenario_options,
            index=1,  # Default to Realista
            key="sector_scenario",
            help="Selecione o cenário para análise de setores"
        )

        st.markdown("---")
        st.markdown("### 🎯 Filtro de SAF (Disponibilidade Real)")

        saf_threshold = st.slider(
            "Threshold mínimo de SAF (%):",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0,
            key="sector_saf_threshold",
            help="Mostrar apenas resíduos com SAF acima deste valor"
        )

        return selected_scenario, saf_threshold


# ============================================================================
# MAIN CONTENT
# ============================================================================

def main():
    """Main page render"""

    # Header
    render_header()

    # Main navigation bar
    render_main_navigation(current_page="setores")
    render_navigation_divider()

    # Sidebar controls
    selected_scenario, saf_threshold = render_sidebar_controls()

    # CRITICAL WARNING - Data being recalculated
    st.warning("""
    ⚠️ **ATENÇÃO: Dados em Recálculo**

    Esta página apresenta valores que estão sendo recalculados com a **fórmula SAF corrigida**.

    **Situação atual:**
    - ✅ **Páginas 1 (Disponibilidade) e 2 (Parâmetros Químicos)**: Atualizadas com valores corretos do banco de dados
    - ⏳ **Esta página**: Em processo de migração para o banco de dados atualizado

    **O que mudou:**
    - Fórmula antiga: `SAF = FC × (1-FCp) × FS × FL` ❌
    - Fórmula correta: `SAF = FC × FCp × FS × FL` ✅
    - FCp agora representa % DISPONÍVEL (não % competindo)

    **Impacto:** Os valores mostrados podem estar inflados em 3x-13x. Utilize as Páginas 1 e 2 para dados validados.

    📊 Página será atualizada em breve com dados corretos do banco de dados.
    """)

    # Display SAF filter info
    if saf_threshold > 0:
        st.info(f"📊 Filtrando resíduos com SAF >= {saf_threshold:.1f}%")

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Setorial",
        "🔄 Comparação de Cenários",
        "📈 Análise de Eletricidade",
        "ℹ️ Metodologia"
    ])

    # ========================================================================
    # TAB 1: SECTOR DASHBOARD
    # ========================================================================

    with tab1:
        render_full_sector_dashboard(selected_scenario)

    # ========================================================================
    # TAB 2: SCENARIO COMPARISON
    # ========================================================================

    with tab2:
        st.markdown("## 🔄 Comparação entre Cenários por Setor")
        st.markdown("""
        Visualize como o potencial de cada setor varia com diferentes cenários.
        """)

        # Scenario selection
        col1, col2 = st.columns(2)

        with col1:
            scenario_1 = st.selectbox(
                "Primeiro Cenário:",
                options=["Pessimista", "Realista", "Otimista", "Teórico (100%)"],
                index=0,
                key="comparison_scenario_1"
            )

        with col2:
            scenario_2 = st.selectbox(
                "Segundo Cenário:",
                options=["Pessimista", "Realista", "Otimista", "Teórico (100%)"],
                index=1,
                key="comparison_scenario_2"
            )

        # Render comparison
        if scenario_1 != scenario_2:
            render_scenario_comparison_all_sectors(scenario_1, scenario_2)

            # Calculate differences
            st.markdown("### 📊 Análise de Diferenças")

            stats_1 = get_sector_statistics(scenario_1)
            stats_2 = get_sector_statistics(scenario_2)

            diff_data = []
            for sector in ["Agricultura", "Pecuária", "Urbano", "Industrial"]:
                potential_1 = stats_1[sector]['total_ch4']
                potential_2 = stats_2[sector]['total_ch4']
                difference = potential_2 - potential_1
                percentage_change = (difference / potential_1 * 100) if potential_1 > 0 else 0

                diff_data.append({
                    'Setor': sector,
                    f'{scenario_1}': f"{potential_1:,.0f}",
                    f'{scenario_2}': f"{potential_2:,.0f}",
                    'Diferença': f"{difference:+,.0f}",
                    'Variação': f"{percentage_change:+.1f}%"
                })

            import pandas as pd
            df_diff = pd.DataFrame(diff_data)

            st.dataframe(
                df_diff,
                use_container_width=True,
                hide_index=True,
                column_config={k: st.column_config.TextColumn(width='medium') for k in df_diff.columns}
            )

        else:
            st.warning("Selecione dois cenários diferentes para comparação")

    # ========================================================================
    # TAB 3: ELECTRICITY ANALYSIS
    # ========================================================================

    with tab3:
        st.markdown("## ⚡ Potencial de Geração Elétrica")
        st.markdown("""
        Análise do potencial de eletricidade que pode ser gerada a partir do biogás em cada setor.
        """)

        render_sector_electricity_potential(selected_scenario, key_suffix="_tab3")

        # Electricity statistics
        st.markdown("### 📊 Estatísticas de Eletricidade")

        stats = get_sector_statistics(selected_scenario)

        # Calculate electricity
        electricity_data = []
        total_gwh = 0

        for sector_name, sector_stats in stats.items():
            ch4_million = sector_stats['total_ch4']
            gwh = (ch4_million * 1_000_000 * 1.43) / 1_000_000
            total_gwh += gwh

            electricity_data.append({
                'Setor': sector_name,
                'Potencial GWh/ano': f"{gwh:.1f}",
                'Casas Alimentadas': f"{int(gwh * 1000 / 0.21):,}",  # ~0.21 MWh per household per year
                'Percentual': 'Calc'  # Will be calculated below
            })

        # Add percentages
        for row in electricity_data:
            gwh_val = float(row['Potencial GWh/ano'])
            percentage = (gwh_val / total_gwh * 100) if total_gwh > 0 else 0
            row['Percentual'] = f"{percentage:.1f}%"

        import pandas as pd
        df_electricity = pd.DataFrame(electricity_data)

        st.dataframe(
            df_electricity,
            use_container_width=True,
            hide_index=True,
            column_config={k: st.column_config.TextColumn(width='medium') for k in df_electricity.columns}
        )

        st.divider()

        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Potencial Total", f"{total_gwh:,.0f} GWh/ano")

        with col2:
            households = int(total_gwh * 1000 / 0.21)
            st.metric("Casas Alimentadas", f"{households:,}")

        with col3:
            # Comparison with São Paulo state consumption
            # SP consumes ~150 TWh/year
            percentage_sp = (total_gwh / 150000 * 100)
            st.metric("% do Consumo SP", f"{percentage_sp:.2f}%")

        with col4:
            # CO₂ equivalent savings
            # 1 MWh avoids ~0.5 tons CO₂
            co2_avoided = total_gwh * 1000 * 0.5 / 1000  # in thousand tons
            st.metric("CO₂ Evitado", f"{co2_avoided:,.0f} Kt/ano")

        st.markdown("""
        **Nota:** Cálculos baseados em:
        - 1 Nm³ CH₄ ≈ 1 kWh (40% eficiência do motor)
        - Consumo residencial médio SP: ~2.1 MWh/ano por domicílio
        - Fator de emissão: ~0.5 ton CO₂/MWh evitado
        """)

    # ========================================================================
    # TAB 4: METHODOLOGY
    # ========================================================================

    with tab4:
        st.markdown("## ℹ️ Metodologia de Análise de Setores")

        st.markdown("""
        ### Estrutura de Setores

        A análise agrupa os resíduos em 4 setores principais:

        | Setor | Descrição | Exemplos |
        |-------|-----------|----------|
        | 🌾 **Agricultura** | Resíduos agrícolas e agroindustriais | Palha, Bagaço, Vinhaça |
        | 🐄 **Pecuária** | Dejetos animais e resíduos pecuários | Bovinos, Suínos, Aves |
        | 🏙️ **Urbano** | Resíduos sólidos urbanos | RSU, Podas, Lodo de esgoto |
        | 🏭 **Industrial** | Efluentes e resíduos industriais | Soro de Laticínios, Cervejarias |

        ### Cálculo de Potencial Setorial

        O potencial total de um setor é calculado como:

        ```
        Potencial Setor = Σ (Potencial Resíduo)
        ```

        Para cada resíduo:
        ```
        Potencial Resíduo = Geração × BMP × Disponibilidade Final
        ```

        ### Conversão para Eletricidade

        A conversão de biogás para energia elétrica usa o fator:

        ```
        Eletricidade (GWh) = Biogás (Mi m³) × 1.43

        Onde:
        - 1 Nm³ CH₄ ≈ 1 kWh (40% eficiência de motor)
        - 1 Mi m³ = 1.000.000 Nm³
        - 1 GWh = 1.000 MWh = 1.000.000 kWh
        ```

        ### Potencial de Geração

        - **Potencial Total:** Soma de todos os resíduos nos 4 cenários
        - **Distribuição:** Percentual do potencial total por setor
        - **Residências:** Casas que poderiam ser alimentadas (consumo médio: 2.1 MWh/ano)

        ### Impacto Ambiental

        Cada MWh de eletricidade gerada por biogás evita aproximadamente:
        - 0.5 ton CO₂ (comparado à eletricidade média da rede)
        - Redução de 30-40% na emissão de metano do resíduo

        ### Limitações da Análise

        1. **Dados Incompletos:** Alguns resíduos têm cenários estimados
        2. **Cenário Teórico:** 100% é referência apenas, não viável na prática
        3. **Infraestrutura:** Assume desenvolvimento de biodigestores
        4. **Logística:** Pressupostos sobre raios de coleta e transporte
        """)

        st.divider()

        st.markdown("### 📚 Referências")

        st.markdown("""
        - ABNT NBR 15808:2020 - Produção de biogás
        - CETESB NP 4231 - Normas para vinhaça
        - Embrapa - Atlas de Biomassa Residual
        - IPCC AR6 - Fatores de emissão
        """)


if __name__ == "__main__":
    main()
