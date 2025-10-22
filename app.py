"""
PanoramaCP2B - Centro Paulista de Estudos em Biogás e Bioprodutos
Homepage - Laboratory Validation Tool for Biogas Research
Modern UI/UX Redesign - Phase 5 Complete Edition
"""

import streamlit as st
from src.ui.main_navigation import render_main_navigation, render_navigation_divider


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PanoramaCP2B - Validação Laboratorial | Phase 5 Complete",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ============================================================================
# MODERN HERO SECTION WITH ANIMATIONS
# ============================================================================

st.markdown("""
<style>
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float-badge {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes fade-in-up {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(5, 150, 105, 0.4),
                    0 0 40px rgba(37, 99, 235, 0.3),
                    0 0 60px rgba(124, 58, 237, 0.2);
    }
    50% {
        box-shadow: 0 0 30px rgba(5, 150, 105, 0.6),
                    0 0 60px rgba(37, 99, 235, 0.5),
                    0 0 90px rgba(124, 58, 237, 0.4);
    }
}

.hero-modern {
    background: linear-gradient(-45deg, #059669, #2563eb, #7c3aed, #10b981);
    background-size: 400% 400%;
    animation: gradient-shift 15s ease infinite;
    color: white;
    padding: 3.5rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    text-align: center;
    border-radius: 0 0 30px 30px;
    position: relative;
    overflow: hidden;
    animation: pulse-glow 3s ease-in-out infinite;
}

.hero-modern::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-content {
    position: relative;
    z-index: 1;
    animation: fade-in-up 0.8s ease-out;
}

.hero-title-modern {
    font-size: 3.5rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
    text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle-modern {
    font-size: 1.5rem;
    font-weight: 500;
    margin: 1rem 0;
    opacity: 0.95;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.hero-tagline {
    font-size: 1.1rem;
    font-weight: 300;
    margin: 0.8rem 0 2rem 0;
    opacity: 0.9;
}

.hero-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    max-width: 1200px;
    margin: 2.5rem auto 0;
}

.stat-card-hero {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    animation: fade-in-up 0.8s ease-out backwards;
}

.stat-card-hero:nth-child(1) { animation-delay: 0.1s; }
.stat-card-hero:nth-child(2) { animation-delay: 0.2s; }
.stat-card-hero:nth-child(3) { animation-delay: 0.3s; }
.stat-card-hero:nth-child(4) { animation-delay: 0.4s; }

.stat-card-hero:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.stat-label {
    font-size: 0.95rem;
    font-weight: 500;
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}

.stat-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.achievement-badge {
    display: inline-block;
    background: rgba(16, 185, 129, 0.2);
    border: 2px solid rgba(16, 185, 129, 0.5);
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    margin: 1.5rem 0.5rem 0;
    font-weight: 600;
    font-size: 0.9rem;
    animation: float-badge 3s ease-in-out infinite;
    backdrop-filter: blur(5px);
}

.achievement-badge:hover {
    background: rgba(16, 185, 129, 0.3);
    transform: scale(1.05);
}

@media (max-width: 768px) {
    .hero-title-modern { font-size: 2.2rem; }
    .hero-subtitle-modern { font-size: 1.1rem; }
    .hero-stats-grid { grid-template-columns: 1fr; gap: 1rem; }
    .stat-value { font-size: 2rem; }
    .hero-modern { padding: 2rem 1rem; }
}
</style>

<div class="hero-modern">
    <div class="hero-content">
        <h1 class="hero-title-modern">
            🧪 PanoramaCP2B
        </h1>
        <h2 class="hero-subtitle-modern">
            Centro Paulista de Estudos em Biogás e Bioprodutos
        </h2>
        <p class="hero-tagline">
            Plataforma de Validação Laboratorial para Pesquisa em Biogás
        </p>

        <div class="hero-stats-grid">
            <div class="stat-card-hero">
                <div class="stat-icon">📚</div>
                <div class="stat-value">38</div>
                <div class="stat-label">Resíduos Validados</div>
            </div>
            <div class="stat-card-hero">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">84%</div>
                <div class="stat-label">SAF Coverage</div>
            </div>
            <div class="stat-card-hero">
                <div class="stat-icon">📖</div>
                <div class="stat-value">20+</div>
                <div class="stat-label">Referências Científicas</div>
            </div>
            <div class="stat-card-hero">
                <div class="stat-icon">🗺️</div>
                <div class="stat-value">645</div>
                <div class="stat-label">Municípios</div>
            </div>
        </div>

        <div>
            <span class="achievement-badge">✅ Phase 5 Complete</span>
            <span class="achievement-badge">🏆 32/38 Resíduos SAF Validados</span>
            <span class="achievement-badge">🚀 Golden Page 2 Released</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# NAVIGATION - Horizontal Bar
# ============================================================================

render_main_navigation(current_page="home")
render_navigation_divider()


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
# PHASE 5 HIGHLIGHTS - MODERN DESIGN
# ============================================================================

st.markdown("""
<style>
.phase5-container {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 50%, #faf5ff 100%);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    border: 2px solid #d1fae5;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
}

.phase5-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #059669 0%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2rem;
}

.updates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.update-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 5px solid;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    animation: fade-in-up 0.6s ease-out backwards;
}

.update-card:nth-child(1) {
    border-left-color: #10b981;
    animation-delay: 0.1s;
}

.update-card:nth-child(2) {
    border-left-color: #3b82f6;
    animation-delay: 0.2s;
}

.update-card:nth-child(3) {
    border-left-color: #8b5cf6;
    animation-delay: 0.3s;
}

.update-card:nth-child(4) {
    border-left-color: #f59e0b;
    animation-delay: 0.4s;
}

.update-card:nth-child(5) {
    border-left-color: #ec4899;
    animation-delay: 0.5s;
}

.update-card:nth-child(6) {
    border-left-color: #6366f1;
    animation-delay: 0.6s;
}

.update-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

.update-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.update-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.update-description {
    font-size: 0.95rem;
    color: #6b7280;
    line-height: 1.5;
}

.status-badge {
    display: inline-block;
    background: #10b981;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
</style>

<div class="phase5-container">
    <h2 class="phase5-title">🎉 Novidades - Phase 5 Complete</h2>

    <div class="updates-grid">
        <div class="update-card">
            <div class="update-icon">✅</div>
            <span class="status-badge">COMPLETE</span>
            <div class="update-title">SAF Validation</div>
            <div class="update-description">
                84% dos resíduos com fatores de disponibilidade calibrados (FC, FCp, FS, FL). Sistema validado com dados operacionais reais.
            </div>
        </div>

        <div class="update-card">
            <div class="update-icon">🔬</div>
            <span class="status-badge">NEW</span>
            <div class="update-title">CH₄ & C:N Parameters</div>
            <div class="update-description">
                Novos parâmetros químicos adicionados: produção específica de metano (ml CH₄/g VS) e relação Carbono:Nitrogênio.
            </div>
        </div>

        <div class="update-card">
            <div class="update-icon">🗺️</div>
            <span class="status-badge">INTEGRATED</span>
            <div class="update-title">Database Integration</div>
            <div class="update-description">
                645 municípios com dados de potencial de biogás integrados. Cobertura completa do Estado de São Paulo.
            </div>
        </div>

        <div class="update-card">
            <div class="update-icon">🏆</div>
            <span class="status-badge">ENHANCED</span>
            <div class="update-title">Priority Ranking</div>
            <div class="update-description">
                Sistema de classificação por viabilidade: EXCEPCIONAL → EXCELENTE → BOM → REGULAR → BAIXO → INVIÁVEL.
            </div>
        </div>

        <div class="update-card">
            <div class="update-icon">🚀</div>
            <span class="status-badge">RELEASED</span>
            <div class="update-title">Golden Page 2</div>
            <div class="update-description">
                Página de Parâmetros Químicos completamente reformulada com visualizações avançadas e comparações interativas.
            </div>
        </div>

        <div class="update-card">
            <div class="update-icon">📊</div>
            <span class="status-badge">VALIDATED</span>
            <div class="update-title">Literature Ranges</div>
            <div class="update-description">
                Ranges MIN/MEAN/MAX de literatura científica validada para todos os parâmetros com 20+ referências peer-reviewed.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================================
# KEY FEATURES - MODERN CARDS
# ============================================================================

st.markdown("""
<style>
.features-section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 3rem 0 2rem 0;
    background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.feature-card-modern {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.feature-card-modern::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #059669, #2563eb, #7c3aed);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}

.feature-card-modern:hover::before {
    transform: scaleX(1);
}

.feature-card-modern:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    border-color: #e5e7eb;
}

.feature-icon-large {
    font-size: 3rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.feature-card-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1.2rem;
}

.feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.feature-list li {
    padding: 0.6rem 0;
    border-bottom: 1px solid #f3f4f6;
    color: #4b5563;
    line-height: 1.6;
    transition: all 0.2s ease;
}

.feature-list li:last-child {
    border-bottom: none;
}

.feature-list li:hover {
    padding-left: 0.5rem;
    color: #059669;
}

.feature-list strong {
    color: #1f2937;
    font-weight: 600;
}

@media (max-width: 1200px) {
    .features-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<h2 class="features-section-title">✨ Principais Funcionalidades</h2>

<div class="features-grid">
    <div class="feature-card-modern">
        <div class="feature-icon-large">🔬</div>
        <h3 class="feature-card-title">Para Pesquisadores</h3>
        <ul class="feature-list">
            <li><strong>Validação de Dados Laboratoriais</strong>: Compare seus resultados com valores de literatura validada</li>
            <li><strong>Análise de Desvios</strong>: Thresholds configurados por parâmetro (±10-20%)</li>
            <li><strong>Status de Validação</strong>: ✅ Dentro da faixa / ⚠️ Desvio aceitável / ❌ Fora da faixa</li>
            <li><strong>Exportação de Relatórios</strong>: CSV com comparação completa para análise</li>
        </ul>
    </div>

    <div class="feature-card-modern">
        <div class="feature-icon-large">📊</div>
        <h3 class="feature-card-title">Dados Disponíveis</h3>
        <ul class="feature-list">
            <li><strong>BMP</strong>: Potencial Metanogênico Bioquímico (ml CH₄/g VS)</li>
            <li><strong>TS/VS</strong>: Sólidos Totais e Voláteis (% massa úmida)</li>
            <li><strong>C:N</strong>: Relação Carbono:Nitrogênio (balanço nutricional)</li>
            <li><strong>CH₄</strong>: Produção específica de metano (ml CH₄/g VS)</li>
            <li><strong>pH, COD, TAN</strong>: Parâmetros operacionais</li>
            <li><strong>Composição</strong>: N, C, P, K, proteína (% massa seca)</li>
            <li><strong>SAF</strong>: Fatores de Disponibilidade (FC, FCp, FS, FL)</li>
        </ul>
    </div>

    <div class="feature-card-modern">
        <div class="feature-icon-large">📚</div>
        <h3 class="feature-card-title">Base Científica</h3>
        <ul class="feature-list">
            <li><strong>Referências Validadas</strong>: Artigos peer-reviewed com DOI completo</li>
            <li><strong>Scopus Indexados</strong>: Links diretos para base Scopus</li>
            <li><strong>Principais Achados</strong>: Resumo dos resultados mais relevantes</li>
            <li><strong>Exportação Bibliográfica</strong>: BibTeX, RIS, CSV</li>
            <li><strong>Cobertura</strong>: 20+ resíduos com referências científicas completas</li>
        </ul>
    </div>

    <div class="feature-card-modern">
        <div class="feature-icon-large">🌾</div>
        <h3 class="feature-card-title">Resíduos Incluídos (38 Total)</h3>
        <ul class="feature-list">
            <li><strong>Agricultura</strong>: 24 resíduos (Cana, Citros, Café, Milho, Soja, etc.)</li>
            <li><strong>Pecuária</strong>: 5 resíduos (Bovinos, Suínos, Aves, Codornas)</li>
            <li><strong>Industrial</strong>: 5 resíduos (Laticínios, Cervejarias, Frigoríficos)</li>
            <li><strong>Urbano</strong>: 4 resíduos (RSU, RPO, Lodo de Esgoto)</li>
            <li><strong>Total Realista</strong>: 6.939 Mi m³ CH₄/ano (297% meta FIESP-SP)</li>
            <li><strong>SAF Validado</strong>: 84% dos resíduos com fatores calibrados</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================================
# METHODOLOGY OVERVIEW
# ============================================================================

st.markdown("## 📖 Metodologia - Sobre a Metodologia Utilizada")

with st.expander("📋 Clique para expandir a documentação completa", expanded=False):
    st.markdown("""
    # Documentação Completa da Metodologia - PanoramaCP2B

    ## 1️⃣ Visão Geral da Plataforma

    O **PanoramaCP2B** é uma plataforma de validação laboratorial desenvolvida pelo Centro Paulista de Estudos em Biogás
    e Bioprodutos (UNICAMP) para pesquisa em biogás. O sistema utiliza uma **metodologia conservadora e baseada em dados reais**
    para estimar o potencial de geração de biogás a partir de resíduos orgânicos no Estado de São Paulo.

    **Objetivos principais:**
    - Fornecer estimativas realistas de disponibilidade de resíduos para biogás
    - Permitir validação de dados laboratoriais contra literatura científica
    - Oferecer base científica completa com referências verificadas
    - Suportar tomada de decisão em políticas públicas e planejamento energético

    ---

    ## 2️⃣ Fontes de Dados Primárias

    ### IBGE/SIDRA - Produção Agrícola
    - **Fonte**: Sistema IBGE de Recuperação de Dados (SIDRA)
    - **Dados**: Produção agrícola por município, área cultivada, rendimento
    - **Frequência**: Anual (último ano disponível)
    - **Cobertura**: Todas as culturas principais de SP

    ### MapBiomas - Cobertura e Uso do Solo
    - **Fonte**: MapBiomas Brasil (mapeamento por satélite)
    - **Dados**: Cobertura vegetal, áreas de pastagem, silvicultura
    - **Resolução**: 30 metros por pixel
    - **Aplicação**: Validação de áreas agrícolas e pecuárias

    ### Secretaria de Defesa Agropecuária - Rebanhos
    - **Fonte**: Coordenadoria de Defesa Agropecuária (CDA/SP)
    - **Dados**: População de bovinos (leite/corte), suínos, aves
    - **Frequência**: Anual
    - **Precisão**: Oficial - Governo do Estado de SP

    ### NIPE/UNICAMP - Fatores de Conversão
    - **Fonte**: Núcleo Interdisciplinar de Planejamento Energético (NIPE)
    - **Dados**: Fatores de conversão para biogás, potencial metanogênico
    - **Base**: 15+ artigos científicos peer-reviewed
    - **Aplicação**: Cálculos de disponibilidade real

    ---

    ## 3️⃣ Metodologia SAF - Fatores de Disponibilidade

    ### Fórmula Geral

    ```
    DISPONIBILIDADE_FINAL = FC × (1 - FCp) × FS × FL × 100%
    ```

    Onde:
    - **FC** = Fator de Coleta (viabilidade técnica)
    - **FCp** = Fator de Competição (usos alternativos)
    - **FS** = Fator Sazonalidade (variação anual)
    - **FL** = Fator Logístico (restrições de transporte)

    ### 🔹 FC - Fator de Coleta (0 a 1)

    Representa a **viabilidade técnica de coleta e processamento** do resíduo.

    | Intervalo | Classificação | Exemplos | Pressupostos |
    |-----------|---------------|----------|-------------|
    | 0.95-1.0 | Muito Alto | Bagaço de cana (usinas), Efluentes | Processamento no local |
    | 0.80-0.95 | Alto | Vinhaça, Cama de frango | Sistema existente ou viável |
    | 0.60-0.80 | Médio | Palha de cana, Dejetos bovinos | Requer investimento logístico |
    | 0.40-0.60 | Baixo | Palha de soja, Cascas de frutas | Disperso, custo alto |
    | <0.40 | Muito Baixo | Resíduos urbanos dispersos | Não operacional |

    **Como é calculado:**
    - Análise de usinas existentes (dados operacionais)
    - Avaliação de infraestrutura disponível
    - Custos de coleta e transporte
    - Perdas no processo de coleta

    ### 🔹 FCp - Fator de Competição (0 a 1)

    Representa a **fração do resíduo já utilizada em usos alternativos**.

    | Resíduo | Uso Alternativo Principal | FCp | Notas |
    |---------|---------------------------|-----|-------|
    | Bagaço de cana | Combustível em usinas | 1.0 | Já utilizado 100% |
    | Vinhaça | Fertilizante agrícola | 0.65 | 65% demanda mercado |
    | Cama de frango | Alimento ruminante | 0.60 | Uso consolidado |
    | Palha de cana | Cobertura de solo | 0.65 | Práticas agrícolas |
    | Dejetos bovinos | Fertilizante direto | 0.40 | Alguns usos alternativos |

    **Pressupostos:**
    - FCp = 1.0 significa 100% do resíduo é competido por outros usos
    - FCp = 0.0 significa nenhuma competição (disponível 100%)
    - Valores baseados em análise de mercado e pesquisas setoriais

    ### 🔹 FS - Fator Sazonalidade (0.7 a 1.0)

    Representa a **variação na disponibilidade ao longo do ano**.

    | Tipo | Padrão | FS | Período Crítico |
    |------|--------|-----|-----------------|
    | Contínuo | Disponível ano todo | 1.0 | Nenhum |
    | Sazonal concentrado | 4-6 meses safra | 0.70-0.75 | Meses de safra |
    | Sazonal moderado | 7-10 meses | 0.80-0.90 | Baixa em entressafra |
    | Semi-contínuo | 10-12 meses | 0.95-0.99 | Mínimo em 1-2 meses |

    **Exemplos práticos:**
    - Vinhaça em usinas: FS = 1.0 (safra concentrada, mas processamento contínuo)
    - Cama de frango: FS = 0.95 (produção contínua com pequenas variações)
    - Palha de cana: FS = 0.70 (apenas durante colheita, Maio-Dezembro)

    ### 🔹 FL - Fator Logístico (0.65 a 1.0)

    Representa a **viabilidade econômica do transporte**.

    | Distância | Viabilidade | FL | Tecnologia |
    |-----------|-------------|-----|-----------|
    | 0-10 km | Muito viável | 1.0 | Coleta direta |
    | 10-20 km | Viável | 0.90 | Caminhões econômicos |
    | 20-30 km | Marginalmente viável | 0.80 | Custos crescentes |
    | 30-50 km | Questionável | 0.70 | Biodigestores móveis |
    | >50 km | Não viável | <0.65 | Impraticável |

    **Pressupostos econômicos:**
    - Custo de combustível: R$ 5.50/litro
    - Rendimento: 6 km/litro
    - Custo de amortização de equipamento
    - Valor de mercado do biogás: ~R$ 1,50/m³

    ---

    ## 4️⃣ Cálculo do Potencial de Biogás

    ### Passo 1: Definir Geração Teórica

    ```
    GERAÇÃO_TEÓRICA = PRODUÇÃO × FATOR_CONVERSÃO
    ```

    Exemplos:
    - **Cana-de-açúcar**: Produção (t) × 0.25 (bagaço kg/t) × BMP residual
    - **Bovinos**: Rebanho (cabeças) × 18 kg/dia de dejetos × 365 dias × BMP
    - **RSU**: População × 1.2 kg/capita/dia × BMP resíduos

    ### Passo 2: Aplicar Fatores de Disponibilidade

    ```
    DISPONIBILIDADE = GERAÇÃO_TEÓRICA × SAF
    ```

    Onde SAF (Surplus Availability Factor) = FC × (1 - FCp) × FS × FL

    ### Passo 3: Calcular Cenários

    **Teórico (100%)**: SAF = 1.0 (sem restrições - não operacional)

    **Otimista**: SAF elevado com pressupostos favoráveis
    - FC máximo, FCp mínimo, FL máximo
    - Exemplo: 80% - 90% do teórico

    **Realista**: SAF calibrado com dados operacionais
    - Baseado em usinas existentes
    - **USAR PARA PLANEJAMENTO** (base recomendada)
    - Exemplo: 25% - 50% do teórico

    **Pessimista**: SAF conservador com pressupostos desfavoráveis
    - FC mínimo, FCp máximo, FL mínimo
    - Exemplo: 10% - 20% do teórico

    ---

    ## 5️⃣ Parâmetros Químicos - Ranges de Literatura

    ### Dados Coletados

    Os seguintes parâmetros são coletados de literatura científica validada:

    | Parâmetro | Sigla | Unidade | Tipo de Dado |
    |-----------|-------|---------|-------------|
    | Potencial Metanogênico Bioquímico | BMP | mL CH₄/g VS | Principal |
    | Sólidos Totais | TS | % | Composição |
    | Sólidos Voláteis | VS | % | Composição |
    | Relação Carbono:Nitrogênio | C:N | - | Balanço |
    | Carbono Orgânico Total | COD | mg/L | Qualidade |
    | pH | pH | - | Condição |
    | Nitrogênio Total | N | % | Composição |
    | Carbono | C | % | Composição |

    ### Método de Coleta de Ranges

    **Busca Sistemática (PRISMA-like):**
    1. Busca em Scopus, Web of Science, SciELO
    2. Filtros: artigos peer-reviewed, últimos 15 anos, contexto tropical
    3. Critérios de inclusão: metodologia clara, dados replicáveis
    4. Extração: MIN, MEAN, MAX de cada parâmetro

    **Exemplo - Vinhaça:**
    - 12 artigos encontrados
    - BMP range: 180 - 280 mL CH₄/g VS (média: 220)
    - C:N ratio: 35 - 80 (média: 55)
    - Referência: Papers de 2015-2023

    ### Validação Laboratorial - Thresholds

    Cada parâmetro possui threshold de desvio aceitável:

    | Parâmetro | Threshold | Justificativa |
    |-----------|-----------|---------------|
    | BMP | ±15% | Variabilidade biológica alta |
    | TS | ±10% | Metodologia gravimétrica precisa |
    | VS | ±12% | Dependente de composição |
    | C:N | ±20% | Composição heterogênea |
    | pH | ±5% | Medição eletrônica precisa |
    | N | ±15% | Método Kjeldahl variável |

    **Interpretação:**
    - ✅ Verde: Dentro do range (< threshold)
    - 🟡 Amarelo: Fora do range mas aceitável (até 1.5x threshold)
    - ❌ Vermelho: Fora do range inaceitável (> 1.5x threshold)

    ---

    ## 6️⃣ Cenários de Disponibilidade - Definições Detalhadas

    ### Cenário 1: TEÓRICO (100%)

    **Definição**: Máxima produção com ZERO restrições

    **Fórmula**:
    ```
    SAF = 1.0 (sem fatores redutivos)
    ```

    **Pressupostos:**
    - Toda produção é coletável
    - Sem competição de mercado
    - Disponível ano inteiro
    - Logística sem limite

    **Quando usar**: Comparações acadêmicas, estimativas superiores

    **Quando NÃO usar**: Planejamento real, investimentos

    ### Cenário 2: OTIMISTA

    **Definição**: Condições favoráveis com tecnologia moderna

    **Fórmula**:
    ```
    SAF = 0.80 a 0.90 (pressupostos otimistas)
    ```

    **Pressupostos:**
    - FC = 0.90 (coleta bem organizada)
    - FCp = 0.30 (pouca competição)
    - FS = 0.95 (sazonalidade mínima)
    - FL = 0.95 (logística eficiente)

    **Quando usar**: Potencial máximo com investimentos

    ### Cenário 3: REALISTA ⭐ (RECOMENDADO)

    **Definição**: Baseado em operações existentes comprovadas

    **Fórmula**:
    ```
    SAF = 0.25 a 0.50 (dados operacionais reais)
    ```

    **Pressupostos:**
    - FC = 0.75 (coleta parcial, limitações reais)
    - FCp = 0.60 (competição significativa)
    - FS = 0.85 (sazonalidade moderada)
    - FL = 0.80 (custos logísticos reais)

    **Quando usar**: **PLANEJAMENTO ESTRATÉGICO** - USE ESTE

    **Base**: Calibrado com usinas funcionando em SP

    ### Cenário 4: PESSIMISTA

    **Definição**: Condições desfavoráveis, fatores limitantes máximos

    **Fórmula**:
    ```
    SAF = 0.10 a 0.20 (pressupostos conservadores)
    ```

    **Pressupostos:**
    - FC = 0.55 (coleta mínima)
    - FCp = 0.80 (alta competição)
    - FS = 0.70 (sazonalidade alta)
    - FL = 0.65 (logística cara)

    **Quando usar**: Análises de risco, piores cenários

    ---

    ## 7️⃣ Limitações e Pressupostos

    ### Limitações Conhecidas

    1. **Dados Agrícolas**
       - IBGE coleta dados anuais (não captura variações sazonais)
       - Alguns municípios têm sub-relatórios
       - Culturas menores podem ter dados agrupados

    2. **Fatores de Conversão**
       - Valores podem variar por cultivar
       - Condições climáticas locais não consideradas
       - BMP varia com método de determinação

    3. **Competição de Mercado**
       - FCp baseado em preços históricos (mercado pode mudar)
       - Não considera novos usos (ex: bioplásticos)
       - Análise pontual em tempo específico

    4. **Logística**
       - FL usa modelo simplificado de distância
       - Não considera infraestrutura viária real
       - Custos de combustível flutuantes

    ### Pressupostos Principais

    1. **Estabilidade de Mercado**: Preços e demandas se mantêm
    2. **Tecnologia Padrão**: Uso de tecnologia convencional
    3. **Legalidade**: Respeito a regulamentações ambientais
    4. **Escala Mínima**: Viabilidade econômica em escala presente

    ---

    ## 8️⃣ Revisão e Atualização

    **Frequência**: Anual (ou quando houver novos dados)

    **Procedimento:**
    1. Coleta de novos dados IBGE/SIDRA
    2. Revisão de literatura recente
    3. Validação com usinas operacionais
    4. Ajuste de fatores se necessário
    5. Publicação de relatório de mudanças

    **Última atualização**: Outubro de 2024

    **Próxima revisão**: Outubro de 2025

    ---

    ## 🏆 Referências Principais

    Base científica do PanoramaCP2B construída com metodologia PRISMA-like utilizando:
    - **30+ artigos peer-reviewed**
    - **Scopus indexados**
    - Contexto Brasil/Tropical
    - Últimos 15 anos de publicações

    Disponíveis na seção **Referências Científicas** da plataforma com links DOI completos.

    ---

    **Documento elaborado por**: Centro Paulista de Estudos em Biogás e Bioprodutos (CP2B/UNICAMP)

    **Versão**: 2.0

    **Data**: Outubro de 2024
    """)

st.markdown("---")


# ============================================================================
# SAF PRIORITY VISUALIZATION & STATUS
# ============================================================================

st.markdown("""
<style>
.status-section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 3rem 0 2.5rem 0;
    background: linear-gradient(135deg, #059669 0%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.priority-showcase {
    background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
    border-radius: 24px;
    padding: 2.5rem;
    margin: 2rem 0;
    border: 2px solid #e5e7eb;
    box-shadow: 0 10px 40px rgba(0,0,0,0.06);
}

.priority-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1.5rem;
    text-align: center;
}

.priority-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.priority-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    border-left: 5px solid;
}

.priority-excepcional {
    border-left-color: #10b981;
    background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
}

.priority-excelente {
    border-left-color: #3b82f6;
    background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
}

.priority-bom {
    border-left-color: #8b5cf6;
    background: linear-gradient(135deg, #f5f3ff 0%, #ffffff 100%);
}

.priority-regular {
    border-left-color: #f59e0b;
    background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
}

.priority-baixo {
    border-left-color: #ef4444;
    background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
}

.priority-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.priority-badge {
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.4rem 0.9rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.8rem;
    color: white;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-excepcional { background: #10b981; }
.badge-excelente { background: #3b82f6; }
.badge-bom { background: #8b5cf6; }
.badge-regular { background: #f59e0b; }
.badge-baixo { background: #ef4444; }

.priority-count {
    font-size: 3rem;
    font-weight: 800;
    color: #1f2937;
    margin: 0.5rem 0;
}

.priority-description {
    font-size: 0.9rem;
    color: #6b7280;
    margin-top: 0.5rem;
}

.priority-range {
    font-size: 1.1rem;
    font-weight: 600;
    color: #374151;
    margin-top: 0.3rem;
}

.top-performers {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}

.performer-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #f3f4f6;
    transition: all 0.2s ease;
}

.performer-item:last-child {
    border-bottom: none;
}

.performer-item:hover {
    background: #f9fafb;
    padding-left: 1.5rem;
}

.performer-rank {
    font-size: 1.5rem;
    font-weight: 700;
    margin-right: 1rem;
    min-width: 40px;
}

.performer-name {
    flex: 1;
    font-weight: 600;
    color: #1f2937;
}

.performer-saf {
    font-size: 1.2rem;
    font-weight: 700;
    color: #10b981;
}
</style>

<h2 class="status-section-title">📈 SAF Priority Distribution & Top Performers</h2>

<div class="priority-showcase">
    <h3 class="priority-title">🏆 Distribuição de Prioridade SAF (32/38 Validados)</h3>

    <div class="priority-grid">
        <div class="priority-card priority-excepcional">
            <span class="priority-badge badge-excepcional">EXCEPCIONAL</span>
            <div class="priority-count">1</div>
            <div class="priority-range">SAF > 70%</div>
            <div class="priority-description">Viabilidade máxima comprovada</div>
        </div>

        <div class="priority-card priority-excelente">
            <span class="priority-badge badge-excelente">EXCELENTE</span>
            <div class="priority-count">3</div>
            <div class="priority-range">SAF 30-70%</div>
            <div class="priority-description">Alta viabilidade econômica</div>
        </div>

        <div class="priority-card priority-bom">
            <span class="priority-badge badge-bom">BOM/MUITO BOM</span>
            <div class="priority-count">7</div>
            <div class="priority-range">SAF 8-13%</div>
            <div class="priority-description">Viabilidade confirmada</div>
        </div>

        <div class="priority-card priority-regular">
            <span class="priority-badge badge-regular">REGULAR/BAIXO</span>
            <div class="priority-count">14</div>
            <div class="priority-range">SAF 4-8%</div>
            <div class="priority-description">Potencial moderado</div>
        </div>

        <div class="priority-card priority-baixo">
            <span class="priority-badge badge-baixo">BAIXA PRIORIDADE</span>
            <div class="priority-count">7</div>
            <div class="priority-range">SAF < 4%</div>
            <div class="priority-description">Viabilidade limitada</div>
        </div>
    </div>

    <div class="top-performers">
        <h4 style="font-size: 1.4rem; font-weight: 700; color: #1f2937; margin-bottom: 1.5rem; text-align: center;">
            🥇 Top 10 Performers - SAF Realista
        </h4>

        <div class="performer-item">
            <div class="performer-rank">🥇</div>
            <div class="performer-name">Bagaço de Cana-de-açúcar</div>
            <div class="performer-saf">80.75%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">🥈</div>
            <div class="performer-name">Soro de Laticínios</div>
            <div class="performer-saf">30.40%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">🥉</div>
            <div class="performer-name">Torta de Filtro (Cana)</div>
            <div class="performer-saf">12.88%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">4</div>
            <div class="performer-name">Mucilagem de Café</div>
            <div class="performer-saf">11.90%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">5</div>
            <div class="performer-name">Vinhaça de Cana-de-açúcar</div>
            <div class="performer-saf">10.26%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">6</div>
            <div class="performer-name">RSU (Resíduo Sólido Urbano)</div>
            <div class="performer-saf">9.88%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">7</div>
            <div class="performer-name">Cama de Frango</div>
            <div class="performer-saf">8.67%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">8</div>
            <div class="performer-name">Dejetos de Suínos</div>
            <div class="performer-saf">7.20%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">9</div>
            <div class="performer-name">Bagaço de Citros</div>
            <div class="performer-saf">6.80%</div>
        </div>

        <div class="performer-item">
            <div class="performer-rank">10</div>
            <div class="performer-name">Dejetos Bovinos (Leite)</div>
            <div class="performer-saf">5.50%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# RESIDUE DATABASE - SECTOR BREAKDOWN
# ============================================================================

st.markdown("""
<style>
.database-section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 3rem 0 2.5rem 0;
    background: linear-gradient(135deg, #1f2937 0%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.sector-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    transition: all 0.4s ease;
    border-top: 6px solid;
    position: relative;
    overflow: hidden;
}

.sector-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(0,0,0,0.02) 100%);
    pointer-events: none;
}

.sector-agriculture {
    border-top-color: #10b981;
}

.sector-livestock {
    border-top-color: #f59e0b;
}

.sector-urban {
    border-top-color: #3b82f6;
}

.sector-industrial {
    border-top-color: #8b5cf6;
}

.sector-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.12);
}

.sector-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}

.sector-icon-large {
    font-size: 3.5rem;
    margin-right: 1rem;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.sector-title {
    flex: 1;
}

.sector-title h3 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
}

.sector-count {
    font-size: 0.9rem;
    color: #6b7280;
    margin-top: 0.3rem;
}

.performer-highlight {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border-left: 4px solid #10b981;
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

.performer-highlight-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #059669;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.8rem;
}

.highlight-item {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
}

.highlight-icon {
    font-size: 1.3rem;
    margin-right: 0.8rem;
}

.highlight-name {
    flex: 1;
    font-weight: 600;
    color: #1f2937;
}

.highlight-badge {
    background: #10b981;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
}

.culture-list {
    margin-top: 1.5rem;
}

.culture-list-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #374151;
    margin-bottom: 0.8rem;
}

.culture-item {
    display: flex;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #f3f4f6;
    transition: all 0.2s ease;
}

.culture-item:last-child {
    border-bottom: none;
}

.culture-item:hover {
    padding-left: 0.5rem;
    background: #f9fafb;
}

.culture-emoji {
    font-size: 1.2rem;
    margin-right: 0.8rem;
}

.culture-text {
    font-size: 0.9rem;
    color: #4b5563;
}

.saf-summary {
    background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1.5rem;
    border: 2px solid #fde68a;
}

.saf-summary-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #92400e;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.saf-stat {
    font-size: 0.9rem;
    color: #78350f;
    margin: 0.3rem 0;
}

@media (max-width: 1200px) {
    .sector-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<h2 class="database-section-title">✅ Banco de Dados Completo CP2B - Phase 5</h2>

<div class="sector-grid">
    <!-- AGRICULTURA -->
    <div class="sector-card sector-agriculture">
        <div class="sector-header">
            <div class="sector-icon-large">🌾</div>
            <div class="sector-title">
                <h3>Agricultura</h3>
                <div class="sector-count">24 resíduos validados</div>
            </div>
        </div>

        <div class="performer-highlight">
            <div class="performer-highlight-title">🏆 Top Performers SAF</div>
            <div class="highlight-item">
                <div class="highlight-icon">🥇</div>
                <div class="highlight-name">Bagaço de Cana</div>
                <div class="highlight-badge">80.75%</div>
            </div>
            <div class="highlight-item">
                <div class="highlight-icon">🏆</div>
                <div class="highlight-name">Torta de Filtro</div>
                <div class="highlight-badge">12.88%</div>
            </div>
            <div class="highlight-item">
                <div class="highlight-icon">✅</div>
                <div class="highlight-name">Mucilagem de Café</div>
                <div class="highlight-badge">11.90%</div>
            </div>
            <div class="highlight-item">
                <div class="highlight-icon">⭐</div>
                <div class="highlight-name">Vinhaça de Cana</div>
                <div class="highlight-badge">10.26%</div>
            </div>
        </div>

        <div class="culture-list">
            <div class="culture-list-title">Principais Culturas:</div>
            <div class="culture-item">
                <div class="culture-emoji">🌾</div>
                <div class="culture-text"><strong>Cana-de-açúcar</strong>: 4 resíduos (Bagaço, Torta, Vinhaça, Palha)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🍊</div>
                <div class="culture-text"><strong>Citros</strong>: 2 resíduos (Bagaço, Cascas)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">☕</div>
                <div class="culture-text"><strong>Café</strong>: 2 resíduos (Mucilagem, Casca/Polpa)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🌽</div>
                <div class="culture-text"><strong>Milho</strong>: 2 resíduos (Palha, Sabugo)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🌱</div>
                <div class="culture-text"><strong>Soja</strong>: 2 resíduos (Palha, Casca)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🌳</div>
                <div class="culture-text"><strong>+ 12 outros</strong>: Feijão, Amendoim, Mandioca, Arroz, etc.</div>
            </div>
        </div>
    </div>

    <!-- PECUÁRIA -->
    <div class="sector-card sector-livestock">
        <div class="sector-header">
            <div class="sector-icon-large">🐄</div>
            <div class="sector-title">
                <h3>Pecuária</h3>
                <div class="sector-count">5 resíduos validados</div>
            </div>
        </div>

        <div class="performer-highlight">
            <div class="performer-highlight-title">⭐ Destaque SAF</div>
            <div class="highlight-item">
                <div class="highlight-icon">🐔</div>
                <div class="highlight-name">Cama de Frango</div>
                <div class="highlight-badge">8.67%</div>
            </div>
        </div>

        <div class="culture-list">
            <div class="culture-list-title">Resíduos Incluídos:</div>
            <div class="culture-item">
                <div class="culture-emoji">🐄</div>
                <div class="culture-text"><strong>Dejetos Bovinos</strong> (Leite + Corte)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🐷</div>
                <div class="culture-text"><strong>Dejetos de Suínos</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🐔</div>
                <div class="culture-text"><strong>Cama de Frango</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🥚</div>
                <div class="culture-text"><strong>Dejetos de Codornas</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🐮</div>
                <div class="culture-text"><strong>Efluentes de Laticínios</strong></div>
            </div>
        </div>
    </div>

    <!-- INDUSTRIAL -->
    <div class="sector-card sector-industrial">
        <div class="sector-header">
            <div class="sector-icon-large">🏭</div>
            <div class="sector-title">
                <h3>Industrial</h3>
                <div class="sector-count">5 resíduos validados</div>
            </div>
        </div>

        <div class="performer-highlight">
            <div class="performer-highlight-title">🥇 Top Performer</div>
            <div class="highlight-item">
                <div class="highlight-icon">🥛</div>
                <div class="highlight-name">Soro de Laticínios</div>
                <div class="highlight-badge">30.40%</div>
            </div>
        </div>

        <div class="culture-list">
            <div class="culture-list-title">Resíduos Incluídos:</div>
            <div class="culture-item">
                <div class="culture-emoji">🥛</div>
                <div class="culture-text"><strong>Soro de Laticínios</strong> (EXCELENTE)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🍺</div>
                <div class="culture-text"><strong>Bagaço de Cervejarias</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🥩</div>
                <div class="culture-text"><strong>Efluente de Frigoríficos</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🍹</div>
                <div class="culture-text"><strong>Resíduos de Processamento</strong></div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🏭</div>
                <div class="culture-text"><strong>Efluentes Industriais</strong></div>
            </div>
        </div>
    </div>

    <!-- URBANO -->
    <div class="sector-card sector-urban">
        <div class="sector-header">
            <div class="sector-icon-large">🏙️</div>
            <div class="sector-title">
                <h3>Urbano</h3>
                <div class="sector-count">4 resíduos validados</div>
            </div>
        </div>

        <div class="performer-highlight">
            <div class="performer-highlight-title">⭐ Destaque SAF</div>
            <div class="highlight-item">
                <div class="highlight-icon">🗑️</div>
                <div class="highlight-name">RSU (Resíduo Sólido Urbano)</div>
                <div class="highlight-badge">9.88%</div>
            </div>
        </div>

        <div class="culture-list">
            <div class="culture-list-title">Resíduos Incluídos:</div>
            <div class="culture-item">
                <div class="culture-emoji">🗑️</div>
                <div class="culture-text"><strong>RSU</strong> (Resíduo Sólido Urbano)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🌳</div>
                <div class="culture-text"><strong>RPO</strong> (Resíduos de Poda Urbana)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">💧</div>
                <div class="culture-text"><strong>Lodo de Esgoto</strong> (ETE)</div>
            </div>
            <div class="culture-item">
                <div class="culture-emoji">🍂</div>
                <div class="culture-text"><strong>Galhos e Folhas</strong></div>
            </div>
        </div>
    </div>
</div>

<div class="saf-summary" style="max-width: 800px; margin: 3rem auto;">
    <div class="saf-summary-title">💡 Metodologia SAF - Phase 5 ✅ COMPLETO</div>
    <div class="saf-stat">✅ <strong>32/38 resíduos</strong> com SAF validado (84%)</div>
    <div class="saf-stat">🎯 Fatores calibrados: <strong>FC, FCp, FS, FL</strong></div>
    <div class="saf-stat">📊 Cenários: Pessimista, <strong>Realista ⭐</strong>, Otimista, Teórico</div>
    <div class="saf-stat">📈 Total Realista: <strong>6.939 Mi m³/ano CH₄</strong> (297% meta FIESP-SP)</div>
    <div class="saf-stat">🏆 Priority Tiers: 1 EXCEPCIONAL, 3 EXCELENTE, 7 BOM/MUITO BOM</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


# ============================================================================
# MODERN FOOTER
# ============================================================================

st.markdown("""
<style>
.footer-modern {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 30px 30px 0 0;
    margin: 4rem -1rem -1rem -1rem;
    box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
}

.footer-logo {
    text-align: center;
    margin-bottom: 2rem;
}

.footer-logo h3 {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.footer-tagline {
    font-size: 1.1rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

.footer-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
    padding: 2rem;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}

.footer-stat {
    text-align: center;
}

.footer-stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #10b981;
    margin-bottom: 0.3rem;
}

.footer-stat-label {
    font-size: 0.85rem;
    color: #d1d5db;
}

.footer-achievement {
    text-align: center;
    margin: 2rem 0;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(59,130,246,0.1) 100%);
    border-radius: 16px;
    border: 2px solid rgba(16,185,129,0.2);
}

.footer-achievement-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #10b981;
    margin-bottom: 0.5rem;
}

.footer-nav-hint {
    text-align: center;
    padding: 1rem;
    background: rgba(59,130,246,0.1);
    border-radius: 12px;
    margin: 1.5rem 0;
    border: 1px solid rgba(59,130,246,0.3);
}

.footer-nav-hint-text {
    font-size: 0.95rem;
    color: #93c5fd;
    font-weight: 500;
}

.footer-bottom {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.footer-bottom-text {
    font-size: 0.85rem;
    color: #6b7280;
}

.footer-version {
    font-size: 0.75rem;
    color: #4b5563;
    margin-top: 0.5rem;
}

@keyframes glow-pulse {
    0%, 100% {
        box-shadow: 0 0 20px rgba(16,185,129,0.3);
    }
    50% {
        box-shadow: 0 0 40px rgba(16,185,129,0.5);
    }
}

.footer-achievement {
    animation: glow-pulse 3s ease-in-out infinite;
}
</style>

<div class="footer-modern">
    <div class="footer-content">
        <div class="footer-logo">
            <h3>🧪 PanoramaCP2B</h3>
            <div class="footer-tagline">
                <strong>Centro Paulista de Estudos em Biogás e Bioprodutos (UNICAMP)</strong>
            </div>
            <div style="color: #9ca3af; font-size: 0.95rem;">
                Plataforma de Validação Laboratorial para Pesquisa em Biogás
            </div>
        </div>

        <div class="footer-stats-grid">
            <div class="footer-stat">
                <div class="footer-stat-value">📚 38</div>
                <div class="footer-stat-label">Resíduos Validados</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">🎯 84%</div>
                <div class="footer-stat-label">SAF Coverage</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">📖 20+</div>
                <div class="footer-stat-label">Referências Científicas</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">🗺️ 645</div>
                <div class="footer-stat-label">Municípios SP</div>
            </div>
        </div>

        <div class="footer-achievement">
            <div class="footer-achievement-title">✅ Phase 5 Complete - SAF Validated Platform</div>
            <div style="color: #d1d5db; font-size: 0.9rem; margin-top: 0.5rem;">
                Sistema completo de validação com metodologia conservadora baseada em dados reais
            </div>
        </div>

        <div class="footer-nav-hint">
            <div class="footer-nav-hint-text">
                💡 Use a barra lateral esquerda ou navegação horizontal para explorar as páginas da plataforma
            </div>
        </div>

        <div class="footer-bottom">
            <div class="footer-bottom-text">
                <strong>PanoramaCP2B</strong> - Desenvolvido por CP2B/UNICAMP
            </div>
            <div class="footer-version">
                Última atualização: Outubro 2025 • Version 2.0 • Phase 5 Complete
            </div>
            <div style="margin-top: 1rem; font-size: 0.8rem; color: #6b7280;">
                🔬 Validação Científica • 📊 Dados Operacionais Reais • 🎯 Metodologia Conservadora
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
