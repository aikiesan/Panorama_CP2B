"""
Dados Laboratoriais - Consulta Rápida
Página para consulta de parâmetros físico-químicos e dados de referência.
"""

import streamlit as st
import pandas as pd
from src import ui_components as ui
from src.data_sources import lab_data_handler as lab

# --- Page Configuration ---
st.set_page_config(
    page_title="Dados Laboratoriais - Panorama de Resíduos SP",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium design system
ui.load_css()

# --- Header ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🔬 Dados Laboratoriais de Referência</h1>
    <p class="hero-subtitle">Consulta Rápida de Parâmetros Físico-Químicos para Resíduos</p>
</div>
""", unsafe_allow_html=True)

# --- Info Box ---
st.markdown("""
<div class="info-card">
    <h3>📚 Sobre Esta Seção</h3>
    <p>
    Aqui você encontra parâmetros laboratoriais de referência para caracterização de resíduos
    e avaliação do potencial de produção de biogás. Os dados incluem:
    </p>
    <ul>
        <li>Teores de sólidos (ST, SV, SF)</li>
        <li>Parâmetros químicos (pH, DQO, C/N)</li>
        <li>Potencial metanogênico (BMP)</li>
        <li>Métodos analíticos padronizados</li>
        <li>Referências técnicas e científicas</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df_lab = lab.load_dados_laboratoriais()

if df_lab.empty:
    st.warning("⚠️ Nenhum dado laboratorial encontrado. Carregando dados de referência padrão...")
    df_lab = lab.get_default_lab_data()

# --- Sidebar: Search and Filters ---
st.sidebar.header("🔍 Busca e Filtros")

# Search box
termo_busca = st.sidebar.text_input(
    "Buscar por termo:",
    placeholder="Ex: pH, esterco, sólidos...",
    help="Busca em tipos de resíduo e parâmetros"
)

# Filter by waste type
tipos_disponiveis = lab.get_tipos_residuo_disponiveis()
if not tipos_disponiveis and not df_lab.empty:
    tipos_disponiveis = sorted(df_lab['tipo_residuo'].unique().tolist())

tipo_selecionado = st.sidebar.multiselect(
    "Filtrar por tipo de resíduo:",
    options=tipos_disponiveis,
    default=None,
    help="Selecione um ou mais tipos de resíduo"
)

# Filter by parameter
parametros_disponiveis = lab.get_parametros_disponiveis()
if not parametros_disponiveis and not df_lab.empty:
    parametros_disponiveis = sorted(df_lab['parametro'].unique().tolist())

parametro_selecionado = st.sidebar.multiselect(
    "Filtrar por parâmetro:",
    options=parametros_disponiveis,
    default=None,
    help="Selecione um ou mais parâmetros"
)

# --- Apply Filters ---
df_filtrado = df_lab.copy()

if termo_busca:
    df_filtrado = lab.buscar_parametro(termo_busca)
    if df_filtrado.empty:
        st.warning(f"Nenhum resultado encontrado para '{termo_busca}'")

if tipo_selecionado:
    df_filtrado = df_filtrado[df_filtrado['tipo_residuo'].isin(tipo_selecionado)]

if parametro_selecionado:
    df_filtrado = df_filtrado[df_filtrado['parametro'].isin(parametro_selecionado)]

# --- Statistics ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_tipos = len(df_filtrado['tipo_residuo'].unique()) if not df_filtrado.empty else 0
    st.metric("📦 Tipos de Resíduo", total_tipos)

with col2:
    total_parametros = len(df_filtrado['parametro'].unique()) if not df_filtrado.empty else 0
    st.metric("🧪 Parâmetros", total_parametros)

with col3:
    total_registros = len(df_filtrado) if not df_filtrado.empty else 0
    st.metric("📊 Registros", total_registros)

with col4:
    metodos_unicos = len(df_filtrado['metodo'].unique()) if not df_filtrado.empty and 'metodo' in df_filtrado.columns else 0
    st.metric("⚗️ Métodos Analíticos", metodos_unicos)

st.markdown("---")

# --- Main Content: Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Tabela Completa",
    "🔬 Por Tipo de Resíduo",
    "🧪 Por Parâmetro",
    "📖 Métodos Analíticos"
])

# Tab 1: Complete Table
with tab1:
    st.subheader("📋 Dados Laboratoriais - Tabela Completa")

    if not df_filtrado.empty:
        # Prepare display columns
        display_cols = ['tipo_residuo', 'parametro', 'valor_tipico', 'unidade', 'metodo', 'referencia']
        display_cols = [col for col in display_cols if col in df_filtrado.columns]

        # Rename columns for better display
        col_rename = {
            'tipo_residuo': 'Tipo de Resíduo',
            'parametro': 'Parâmetro',
            'valor_tipico': 'Valor Típico',
            'unidade': 'Unidade',
            'metodo': 'Método',
            'referencia': 'Referência'
        }

        df_display = df_filtrado[display_cols].copy()
        df_display.rename(columns=col_rename, inplace=True)

        # Display with formatting
        st.dataframe(
            df_display,
            use_container_width=True,
            height=500
        )

        # Download button
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv,
            file_name="dados_laboratoriais.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhum dado disponível com os filtros aplicados.")

# Tab 2: By Waste Type
with tab2:
    st.subheader("🔬 Consulta por Tipo de Resíduo")

    residuo_consulta = st.selectbox(
        "Selecione o tipo de resíduo:",
        options=tipos_disponiveis if tipos_disponiveis else ["Nenhum disponível"],
        key="residuo_tab2"
    )

    if residuo_consulta and residuo_consulta != "Nenhum disponível":
        df_residuo = lab.get_parametros_by_residuo(residuo_consulta)

        if df_residuo.empty:
            df_residuo = df_lab[df_lab['tipo_residuo'] == residuo_consulta] if not df_lab.empty else pd.DataFrame()

        if not df_residuo.empty:
            st.markdown(f"### 📊 Parâmetros para: **{residuo_consulta}**")

            # Display as cards
            for _, row in df_residuo.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="parameter-card">
                        <h4 style="margin-top: 0; color: #667eea;">🧪 {row['parametro']}</h4>
                        <p style="font-size: 1.3em; font-weight: bold; color: #2c3e50;">
                            {row['valor_tipico']} {row['unidade']}
                        </p>
                        <p style="font-size: 0.9em; color: #555;">
                            <strong>Método:</strong> {row['metodo']}<br>
                            <strong>Referência:</strong> {row['referencia']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"Nenhum parâmetro encontrado para {residuo_consulta}")

# Tab 3: By Parameter
with tab3:
    st.subheader("🧪 Consulta por Parâmetro")

    parametro_consulta = st.selectbox(
        "Selecione o parâmetro:",
        options=parametros_disponiveis if parametros_disponiveis else ["Nenhum disponível"],
        key="parametro_tab3"
    )

    if parametro_consulta and parametro_consulta != "Nenhum disponível":
        df_parametro = lab.get_parametro_especifico(parametro_consulta)

        if df_parametro.empty:
            df_parametro = df_lab[df_lab['parametro'] == parametro_consulta] if not df_lab.empty else pd.DataFrame()

        if not df_parametro.empty:
            st.markdown(f"### 📊 **{parametro_consulta}** - Comparação entre Resíduos")

            # Create comparison table
            display_cols = ['tipo_residuo', 'valor_tipico', 'unidade', 'metodo']
            display_cols = [col for col in display_cols if col in df_parametro.columns]

            df_comp = df_parametro[display_cols].copy()
            df_comp.rename(columns={
                'tipo_residuo': 'Tipo de Resíduo',
                'valor_tipico': 'Valor Típico',
                'unidade': 'Unidade',
                'metodo': 'Método'
            }, inplace=True)

            st.dataframe(df_comp, use_container_width=True)

            # Additional info
            st.info(f"💡 **Interpretação**: Este parâmetro varia significativamente entre os diferentes tipos de resíduos.")
        else:
            st.info(f"Nenhum dado encontrado para {parametro_consulta}")

# Tab 4: Analytical Methods
with tab4:
    st.subheader("📖 Métodos Analíticos Utilizados")

    df_metodos = lab.get_metodos_analiticos()

    if df_metodos.empty and not df_lab.empty and 'metodo' in df_lab.columns:
        df_metodos = df_lab.groupby('metodo').size().reset_index(name='count')
        df_metodos = df_metodos.sort_values('count', ascending=False)

    if not df_metodos.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📚 Lista de Métodos")

            # Expand on methods
            metodos_info = {
                'APHA 2540 B': {
                    'nome': 'Determinação de Sólidos Totais',
                    'descricao': 'Método gravimétrico para determinação de sólidos totais por evaporação a 103-105°C'
                },
                'APHA 2540 E': {
                    'nome': 'Determinação de Sólidos Fixos e Voláteis',
                    'descricao': 'Calcinação a 550°C para separação da fração orgânica (volátil) e inorgânica (fixa)'
                },
                'VDI 4630': {
                    'nome': 'Teste de Potencial Metanogênico (BMP)',
                    'descricao': 'Norma alemã para ensaios de fermentação e produção de biogás de substratos e digestato'
                },
                'APHA 4500-H⁺': {
                    'nome': 'Determinação de pH',
                    'descricao': 'Medição potenciométrica do pH utilizando eletrodo de vidro'
                },
                'APHA 5220 D': {
                    'nome': 'Demanda Química de Oxigênio (DQO)',
                    'descricao': 'Método colorimétrico com refluxo fechado para determinação de DQO'
                },
                'Elementar': {
                    'nome': 'Análise Elementar C/H/N',
                    'descricao': 'Determinação de carbono, hidrogênio e nitrogênio por combustão'
                },
                'BMP Test': {
                    'nome': 'Biochemical Methane Potential',
                    'descricao': 'Ensaio de laboratório para medir o potencial de produção de metano de um substrato'
                }
            }

            for _, row in df_metodos.iterrows():
                metodo = row['metodo']
                count = row['count']

                info = metodos_info.get(metodo, {
                    'nome': metodo,
                    'descricao': 'Método analítico padronizado'
                })

                with st.expander(f"📖 {metodo} ({count} usos)"):
                    st.markdown(f"**{info['nome']}**")
                    st.write(info['descricao'])

        with col2:
            st.markdown("### 📊 Uso dos Métodos")

            import plotly.express as px

            fig = px.bar(
                df_metodos.head(10),
                x='count',
                y='metodo',
                orientation='h',
                labels={'count': 'Quantidade de Usos', 'metodo': 'Método'},
                title="Top 10 Métodos Mais Utilizados"
            )

            fig.update_layout(
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum método analítico cadastrado.")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <h3 style="color: #667eea;">🔬 Dados Laboratoriais</h3>
    <p><strong>Consulta rápida de parâmetros físico-químicos</strong></p>
    <p style="font-size: 0.85em;">
        Os valores apresentados são referências típicas da literatura técnica e científica.<br>
        Para análises específicas, consulte laboratórios especializados certificados.
    </p>
    <p style="font-size: 0.85em; margin-top: 10px;">
        <strong>Referências principais:</strong> APHA (Standard Methods), VDI 4630, Literatura Científica
    </p>
</div>
""", unsafe_allow_html=True)
