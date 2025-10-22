"""
Homepage UI Components - PanoramaCP2B
Following SOLID principles - Single Responsibility for each component
Maintains elegant, minimalistic scientific design aesthetic
"""

import streamlit as st


def render_hero_section():
    """
    Renders the hero section with platform title and Phase 5 statistics.
    Maintains clean, professional scientific aesthetic.
    """
    st.markdown("""
    <div style='background: linear-gradient(135deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
                color: white; padding: 2.5rem; margin: -1rem -1rem 1.5rem -1rem;
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
        <div style='margin-top: 15px; font-size: 0.9rem; opacity: 0.85;'>
            📊 38 Resíduos Validados • 🎯 84% SAF Coverage • 📚 20+ Referências Científicas • 🗺️ 645 Municípios
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_about_section():
    """
    Renders the about section describing the platform's purpose.
    """
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


def render_phase5_highlights():
    """
    Renders Phase 5 completion highlights in a clean info box.
    """
    st.markdown("## 🎉 Novidades - Phase 5 Complete")

    st.info("""
    **🚀 Últimas Atualizações da Plataforma:**

    - ✅ **SAF Validation Complete**: 84% dos resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)
    - ✅ **CH₄ & C:N Parameters**: Novos parâmetros químicos adicionados (produção específica de metano e relação C/N)
    - ✅ **Database Integration**: 645 municípios com dados de potencial de biogás integrados
    - ✅ **Priority Ranking**: Sistema de classificação por viabilidade (EXCEPCIONAL → INVIÁVEL)
    - ✅ **Golden Page 2**: Página de Parâmetros Químicos completamente reformulada com visualizações avançadas
    - 📊 **Literature Ranges**: Ranges MIN/MEAN/MAX de literatura científica validada para todos os parâmetros
    """)

    st.markdown("---")


def render_features_grid():
    """
    Renders the main features in a 2-column grid layout.
    Maintains clean, professional design.
    """
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
        - **CH₄**: Produção específica de metano (ml CH₄/g VS)
        - **pH, COD, TAN**: Parâmetros operacionais
        - **Composição**: N, C, P, K, proteína
        - **SAF**: Fatores de Disponibilidade (FC, FCp, FS, FL)
        """)

    with col2:
        st.markdown("""
        ### 📚 Base Científica

        - **Referências Validadas**: Artigos peer-reviewed com DOI
        - **Scopus Indexados**: Links diretos para base Scopus
        - **Principais Achados**: Resumo dos resultados mais relevantes
        - **Exportação Bibliográfica**: BibTeX, RIS, CSV
        - **Cobertura**: 20+ resíduos com referências científicas completas

        ### 🌾 Resíduos Incluídos (38 Total)

        - **Agricultura**: 24 resíduos (Cana, Citros, Café, Milho, Soja, etc.)
        - **Pecuária**: 5 resíduos (Bovinos, Suínos, Aves, Codornas)
        - **Industrial**: 5 resíduos (Laticínios, Cervejarias, Frigoríficos)
        - **Urbano**: 4 resíduos (RSU, RPO, Lodo de Esgoto)
        - **Total Realista**: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)
        - **SAF Validado**: 84% dos resíduos com fatores de disponibilidade calibrados
        """)

    st.markdown("---")


def render_saf_priority_summary():
    """
    Renders a clean summary of SAF priority distribution and top performers.
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
    Renders sector breakdown with top performers.
    Maintains clean, scientific presentation.
    """
    st.markdown("---")

    st.markdown("## ✅ Banco de Dados Completo CP2B - Phase 5 (84% SAF Validado)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🌾 Agricultura (24 resíduos)

        **Top Performers - SAF Validado:**
        - 🥇 **Bagaço de cana** (SAF: 80.75% - EXCEPCIONAL)
        - 🏆 **Torta de Filtro** (SAF: 12.88% - MUITO BOM)
        - ⭐ **Vinhaça de Cana-de-açúcar** (SAF: 10.26% - BOM)
        - ✅ **Mucilagem de Café** (SAF: 11.90% - MUITO BOM)

        **Principais Culturas:**
        - 🌾 **Cana-de-açúcar** (4 resíduos - Bagaço, Torta, Vinhaça, Palha)
        - 🍊 **Citros** (2 resíduos - Bagaço, Cascas)
        - ☕ **Café** (2 resíduos - Mucilagem, Casca/Polpa)
        - 🌽 **Milho** (2 resíduos - Palha, Sabugo)
        - 🌱 **Soja** (2 resíduos - Palha, Casca)
        - 🌳 **+ 12 outros** resíduos agrícolas (Feijão, Amendoim, Mandioca, etc.)

        ### 🐄 Pecuária (5 resíduos)

        - 🐔 **Cama de Frango** (SAF: 8.67% - BOM)
        - 🐄 **Dejetos Bovinos** (Leite + Corte)
        - 🐷 **Dejetos de Suínos**
        - 🥚 **Dejetos de Codornas**
        - 🐮 **Efluentes de Laticínios**
        """)

    with col2:
        st.markdown("""
        ### 🏙️ Urbano (4 resíduos)

        - 🗑️ **RSU** (Resíduo Sólido Urbano - SAF: 9.88% - BOM)
        - 🌳 **RPO** (Resíduos de Poda Urbana)
        - 💧 **Lodo de Esgoto** (ETE)
        - 🍂 **Galhos e Folhas**

        ### 🏭 Industrial (5 resíduos)

        **Top Performer:**
        - 🥇 **Soro de Laticínios** (SAF: 30.40% - EXCELENTE)

        **Outros Resíduos:**
        - 🍺 **Bagaço de Cervejarias**
        - 🥩 **Efluente de Frigoríficos**
        - 🍹 **Resíduos de Processamento de Alimentos**
        - 🏭 **Efluentes Industriais**

        ### 💡 Metodologia SAF - Phase 5 ✅ COMPLETO

        - ✅ **32/38 resíduos** com SAF validado (84%)
        - 🎯 Fatores calibrados: FC, FCp, FS, FL
        - 📊 Cenários: Pessimista, Realista ⭐, Otimista, Teórico
        - 📈 **Total Realista: 6.939 Mi m³/ano CH₄**
        - 🏆 **Priority Tiers**: 1 EXCEPCIONAL, 3 EXCELENTE, 7 BOM/MUITO BOM
        """)

    st.markdown("---")


def render_footer():
    """
    Renders the footer with platform information and version.
    """
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
        <p style='font-size: 0.9rem; color: #059669; margin-top: 1rem; font-weight: 600;'>
            ✅ Phase 5 Complete - SAF Validated Platform
        </p>
        <p style='font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;'>
            📊 38 Resíduos • 🎯 84% SAF Coverage • 📚 20+ Referências • 🗺️ 645 Municípios
        </p>
        <p style='font-size: 0.8rem; color: #9ca3af; margin-top: 1.5rem; font-style: italic;'>
            💡 Use a barra lateral esquerda para navegar entre as páginas
        </p>
        <p style='font-size: 0.75rem; color: #d1d5db; margin-top: 1rem;'>
            Última atualização: Outubro 2025 • Version 2.0
        </p>
    </div>
    """, unsafe_allow_html=True)
