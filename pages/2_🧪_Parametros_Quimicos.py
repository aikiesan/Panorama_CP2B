"""
Page 2: Parâmetros Químicos e Laboratoriais
CP2B - Chemical composition analysis and laboratory data comparison tool
"""

import streamlit as st
import pandas as pd
from datetime import date

from src.research_data import (
    get_available_residues,
    get_residue_data,
    get_residue_icon
)
from src.ui_components import render_full_selector
from src.lab_comparison import (
    LabComparison,
    initialize_lab_session,
    save_lab_result,
    get_lab_results,
    clear_lab_results,
    export_comparison_report
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Parâmetros Químicos - CP2B",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize lab session
initialize_lab_session()


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
            🧪 Parâmetros Químicos e Laboratoriais
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Composição Química • BMP • Validação Laboratorial
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Referências Literatura • 🔬 Dados Lab • ⚗️ Comparação • 📈 Validação
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CHEMICAL PARAMETERS DISPLAY
# ============================================================================

def render_chemical_parameters(chemical_params):
    """Display all chemical parameters"""
    st.markdown("### 📊 Composição Química (Dados de Literatura)")

    # Main chemical parameters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💨 BMP",
            f"{chemical_params.bmp:.1f}",
            help=f"Potencial Metanogênico Bioquímico\nUnidade: {chemical_params.bmp_unit}"
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
            "📦 Sólidos Totais (TS)",
            f"{chemical_params.ts:.1f}%",
            help="Total de sólidos no resíduo (base úmida)"
        )

    with col4:
        st.metric(
            "🔥 Sólidos Voláteis (VS)",
            f"{chemical_params.vs:.1f}%",
            help=f"Fração volátil dos sólidos\nBase: {chemical_params.vs_basis}"
        )

    st.markdown("---")

    # Additional parameters in expandable sections
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🧬 Parâmetros de Composição", expanded=True):
            params_dict = {}

            if chemical_params.cn_ratio:
                params_dict['Relação C:N'] = f"{chemical_params.cn_ratio:.2f}"
            if chemical_params.carbon:
                params_dict['Carbono (C)'] = f"{chemical_params.carbon:.2f}%"
            if chemical_params.nitrogen:
                params_dict['Nitrogênio (N)'] = f"{chemical_params.nitrogen:.2f}%"
            if chemical_params.phosphorus:
                params_dict['Fósforo (P₂O₅)'] = f"{chemical_params.phosphorus:.2f}%"
            if chemical_params.potassium:
                params_dict['Potássio (K₂O)'] = f"{chemical_params.potassium:.2f}%"
            if chemical_params.protein:
                params_dict['Proteína'] = f"{chemical_params.protein:.2f}%"

            df_comp = pd.DataFrame([
                {'Parâmetro': k, 'Valor': v} for k, v in params_dict.items()
            ])

            st.dataframe(df_comp, hide_index=True, use_container_width=True)

    with col2:
        with st.expander("⚗️ Parâmetros Operacionais", expanded=True):
            params_dict = {}

            if chemical_params.ph:
                params_dict['pH'] = f"{chemical_params.ph:.2f}"
            if chemical_params.cod:
                params_dict['DQO'] = f"{chemical_params.cod:.0f} mg/L"
            if chemical_params.ch4_content:
                params_dict['Conteúdo CH₄'] = f"{chemical_params.ch4_content:.1f}%"
            if chemical_params.toc:
                params_dict['COT (Carbono Orgânico Total)'] = f"{chemical_params.toc:.2f}%"

            df_oper = pd.DataFrame([
                {'Parâmetro': k, 'Valor': v} for k, v in params_dict.items()
            ])

            st.dataframe(df_oper, hide_index=True, use_container_width=True)


# ============================================================================
# OPERATIONAL PARAMETERS
# ============================================================================

def render_operational_parameters(operational):
    """Display operational parameters for AD"""
    st.markdown("### 🔧 Parâmetros Operacionais para Biodigestão")

    oper_dict = operational.to_dict()

    df_oper = pd.DataFrame([
        {'Parâmetro': k, 'Valor': v} for k, v in oper_dict.items()
    ])

    st.dataframe(df_oper, hide_index=True, use_container_width=True)


# ============================================================================
# LAB DATA INPUT TOOL
# ============================================================================

def render_lab_input_tool(residue_name, residue_data):
    """Render laboratory data input and comparison tool"""
    st.markdown("### 🔬 Ferramenta de Comparação Laboratorial")

    st.info("""
    **💡 Como usar:**
    1. Insira os valores medidos em laboratório nos campos abaixo
    2. Compare automaticamente com os valores de referência da literatura
    3. Verifique o status de validação (✅ Dentro da faixa / ⚠️ Desvio / ❌ Fora da faixa)
    4. Exporte o relatório de comparação
    """)

    # Input form
    with st.form(key='lab_input_form'):
        st.markdown("#### 📝 Inserir Dados Laboratoriais")

        col1, col2, col3 = st.columns(3)

        lab_data = {}

        with col1:
            lab_data['bmp'] = st.number_input(
                "BMP (m³ CH₄/kg VS)",
                min_value=0.0,
                value=0.0,
                step=0.1,
                help="Potencial Metanogênico Bioquímico"
            )

            lab_data['ts'] = st.number_input(
                "Sólidos Totais (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

            lab_data['vs'] = st.number_input(
                "Sólidos Voláteis (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

        with col2:
            lab_data['moisture'] = st.number_input(
                "Umidade (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

            lab_data['cn_ratio'] = st.number_input(
                "Relação C:N",
                min_value=0.0,
                value=0.0,
                step=0.1
            )

            lab_data['ph'] = st.number_input(
                "pH",
                min_value=0.0,
                max_value=14.0,
                value=0.0,
                step=0.1
            )

        with col3:
            lab_data['nitrogen'] = st.number_input(
                "Nitrogênio (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

            lab_data['carbon'] = st.number_input(
                "Carbono (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

            lab_data['ch4_content'] = st.number_input(
                "Conteúdo CH₄ (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1
            )

        # Metadata
        st.markdown("#### 📋 Metadados (Opcional)")
        col1, col2 = st.columns(2)

        with col1:
            lab_name = st.text_input("Nome do Laboratório")
            measurement_date = st.date_input("Data da Medição", value=date.today())

        with col2:
            operator = st.text_input("Responsável pela Análise")
            notes = st.text_area("Observações", height=80)

        submit_button = st.form_submit_button("🔍 Comparar com Referência")

    # Process form submission
    if submit_button:
        # Filter out zero values
        filtered_lab_data = {k: v for k, v in lab_data.items() if v > 0}

        if not filtered_lab_data:
            st.warning("⚠️ Por favor, insira pelo menos um valor para comparação")
            return

        # Save to session state
        for param, value in filtered_lab_data.items():
            save_lab_result(residue_name, param, value)

        st.session_state.lab_metadata = {
            'lab_name': lab_name,
            'measurement_date': str(measurement_date),
            'operator': operator,
            'notes': notes
        }

        st.success("✅ Dados laboratoriais salvos! Veja a comparação abaixo.")

    # Display comparison if data exists
    lab_results = get_lab_results(residue_name)

    if lab_results:
        st.markdown("---")
        st.markdown("### 📊 Resultado da Comparação")

        # Create comparison object
        comparator = LabComparison(residue_data)
        comparison_df = comparator.create_comparison_report(lab_results)

        # Display comparison table
        st.dataframe(
            comparison_df,
            hide_index=True,
            use_container_width=True
        )

        # Export button
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            csv_data = export_comparison_report(comparison_df, residue_name)
            st.download_button(
                label="📥 Exportar CSV",
                data=csv_data,
                file_name=f"comparacao_{residue_name}_{date.today()}.csv",
                mime="text/csv"
            )

        with col2:
            if st.button("🗑️ Limpar Dados"):
                clear_lab_results(residue_name)
                st.rerun()


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function"""
    render_header()

    # New parallel sector + residue selector
    selected_residue = render_full_selector(key_prefix="parametros")

    if not selected_residue:
        return

    st.markdown("---")

    # Load residue data
    residue_data = get_residue_data(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados")
        return

    # Render all sections
    render_chemical_parameters(residue_data.chemical_params)

    st.markdown("---")

    render_operational_parameters(residue_data.operational)

    st.markdown("---")

    render_lab_input_tool(selected_residue, residue_data)


if __name__ == "__main__":
    main()
