"""
Page 4: Comparação Laboratorial
CP2B - Laboratory data comparison tool
"""

import streamlit as st
import pandas as pd
from datetime import date

from src.data.residue_registry import (
    get_available_residues,
    get_residue_data,
    get_residue_icon
)
from src.ui.tabs import render_sector_tabs
from src.ui.horizontal_nav import render_horizontal_nav
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
    page_title="Comparação Laboratorial - CP2B",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize lab session
initialize_lab_session()


# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render header for lab comparison page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 2rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🔬 Ferramenta de Comparação Laboratorial
        </h1>
        <p style='margin: 15px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 300;'>
            Valide Seus Dados de Laboratório com a Literatura
        </p>
        <div style='margin-top: 15px; font-size: 0.95rem; opacity: 0.8;'>
            📊 Comparação Automática • ✅ Status de Validação • 📥 Exportação CSV
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# LAB DATA INPUT TOOL
# ============================================================================

def render_lab_input_tool(residue_name, residue_data):
    """Render laboratory data input and comparison tool"""
    st.markdown("### 📝 Como Usar Esta Ferramenta")

    st.info("""
    **💡 Passo a passo:**
    1. **Selecione** o setor e resíduo acima
    2. **Insira** os valores medidos em laboratório nos campos abaixo
    3. **Compare** automaticamente com os valores de referência da literatura
    4. **Verifique** o status de validação:
       - ✅ **Dentro da faixa**: Resultado válido (desvio ≤ threshold)
       - ⚠️ **Desvio aceitável**: Resultado próximo (desvio moderado)
       - ❌ **Fora da faixa**: Resultado atípico (verificar medição)
    5. **Exporte** o relatório de comparação em CSV
    """)

    st.markdown("---")

    # Input form
    with st.form(key='lab_input_form'):
        st.markdown("### 📝 Inserir Dados Laboratoriais")

        col1, col2, col3 = st.columns(3)

        lab_data = {}

        with col1:
            st.markdown("#### Parâmetros Principais")

            lab_data['bmp'] = st.number_input(
                "BMP (m³ CH₄/kg VS)",
                min_value=0.0,
                value=0.0,
                step=0.01,
                help="Potencial Metanogênico Bioquímico"
            )

            lab_data['ts'] = st.number_input(
                "Sólidos Totais (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Total de sólidos (base úmida)"
            )

            lab_data['vs'] = st.number_input(
                "Sólidos Voláteis (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Fração volátil dos sólidos"
            )

            lab_data['moisture'] = st.number_input(
                "Umidade (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Conteúdo de umidade"
            )

        with col2:
            st.markdown("#### Composição Química")

            lab_data['cn_ratio'] = st.number_input(
                "Relação C:N",
                min_value=0.0,
                value=0.0,
                step=0.1,
                help="Relação Carbono:Nitrogênio"
            )

            lab_data['nitrogen'] = st.number_input(
                "Nitrogênio (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.01,
                help="Conteúdo de nitrogênio"
            )

            lab_data['carbon'] = st.number_input(
                "Carbono (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Conteúdo de carbono"
            )

            lab_data['ph'] = st.number_input(
                "pH",
                min_value=0.0,
                max_value=14.0,
                value=0.0,
                step=0.1,
                help="Potencial hidrogeniônico"
            )

        with col3:
            st.markdown("#### Parâmetros Operacionais")

            lab_data['ch4_content'] = st.number_input(
                "Conteúdo CH₄ (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Percentual de metano no biogás"
            )

            lab_data['cod'] = st.number_input(
                "DQO (mg/L)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                help="Demanda Química de Oxigênio"
            )

            lab_data['phosphorus'] = st.number_input(
                "Fósforo P₂O₅ (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.01,
                help="Conteúdo de fósforo"
            )

            lab_data['potassium'] = st.number_input(
                "Potássio K₂O (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.01,
                help="Conteúdo de potássio"
            )

        # Metadata
        st.markdown("---")
        st.markdown("### 📋 Metadados (Opcional)")

        col1, col2, col3 = st.columns(3)

        with col1:
            lab_name = st.text_input("🏢 Nome do Laboratório", placeholder="Ex: Lab UNICAMP")
            measurement_date = st.date_input("📅 Data da Medição", value=date.today())

        with col2:
            operator = st.text_input("👤 Responsável pela Análise", placeholder="Ex: Dr. João Silva")
            method = st.text_input("⚗️ Método Utilizado", placeholder="Ex: VDI 4630")

        with col3:
            sample_id = st.text_input("🔖 ID da Amostra", placeholder="Ex: RSU-SP-001")
            notes = st.text_area("📝 Observações", height=80, placeholder="Notas adicionais sobre a análise...")

        submit_button = st.form_submit_button("🔍 Comparar com Referência", use_container_width=True, type="primary")

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
            'method': method,
            'sample_id': sample_id,
            'notes': notes
        }

        st.success("✅ Dados laboratoriais salvos! Veja a comparação abaixo.")

    # Display comparison if data exists
    lab_results = get_lab_results(residue_name)

    if lab_results:
        st.markdown("---")
        st.markdown("### 📊 Resultado da Comparação")

        # Show metadata if available
        if 'lab_metadata' in st.session_state and st.session_state.lab_metadata['lab_name']:
            with st.expander("📋 Informações da Análise", expanded=False):
                metadata = st.session_state.lab_metadata
                col1, col2, col3 = st.columns(3)

                with col1:
                    if metadata['lab_name']:
                        st.write(f"**🏢 Laboratório:** {metadata['lab_name']}")
                    if metadata['measurement_date']:
                        st.write(f"**📅 Data:** {metadata['measurement_date']}")

                with col2:
                    if metadata.get('operator'):
                        st.write(f"**👤 Responsável:** {metadata['operator']}")
                    if metadata.get('method'):
                        st.write(f"**⚗️ Método:** {metadata['method']}")

                with col3:
                    if metadata.get('sample_id'):
                        st.write(f"**🔖 ID Amostra:** {metadata['sample_id']}")
                    if metadata.get('notes'):
                        st.write(f"**📝 Observações:** {metadata['notes']}")

        # Create comparison object
        comparator = LabComparison(residue_data)
        comparison_df = comparator.create_comparison_report(lab_results)

        # Display comparison table
        st.dataframe(
            comparison_df,
            hide_index=True,
            use_container_width=True,
            height=400
        )

        # Summary statistics
        status_counts = comparison_df['Status'].str.split(' ').str[0].value_counts()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Total de Parâmetros", len(comparison_df))

        with col2:
            valid_count = status_counts.get('✅', 0)
            st.metric("✅ Dentro da Faixa", valid_count)

        with col3:
            warning_count = status_counts.get('⚠️', 0)
            st.metric("⚠️ Desvio Aceitável", warning_count)

        with col4:
            error_count = status_counts.get('❌', 0)
            st.metric("❌ Fora da Faixa", error_count)

        # Export and clear buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

        with col1:
            csv_data = export_comparison_report(comparison_df, residue_name)
            st.download_button(
                label="📥 Exportar CSV",
                data=csv_data,
                file_name=f"comparacao_{residue_name}_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            if st.button("🗑️ Limpar Dados", use_container_width=True):
                clear_lab_results(residue_name)
                st.rerun()

        with col3:
            if st.button("🔄 Nova Análise", use_container_width=True):
                clear_lab_results(residue_name)
                st.rerun()


# ============================================================================
# MAIN RENDER
# ============================================================================

def main():
    """Main page render function"""
    render_header()

    # Horizontal navigation tabs
    render_horizontal_nav("Lab")

    # Sector and residue selection
    selected_sector, selected_residue = render_sector_tabs(key_prefix="lab_comp")

    if not selected_residue:
        st.info("👆 Selecione um setor e resíduo acima para começar a comparação")

        # Show example/instructions
        st.markdown("---")
        st.markdown("### 🎯 Sobre Esta Ferramenta")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 📚 Base Científica

            Esta ferramenta compara seus dados laboratoriais com **valores de referência
            validados** extraídos de artigos científicos peer-reviewed.

            **Benefícios:**
            - ✅ Validação rápida de resultados
            - ✅ Identificação de outliers
            - ✅ Comparação com literatura brasileira
            - ✅ Exportação de relatórios profissionais
            """)

        with col2:
            st.markdown("""
            #### 🔬 Thresholds de Validação

            Os limites de aceitação são baseados na variabilidade natural de cada parâmetro:

            - **BMP**: ±15% (alta variabilidade biológica)
            - **ST/SV**: ±10% (metodologia gravimétrica)
            - **C:N**: ±20% (composição heterogênea)
            - **pH**: ±5% (medição precisa)
            - **DQO**: ±20% (método colorimétrico)
            """)

        return

    st.markdown("---")

    # Load residue data
    residue_data = get_residue_data(selected_residue)

    if not residue_data:
        st.error("⚠️ Dados não encontrados")
        return

    # Render lab input tool
    render_lab_input_tool(selected_residue, residue_data)


if __name__ == "__main__":
    main()
