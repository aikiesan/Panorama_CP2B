# 🎯 Plano de Integração SOLID: Metodologia de Disponibilidade
**Status:** Aprovado pelo usuário - Pronto para implementação
**Data:** 16/10/2025
**Progresso:** Phase 1.1 Completa (AvailabilityCalculator criado)

---

## 📊 Status Atual

### ✅ Completado:
1. **Phase 1.1**: `src/services/availability_calculator.py` criado
   - Classe `AvailabilityCalculator` com fórmula validada
   - Método `calculate(fc, fcp, fs, fl)` → retorna % disponibilidade
   - Método `calculate_from_factors()` → retorna % + quantidade absoluta
   - Método `explain_calculation()` → explicação passo-a-passo
   - Método `validate_factors()` → validação de inputs
   - **210 linhas, bem documentado, testável**

2. **Estrutura de pastas**: `src/services/` criada com `__init__.py`

3. **Scenarios estruturados**: Todos os arquivos de resíduos corrigidos (flat float structure)

4. **App funcionando**: Rodando em http://localhost:8502 sem erros

---

## 🔄 Próximas Fases (Ordem de Implementação)

### **Phase 1.2: ScenarioManager Service** ⏭️ PRÓXIMO
**Arquivo:** `src/services/scenario_manager.py`

**Responsabilidade:** Gerenciar 4 cenários (Pessimista, Realista, Otimista, Teórico)

**Estrutura:**
```python
class ScenarioManager:
    """Manage availability scenarios with different factor combinations"""

    SCENARIOS = {
        'Pessimista': 'Conservative factors (max competition)',
        'Realista': 'Calibrated real-world factors (baseline)',
        'Otimista': 'Optimistic factors (min competition)',
        'Teórico (100%)': 'No competition (theoretical max)'
    }

    @staticmethod
    def get_scenario_factors(scenario_name: str, residue_data) -> dict:
        """
        Get adjusted factors for a specific scenario.

        Args:
            scenario_name: 'Pessimista', 'Realista', 'Otimista', or 'Teórico (100%)'
            residue_data: ResidueData object with baseline factors

        Returns:
            {'fc': float, 'fcp': float, 'fs': float, 'fl': float}

        Example for Palha de Cana:
            Realista: fc=0.80, fcp=0.65, fs=1.0, fl=0.90 → 25.2%
            Pessimista: fc=0.60, fcp=0.75, fs=0.85, fl=0.80 → 10.2%
            Otimista: fc=0.80, fcp=0.50, fs=1.0, fl=0.90 → 36.0%
            Teórico: fc=1.0, fcp=0.0, fs=1.0, fl=1.0 → 100%
        """
        pass  # Implementar usando ranges de ParameterRange

    @staticmethod
    def compare_scenarios(residue_data) -> dict:
        """
        Compare all 4 scenarios for a residue.

        Returns:
            {
                'Pessimista': {'availability': 10.2, 'ch4': 1250.5},
                'Realista': {'availability': 25.2, 'ch4': 3090.0},
                'Otimista': {'availability': 36.0, 'ch4': 4416.0},
                'Teórico (100%)': {'availability': 100.0, 'ch4': 12270.0}
            }
        """
        pass

    @staticmethod
    def calculate_reduction(realistic: float, theoretical: float) -> float:
        """Calculate % reduction from theoretical to realistic"""
        return ((theoretical - realistic) / theoretical * 100) if theoretical > 0 else 0
```

**Uso de ranges:** Usar `ParameterRange.min` para Pessimista, `ParameterRange.mean` para Realista, `ParameterRange.max` para Otimista

---

### **Phase 1.3: ContributionAnalyzer Service**
**Arquivo:** `src/services/contribution_analyzer.py`

**Responsabilidade:** Analisar contribuições de sub-resíduos e ranking de municípios

**Estrutura:**
```python
class ContributionAnalyzer:
    """Analyze contributions and rankings"""

    @staticmethod
    def calculate_contributions(residue_list: List[ResidueData]) -> List[dict]:
        """
        Calculate % contribution of each residue to total.

        For Cana sub-residues:
            [
                {'name': 'Palha', 'ch4': 5620.0, 'percentage': 92.4},
                {'name': 'Vinhaça', 'ch4': 150.0, 'percentage': 2.5},
                {'name': 'Torta', 'ch4': 310.0, 'percentage': 5.1},
                {'name': 'Bagaço', 'ch4': 0.0, 'percentage': 0.0}
            ]
        """
        pass

    @staticmethod
    def rank_municipalities(residue_data, top_n: int = 10) -> List[dict]:
        """
        Rank top N municipalities by CH4 potential.

        Returns:
            [
                {'rank': 1, 'name': 'Sertãozinho', 'ch4': 120.5, 'electricity': 172.3},
                {'rank': 2, 'name': 'Guariba', 'ch4': 98.3, 'electricity': 140.6},
                ...
            ]
        """
        pass

    @staticmethod
    def aggregate_by_sector(all_residues: dict) -> dict:
        """Aggregate totals by sector (Agricultura, Pecuária, Urbano, Industrial)"""
        pass
```

---

## 📦 Phase 2: UI Components

### **2.1: availability_card.py**
```python
def render_availability_card(residue_data: ResidueData, scenario: str = 'Realista'):
    """
    Render expanded availability card for a residue/sub-residue.

    Shows:
    - Name and icon
    - Generation (kg/ton or m³/m³)
    - Current destination
    - Methane potential (PM)
    - Moisture %
    - FC, FCp, FS, FL factors with MIN/MEAN/MAX ranges
    - Final availability % (calculated)
    - Technical justification (collapsible)
    """
    pass
```

### **2.2: scenario_selector.py**
```python
def render_scenario_selector(key: str = 'scenario_selector') -> str:
    """
    Horizontal radio buttons for 4 scenarios.

    Returns selected scenario name: 'Pessimista', 'Realista', 'Otimista', or 'Teórico (100%)'
    """
    pass
```

### **2.3: contribution_chart.py**
```python
def render_contribution_pie_chart(contributions: List[dict]):
    """Plotly pie chart showing % contribution of each sub-residue"""
    pass

def render_contribution_bar_chart(contributions: List[dict]):
    """Plotly bar chart comparing sub-residues"""
    pass
```

### **2.4: municipality_ranking.py**
```python
def render_top_municipalities_table(municipalities: List[dict], top_n: int = 10):
    """Table with top N municipalities + CH4 + electricity potential"""
    pass

def render_municipality_map(municipalities: List[dict]):
    """Interactive map (Plotly) showing top municipalities (future)"""
    pass
```

### **2.5: validation_panel.py**
```python
def render_data_validation(residue_data: ResidueData):
    """
    Show data validation:
    - SIDRA vs MapBiomas comparison
    - Coverage statistics (municipalities, usinas)
    - Expected divergence explanation
    """
    pass
```

---

## 📊 Phase 3: Data Enrichment

### **3.1: Update ResidueData Model**
**Arquivo:** `src/models/residue_models.py`

**Adicionar campo:**
```python
@dataclass
class ResidueData:
    # ... campos existentes ...

    sub_residues: Optional[List['ResidueData']] = None  # NEW

    def get_sub_residue(self, name: str) -> Optional['ResidueData']:
        """Get sub-residue by name"""
        if not self.sub_residues:
            return None
        return next((r for r in self.sub_residues if r.name == name), None)

    def get_total_ch4(self, scenario: str = 'Realista') -> float:
        """Calculate total CH4 from all sub-residues"""
        if not self.sub_residues:
            return self.scenarios.get(scenario, 0)
        return sum(r.scenarios.get(scenario, 0) for r in self.sub_residues)
```

### **3.2: Reorganizar Cana em Sub-residues**
**Criar:** `src/data/agricultura/cana.py` (arquivo principal)

**Estrutura:**
```python
from .cana_bagaco import BAGACO_DATA
from .cana_palha import PALHA_DATA
from .cana_vinhaca import VINHACA_DATA
from .cana_torta import TORTA_DATA

CANA_DATA = ResidueData(
    name="Cana-de-açúcar",
    category="Agricultura",
    icon="🌾",
    generation="439 Mi ton/ano (SP 2023)",
    destination="Ver sub-resíduos detalhados",
    chemical_params=...,  # Agregado
    availability=...,  # Calculado como média ponderada
    operational=...,
    justification="...",
    scenarios={  # Agregado de todos sub-residues
        "Pessimista": 4354.0,
        "Realista": 6077.0,
        "Otimista": 10089.0,
        "Teórico (100%)": 21000.0
    },
    references=[],  # Consolidado
    sub_residues=[
        BAGACO_DATA,
        PALHA_DATA,
        VINHACA_DATA,
        TORTA_DATA
    ]  # NEW!
)
```

---

## 🎨 Phase 4: Enhanced Disponibilidade Page

### **Nova Estrutura `pages/1_📊_Disponibilidade.py`:**

```python
# IMPORTS
from src.services import AvailabilityCalculator, ScenarioManager, ContributionAnalyzer
from src.ui.components import (
    render_availability_card,
    render_scenario_selector,
    render_contribution_pie_chart,
    render_top_municipalities_table,
    render_data_validation
)

def main():
    # 1. HEADER (já existe)
    render_header()

    # 2. NAVIGATION (já existe)
    render_horizontal_nav("Disponibilidade")

    # 3. SECTOR & RESIDUE SELECTION (já existe)
    selected_sector, selected_residue = render_sector_tabs(key_prefix="disponibilidade")

    if not selected_residue:
        st.info("👆 Selecione um setor e resíduo acima")
        return

    residue_data = get_residue_data(selected_residue)

    # 4. SCENARIO SELECTOR (NEW)
    selected_scenario = render_scenario_selector()

    # 5. MAIN RESULTS (expandido com cenário dinâmico)
    render_main_results_enhanced(residue_data, selected_scenario)

    # 6. SUB-RESIDUE CARDS (NEW - principal feature!)
    if residue_data.sub_residues:
        st.markdown("### 🔬 Disponibilidade por Sub-Resíduo")
        for sub_residue in residue_data.sub_residues:
            render_availability_card(sub_residue, selected_scenario)
    else:
        # Single residue (não tem sub-residues)
        render_availability_card(residue_data, selected_scenario)

    # 7. CONTRIBUTION ANALYSIS (NEW)
    if residue_data.sub_residues:
        contributions = ContributionAnalyzer.calculate_contributions(
            residue_data.sub_residues
        )
        col1, col2 = st.columns(2)
        with col1:
            render_contribution_pie_chart(contributions)
        with col2:
            render_contribution_bar_chart(contributions)

    # 8. SCENARIO COMPARISON (melhorado)
    render_scenario_comparison_enhanced(residue_data.scenarios, selected_scenario)

    # 9. TOP MUNICIPALITIES (NEW)
    if residue_data.top_municipalities:
        municipalities = ContributionAnalyzer.rank_municipalities(residue_data)
        render_top_municipalities_table(municipalities)

    # 10. DATA VALIDATION (NEW)
    render_data_validation(residue_data)

    # 11. JUSTIFICATION (já existe)
    render_justification(residue_data)
```

---

## 🧪 Phase 5: Testing & Polish

### **Checklist:**
- [ ] Testar AvailabilityCalculator com dados reais de Cana
- [ ] Validar cálculos de cenários (comparar com metodologia original)
- [ ] Testar com todos os resíduos (Agricultura, Pecuária, Urbano)
- [ ] Verificar responsividade em telas pequenas
- [ ] Adicionar tooltips explicativos em todos os componentes
- [ ] Verificar consistência visual (cores, espaçamentos)
- [ ] Testar navegação entre cenários (state management)
- [ ] Validar exportação de dados (CSV, JSON)
- [ ] Performance: medir tempo de renderização
- [ ] Acessibilidade: testar com leitor de tela

---

## 📁 Arquivos Criados (Progresso)

### ✅ Completados:
1. `src/services/__init__.py`
2. `src/services/availability_calculator.py` (210 linhas)

### ⏳ Pendentes:
3. `src/services/scenario_manager.py` (~200 linhas)
4. `src/services/contribution_analyzer.py` (~150 linhas)
5. `src/ui/components/__init__.py`
6. `src/ui/components/availability_card.py` (~150 linhas)
7. `src/ui/components/scenario_selector.py` (~80 linhas)
8. `src/ui/components/contribution_chart.py` (~120 linhas)
9. `src/ui/components/municipality_ranking.py` (~100 linhas)
10. `src/ui/components/validation_panel.py` (~100 linhas)
11. `src/data/agricultura/cana.py` (arquivo agregador)
12. Atualizar `src/models/residue_models.py` (adicionar sub_residues)
13. Reescrever `pages/1_📊_Disponibilidade.py` (~400 linhas)

**Total estimado:** ~1600 linhas de código novo/atualizado

---

## 🎯 Objetivo Final

**Dashboard Completo:**
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Disponibilidade de Resíduos para Biogás                 │
│ Fatores de Disponibilidade Real e Cenários de Potencial    │
└─────────────────────────────────────────────────────────────┘

🎯 Selecione o Setor e Resíduo
Setor: [🌾 Agricultura ▼]    Resíduo: [🌾 Cana-de-açúcar ▼]

🎭 Cenário de Disponibilidade
( ) Pessimista  (•) Realista  ( ) Otimista  ( ) Teórico 100%

📊 Principais Resultados (Cenário Realista)
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 💨 Biogás   │ 📉 Redução  │ ✅ Dispon.  │ ⚡ Energia  │
│ 6.077 Mi m³ │ 72% teórico │ 25.2%       │ 8.690 GWh  │
└─────────────┴─────────────┴─────────────┴─────────────┘

🔬 Disponibilidade por Sub-Resíduo

▼ 🌾 Bagaço de Cana - Disponibilidade: 0.0%
  📈 Geração: 280 kg/ton cana
  🎯 Destino: 100% cogeração elétrica e vapor
  💧 PM: 175 m³ CH₄/ton MS | 💦 Umidade: 50%
  🔢 FC:1.0 | FCp:1.0 | FS:1.0 | FL:1.0 → 0.0%
  📝 Justificativa: Competição obrigatória com cogeração...

▼ 🌾 Palha de Cana - Disponibilidade: 25.2%
  📈 Geração: 280 kg/ton cana
  🎯 Destino: 65% retorno solo + 35% E2G/bioenergia
  💧 PM: 200 m³ CH₄/ton MS | 💦 Umidade: 15%
  🔢 Fatores (MIN/MEAN/MAX):
      FC: 0.60/0.80/0.80 → Adotado: 0.80
      FCp: 0.40/0.65/0.65 → Adotado: 0.65
      FS: 0.70/0.85/1.0 → Adotado: 1.0
      FL: 0.80/0.90/0.90 → Adotado: 0.90
  ✅ Disponibilidade Final: 25.2%
  📝 Justificativa: Embrapa recomenda 50-70% retorno...

[... Vinhaça + Torta ...]

📊 Contribuição por Sub-Resíduo
┌─────────────┬─────────────┐
│ Palha 92.4% │ [Pie Chart] │
│ Torta 5.1%  │   & Bar     │
│ Vinhaça 2.5%│   Charts    │
└─────────────┴─────────────┘

🏆 Top 10 Municípios Produtores
┌────┬─────────────┬────────┬───────┐
│ #  │ Município   │ CH₄    │ GWh   │
├────┼─────────────┼────────┼───────┤
│ 1  │ Sertãozinho │ 120.5  │ 172.3 │
│ 2  │ Guariba     │ 98.3   │ 140.6 │
└────┴─────────────┴────────┴───────┘

✅ Validação dos Dados
🗺️ SIDRA: 5.48 Mi ha | 🛰️ MapBiomas: 5.85 Mi ha
Divergência: +6.5% (esperada - ciclo semi-perene)
```

---

## 💡 Notas Importantes

1. **ParameterRange usage**: Todos os fatores já têm ranges (min/mean/max) nos arquivos de resíduos
2. **Backward compatibility**: Manter páginas antigas funcionando durante migração
3. **Performance**: Usar `@st.cache_data` para cálculos pesados
4. **Testing**: Criar `tests/services/` para unit tests dos services
5. **Documentation**: Manter docstrings completas em todos os métodos

---

## 🚀 Comandos Úteis para Próxima Sessão

```bash
# Verificar app funcionando
streamlit run app.py --server.port 8502

# Testar imports
python -c "from src.services import AvailabilityCalculator; print(AvailabilityCalculator.calculate(0.8, 0.65, 1.0, 0.9))"

# Rodar testes (quando criados)
pytest tests/services/

# Limpar cache
python -c "import pathlib; [f.unlink() for f in pathlib.Path('src').rglob('*.pyc')]"
```

---

**Próxima Sessão: Começar com Phase 1.2 (ScenarioManager)**
