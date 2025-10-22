"""
Homepage UI Components - PanoramaCP2B
Following SOLID principles - Single Responsibility for each component
Using Streamlit-native components for 100% reliable rendering
"""

import streamlit as st


def render_hero_section():
    """
    Renders the hero section with platform title and Phase 5 statistics.
    Uses Streamlit-native components for reliability.
    """
    # Gradient header with simple HTML (no comments, no complex nesting)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
                color: white; padding: 2.5rem 2rem; margin: -1rem -1rem 1.5rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🧪 PanoramaCP2B
        </h1>
        <h2 style='margin: 12px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 400;'>
            Centro Paulista de Estudos em Biogás e Bioprodutos
        </h2>
        <p style='margin: 15px 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 300;'>
            Plataforma de Validação Laboratorial para Pesquisa em Biogás
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Phase 5 Badge using Streamlit success message
    st.success("✅ **Phase 5 Complete** - SAF Validated Platform (84% Coverage)")

    # Stats using Streamlit columns and metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Resíduos Validados", "38", help="Agricultura (24), Pecuária (5), Industrial (5), Urbano (4)")

    with col2:
        st.metric("SAF Coverage", "84%", help="32/38 resíduos com fatores validados")

    with col3:
        st.metric("Referências", "20+", help="Artigos peer-reviewed com DOI")

    with col4:
        st.metric("Municípios SP", "645", help="Cobertura completa do Estado")


def render_about_section():
    """
    Renders the about section with simple markdown.
    """
    st.markdown("## 🎯 Sobre a Plataforma")

    st.info("""
    O **PanoramaCP2B** é uma ferramenta especializada para pesquisadores que trabalham com
    caracterização de resíduos orgânicos e produção de biogás. A plataforma oferece:

    - **Dados Validados de Literatura**: Composição química e potencial metanogênico de diversos resíduos
    - **Ferramenta de Comparação Laboratorial**: Compare seus resultados de laboratório com valores de referência
    - **Base Científica Completa**: Acesso a referências científicas com DOI e links Scopus
    - **Metodologia Conservadora**: Fatores de disponibilidade baseados em dados reais de usinas
    """)

    st.markdown("---")


def render_phase5_highlights():
    """
    Renders Phase 5 completion highlights using only Streamlit native components.
    """
    st.markdown("## 🎉 Novidades - Phase 5 Complete")

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ SAF Validation Complete")
        st.write("84% dos resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)")

    with col2:
        st.markdown("### 🔬 CH₄ & C:N Parameters")
        st.write("Novos parâmetros químicos: produção de metano e relação Carbono:Nitrogênio")

    with col3:
        st.markdown("### 🗺️ Database Integration")
        st.write("645 municípios com dados de potencial de biogás integrados")

    # Row 2
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("### 🏆 Priority Ranking")
        st.write("Sistema de classificação por viabilidade: EXCEPCIONAL → INVIÁVEL")

    with col5:
        st.markdown("### 🚀 Golden Page 2")
        st.write("Parâmetros Químicos completamente reformulados com visualizações avançadas")

    with col6:
        st.markdown("### 📊 Literature Ranges")
        st.write("Ranges MIN/MEAN/MAX validados para todos os parâmetros")

    st.markdown("---")


def render_features_grid():
    """
    Renders the main features using Streamlit native components.
    """
    st.markdown("## ✨ Principais Funcionalidades")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("### 🔬 Para Pesquisadores")
            st.markdown("""
            - **Validação de Dados Laboratoriais**: Compare seus resultados com valores de literatura
            - **Análise de Desvios**: Thresholds configurados por parâmetro (±10-20%)
            - **Status de Validação**: ✅ Dentro da faixa / ⚠️ Desvio aceitável / ❌ Fora da faixa
            - **Exportação de Relatórios**: CSV com comparação completa
            """)

        st.markdown("")  # Spacing

        with st.container():
            st.markdown("### 📊 Dados Disponíveis")
            st.markdown("""
            - **BMP**: Potencial Metanogênico Bioquímico
            - **TS/VS**: Sólidos Totais e Voláteis
            - **C:N**: Relação Carbono:Nitrogênio
            - **CH₄**: Produção específica de metano (ml CH₄/g VS)
            - **pH, COD, TAN**: Parâmetros operacionais
            - **Composição**: N, C, P, K, proteína
            - **SAF**: Fatores de Disponibilidade (FC, FCp, FS, FL)
            """)

    with col2:
        with st.container():
            st.markdown("### 📚 Base Científica")
            st.markdown("""
            - **Referências Validadas**: Artigos peer-reviewed com DOI
            - **Scopus Indexados**: Links diretos para base Scopus
            - **Principais Achados**: Resumo dos resultados relevantes de cada paper
            - **Exportação Bibliográfica**: Formatos BibTeX, RIS, CSV
            - **Cobertura**: 20+ resíduos com referências científicas completas
            """)

        st.markdown("")  # Spacing

        with st.container():
            st.markdown("### 🌾 Resíduos Incluídos (38 Total)")
            st.markdown("""
            - **Agricultura**: 24 resíduos (Cana, Citros, Café, Milho, Soja, e mais)
            - **Pecuária**: 5 resíduos (Bovinos, Suínos, Aves, Codornas)
            - **Industrial**: 5 resíduos (Laticínios, Cervejarias, Frigoríficos)
            - **Urbano**: 4 resíduos (RSU, RPO, Lodo de Esgoto)
            - **Total Realista**: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)
            - **SAF Validado**: 84% dos resíduos com fatores de disponibilidade calibrados
            """)

    st.markdown("---")


def render_saf_priority_summary():
    """
    Renders SAF priority summary with metric cards.
    """
    st.markdown("## 📈 Status Atual")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Resíduos Disponíveis", "38",
                  help="Agricultura (24), Pecuária (5), Industrial (5), Urbano (4) - Phase 5 Complete")

    with col2:
        st.metric("🎯 SAF Validação", "84%",
                  help="32/38 resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)")

    with col3:
        st.metric("🔬 Parâmetros Químicos", "15+",
                  help="BMP, TS, VS, C:N, CH₄, pH, COD, N, C, P, K com ranges MIN/MEAN/MAX de literatura")

    with col4:
        st.metric("⚗️ Potencial Realista", "6.939 Mi m³/ano",
                  help="Cenário Realista com fatores SAF validados - 297% meta FIESP-SP")


def render_sector_overview():
    """
    Renders sector breakdown using only Streamlit native components.
    """
    st.markdown("---")

    st.markdown("## ✅ Banco de Dados Completo CP2B - Phase 5 (84% SAF Validado)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌾 Agricultura (24 resíduos)")
        st.success("""
        **🏆 Top Performers SAF**
        - 🥇 **Bagaço de cana**: 80.75% - EXCEPCIONAL
        - 🏆 **Torta de Filtro**: 12.88% - MUITO BOM
        - ✅ **Mucilagem de Café**: 11.90% - MUITO BOM
        - ⭐ **Vinhaça de Cana**: 10.26% - BOM
        """)

        st.markdown("""
        **Principais Culturas:**
        - 🌾 **Cana-de-açúcar**: 4 resíduos (Bagaço, Torta, Vinhaça, Palha)
        - 🍊 **Citros**: 2 resíduos (Bagaço, Cascas)
        - ☕ **Café**: 2 resíduos (Mucilagem, Casca/Polpa)
        - 🌽 **Milho**: 2 resíduos (Palha, Sabugo)
        - 🌱 **Soja**: 2 resíduos (Palha, Casca)
        - 🌳 **+ 12 outros** resíduos agrícolas
        """)

        st.markdown("")  # Spacing

        st.markdown("### 🐄 Pecuária (5 resíduos)")
        st.info("""
        **⭐ Destaque SAF**
        - 🐔 **Cama de Frango**: 8.67% - BOM
        """)

        st.markdown("""
        - 🐄 **Dejetos Bovinos** (Leite + Corte)
        - 🐷 **Dejetos de Suínos**
        - 🐔 **Cama de Frango**
        - 🥚 **Dejetos de Codornas**
        - 🐮 **Efluentes de Laticínios**
        """)

    with col2:
        st.markdown("### 🏭 Industrial (5 resíduos)")
        st.success("""
        **🥇 Top Performer**
        - 🥛 **Soro de Laticínios**: 30.40% - EXCELENTE
        """)

        st.markdown("""
        - 🥛 **Soro de Laticínios** (EXCELENTE)
        - 🍺 **Bagaço de Cervejarias**
        - 🥩 **Efluente de Frigoríficos**
        - 🍹 **Resíduos de Processamento**
        - 🏭 **Efluentes Industriais**
        """)

        st.markdown("")  # Spacing

        st.markdown("### 🏙️ Urbano (4 resíduos)")
        st.info("""
        **⭐ Destaque SAF**
        - 🗑️ **RSU**: 9.88% - BOM
        """)

        st.markdown("""
        - 🗑️ **RSU** (Resíduo Sólido Urbano)
        - 🌳 **RPO** (Resíduos de Poda Urbana)
        - 💧 **Lodo de Esgoto** (ETE)
        - 🍂 **Galhos e Folhas**
        """)

    # SAF Summary
    st.warning("""
    **💡 Metodologia SAF - Phase 5 ✅ COMPLETO**

    - ✅ **32/38 resíduos** com SAF validado (84%)
    - 🎯 Fatores calibrados: **FC, FCp, FS, FL**
    - 📊 Cenários: Pessimista, **Realista ⭐**, Otimista, Teórico
    - 📈 Total Realista: **6.939 Mi m³/ano CH₄** (297% meta FIESP-SP)
    - 🏆 Priority Tiers: 1 EXCEPCIONAL, 3 EXCELENTE, 7 BOM/MUITO BOM
    """)

    st.markdown("---")


def render_footer():
    """
    Renders the footer with platform information using simple markdown.
    """
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h3>🧪 PanoramaCP2B</h3>
        <p><strong>Centro Paulista de Estudos em Biogás e Bioprodutos</strong></p>
        <p>Plataforma de Validação Laboratorial para Pesquisa em Biogás</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Phase 5 Complete - SAF Validated Platform")

    st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
        <p>📊 38 Resíduos • 🎯 84% SAF Coverage • 📚 20+ Referências • 🗺️ 645 Municípios</p>
        <p style='font-style: italic;'>💡 Use a barra lateral esquerda para navegar entre as páginas</p>
        <p style='font-size: 0.8rem; color: #9ca3af;'>Última atualização: Outubro 2025 • Version 2.0 • UNICAMP</p>
    </div>
    """, unsafe_allow_html=True)
