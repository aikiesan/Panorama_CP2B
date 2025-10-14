"""
PanoramaCP2B - Centro Paulista de Estudos em Biogás e Bioprodutos
Homepage - Laboratory Validation Tool for Biogas Research
"""

import streamlit as st


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PanoramaCP2B - Validação Laboratorial",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style='background: linear-gradient(135deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
            color: white; padding: 3rem; margin: -1rem -1rem 2rem -1rem;
            text-align: center; border-radius: 0 0 30px 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
    <h1 style='margin: 0; font-size: 3.5rem; font-weight: 800; letter-spacing: -1px;'>
        🧪 PanoramaCP2B
    </h1>
    <h2 style='margin: 15px 0 0 0; font-size: 1.6rem; opacity: 0.95; font-weight: 400;'>
        Centro Paulista de Estudos em Biogás e Bioprodutos
    </h2>
    <p style='margin: 20px 0 0 0; font-size: 1.2rem; opacity: 0.9; font-weight: 300;'>
        Plataforma de Validação Laboratorial para Pesquisa em Biogás
    </p>
    <div style='margin-top: 20px; font-size: 1rem; opacity: 0.85;'>
        📊 Dados Validados • 🔬 Comparação Laboratorial • 📚 Referências DOI • ⚗️ Metodologia Científica
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# ABOUT SECTION
# ============================================================================

st.markdown("## 🎯 Sobre a Plataforma")

st.markdown("""
O **PanoramaCP2B** é uma ferramenta especializada para pesquisadores que trabalham com
caracterização de resíduos orgânicos e produção de biogás. A plataforma oferece:

- **Dados Validados de Literatura**: Composição química e potencial metanogênico de diversos resíduos
- **Ferramenta de Comparação Laboratorial**: Compare seus resultados de laboratório com valores de referência
- **Base Científica Completa**: Acesso a referências científicas com DOI e links Scopus
- **Metodologia Conservadora**: Fatores de disponibilidade baseados em dados reais de usinas
""")

st.markdown("---")


# ============================================================================
# NAVIGATION CARDS
# ============================================================================

st.markdown("## 📑 Navegação")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                padding: 1.2rem; border-radius: 15px; text-align: center;
                border: 2px solid #2563eb; min-height: 220px;'>
        <div style='font-size: 2.8rem; margin-bottom: 0.6rem;'>📊</div>
        <h3 style='color: #1e3a8a; margin-bottom: 0.7rem; font-size: 1.2rem; font-weight: 700;'>Disponibilidade de Resíduos</h3>
        <p style='color: #1e40af; font-size: 0.88rem; line-height: 1.4; margin-bottom: 0.7rem;'>
            Fatores de disponibilidade real, cenários de potencial, e análise de competição
            por usos estabelecidos
        </p>
        <p style='color: #3b82f6; font-size: 0.8rem; margin-top: 0.7rem;'>
            📈 Cenários • 🔢 Fatores • 🏆 Top Municípios
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    if st.button("Ir para Disponibilidade", key="btn_disp", use_container_width=True):
        st.switch_page("pages/1_📊_Disponibilidade.py")

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
                padding: 1.2rem; border-radius: 15px; text-align: center;
                border: 2px solid #7c3aed; min-height: 220px;'>
        <div style='font-size: 2.8rem; margin-bottom: 0.6rem;'>🧪</div>
        <h3 style='color: #5b21b6; margin-bottom: 0.7rem; font-size: 1.2rem; font-weight: 700;'>Parâmetros Químicos</h3>
        <p style='color: #6b21a8; font-size: 0.88rem; line-height: 1.4; margin-bottom: 0.7rem;'>
            Composição química completa (BMP, TS, VS, C:N, pH) com ferramenta
            integrada para comparação laboratorial
        </p>
        <p style='color: #7c3aed; font-size: 0.8rem; margin-top: 0.7rem;'>
            ⚗️ Composição • 🔬 Validação Lab • 📥 Relatório
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    if st.button("Ir para Parâmetros Químicos", key="btn_quim", use_container_width=True):
        st.switch_page("pages/2_🧪_Parametros_Quimicos.py")

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
                padding: 1.2rem; border-radius: 15px; text-align: center;
                border: 2px solid #f59e0b; min-height: 220px;'>
        <div style='font-size: 2.8rem; margin-bottom: 0.6rem;'>📚</div>
        <h3 style='color: #92400e; margin-bottom: 0.7rem; font-size: 1.2rem; font-weight: 700;'>Referências Científicas</h3>
        <p style='color: #b45309; font-size: 0.88rem; line-height: 1.4; margin-bottom: 0.7rem;'>
            Base completa de artigos científicos com DOI, Scopus, principais achados,
            e exportação BibTeX/RIS/CSV
        </p>
        <p style='color: #d97706; font-size: 0.8rem; margin-top: 0.7rem;'>
            📄 DOI • 🔍 Scopus • 📥 BibTeX/RIS
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    if st.button("Ir para Referências", key="btn_ref", use_container_width=True):
        st.switch_page("pages/3_📚_Referencias_Cientificas.py")

st.markdown("---")


# ============================================================================
# KEY FEATURES
# ============================================================================

st.markdown("## ✨ Principais Funcionalidades")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔬 Para Pesquisadores

    - **Validação de Dados Laboratoriais**: Compare seus resultados com valores de literatura
    - **Análise de Desvios**: Thresholds configurados por parâmetro (±10-20%)
    - **Status de Validação**: ✅ Dentro da faixa / ⚠️ Desvio aceitável / ❌ Fora da faixa
    - **Exportação de Relatórios**: CSV com comparação completa

    ### 📊 Dados Disponíveis

    - **BMP**: Potencial Metanogênico Bioquímico
    - **TS/VS**: Sólidos Totais e Voláteis
    - **C:N**: Relação Carbono:Nitrogênio
    - **pH, COD, TAN**: Parâmetros operacionais
    - **Composição**: N, C, P, K, proteína
    """)

with col2:
    st.markdown("""
    ### 📚 Base Científica

    - **Referências Validadas**: Artigos peer-reviewed com DOI
    - **Scopus Indexados**: Links diretos para base Scopus
    - **Principais Achados**: Resumo dos resultados mais relevantes
    - **Exportação Bibliográfica**: BibTeX, RIS, CSV

    ### 🌾 Resíduos Incluídos (7 Total)

    - **Agricultura**: Vinhaça de Cana, Palha de Cana, Torta de Filtro
    - **Pecuária**: Avicultura (Frango), Bovinocultura (Leite+Corte), Suinocultura, Codornas
    - **Total Realista**: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)
    - **Expansível**: Banco CP2B v2.0 com 50+ papers validados
    """)

st.markdown("---")


# ============================================================================
# METHODOLOGY OVERVIEW
# ============================================================================

st.markdown("## 📖 Metodologia")

with st.expander("ℹ️ Sobre a Metodologia Utilizada", expanded=False):
    st.markdown("""
    ### 🔬 Abordagem Conservadora

    Os dados apresentados seguem uma **metodologia conservadora** baseada em:

    1. **Dados de Literatura Validados**: Apenas artigos peer-reviewed com metodologia clara
    2. **Fatores de Correção Reais**: Baseados em operação de usinas existentes
    3. **Competição por Usos**: Consideração de mercados estabelecidos (fertilizante, ração)
    4. **Restrições Logísticas**: Raio econômico de transporte (20-30 km típico)

    ### 📊 Cenários de Disponibilidade

    - **Teórico (100%)**: Produção total sem competições (não operacional)
    - **Otimista**: Fatores otimistas, menor competição
    - **Realista**: Calibrado com dados reais (base para planejamento)
    - **Pessimista**: Fatores conservadores máximos

    ### ✅ Validação Laboratorial

    A ferramenta de comparação utiliza **thresholds de desvio** baseados em:
    - Variabilidade natural do parâmetro
    - Precisão típica de metodologias laboratoriais
    - Ranges reportados em literatura

    **Exemplos de Thresholds:**
    - BMP: ±15% (alta variabilidade biológica)
    - TS/VS: ±10% (metodologia gravimétrica)
    - C:N: ±20% (composição heterogênea)
    - pH: ±5% (medição precisa)

    ### 📚 Revisão de Literatura

    Base científica construída com metodologia **PRISMA-like**:
    - Busca sistemática em Scopus, Web of Science, SciELO
    - Critérios de inclusão/exclusão claros
    - Priorização de contexto brasileiro/tropical
    - Classificação por relevância e tipo de dado
    """)

st.markdown("---")


# ============================================================================
# CURRENT STATUS
# ============================================================================

st.markdown("## 📈 Status Atual")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Resíduos Disponíveis", "7", help="Todos validados: Avicultura, Bovinocultura, Vinhaça, Palha Cana, Torta Filtro, Suinocultura, Codornas")

with col2:
    st.metric("📄 Artigos Referenciados", "50+", help="Base científica completa com DOI e Scopus")

with col3:
    st.metric("🔬 Parâmetros Químicos", "15+", help="BMP, TS, VS, C:N, pH, COD, N, C, P, K, proteína, etc.")

with col4:
    st.metric("⚗️ Potencial Realista", "6.939 Mi m³/ano", help="297% da meta FIESP-SP (2,34 Mi m³/ano)")


# ============================================================================
# ROADMAP
# ============================================================================

st.markdown("---")

st.markdown("## ✅ Banco de Dados Completo CP2B v2.0")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌾 Agricultura (3 resíduos)

    - ✅ **Vinhaça de Cana-de-açúcar** (completo)
    - ✅ **Palha de Cana** (completo)
    - ✅ **Torta de Filtro** (completo)

    ### 🐄 Pecuária (4 resíduos)

    - ✅ **Avicultura** (Cama de Frango)
    - ✅ **Bovinocultura** (Leite + Corte)
    - ✅ **Suinocultura** (Dejetos)
    - ✅ **Codornas** (Dejetos)
    """)

with col2:
    st.markdown("""
    ### 📊 Próximos Resíduos (Pipeline)

    - 🍊 **Citros** (laranja, limão)
    - 🌽 **Milho** (palha e sabugo)
    - 🫘 **Soja** (palha e restos)
    - ☕ **Café** (casca e polpa)
    - 🏙️ **RSU/RPO** (resíduos urbanos)

    ### 💡 Metodologia SAF

    - Fatores de disponibilidade recalibrados
    - Cenários: Pessimista, Realista, Otimista, Teórico
    - Total: **6.939 Mi m³/ano** (realista)
    """)

st.markdown("---")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
            border-radius: 20px; margin-top: 2rem;'>
    <h3 style='color: #059669; margin-bottom: 1rem;'>🧪 PanoramaCP2B</h3>
    <p style='font-size: 1.1rem; color: #374151; margin-bottom: 0.5rem;'>
        <strong>Centro Paulista de Estudos em Biogás e Bioprodutos</strong>
    </p>
    <p style='font-size: 0.95rem; color: #6b7280;'>
        Plataforma de Validação Laboratorial para Pesquisa em Biogás
    </p>
    <p style='font-size: 0.85rem; color: #9ca3af; margin-top: 1rem;'>
        📊 Dados Validados • 🔬 Metodologia Científica • 📚 Literatura Revisada
    </p>
    <p style='font-size: 0.8rem; color: #9ca3af; margin-top: 1.5rem; font-style: italic;'>
        💡 Use a barra lateral esquerda para navegar entre as páginas
    </p>
</div>
""", unsafe_allow_html=True)
