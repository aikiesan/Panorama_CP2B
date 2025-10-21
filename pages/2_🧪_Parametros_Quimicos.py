"""
Page 2: Parâmetros Químicos e Operacionais
CP2B - Chemical composition analysis with literature ranges
DATABASE INTEGRATED - Phase 1.1 Complete
"""

import streamlit as st
import pandas as pd

# Database integration (replaces residue_registry)
from src.data_handler import (
    get_all_residues_with_params,
    get_residue_by_name,
    get_residues_for_dropdown,
    load_residue_from_db
)

# New visualization components
from src.ui.chart_components import (
    create_bmp_comparison_bar,
    create_parameter_boxplot
)

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
            📊 Valores de Literatura • 📈 Ranges Validados • ⚗️ Metodologia Conservadora • 🗄️ Database Integrado
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# DATABASE-DRIVEN DROPDOWN SELECTOR
# ============================================================================

def render_hierarchical_residue_selector():
    """Render 3-level hierarchical selector: Setor → Subsetor → Resíduo"""
    from src.data.hierarchy_helper import HierarchyHelper

    st.markdown("### 🎯 Selecione o Resíduo")

    helper = HierarchyHelper()
    tree = helper.get_hierarchy_tree()

    col1, col2, col3 = st.columns(3)

    with col1:
        setor_options = []
        setor_labels = []

        for setor_cod, setor_data in tree.items():
            setor_options.append(setor_cod)
            setor_labels.append(f"{setor_data['emoji']} {setor_data['nome']}")

        selected_setor_idx = st.selectbox(
            "Setor:",
            range(len(setor_options)),
            format_func=lambda x: setor_labels[x],
            key="parametros_setor_selector"
        )

        selected_setor = setor_options[selected_setor_idx]

    with col2:
        subsetor_options = []
        subsetor_labels = []

        for subsetor_cod, subsetor_data in tree[selected_setor]['subsetores'].items():
            subsetor_options.append(subsetor_cod)
            residuo_count = len(subsetor_data['residuos'])
            subsetor_labels.append(f"{subsetor_data['nome']} ({residuo_count})")

        selected_subsetor_idx = st.selectbox(
            "Subsetor:",
            range(len(subsetor_options)),
            format_func=lambda x: subsetor_labels[x],
            key="parametros_subsetor_selector"
        )

        selected_subsetor = subsetor_options[selected_subsetor_idx]

    with col3:
        residuos = tree[selected_setor]['subsetores'][selected_subsetor]['residuos']

        residuo_options = [r['codigo'] for r in residuos]
        residuo_labels = [r['nome'] for r in residuos]

        selected_residuo_idx = st.selectbox(
            "Resíduo:",
            range(len(residuo_options)),
            format_func=lambda x: residuo_labels[x],
            key="parametros_residuo_selector"
        )

        selected_residuo_codigo = residuo_options[selected_residuo_idx]

    # Load full residue data from database using codigo
    residue_data = load_residue_from_db(selected_residuo_codigo)

    return residue_data



# ============================================================================
# CHEMICAL PARAMETERS DISPLAY (FROM DATABASE)
# ============================================================================

def render_chemical_parameters_from_db(residue_data):
    """Display chemical parameters from database dict structure"""
    st.markdown("### 🧬 Parâmetros de Composição (Literatura Validada)")

    st.info("""
    **📊 Como interpretar a tabela:**
    - **Mínimo**: Valor mínimo encontrado na literatura revisada
    - **Média/Valor**: Valor conservador adotado no CP2B (baseado em média ponderada)
    - **Máximo**: Valor máximo encontrado na literatura revisada
    - **Unidade**: Unidade de medida do parâmetro
    """)

    # Build table from database columns
    params_data = []

    # BMP
    params_data.append({
        "Parâmetro": "BMP (Potencial Metanogênico)",
        "Mínimo": f"{residue_data.get('bmp_min', 0):.1f}" if pd.notna(residue_data.get('bmp_min')) else "N/A",
        "Média/Valor": f"{residue_data.get('bmp_medio', 0):.1f}",
        "Máximo": f"{residue_data.get('bmp_max', 0):.1f}" if pd.notna(residue_data.get('bmp_max')) else "N/A",
        "Unidade": "mL CH₄/g VS"
    })

    # TS (Sólidos Totais)
    params_data.append({
        "Parâmetro": "TS (Sólidos Totais)",
        "Mínimo": f"{residue_data.get('ts_min', 0):.1f}" if pd.notna(residue_data.get('ts_min')) else "N/A",
        "Média/Valor": f"{residue_data.get('ts_medio', 0):.1f}",
        "Máximo": f"{residue_data.get('ts_max', 0):.1f}" if pd.notna(residue_data.get('ts_max')) else "N/A",
        "Unidade": "%"
    })

    # VS (Sólidos Voláteis)
    params_data.append({
        "Parâmetro": "VS (Sólidos Voláteis)",
        "Mínimo": f"{residue_data.get('vs_min', 0):.1f}" if pd.notna(residue_data.get('vs_min')) else "N/A",
        "Média/Valor": f"{residue_data.get('vs_medio', 0):.1f}",
        "Máximo": f"{residue_data.get('vs_max', 0):.1f}" if pd.notna(residue_data.get('vs_max')) else "N/A",
        "Unidade": "% (base TS)"
    })

    df = pd.DataFrame(params_data)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=200,
        column_config={
            "Parâmetro": st.column_config.TextColumn("Parâmetro", width="large"),
            "Mínimo": st.column_config.TextColumn("Mínimo", width="small"),
            "Média/Valor": st.column_config.TextColumn("Média/Valor ✅", width="small"),
            "Máximo": st.column_config.TextColumn("Máximo", width="small"),
            "Unidade": st.column_config.TextColumn("Unidade", width="medium"),
        }
    )

    # Key metrics
    st.markdown("#### 📌 Destaques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        bmp_value = residue_data.get('bmp_medio', 0)
        st.metric(
            "💨 BMP",
            f"{bmp_value:.1f}",
            help="Potencial Metanogênico\nmL CH₄/g VS"
        )
        st.caption("mL CH₄/g VS")

    with col2:
        ts_value = residue_data.get('ts_medio', 0)
        moisture = 100 - ts_value if ts_value > 0 else 0
        st.metric(
            "💧 Umidade",
            f"{moisture:.1f}%",
            help="Conteúdo de umidade do resíduo"
        )

    with col3:
        st.metric(
            "📦 Sólidos Totais",
            f"{ts_value:.1f}%",
            help="Total de sólidos (base úmida)"
        )

    with col4:
        vs_value = residue_data.get('vs_medio', 0)
        st.metric(
            "🔥 Sólidos Voláteis",
            f"{vs_value:.1f}%",
            help="Fração volátil (base TS)"
        )


# ============================================================================
# AVAILABILITY FACTORS DISPLAY
# ============================================================================

def render_availability_factors(residue_data):
    """Display availability factors from database"""
    st.markdown("### 📊 Fatores de Disponibilidade (SAF)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fc = residue_data.get('fc_medio', 0)
        st.metric("FC (Coleta)", f"{fc:.0%}", help="Fator de Coleta")

    with col2:
        fcp = residue_data.get('fcp_medio', 0)
        st.metric("FCp (Competição)", f"{fcp:.0%}", help="Fator de Competição")

    with col3:
        fs = residue_data.get('fs_medio', 0)
        st.metric("FS (Sazonalidade)", f"{fs:.0%}", help="Fator de Sazonalidade")

    with col4:
        fl = residue_data.get('fl_medio', 0)
        st.metric("FL (Logística)", f"{fl:.0%}", help="Fator Logístico")

    # Calculate SAF (corrected formula - FCp = % available)
    from src.data_handler import calculate_saf
    saf = calculate_saf(fc, fcp, fs, fl)
    st.markdown(f"**Disponibilidade Final (SAF):** {saf:.1f}%")


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function - Database Integrated"""
    render_header()

    # Main navigation bar
    render_main_navigation(current_page="parametros")
    render_navigation_divider()

    # ========================================================================
    # SECTION 1: BMP COMPARISON CHART (ALL RESIDUES)
    # ========================================================================

    st.markdown("### 📊 Comparação de BMP - Todos os Resíduos")

    st.info("""
    **Visualização completa do banco de dados:** Todos os 38 resíduos catalogados com BMP validado.
    Cores indicam o setor: 🌾 Agricultura (verde), 🐄 Pecuária (laranja), 🏙️ Urbano (roxo), 🏭 Industrial (azul)
    """)

    try:
        df_all = get_all_residues_with_params()
        fig_bmp = create_bmp_comparison_bar(df_all)
        st.plotly_chart(fig_bmp, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar gráfico de comparação: {e}")

    st.markdown("---")

    # ========================================================================
    # SECTION 2: PARAMETER BOX PLOTS BY SECTOR
    # ========================================================================

    st.markdown("### 📈 Distribuição de Parâmetros por Setor")

    col1, col2, col3 = st.columns(3)

    try:
        df_all = get_all_residues_with_params()

        with col1:
            fig_bmp_box = create_parameter_boxplot(df_all, 'bmp', 'BMP', 'mL CH₄/g VS')
            st.plotly_chart(fig_bmp_box, use_container_width=True)

        with col2:
            fig_ts_box = create_parameter_boxplot(df_all, 'ts', 'Sólidos Totais', '%')
            st.plotly_chart(fig_ts_box, use_container_width=True)

        with col3:
            fig_vs_box = create_parameter_boxplot(df_all, 'vs', 'Sólidos Voláteis', '%')
            st.plotly_chart(fig_vs_box, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar box plots: {e}")

    st.markdown("---")

    # ========================================================================
    # SECTION 3: INDIVIDUAL RESIDUE SELECTION
    # ========================================================================

    # Selector returns full residue data dict
    residue_data = render_hierarchical_residue_selector()

    if not residue_data:
        st.info("👆 Selecione um setor e resíduo acima para visualizar os dados detalhados")

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
            #### 🗄️ Banco de Dados Integrado

            Esta página agora carrega dados diretamente do banco de dados validado:

            **Estatísticas:**
            - **38 resíduos** catalogados e validados
            - **100% completude** - todos os resíduos têm BMP > 0
            - **4 setores** (Agricultura, Pecuária, Urbano, Industrial)
            - **Ranges validados** (mín/médio/máx) da literatura

            **📊 Ranges MIN/MEAN/MAX:**
            Os ranges mostram a variabilidade encontrada na literatura, permitindo
            entender a robustez do processo e adaptar para condições locais.
            """)

        return

    st.markdown("---")

    # Data already loaded by selector - no need to load again!
    # residue_data is already a dict with all fields from database

    # Display residue info
    st.markdown(f"## {residue_data.get('nome', 'N/A')}")

    sector_names = {
        'AG_AGRICULTURA': '🌾 Agricultura',
        'PC_PECUARIA': '🐄 Pecuária',
        'UR_URBANO': '🏙️ Urbano',
        'IN_INDUSTRIAL': '🏭 Industrial'
    }

    st.markdown(f"**Setor:** {sector_names.get(residue_data.get('setor', ''), 'N/A')}")

    st.markdown("---")

    # Render all sections
    render_chemical_parameters_from_db(residue_data)

    st.markdown("---")

    render_availability_factors(residue_data)

    st.markdown("---")

    # Link to lab comparison tool
    st.markdown("### 🔬 Próximo Passo: Validação Laboratorial")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if st.button("🔬 Ir para Comparação Laboratorial", use_container_width=True, type="primary"):
            st.switch_page("pages/4_🔬_Comparacao_Laboratorial.py")

    st.info("💡 **Dica:** Use a ferramenta de comparação laboratorial para validar seus dados experimentais com os valores de referência apresentados acima!")


if __name__ == "__main__":
    main()
