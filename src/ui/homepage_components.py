"""
Homepage UI Components - PanoramaCP2B
Following SOLID principles - Single Responsibility for each component
Using Streamlit-native components for 100% reliable rendering
"""

import streamlit as st
from src.data.residue_registry import RESIDUES_REGISTRY


def _get_residue_stats():
    """Calculate real statistics from residue registry"""
    total = len(RESIDUES_REGISTRY)

    # Count by category
    counts = {}
    for residue in RESIDUES_REGISTRY.values():
        cat = residue.category
        counts[cat] = counts.get(cat, 0) + 1

    # Count SAF validated (has valid availability factors)
    saf_validated = sum(1 for r in RESIDUES_REGISTRY.values()
                        if r.availability.fc > 0 and r.availability.fcp >= 0
                        and r.availability.fs > 0 and r.availability.fl > 0)

    # Count residues with SAF_REAL > 0
    saf_with_values = sum(1 for r in RESIDUES_REGISTRY.values()
                          if r.saf_real is not None and r.saf_real > 0)

    saf_percentage = round((saf_validated / total) * 100) if total > 0 else 0

    return {
        'total': total,
        'agricultura': counts.get('Agricultura', 0),
        'pecuaria': counts.get('Pecuária', 0),
        'industrial': counts.get('Industrial', 0),
        'urbano': counts.get('Urbano', 0),
        'saf_validated': saf_validated,
        'saf_percentage': saf_percentage,
        'saf_with_values': saf_with_values
    }


def _get_top_saf_performers(category, limit=4):
    """Get top SAF performers for a category"""
    residues = [
        (name, r.saf_real, r.priority_tier)
        for name, r in RESIDUES_REGISTRY.items()
        if r.category == category and r.saf_real is not None and r.saf_real > 0
    ]
    residues.sort(key=lambda x: x[1], reverse=True)
    return residues[:limit]


def render_hero_section():
    """
    Renders the hero section with platform title and Phase 5 statistics.
    Uses real data from residue registry.
    """
    # Get real statistics
    stats = _get_residue_stats()

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
    st.success(f"✅ **Phase 5 Complete** - SAF Validated Platform ({stats['saf_percentage']}% Coverage)")

    # Stats using Streamlit columns and metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Resíduos Validados", str(stats['total']),
                  help=f"Agricultura ({stats['agricultura']}), Pecuária ({stats['pecuaria']}), Industrial ({stats['industrial']}), Urbano ({stats['urbano']})")

    with col2:
        st.metric("SAF Coverage", f"{stats['saf_percentage']}%",
                  help=f"{stats['saf_validated']}/{stats['total']} resíduos com fatores validados")

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
    Renders Phase 5 completion highlights using real data.
    """
    stats = _get_residue_stats()

    st.markdown("## 🎉 Novidades - Phase 5 Complete")

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ SAF Validation Complete")
        st.write(f"{stats['saf_percentage']}% dos resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)")

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
            stats = _get_residue_stats()
            st.markdown(f"### 🌾 Resíduos Incluídos ({stats['total']} Total)")
            st.markdown(f"""
            - **Agricultura**: {stats['agricultura']} resíduos (Cana, Citros, Café, Milho, Soja, e mais)
            - **Pecuária**: {stats['pecuaria']} resíduos (Bovinos, Suínos, Aves, Codornas)
            - **Industrial**: {stats['industrial']} resíduos (Laticínios, Cervejarias, Frigoríficos)
            - **Urbano**: {stats['urbano']} resíduos (RSU, RPO, Lodo de Esgoto)
            - **Total Realista**: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)
            - **SAF Validado**: {stats['saf_percentage']}% dos resíduos com fatores de disponibilidade calibrados
            """)

    st.markdown("---")


def render_saf_priority_summary():
    """
    Renders SAF priority summary with metric cards using real data.
    """
    stats = _get_residue_stats()

    st.markdown("## 📈 Status Atual")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Resíduos Disponíveis", str(stats['total']),
                  help=f"Agricultura ({stats['agricultura']}), Pecuária ({stats['pecuaria']}), Industrial ({stats['industrial']}), Urbano ({stats['urbano']}) - Phase 5 Complete")

    with col2:
        st.metric("🎯 SAF Validação", f"{stats['saf_percentage']}%",
                  help=f"{stats['saf_validated']}/{stats['total']} resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)")

    with col3:
        st.metric("🔬 Parâmetros Químicos", "15+",
                  help="BMP, TS, VS, C:N, CH₄, pH, COD, N, C, P, K com ranges MIN/MEAN/MAX de literatura")

    with col4:
        st.metric("⚗️ Potencial Realista", "6.939 Mi m³/ano",
                  help="Cenário Realista com fatores SAF validados - 297% meta FIESP-SP")


def render_sector_overview():
    """
    Renders sector breakdown using real data from residue registry.
    """
    stats = _get_residue_stats()

    st.markdown("---")

    st.markdown(f"## ✅ Banco de Dados Completo CP2B - Phase 5 ({stats['saf_percentage']}% SAF Validado)")

    col1, col2 = st.columns(2)

    with col1:
        # Agriculture sector
        st.markdown(f"### 🌾 Agricultura ({stats['agricultura']} resíduos)")

        # Get top SAF performers for Agricultura
        top_agr = _get_top_saf_performers('Agricultura', 4)

        if top_agr:
            saf_lines = []
            icons = ['🥇', '🏆', '✅', '⭐']
            for i, (name, saf, tier) in enumerate(top_agr):
                icon = icons[i] if i < len(icons) else '•'
                saf_lines.append(f"- {icon} **{name}**: {saf:.2f}% - {tier}")

            st.success("**🏆 Top Performers SAF**\n" + '\n'.join(saf_lines))
        else:
            st.info("**ℹ️ SAF em Desenvolvimento**\nDados SAF em processo de validação")

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

        # Pecuária sector
        st.markdown(f"### 🐄 Pecuária ({stats['pecuaria']} resíduos)")

        top_pec = _get_top_saf_performers('Pecuária', 3)

        if top_pec:
            saf_lines = []
            for i, (name, saf, tier) in enumerate(top_pec):
                saf_lines.append(f"- {'⭐' if i == 0 else '•'} **{name}**: {saf:.2f}% - {tier}")
            st.info("**⭐ Destaque SAF**\n" + '\n'.join(saf_lines))
        else:
            st.info("**ℹ️ SAF em Desenvolvimento**\nDados SAF em processo de validação")

        st.markdown("""
        - 🐄 **Dejetos Bovinos** (Leite + Corte)
        - 🐷 **Dejetos de Suínos**
        - 🐔 **Cama de Frango**
        - 🥚 **Dejetos de Codornas**
        - 🐮 **Efluentes de Laticínios**
        """)

    with col2:
        # Industrial sector
        st.markdown(f"### 🏭 Industrial ({stats['industrial']} resíduos)")

        top_ind = _get_top_saf_performers('Industrial', 3)

        if top_ind:
            saf_lines = []
            for i, (name, saf, tier) in enumerate(top_ind):
                saf_lines.append(f"- {'🥇' if i == 0 else '•'} **{name}**: {saf:.2f}% - {tier}")
            st.success("**🥇 Top Performer**\n" + '\n'.join(saf_lines))
        else:
            st.info("**ℹ️ SAF em Desenvolvimento**\nDados SAF em processo de validação")

        st.markdown("""
        - 🥛 **Soro de Laticínios** (EXCELENTE)
        - 🍺 **Bagaço de Cervejarias**
        - 🥩 **Efluente de Frigoríficos**
        - 🍹 **Resíduos de Processamento**
        - 🏭 **Efluentes Industriais**
        """)

        st.markdown("")  # Spacing

        # Urbano sector
        st.markdown(f"### 🏙️ Urbano ({stats['urbano']} resíduos)")

        top_urb = _get_top_saf_performers('Urbano', 3)

        if top_urb:
            saf_lines = []
            for i, (name, saf, tier) in enumerate(top_urb):
                saf_lines.append(f"- {'⭐' if i == 0 else '•'} **{name}**: {saf:.2f}% - {tier}")
            st.info("**⭐ Destaque SAF**\n" + '\n'.join(saf_lines))
        else:
            st.info("**ℹ️ SAF em Desenvolvimento**\nDados SAF em processo de validação")

        st.markdown("""
        - 🗑️ **RSU** (Resíduo Sólido Urbano)
        - 🌳 **RPO** (Resíduos de Poda Urbana)
        - 💧 **Lodo de Esgoto** (ETE)
        - 🍂 **Galhos e Folhas**
        """)

    # SAF Summary with real data
    st.warning(f"""
    **💡 Metodologia SAF - Phase 5 ✅ COMPLETO**

    - ✅ **{stats['saf_validated']}/{stats['total']} resíduos** com SAF validado ({stats['saf_percentage']}%)
    - 🎯 Fatores calibrados: **FC, FCp, FS, FL**
    - 📊 Cenários: Pessimista, **Realista ⭐**, Otimista, Teórico
    - 📈 Total Realista: **6.939 Mi m³/ano CH₄** (297% meta FIESP-SP)
    - 🏆 Resíduos com SAF calculado: **{stats['saf_with_values']}** resíduos
    """)

    st.markdown("---")


def render_footer():
    """
    Renders the footer with platform information using real data.
    """
    stats = _get_residue_stats()

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h3>🧪 PanoramaCP2B</h3>
        <p><strong>Centro Paulista de Estudos em Biogás e Bioprodutos</strong></p>
        <p>Plataforma de Validação Laboratorial para Pesquisa em Biogás</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Phase 5 Complete - SAF Validated Platform")

    st.markdown(f"""
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
        <p>📊 {stats['total']} Resíduos • 🎯 {stats['saf_percentage']}% SAF Coverage • 📚 20+ Referências • 🗺️ 645 Municípios</p>
        <p style='font-style: italic;'>💡 Use a barra lateral esquerda para navegar entre as páginas</p>
        <p style='font-size: 0.8rem; color: #9ca3af;'>Última atualização: Outubro 2025 • Version 2.0 • UNICAMP</p>
    </div>
    """, unsafe_allow_html=True)
