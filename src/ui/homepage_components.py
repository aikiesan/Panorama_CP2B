"""
Homepage UI Components - PanoramaCP2B
Following SOLID principles - Single Responsibility for each component
Elegant, minimalistic scientific design aesthetic with improved UI/UX
"""

import streamlit as st


def render_hero_section():
    """
    Renders the hero section with platform title and Phase 5 statistics.
    Enhanced with better visual hierarchy and glassmorphism effects.
    """
    st.markdown("""
    <div style='background: linear-gradient(135deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
                color: white; padding: 3rem 2rem; margin: -1rem -1rem 1.5rem -1rem;
                text-align: center; border-radius: 0 0 25px 25px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
        <h1 style='margin: 0; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;'>
            🧪 PanoramaCP2B
        </h1>
        <h2 style='margin: 12px 0 0 0; font-size: 1.3rem; opacity: 0.95; font-weight: 400;'>
            Centro Paulista de Estudos em Biogás e Bioprodutos
        </h2>
        <p style='margin: 15px 0 20px 0; font-size: 1rem; opacity: 0.9; font-weight: 300;'>
            Plataforma de Validação Laboratorial para Pesquisa em Biogás
        </p>

        <!-- Phase 5 Badge -->
        <div style='display: inline-block; background: rgba(16, 185, 129, 0.2);
                    border: 2px solid rgba(16, 185, 129, 0.5); border-radius: 20px;
                    padding: 0.5rem 1.2rem; margin: 10px 0 20px 0; backdrop-filter: blur(10px);'>
            <span style='font-weight: 600; font-size: 0.9rem;'>✅ Phase 5 Complete - SAF Validated</span>
        </div>

        <!-- Stats Grid -->
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 1rem; max-width: 900px; margin: 0 auto; margin-top: 1.5rem;'>
            <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
                        border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.2);'>
                <div style='font-size: 2rem; font-weight: 700;'>38</div>
                <div style='font-size: 0.85rem; opacity: 0.9;'>Resíduos Validados</div>
            </div>
            <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
                        border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.2);'>
                <div style='font-size: 2rem; font-weight: 700;'>84%</div>
                <div style='font-size: 0.85rem; opacity: 0.9;'>SAF Coverage</div>
            </div>
            <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
                        border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.2);'>
                <div style='font-size: 2rem; font-weight: 700;'>20+</div>
                <div style='font-size: 0.85rem; opacity: 0.9;'>Referências</div>
            </div>
            <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
                        border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,0.2);'>
                <div style='font-size: 2rem; font-weight: 700;'>645</div>
                <div style='font-size: 0.85rem; opacity: 0.9;'>Municípios SP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_about_section():
    """
    Renders the about section with elegant card design.
    """
    st.markdown("## 🎯 Sobre a Plataforma")

    st.markdown("""
    <div style='background: white; border: 1px solid #e5e7eb; border-radius: 12px;
                padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
        <p style='margin: 0 0 1rem 0; line-height: 1.6;'>
            O <strong>PanoramaCP2B</strong> é uma ferramenta especializada para pesquisadores que trabalham com
            caracterização de resíduos orgânicos e produção de biogás. A plataforma oferece:
        </p>
        <ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
            <li><strong>Dados Validados de Literatura</strong>: Composição química e potencial metanogênico de diversos resíduos</li>
            <li><strong>Ferramenta de Comparação Laboratorial</strong>: Compare seus resultados de laboratório com valores de referência</li>
            <li><strong>Base Científica Completa</strong>: Acesso a referências científicas com DOI e links Scopus</li>
            <li><strong>Metodologia Conservadora</strong>: Fatores de disponibilidade baseados em dados reais de usinas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


def render_phase5_highlights():
    """
    Renders Phase 5 completion highlights with elegant card grid design.
    """
    st.markdown("## 🎉 Novidades - Phase 5 Complete")

    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1rem; margin: 1.5rem 0;'>

        <!-- SAF Validation -->
        <div style='background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
                    border-left: 4px solid #10b981; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>✅</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                SAF Validation Complete
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                84% dos resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL)
            </div>
        </div>

        <!-- CH4 & C:N -->
        <div style='background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
                    border-left: 4px solid #3b82f6; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🔬</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                CH₄ & C:N Parameters
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                Novos parâmetros químicos: produção de metano e relação Carbono:Nitrogênio
            </div>
        </div>

        <!-- Database Integration -->
        <div style='background: linear-gradient(135deg, #f5f3ff 0%, #ffffff 100%);
                    border-left: 4px solid #8b5cf6; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🗺️</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                Database Integration
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                645 municípios com dados de potencial de biogás integrados
            </div>
        </div>

        <!-- Priority Ranking -->
        <div style='background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
                    border-left: 4px solid #f59e0b; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🏆</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                Priority Ranking
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                Classificação por viabilidade: EXCEPCIONAL → INVIÁVEL
            </div>
        </div>

        <!-- Golden Page 2 -->
        <div style='background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
                    border-left: 4px solid #ec4899; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🚀</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                Golden Page 2
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                Parâmetros Químicos reformulados com visualizações avançadas
            </div>
        </div>

        <!-- Literature Ranges -->
        <div style='background: linear-gradient(135deg, #ecfeff 0%, #ffffff 100%);
                    border-left: 4px solid #06b6d4; border-radius: 12px; padding: 1.2rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📊</div>
            <div style='font-weight: 600; font-size: 1.05rem; color: #1f2937; margin-bottom: 0.5rem;'>
                Literature Ranges
            </div>
            <div style='font-size: 0.9rem; color: #6b7280; line-height: 1.5;'>
                Ranges MIN/MEAN/MAX validados para todos os parâmetros
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


def render_features_grid():
    """
    Renders the main features in a 2-column grid with elegant cards.
    """
    st.markdown("## ✨ Principais Funcionalidades")

    col1, col2 = st.columns(2)

    with col1:
        # Researchers card
        st.markdown("""
        <div style='background: white; border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600; color: #1f2937;'>
                🔬 Para Pesquisadores
            </h3>
            <ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
                <li><strong>Validação de Dados Laboratoriais</strong>: Compare resultados com literatura</li>
                <li><strong>Análise de Desvios</strong>: Thresholds configurados (±10-20%)</li>
                <li><strong>Status de Validação</strong>: ✅ Dentro / ⚠️ Aceitável / ❌ Fora da faixa</li>
                <li><strong>Exportação de Relatórios</strong>: CSV com comparação completa</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Available data card
        st.markdown("""
        <div style='background: white; border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600; color: #1f2937;'>
                📊 Dados Disponíveis
            </h3>
            <ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
                <li><strong>BMP</strong>: Potencial Metanogênico Bioquímico</li>
                <li><strong>TS/VS</strong>: Sólidos Totais e Voláteis</li>
                <li><strong>C:N</strong>: Relação Carbono:Nitrogênio</li>
                <li><strong>CH₄</strong>: Produção específica de metano</li>
                <li><strong>pH, COD, TAN</strong>: Parâmetros operacionais</li>
                <li><strong>Composição</strong>: N, C, P, K, proteína</li>
                <li><strong>SAF</strong>: Fatores de Disponibilidade (FC, FCp, FS, FL)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Scientific base card
        st.markdown("""
        <div style='background: white; border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600; color: #1f2937;'>
                📚 Base Científica
            </h3>
            <ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
                <li><strong>Referências Validadas</strong>: Artigos peer-reviewed com DOI</li>
                <li><strong>Scopus Indexados</strong>: Links diretos para base Scopus</li>
                <li><strong>Principais Achados</strong>: Resumo dos resultados relevantes</li>
                <li><strong>Exportação Bibliográfica</strong>: BibTeX, RIS, CSV</li>
                <li><strong>Cobertura</strong>: 20+ resíduos com referências completas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Residues included card
        st.markdown("""
        <div style='background: white; border: 1px solid #e5e7eb; border-radius: 12px;
                    padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600; color: #1f2937;'>
                🌾 Resíduos Incluídos (38 Total)
            </h3>
            <ul style='margin: 0; padding-left: 1.5rem; line-height: 1.8;'>
                <li><strong>Agricultura</strong>: 24 resíduos (Cana, Citros, Café, Milho, Soja)</li>
                <li><strong>Pecuária</strong>: 5 resíduos (Bovinos, Suínos, Aves, Codornas)</li>
                <li><strong>Industrial</strong>: 5 resíduos (Laticínios, Cervejarias, Frigoríficos)</li>
                <li><strong>Urbano</strong>: 4 resíduos (RSU, RPO, Lodo de Esgoto)</li>
                <li><strong>Total Realista</strong>: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)</li>
                <li><strong>SAF Validado</strong>: 84% dos resíduos com fatores calibrados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


def render_saf_priority_summary():
    """
    Renders SAF priority summary with enhanced metric cards.
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
    Renders sector breakdown with elegant cards and top performers.
    """
    st.markdown("---")

    st.markdown("## ✅ Banco de Dados Completo CP2B - Phase 5 (84% SAF Validado)")

    col1, col2 = st.columns(2)

    with col1:
        # Agriculture sector
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
                    border: 1px solid #d1fae5; border-radius: 12px; padding: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 700; color: #1f2937;'>
                🌾 Agricultura (24 resíduos)
            </h3>

            <div style='background: rgba(16,185,129,0.1); border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;'>
                <div style='font-weight: 600; font-size: 0.9rem; color: #059669; margin-bottom: 0.5rem;'>
                    🏆 Top Performers SAF
                </div>
                <div style='font-size: 0.85rem; color: #1f2937; line-height: 1.6;'>
                    • 🥇 <strong>Bagaço de cana</strong>: 80.75% - EXCEPCIONAL<br>
                    • 🏆 <strong>Torta de Filtro</strong>: 12.88% - MUITO BOM<br>
                    • ✅ <strong>Mucilagem de Café</strong>: 11.90% - MUITO BOM<br>
                    • ⭐ <strong>Vinhaça de Cana</strong>: 10.26% - BOM
                </div>
            </div>

            <div style='font-weight: 600; font-size: 0.95rem; color: #374151; margin-bottom: 0.5rem;'>
                Principais Culturas:
            </div>
            <div style='font-size: 0.85rem; color: #6b7280; line-height: 1.7;'>
                • 🌾 <strong>Cana-de-açúcar</strong>: 4 resíduos (Bagaço, Torta, Vinhaça, Palha)<br>
                • 🍊 <strong>Citros</strong>: 2 resíduos (Bagaço, Cascas)<br>
                • ☕ <strong>Café</strong>: 2 resíduos (Mucilagem, Casca/Polpa)<br>
                • 🌽 <strong>Milho</strong>: 2 resíduos (Palha, Sabugo)<br>
                • 🌱 <strong>Soja</strong>: 2 resíduos (Palha, Casca)<br>
                • 🌳 <strong>+ 12 outros</strong> resíduos agrícolas
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Livestock sector
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
                    border: 1px solid #fef3c7; border-radius: 12px; padding: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 700; color: #1f2937;'>
                🐄 Pecuária (5 resíduos)
            </h3>

            <div style='background: rgba(245,158,11,0.1); border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;'>
                <div style='font-weight: 600; font-size: 0.9rem; color: #d97706; margin-bottom: 0.5rem;'>
                    ⭐ Destaque SAF
                </div>
                <div style='font-size: 0.85rem; color: #1f2937;'>
                    • 🐔 <strong>Cama de Frango</strong>: 8.67% - BOM
                </div>
            </div>

            <div style='font-size: 0.85rem; color: #6b7280; line-height: 1.7;'>
                • 🐄 <strong>Dejetos Bovinos</strong> (Leite + Corte)<br>
                • 🐷 <strong>Dejetos de Suínos</strong><br>
                • 🐔 <strong>Cama de Frango</strong><br>
                • 🥚 <strong>Dejetos de Codornas</strong><br>
                • 🐮 <strong>Efluentes de Laticínios</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Industrial sector
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f5f3ff 0%, #ffffff 100%);
                    border: 1px solid #e9d5ff; border-radius: 12px; padding: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 700; color: #1f2937;'>
                🏭 Industrial (5 resíduos)
            </h3>

            <div style='background: rgba(139,92,246,0.1); border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;'>
                <div style='font-weight: 600; font-size: 0.9rem; color: #7c3aed; margin-bottom: 0.5rem;'>
                    🥇 Top Performer
                </div>
                <div style='font-size: 0.85rem; color: #1f2937;'>
                    • 🥛 <strong>Soro de Laticínios</strong>: 30.40% - EXCELENTE
                </div>
            </div>

            <div style='font-size: 0.85rem; color: #6b7280; line-height: 1.7;'>
                • 🥛 <strong>Soro de Laticínios</strong> (EXCELENTE)<br>
                • 🍺 <strong>Bagaço de Cervejarias</strong><br>
                • 🥩 <strong>Efluente de Frigoríficos</strong><br>
                • 🍹 <strong>Resíduos de Processamento</strong><br>
                • 🏭 <strong>Efluentes Industriais</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Urban sector
        st.markdown("""
        <div style='background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
                    border: 1px solid #dbeafe; border-radius: 12px; padding: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem;'>
            <h3 style='margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 700; color: #1f2937;'>
                🏙️ Urbano (4 resíduos)
            </h3>

            <div style='background: rgba(59,130,246,0.1); border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;'>
                <div style='font-weight: 600; font-size: 0.9rem; color: #2563eb; margin-bottom: 0.5rem;'>
                    ⭐ Destaque SAF
                </div>
                <div style='font-size: 0.85rem; color: #1f2937;'>
                    • 🗑️ <strong>RSU</strong>: 9.88% - BOM
                </div>
            </div>

            <div style='font-size: 0.85rem; color: #6b7280; line-height: 1.7;'>
                • 🗑️ <strong>RSU</strong> (Resíduo Sólido Urbano)<br>
                • 🌳 <strong>RPO</strong> (Resíduos de Poda Urbana)<br>
                • 💧 <strong>Lodo de Esgoto</strong> (ETE)<br>
                • 🍂 <strong>Galhos e Folhas</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # SAF Summary
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
                border: 2px solid #fde68a; border-radius: 12px; padding: 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08); max-width: 800px; margin: 2rem auto;'>
        <div style='font-weight: 700; font-size: 1.1rem; color: #92400e; margin-bottom: 0.8rem;'>
            💡 Metodologia SAF - Phase 5 ✅ COMPLETO
        </div>
        <div style='font-size: 0.9rem; color: #78350f; line-height: 1.8;'>
            ✅ <strong>32/38 resíduos</strong> com SAF validado (84%)<br>
            🎯 Fatores calibrados: <strong>FC, FCp, FS, FL</strong><br>
            📊 Cenários: Pessimista, <strong>Realista ⭐</strong>, Otimista, Teórico<br>
            📈 Total Realista: <strong>6.939 Mi m³/ano CH₄</strong> (297% meta FIESP-SP)<br>
            🏆 Priority Tiers: 1 EXCEPCIONAL, 3 EXCELENTE, 7 BOM/MUITO BOM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


def render_footer():
    """
    Renders the footer with platform information and version.
    Enhanced design with better information hierarchy.
    """
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2.5rem;
                background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
                border-radius: 20px; margin-top: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
        <h3 style='color: #059669; margin-bottom: 0.8rem; font-size: 1.8rem; font-weight: 700;'>
            🧪 PanoramaCP2B
        </h3>
        <p style='font-size: 1.1rem; color: #374151; margin-bottom: 0.5rem;'>
            <strong>Centro Paulista de Estudos em Biogás e Bioprodutos</strong>
        </p>
        <p style='font-size: 0.95rem; color: #6b7280;'>
            Plataforma de Validação Laboratorial para Pesquisa em Biogás
        </p>

        <div style='background: rgba(5,150,105,0.1); border-radius: 12px; padding: 0.8rem;
                    margin: 1.5rem auto; max-width: 600px;'>
            <p style='font-size: 0.95rem; color: #059669; margin: 0; font-weight: 600;'>
                ✅ Phase 5 Complete - SAF Validated Platform
            </p>
        </div>

        <p style='font-size: 0.85rem; color: #9ca3af; margin-top: 1rem;'>
            📊 38 Resíduos • 🎯 84% SAF Coverage • 📚 20+ Referências • 🗺️ 645 Municípios
        </p>
        <p style='font-size: 0.8rem; color: #9ca3af; margin-top: 1.5rem; font-style: italic;'>
            💡 Use a barra lateral esquerda para navegar entre as páginas
        </p>
        <p style='font-size: 0.75rem; color: #d1d5db; margin-top: 1rem;'>
            Última atualização: Outubro 2025 • Version 2.0 • UNICAMP
        </p>
    </div>
    """, unsafe_allow_html=True)
