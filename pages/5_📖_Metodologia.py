"""
Página de Metodologia - PanoramaCP2B
Documentação completa da metodologia FDE e processos de cálculo
"""

import streamlit as st
from src.ui.main_navigation import render_main_navigation, render_navigation_divider


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Metodologia - PanoramaCP2B",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style='background: linear-gradient(135deg, #059669 0%, #2563eb 50%, #7c3aed 100%);
            color: white; padding: 2.5rem; margin: -1rem -1rem 1.5rem -1rem;
            text-align: center; border-radius: 0 0 25px 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);'>
    <h1 style='margin: 0; font-size: 2.5rem; font-weight: 700;'>
        📖 Metodologia CP2B
    </h1>
    <p style='margin: 15px 0 0 0; font-size: 1.1rem; opacity: 0.95;'>
        Documentação Completa da Metodologia FDE e Processos de Cálculo
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# NAVIGATION
# ============================================================================

render_main_navigation(current_page="metodologia")
render_navigation_divider()


# ============================================================================
# METHODOLOGY CONTENT
# ============================================================================

st.markdown("# Documentação Completa da Metodologia - PanoramaCP2B")

# ============================================================================
# SECTION 1: OVERVIEW
# ============================================================================

st.markdown("## 1️⃣ Visão Geral da Plataforma")

st.markdown("""
O **PanoramaCP2B** é uma plataforma de validação laboratorial desenvolvida pelo Centro Paulista de Estudos em Biogás
e Bioprodutos (UNICAMP) para pesquisa em biogás. O sistema utiliza uma **metodologia conservadora e baseada em dados reais**
para estimar o potencial de geração de biogás a partir de resíduos orgânicos no Estado de São Paulo.

**Objetivos principais:**
- Fornecer estimativas realistas de disponibilidade de resíduos para biogás
- Permitir validação de dados laboratoriais contra literatura científica
- Oferecer base científica completa com referências verificadas
- Suportar tomada de decisão em políticas públicas e planejamento energético
""")

st.markdown("---")

# ============================================================================
# SECTION 2: DATA SOURCES
# ============================================================================

st.markdown("## 2️⃣ Fontes de Dados Primárias")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
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
    """)

with col2:
    st.markdown("""
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
    """)

st.markdown("---")

# ============================================================================
# SECTION 3: FDE METHODOLOGY
# ============================================================================

st.markdown("## 3️⃣ Metodologia FDE - Fatores de Disponibilidade")

st.info("""
**Fórmula Geral - FDE (Fator de Disponibilidade Efetiva)**

```
DISPONIBILIDADE_FINAL = FC × (1 - FCp) × FS × FL × 100%
```

Onde:
- **FC** = Fator de Coleta (viabilidade técnica)
- **FCp** = Fator de Competição (usos alternativos)
- **FS** = Fator Sazonalidade (variação anual)
- **FL** = Fator Logístico (restrições de transporte)
""")

# FC - Fator de Coleta
with st.expander("🔹 FC - Fator de Coleta (0 a 1)", expanded=False):
    st.markdown("""
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
    """)

# FCp - Fator de Competição
with st.expander("🔹 FCp - Fator de Competição (0 a 1)", expanded=False):
    st.markdown("""
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
    """)

# FS - Fator Sazonalidade
with st.expander("🔹 FS - Fator Sazonalidade (0.7 a 1.0)", expanded=False):
    st.markdown("""
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
    """)

# FL - Fator Logístico
with st.expander("🔹 FL - Fator Logístico (0.65 a 1.0)", expanded=False):
    st.markdown("""
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
    """)

st.markdown("---")

# ============================================================================
# SECTION 4: BIOGAS CALCULATION
# ============================================================================

st.markdown("## 4️⃣ Cálculo do Potencial de Biogás")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Passo 1: Geração Teórica

    ```
    GERAÇÃO_TEÓRICA =
    PRODUÇÃO × FATOR_CONVERSÃO
    ```

    **Exemplos:**
    - **Cana**: Produção (t) × 0.25 × BMP
    - **Bovinos**: Rebanho × 18 kg/dia × 365 × BMP
    - **RSU**: População × 1.2 kg/cap/dia × BMP
    """)

with col2:
    st.markdown("""
    ### Passo 2: Aplicar FDE

    ```
    DISPONIBILIDADE =
    GERAÇÃO_TEÓRICA × FDE
    ```

    Onde:
    ```
    FDE = FC × (1 - FCp) × FS × FL
    ```
    """)

with col3:
    st.markdown("""
    ### Passo 3: Cenários

    - **Teórico (100%)**: FDE = 1.0
    - **Otimista**: FDE = 0.80-0.90
    - **Realista ⭐**: FDE = 0.25-0.50
    - **Pessimista**: FDE = 0.10-0.20
    """)

st.markdown("---")

# ============================================================================
# SECTION 5: CHEMICAL PARAMETERS
# ============================================================================

st.markdown("## 5️⃣ Parâmetros Químicos - Ranges de Literatura")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Dados Coletados

    Os seguintes parâmetros são coletados de literatura científica validada:

    | Parâmetro | Sigla | Unidade | Tipo |
    |-----------|-------|---------|------|
    | Potencial Metanogênico | BMP | mL CH₄/g VS | Principal |
    | Sólidos Totais | TS | % | Composição |
    | Sólidos Voláteis | VS | % | Composição |
    | Relação C:N | C:N | - | Balanço |
    | COD | COD | mg/L | Qualidade |
    | pH | pH | - | Condição |
    | Nitrogênio Total | N | % | Composição |
    | Carbono | C | % | Composição |
    """)

with col2:
    st.markdown("""
    ### Método de Coleta

    **Busca Sistemática (PRISMA-like):**
    1. Busca em Scopus, Web of Science, SciELO
    2. Filtros: peer-reviewed, 15 anos, contexto tropical
    3. Critérios: metodologia clara, dados replicáveis
    4. Extração: MIN, MEAN, MAX

    **Exemplo - Vinhaça:**
    - 12 artigos encontrados
    - BMP: 180 - 280 mL CH₄/g VS (média: 220)
    - C:N ratio: 35 - 80 (média: 55)
    - Referência: Papers 2015-2023
    """)

st.markdown("""
### Validação Laboratorial - Thresholds

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
""")

st.markdown("---")

# ============================================================================
# SECTION 6: SCENARIOS
# ============================================================================

st.markdown("## 6️⃣ Cenários de Disponibilidade - Definições Detalhadas")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Teórico", "📈 Otimista", "⭐ Realista", "📉 Pessimista"])

with tab1:
    st.markdown("""
    ### Cenário 1: TEÓRICO (100%)

    **Definição**: Máxima produção com ZERO restrições

    **Fórmula**: `FDE = 1.0`

    **Pressupostos:**
    - Toda produção é coletável
    - Sem competição de mercado
    - Disponível ano inteiro
    - Logística sem limite

    **Quando usar**: Comparações acadêmicas, estimativas superiores

    **Quando NÃO usar**: Planejamento real, investimentos
    """)

with tab2:
    st.markdown("""
    ### Cenário 2: OTIMISTA

    **Definição**: Condições favoráveis com tecnologia moderna

    **Fórmula**: `FDE = 0.80 a 0.90`

    **Pressupostos:**
    - FC = 0.90 (coleta bem organizada)
    - FCp = 0.30 (pouca competição)
    - FS = 0.95 (sazonalidade mínima)
    - FL = 0.95 (logística eficiente)

    **Quando usar**: Potencial máximo com investimentos
    """)

with tab3:
    st.success("""
    ### Cenário 3: REALISTA ⭐ (RECOMENDADO)

    **Definição**: Baseado em operações existentes comprovadas

    **Fórmula**: `FDE = 0.25 a 0.50`

    **Pressupostos:**
    - FC = 0.75 (coleta parcial, limitações reais)
    - FCp = 0.60 (competição significativa)
    - FS = 0.85 (sazonalidade moderada)
    - FL = 0.80 (custos logísticos reais)

    **Quando usar**: **PLANEJAMENTO ESTRATÉGICO** - USE ESTE

    **Base**: Calibrado com usinas funcionando em SP
    """)

with tab4:
    st.markdown("""
    ### Cenário 4: PESSIMISTA

    **Definição**: Condições desfavoráveis, fatores limitantes máximos

    **Fórmula**: `FDE = 0.10 a 0.20`

    **Pressupostos:**
    - FC = 0.55 (coleta mínima)
    - FCp = 0.80 (alta competição)
    - FS = 0.70 (sazonalidade alta)
    - FL = 0.65 (logística cara)

    **Quando usar**: Análises de risco, piores cenários
    """)

st.markdown("---")

# ============================================================================
# SECTION 7: LIMITATIONS
# ============================================================================

st.markdown("## 7️⃣ Limitações e Pressupostos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Limitações Conhecidas

    **1. Dados Agrícolas**
    - IBGE: dados anuais (não captura variações sazonais)
    - Alguns municípios têm sub-relatórios
    - Culturas menores podem ter dados agrupados

    **2. Fatores de Conversão**
    - Valores podem variar por cultivar
    - Condições climáticas locais não consideradas
    - BMP varia com método de determinação

    **3. Competição de Mercado**
    - FCp baseado em preços históricos (mercado pode mudar)
    - Não considera novos usos (ex: bioplásticos)
    - Análise pontual em tempo específico

    **4. Logística**
    - FL usa modelo simplificado de distância
    - Não considera infraestrutura viária real
    - Custos de combustível flutuantes
    """)

with col2:
    st.markdown("""
    ### Pressupostos Principais

    1. **Estabilidade de Mercado**: Preços e demandas se mantêm
    2. **Tecnologia Padrão**: Uso de tecnologia convencional
    3. **Legalidade**: Respeito a regulamentações ambientais
    4. **Escala Mínima**: Viabilidade econômica em escala presente
    """)

st.markdown("---")

# ============================================================================
# SECTION 8: UPDATES
# ============================================================================

st.markdown("## 8️⃣ Revisão e Atualização")

st.info("""
**Frequência**: Anual (ou quando houver novos dados)

**Procedimento:**
1. Coleta de novos dados IBGE/SIDRA
2. Revisão de literatura recente
3. Validação com usinas operacionais
4. Ajuste de fatores se necessário
5. Publicação de relatório de mudanças

**Última atualização**: Outubro de 2024

**Próxima revisão**: Outubro de 2025
""")

st.markdown("---")

# ============================================================================
# REFERENCES
# ============================================================================

st.markdown("## 🏆 Referências Principais")

st.markdown("""
Base científica do PanoramaCP2B construída com metodologia PRISMA-like utilizando:
- **30+ artigos peer-reviewed**
- **Scopus indexados**
- Contexto Brasil/Tropical
- Últimos 15 anos de publicações

Disponíveis na seção **Referências Científicas** da plataforma com links DOI completos.
""")

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
            border-radius: 20px; margin-top: 2rem;'>
    <p style='font-size: 0.85rem; color: #9ca3af;'>
        <strong>Documento elaborado por</strong>: Centro Paulista de Estudos em Biogás e Bioprodutos (CP2B/UNICAMP)
    </p>
    <p style='font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;'>
        <strong>Versão</strong>: 2.0 • <strong>Data</strong>: Outubro de 2024
    </p>
</div>
""", unsafe_allow_html=True)
