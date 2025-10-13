# Panorama de Resíduos — São Paulo

## 📋 Resumo do Projeto

### Objetivo Principal
Plataforma web de **consulta e visualização de dados** sobre o potencial energético de resíduos agrícolas, pecuários e urbanos no estado de São Paulo, com foco em biogás e bioenergia.

### Público-Alvo
- **Formuladores de políticas públicas** (Policy Makers)
- **Pesquisadores acadêmicos**
- **Profissionais do setor energético**
- **Estudantes e educadores**

### Propósito
Servir como um **"farol educacional"** para disseminar conhecimento sobre:
- Tipos de resíduos disponíveis (culturas agrícolas, rebanhos, resíduos urbanos)
- Composição química e características dos resíduos
- Potencial de geração de biogás
- Distribuição geográfica dos resíduos no estado de SP
- Metodologias e fontes científicas dos dados

---

## 🎯 Características Principais

### 1. **Sistema de Consulta (não estimativo)**
- Apresenta **apenas dados reais e verificados**
- Evita cálculos estimativos não comprovados
- Transparência total sobre fontes e metodologia

### 2. **Interface Minimalista e Contemporânea**
- Design limpo com paleta de cores sustentáveis (verdes, azuis)
- Foco na usabilidade e acessibilidade
- Navegação intuitiva com seleção por **botões clicáveis** (não dropdowns)

### 3. **Visualizações de Dados**
- Gráficos interativos (Plotly): donut, barras, dispersão
- Tabelas de dados detalhados
- Download de dados em formato CSV
- Responsivo e otimizado para diferentes dispositivos

### 4. **Credibilidade Científica**
- Citação clara das fontes de dados
- Seção de metodologia acessível
- Referências a instituições reconhecidas (IBGE, UNICAMP, MapBiomas)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Streamlit** | Framework principal para prototipagem rápida |
| **Plotly** | Visualizações interativas customizadas |
| **Pandas** | Manipulação e análise de dados |
| **SQLite** | Armazenamento local de dados |
| **CSS Customizado** | Design system premium e minimalista |

---

## 📊 Fontes de Dados

1. **SIDRA/IBGE** — Produção agrícola e área cultivada
2. **MapBiomas** — Cobertura e uso do solo
3. **Defesa Agropecuária SP** — Dados de rebanhos
4. **NIPE/UNICAMP** — Fatores de conversão e potencial energético

---

## 🚀 Arquitetura do Código (SOLID)

### Princípios Aplicados
- **Single Responsibility Principle (SRP)**: Módulos separados para dados, visualização e UI
- **Separação de Camadas**:
  - `src/data_handler.py` — Lógica de dados e queries
  - `src/plotter.py` & `src/plotly_theme.py` — Criação de gráficos
  - `src/ui_components_premium.py` — Componentes reutilizáveis de UI
  - `pages/*.py` — Páginas individuais da aplicação
  - `assets/styles.css` — Design system centralizado

### Estrutura de Diretórios
```
PanoramaCP2B/
├── src/
│   ├── data_handler.py          # Camada de dados
│   ├── plotter.py               # Gráficos básicos
│   ├── plotly_theme.py          # Tema customizado
│   └── ui_components_premium.py # Componentes UI
├── pages/
│   ├── 2_Analise_Regional.py
│   ├── 3_Premium_Design_Demo.py
│   ├── 9_Design_Acolhedor.py
│   └── 10_Panorama_Limpo.py    # Versão final limpa
├── assets/
│   └── styles.css               # Design system
├── data/
│   └── *.db, *.xls             # Dados locais
├── app.py                       # Página inicial
├── requirements.txt
└── README.md
```

---

## 🎨 Design System

### Paleta de Cores
- **Verde Primário**: `#27ae60`, `#2ecc71` (sustentabilidade)
- **Azul Tecnologia**: `#2EC4B6`, `#00D9FF`
- **Texto**: `#0F1A2A` (deep navy)
- **Backgrounds**: `#FFFFFF` (branco limpo)
- **Acentos**: `#5CB85C` (positivo), `#FF6B6B` (alerta)

### Tipografia
- **Font**: Inter (sans-serif)
- Hierarquia clara: títulos, subtítulos, corpo de texto
- Legibilidade otimizada (WCAG 2.1 AA)

---

## 📍 Estado Atual do Projeto

### ✅ Implementado
- [x] Estrutura modular seguindo SOLID
- [x] Design system premium e minimalista
- [x] Seleção de dados por botões clicáveis
- [x] Visualizações interativas (Plotly)
- [x] Sistema de consulta sem estimativas
- [x] Seção de fontes e metodologia
- [x] Download de dados (CSV)
- [x] Interface em PT-BR
- [x] Múltiplas páginas (navegação Streamlit)

### 🔄 Em Desenvolvimento
- [ ] Integração com banco de dados real (SQLite)
- [ ] Dados reais de municípios de SP
- [ ] Sistema de filtros avançados
- [ ] Mapas geográficos (GeoJSON)
- [ ] Comparações temporais (séries históricas)

### 🎯 Próximos Passos
1. Conectar aos dados reais do NIPE/IBGE
2. Implementar mapas interativos de SP
3. Adicionar análises comparativas
4. Sistema de exportação de relatórios
5. Documentação completa para usuários

---

## 🌱 Missão

> **"Democratizar o acesso a dados sobre resíduos e bioenergia no estado de São Paulo, promovendo a tomada de decisões baseada em evidências para um futuro mais sustentável."**

---

## 👥 Equipe

**Centro de Pesquisa para Inovação em Biogás (CP2B)**  
Universidade Estadual de Campinas (UNICAMP)

---

**Última atualização:** Outubro de 2024  
**Versão:** 1.0 (Protótipo Funcional)

