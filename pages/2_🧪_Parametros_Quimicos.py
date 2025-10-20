"""
Page 2: Parâmetros Químicos e Operacionais
CP2B - Chemical composition analysis with literature ranges
"""

import streamlit as st
import pandas as pd

from src.data.residue_registry import (
    get_available_residues,
    get_residue_data,
    get_residue_icon
)
from src.ui.tabs import render_sector_tabs
from src.ui.horizontal_nav import render_horizontal_nav
from src.ui.main_navigation import render_main_navigation, render_navigation_divider


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Parâmetros Químicos - CP2B",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render header for chemical parameters page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🧪 Parâmetros Químicos e Operacionais
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Composição Química • BMP • Parâmetros Operacionais
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Valores de Literatura • 📈 Ranges Validados • ⚗️ Metodologia Conservadora
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CHEMICAL PARAMETERS DISPLAY WITH RANGES
# ============================================================================

def render_chemical_parameters_table(chemical_params):
    """Display chemical parameters in table format with MIN/MEAN/MAX"""
    st.markdown("### 🧬 Parâmetros de Composição (Literatura Validada)")

    st.info("""
    **📊 Como interpretar a tabela:**
    - **Mínimo**: Valor mínimo encontrado na literatura revisada
    - **Média/Valor**: Valor conservador adotado no CP2B (baseado em média ponderada)
    - **Máximo**: Valor máximo encontrado na literatura revisada
    - **Unidade**: Unidade de medida do parâmetro
    """)

    # Get table data from the model
    ranges_data = chemical_params.to_range_table()

    if ranges_data:
        df = pd.DataFrame(ranges_data)

        # Style the dataframe
        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            height=500,
            column_config={
                "Parâmetro": st.column_config.TextColumn("Parâmetro", width="medium"),
                "Mínimo": st.column_config.TextColumn("Mínimo", width="small"),
                "Média/Valor": st.column_config.TextColumn("Média/Valor ✅", width="small"),
                "Máximo": st.column_config.TextColumn("Máximo", width="small"),
                "Unidade": st.column_config.TextColumn("Unidade", width="small"),
            }
        )

        # Show key metrics in columns
        st.markdown("#### 📌 Destaques")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💨 BMP",
                f"{chemical_params.bmp:.2f}",
                help=f"Potencial Metanogênico\n{chemical_params.bmp_unit}"
            )
            st.caption(chemical_params.bmp_unit)

        with col2:
            st.metric(
                "💧 Umidade",
                f"{chemical_params.moisture:.1f}%",
                help="Conteúdo de umidade do resíduo"
            )

        with col3:
            st.metric(
                "📦 Sólidos Totais",
                f"{chemical_params.ts:.1f}%",
                help="Total de sólidos (base úmida)"
            )

        with col4:
            st.metric(
                "🔥 Sólidos Voláteis",
                f"{chemical_params.vs:.1f}%",
                help=f"Fração volátil\n{chemical_params.vs_basis}"
            )
    else:
        st.warning("Nenhum dado de composição química disponível")


# ============================================================================
# OPERATIONAL PARAMETERS DISPLAY WITH RANGES
# ============================================================================

def render_operational_parameters_table(operational):
    """Display operational parameters in table format with MIN/MEAN/MAX"""
    st.markdown("### 🔧 Parâmetros Operacionais para Biodigestão")

    st.info("""
    **⚗️ Parâmetros recomendados para operação de biodigestores anaeróbios:**
    - **Mínimo/Máximo**: Limites operacionais encontrados na literatura
    - **Valor Operacional**: Condição ótima recomendada para este resíduo
    """)

    # Get table data from the model
    ranges_data = operational.to_range_table()

    if ranges_data:
        df = pd.DataFrame(ranges_data)

        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            height=300,
            column_config={
                "Parâmetro": st.column_config.TextColumn("Parâmetro", width="medium"),
                "Mínimo": st.column_config.TextColumn("Mínimo", width="small"),
                "Valor Operacional": st.column_config.TextColumn("Valor Operacional ✅", width="medium"),
                "Máximo": st.column_config.TextColumn("Máximo", width="small"),
            }
        )

        # Show key operational metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⏱️ TRH",
                operational.hrt,
                help="Tempo de Retenção Hidráulica"
            )

        with col2:
            st.metric(
                "🌡️ Temperatura",
                operational.temperature,
                help="Temperatura operacional do biodigestor"
            )

        with col3:
            if operational.reactor_type:
                st.metric(
                    "⚗️ Tipo de Reator",
                    operational.reactor_type,
                    help="Configuração recomendada"
                )
    else:
        st.warning("Nenhum parâmetro operacional disponível")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function"""
    render_header()

    # Main navigation bar
    render_main_navigation(current_page="parametros")
    render_navigation_divider()

    # Horizontal navigation tabs
    render_horizontal_nav("Parametros")

    # Simple tab navigation (replaces complex cards)
    selected_sector, selected_residue = render_sector_tabs(key_prefix="parametros")

    if not selected_residue:
        st.info("👆 Selecione um setor e resíduo acima para visualizar os dados")

        # Show instructions
        st.markdown("---")
        st.markdown("### 📚 Sobre os Parâmetros Químicos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🧬 Composição Química

            A composição química é fundamental para entender o potencial de produção de biogás de cada resíduo.

            **Parâmetros principais:**
            - **BMP** (Biochemical Methane Potential): Potencial metanogênico
            - **ST/SV** (Sólidos Totais/Voláteis): Conteúdo orgânico
            - **C:N** (Relação Carbono:Nitrogênio): Equilíbrio nutricional
            - **Nutrientes** (N, P, K): Composição do biofertilizante

            Os valores apresentados são baseados em **revisão sistemática da literatura científica**,
            com foco em estudos brasileiros e contexto tropical.
            """)

        with col2:
            st.markdown("""
            #### 🔧 Parâmetros Operacionais

            Os parâmetros operacionais definem as condições ótimas para biodigestão.

            **Principais parâmetros:**
            - **TRH**: Tempo de Retenção Hidráulica (dias)
            - **Temperatura**: Mesofílico (30-37°C) ou Termofílico (50-60°C)
            - **TCO**: Taxa de Carga Orgânica (kg SV/m³/dia)
            - **Tipo de Reator**: CSTR, UASB, Batch, etc.

            **📊 Ranges MIN/MEAN/MAX:**
            Os ranges mostram a variabilidade encontrada na literatura, permitindo
            entender a robustez do processo e adaptar para condições locais.
            """)

        st.markdown("---")
        st.markdown("### 🔬 Validação Laboratorial")

        st.info("""
        **Tem dados de laboratório?** Use a **[Ferramenta de Comparação Laboratorial](/🔬_Comparacao_Laboratorial)**
        para validar seus resultados comparando com os valores de referência da literatura!

        A ferramenta calcula desvios automaticamente e indica se seus dados estão dentro da faixa esperada.
        """)

        return

    st.markdown("---")

    # Load residue data
    residue_data = get_residue_data(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados")
        return

    # Render all sections
    render_chemical_parameters_table(residue_data.chemical_params)

    st.markdown("---")

    render_operational_parameters_table(residue_data.operational)

    st.markdown("---")

    # Link to lab comparison tool
    st.markdown("### 🔬 Próximo Passo: Validação Laboratorial")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if st.button("🔬 Ir para Comparação Laboratorial", width="stretch", type="primary"):
            st.switch_page("pages/4_🔬_Comparacao_Laboratorial.py")

    st.info("💡 **Dica:** Use a ferramenta de comparação laboratorial para validar seus dados experimentais com os valores de referência apresentados acima!")


if __name__ == "__main__":
    main()
