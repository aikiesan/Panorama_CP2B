# 🌱 Panorama de Resíduos - Estado de São Paulo

**Sistema de consulta e visualização de dados sobre potencial energético de resíduos**

Plataforma desenvolvida com Streamlit focada em **consulta de dados reais** e exploração do potencial de resíduos (agrícolas, pecuários e urbanos) para geração de bioenergia no Estado de São Paulo.

---

## 📋 Sobre o Projeto

Sistema web para consulta de dados sobre o potencial energético de resíduos em São Paulo, servindo como **ferramenta educacional e de análise** para:

- 👨‍💼 **Formuladores de políticas públicas**
- 🔬 **Pesquisadores e acadêmicos**
- ⚡ **Profissionais do setor energético**
- 📚 **Estudantes e educadores**

### 🎯 Características Principais

- **Sistema de Consulta Puro**: Apresenta dados reais verificados, sem estimativas não comprovadas
- **Design Minimalista**: Interface limpa e contemporânea com foco em usabilidade
- **Seleção Intuitiva**: Botões clicáveis ao invés de dropdowns para melhor UX
- **Visualizações Interativas**: Gráficos dinâmicos com Plotly
- **Transparência Total**: Citação clara de fontes e metodologia científica
- **Download de Dados**: Exportação em CSV para análise própria

### 📊 Tipos de Resíduos Cobertos

- 🌾 **Agrícolas**: Cana-de-açúcar, soja, milho, café, arroz, etc.
- 🐄 **Pecuários**: Bovinos, suínos, aves, piscicultura
- 🏙️ **Urbanos**: Resíduos sólidos urbanos (RSU) e resíduos de poda (RPO)

---

## 🏗️ Arquitetura (SOLID Principles)

```
PanoramaCP2B/
├── assets/
│   └── styles.css                    # Design system customizado
├── data/
│   ├── cp2b_maps.db                  # Banco de dados SQLite
│   └── processed/
│       └── sp_municipios_simplified_0_001.geojson
├── pages/
│   ├── 10_Panorama_Limpo.py         # Página principal limpa
│   ├── 2_Analise_Regional.py        # Análise por município
│   ├── 3_Residuos_Agricolas.py      # Resíduos agrícolas
│   ├── 4_Residuos_Pecuarios.py      # Resíduos pecuários
│   ├── 5_Residuos_Urbanos.py        # Resíduos urbanos
│   └── 6_Dados_Laboratoriais.py     # Dados de composição
├── src/
│   ├── data_handler.py              # Camada de dados (SRP)
│   ├── plotter.py                   # Gráficos básicos (SRP)
│   ├── plotly_theme.py              # Tema customizado Plotly
│   ├── ui_components.py             # Componentes UI básicos
│   ├── ui_components_premium.py     # Componentes UI premium
│   └── data_sources/                # Handlers específicos por fonte
│       ├── agro_handler.py
│       ├── lab_data_handler.py
│       ├── mapbiomas_handler.py
│       ├── sidra_handler.py
│       └── socioeco_handler.py
├── app.py                           # Aplicação principal
├── requirements.txt
├── README.md                        # Este arquivo
└── PROJETO_RESUMO.md               # Resumo executivo do projeto
```

### ✅ Princípios SOLID Aplicados

- **S (Single Responsibility)**: Cada módulo tem uma responsabilidade única
  - `data_handler.py`: Acesso e processamento de dados
  - `plotter.py` / `plotly_theme.py`: Criação de visualizações
  - `ui_components*.py`: Componentes de interface
  
- **O (Open/Closed)**: Fácil adicionar novos gráficos sem modificar código existente

- **L (Liskov Substitution)**: Funções retornam formatos consistentes

- **I (Interface Segregation)**: Funções pequenas e focadas

- **D (Dependency Inversion)**: Aplicação depende de abstrações

---

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Navegue até a pasta do projeto**

```bash
cd PanoramaCP2B
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**

```bash
pip install -r requirements.txt
```

5. **Execute a aplicação**

```bash
streamlit run pages/10_Panorama_Limpo.py
```

6. **Acesse no navegador**

A aplicação estará disponível em: `http://localhost:8501`

---

## 📊 Funcionalidades

### Página Principal (10_Panorama_Limpo.py)

#### 🔘 Seleção por Botões
- **Cultura Agrícola**: Botões clicáveis para cada cultura
- **Tipo de Resíduo**: Seleção dinâmica baseada na cultura escolhida
- **Ano de Referência**: Escolha do ano dos dados

#### 📈 Visualizações de Dados
- **Composição Química**: Gráfico donut + tabela detalhada
- **Geração por Região**: Gráfico de barras + dados tabulares
- **Dados Municipais Completos**: Tabela navegável com dados reais

#### 💾 Exportação
- **Download CSV**: Baixe os dados completos para análise própria

#### 📖 Transparência
- **Seção de Fontes**: Expandível com metodologia e referências

### Outras Páginas

- **Análise Regional**: Análise detalhada por município
- **Resíduos Agrícolas**: Dados específicos do setor agrícola
- **Resíduos Pecuários**: Dados do setor pecuário
- **Resíduos Urbanos**: Dados de RSU e RPO
- **Dados Laboratoriais**: Composição química dos resíduos

---

## 🗄️ Fontes de Dados

| Fonte | Dados Fornecidos |
|-------|------------------|
| **SIDRA/IBGE** | Produção agrícola, área cultivada, dados demográficos |
| **MapBiomas** | Cobertura e uso do solo |
| **Defesa Agropecuária SP** | Dados de rebanhos e produção animal |
| **NIPE/UNICAMP** | Fatores de conversão, potencial energético |

**Metodologia**: Dados calculados com base em fatores de conversão científicos aplicados à produção reportada pelas fontes oficiais.

**Última atualização dos dados**: Março de 2024

---

## 🎨 Design System

### Paleta de Cores (Sustentabilidade)

```css
--green-primary: #27ae60    /* Verde sustentável */
--green-light: #2ecc71      /* Verde claro */
--teal-tech: #2EC4B6        /* Azul-verde tecnologia */
--cyan-bright: #00D9FF      /* Ciano brilhante */
--text-primary: #0F1A2A     /* Texto principal */
--background: #FFFFFF       /* Fundo limpo */
```

### Tipografia

- **Fonte**: Inter (sans-serif)
- **Hierarquia clara**: Títulos, subtítulos, corpo de texto
- **Acessibilidade**: WCAG 2.1 AA compliance

---

## 📈 Performance

- ✅ **Caching**: Uso de `@st.cache_data` para otimizar consultas
- ✅ **GeoJSON Simplificado**: Geometrias otimizadas para renderização rápida
- ✅ **Lazy Loading**: Dados carregados sob demanda
- ✅ **Session State**: Gerenciamento eficiente de estado da aplicação

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Streamlit** | Framework principal para prototipagem |
| **Plotly** | Visualizações interativas customizadas |
| **Pandas** | Manipulação e análise de dados |
| **SQLite** | Armazenamento local de dados |
| **CSS Custom** | Design system premium |

---

## 🤝 Contribuindo

Para adicionar funcionalidades ou melhorias:

1. Mantenha a separação de responsabilidades (SOLID)
2. Adicione docstrings em todas as funções
3. Use type hints quando possível
4. Teste localmente antes de integrar
5. Mantenha o foco em dados reais e verificados

---

## 📄 Documentação Adicional

- **`PROJETO_RESUMO.md`**: Resumo executivo completo do projeto
- **`requirements.txt`**: Lista de dependências Python
- **`assets/styles.css`**: Sistema de design CSS completo

---

## 👥 Equipe

**Centro de Pesquisa para Inovação em Biogás (CP2B)**  
Universidade Estadual de Campinas (UNICAMP)

---

## 📞 Contato

Para dúvidas, sugestões ou colaborações, entre em contato através do repositório.

---

**Versão**: 1.0 (Protótipo Funcional)  
**Última atualização**: Outubro de 2024
