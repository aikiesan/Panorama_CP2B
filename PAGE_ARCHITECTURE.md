# PanoramaCP2B - Arquitetura de Páginas

## Visão Geral das Páginas e Responsabilidades

Cada página tem um propósito bem definido para evitar redundância. Aqui está a estrutura:

---

## **Page 1: 📊 Disponibilidade de Resíduos**
**URL:** `localhost:8503` (main page)
**Responsabilidade:** Visão executiva + cenários de potencial de biogás

### Estrutura de Seções:
```
1. AVAILABILITY CARD (Full Width)
   ├── Geração do resíduo
   ├── Potencial de biogás (Realista)
   ├── Eletricidade equivalente
   ├── Umidade
   ├── ⚗️ [Expander] Parâmetros Químicos (MIN/MEAN/MAX)
   ├── 🔧 [Expander] Parâmetros Operacionais
   ├── ✅ [Expander] Fatores de Disponibilidade
   ├── 🎯 [Expander] Destino Atual
   ├── 📝 [Expander] Justificativa Técnica
   └── 📚 [Expander] Referências Científicas

2. SCENARIO SELECTOR (Full Width - Horizontal)
   └── Pessimista | Realista | Otimista | Teórico (100%)

3. MAIN RESULTS METRICS (4 Colunas)
   ├── 💨 Potencial (Cenário Selecionado)
   ├── 📉 Redução vs Teórico
   ├── ✅ Disponibilidade Final
   └── ⚡ Energia Equivalente

4. SCENARIO COMPARISON + CONTRIBUTION CHARTS (Side by Side)
   ├── Gráfico de barras: Comparação cenários
   └── Gráfico: Contribuição de sub-resíduos (se aplicável)

5. MUNICIPALITY RANKING
   └── Tabela: Top municípios produtores

6. DATA VALIDATION PANEL
   └── Status de validação dos dados

7. TECHNICAL JUSTIFICATION (Collapsible)
   └── Explicação completa da metodologia
```

### O que **NÃO** contém:
- ❌ Tabelas repetidas de parâmetros químicos (já no AvailabilityCard)
- ❌ Gráficos detalhados de composição (ver Page 2)
- ❌ Dados laboratoriais (ver Page 4)
- ❌ Comparações entre múltiplos resíduos (ver Page 3)

---

## **Page 2: 🧪 Parâmetros Químicos e Operacionais**
**URL:** `/pages/2_🧪_Parametros_Quimicos.py`
**Responsabilidade:** Análise detalhada de composição química e operação

### Estrutura:
```
1. CHEMICAL PARAMETERS TABLE (Detalhado)
   ├── Tabela completa: MIN | MEAN/VALOR | MAX | UNIDADE
   ├── Destaques (4 métricas): BMP, Umidade, ST, SV
   └── Explicação de interpretação

2. OPERATIONAL PARAMETERS TABLE (Detalhado)
   ├── Tabela completa: HRT, Temperatura, TCO, Tipo de Reator
   ├── Destaques (3 métricas): TRH, Temperatura, Tipo
   └── Guia operacional

3. LINK para COMPARISON LABORATORIAL
```

### O que **É**:
- ✅ Especializado em COMPARAÇÕES detalhadas
- ✅ Ranges MIN/MEAN/MAX com explicações
- ✅ Referência para ajustar parâmetros locais
- ✅ Ponte para validação laboratorial

### O que **NÃO**:
- ❌ Disponibilidade (ver Page 1)
- ❌ Cenários (ver Page 1)
- ❌ Comparação experimental (ver Page 4)

---

## **Page 3: 📚 Referências Científicas**
**URL:** `/pages/3_📚_Referencias_Cientificas.py`
**Responsabilidade:** Base de dados bibliográfica e citações

---

## **Page 4: 🔬 Comparação Laboratorial**
**URL:** `/pages/4_🔬_Comparacao_Laboratorial.py`
**Responsabilidade:** Validar dados experimentais contra literatura

### Fluxo recomendado:
```
Page 1 (Disponibilidade)
  → Vejo o valor de referência
    → Page 2 (Parâmetros Químicos)
      → Entendo a composição
        → Page 4 (Comparação Laboratorial)
          → Valido meus dados experimentais
```

---

## **Componentes Reutilizáveis**

### `AvailabilityCard`
**Localização:** `src/ui/availability_card.py`
**Usado em:** Page 1 (Disponibilidade)
**Conteúdo:**
- Informações gerais do resíduo
- **Parâmetros químicos** (expandível)
- **Parâmetros operacionais** (expandível)
- **Fatores de disponibilidade** (expandível)
- Sub-resíduos (se composite)
- Referências

**IMPORTANTE:** Este é o único lugar onde os parâmetros aparecem na tela. Não repetir em outras seções.

### `render_chemical_parameters_table()`
**Localização:** Page 2
**Conteúdo:** Tabela detalhada de parâmetros químicos
**Diferença do AvailabilityCard:**
- Mais espaço vertical
- Foco exclusivo em composição
- Métricas de destaques
- Linkagem para comparação

---

## **Regras de Ouro**

### ✅ Faça:
1. **Especialização**: Cada página tem um propósito bem definido
2. **Progressão**: User journey é linear (1 → 2 → 3 → 4)
3. **Referência**: Links internos para navegar entre contextos
4. **Reutilização**: Componentes compartilhados sem duplicação

### ❌ Evite:
1. **Redundância**: Mesma tabela em duas páginas
2. **Sprawl**: Muita informação em uma página
3. **Confusão**: Duas funções com nomes similares
4. **Silos**: Páginas desconectadas sem contexto

---

## **Exemplo: Fluxo do Usuário**

```
Usuário acessa Page 1 (Disponibilidade)
  ↓
Vê resumo executivo + AvailabilityCard
  ↓
Quer entender melhor a composição
  ↓
Clica em "Parâmetros Químicos" (Page 2)
  ↓
Vê tabelas detalhadas com comparações
  ↓
Tem dados de laboratório para validar
  ↓
Vai para "Comparação Laboratorial" (Page 4)
  ↓
Valida seus dados
  ↓
Volta para Page 1 com mais confiança
```

---

## **Última Atualização**
- **Data:** 2025-10-17
- **Commit:** `6dc3509` - Removida redundância de tabelas
- **Mudança:** SECTION 6 (duplicate availability factors) removida de Page 1
