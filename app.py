"""
PanoramaCP2B - Centro Paulista de Estudos em Biogás e Bioprodutos
Homepage - Laboratory Validation Tool for Biogas Research
Phase 5 Complete Edition
"""

import streamlit as st
from src.ui.main_navigation import render_main_navigation, render_navigation_divider
from src.ui.homepage_components import (
    render_hero_section,
    render_about_section,
    render_phase5_highlights,
    render_features_grid,
    render_saf_priority_summary,
    render_sector_overview,
    render_footer
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PanoramaCP2B - Validação Laboratorial | Phase 5 Complete",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# RENDER HOMEPAGE COMPONENTS (SOLID ARCHITECTURE)
# ============================================================================

# Hero section with platform title and Phase 5 statistics
render_hero_section()

# Horizontal navigation bar
render_main_navigation(current_page="home")
render_navigation_divider()

# About platform section
render_about_section()

# Phase 5 completion highlights
render_phase5_highlights()

# Main features grid (2 columns)
render_features_grid()

# Methodology section (expandable) - keeping existing implementation
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

# SAF priority summary with metrics
render_saf_priority_summary()

# Sector overview with top performers
render_sector_overview()

# Footer
render_footer()
