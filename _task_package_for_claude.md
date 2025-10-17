Olá, Claude Code. Vamos iniciar a próxima fase do projeto PanoramaCP2B.

### 🎯 1. OBJETIVO DA TAREFA

Vamos focar em **completar o setor Industrial**.

**Objetivo:** Popular os dados para os 4 resíduos industriais identificados:
1. Soro de laticínios (leite)
2. Soro de laticínios (derivados)
3. Bagaço de cervejarias
4. Efluente de frigoríficos

**Requisitos:**
1. Criar os arquivos Python correspondentes para cada resíduo dentro de `src/data/industrial/`.
2. Usar os dados do nosso banco de dados validado para preencher os objetos `ResidueData`.
3. Adicionar os novos resíduos ao arquivo `src/data/industrial/__init__.py` para que eles sejam carregados no registro central.
4. Garantir que todos os novos dados passem pela validação do método `.validate()`.

---

### 🗺️ 2. ESTRUTURA DOS ARQUIVOS

Aqui está a estrutura de arquivos relevante para esta tarefa:

```
ERRO: O comando 'tree' não foi encontrado. Por favor, forneça a estrutura manualmente.```

---

### 📦 3. CONTEÚDO DOS ARQUIVOS

Aqui está o conteúdo atual dos arquivos que precisamos modificar ou referenciar.

--- START OF FILE src/data/industrial/__init__.py ---

```python
"""
Industrial Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all industrial residues
Currently: Placeholders for future implementation
"""

# Registry of all industrial residues (empty for now)
INDUSTRIAL_RESIDUES = {}

# Sector metadata
INDUSTRIAL_SECTOR_INFO = {
    "name": "Industrial",
    "icon": "🏭",
    "description": "Efluentes e resíduos industriais",
    "color": "#8b5cf6",
    "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%)",
    "border_color": "#8b5cf6",
    "residues": list(INDUSTRIAL_RESIDUES.keys())  # Empty list
}

__all__ = [
    'INDUSTRIAL_RESIDUES',
    'INDUSTRIAL_SECTOR_INFO',
]

```

--- END OF FILE src/data/industrial/__init__.py ---

--- START OF FILE src/data/urbano/rpo.py ---

```python
"""
RPO - Poda Urbana - Placeholder
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only RPO - Poda Urbana data (placeholder)
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# RPO - PODA URBANA (PLACEHOLDER)
# ============================================================================

RPO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=75.0,
    bmp_unit="Estimativa preliminar | Aguardando estudos específicos",
    ts=50.0,
    vs=80.0,
    vs_basis="Estimativa - alta lignina",
    moisture=50.0,
    cn_ratio=40.0,
    ph=None,
    ch4_content=55.0
)

RPO_AVAILABILITY = AvailabilityFactors(
    fc=0.7,
    fcp=0.3,
    fs=0.8,
    fl=0.9,
    final_availability=35.0
)

RPO_OPERATIONAL = OperationalParameters(
    hrt="40-60 dias",
    temperature="35-40°C mesofílica",
    reactor_type="CSTR, pré-tratamento recomendado",
    olr="Dados não disponíveis"
)

RPO_JUSTIFICATION = """
**⚠️ DADOS PRELIMINARES - AGUARDANDO VALIDAÇÃO**

RPO mencionado em estudos como parte de GFW (Garden Food Waste) mas sem caracterização específica.
Necessário: estudos BMP dedicados, análise de sazonalidade, avaliação de pré-tratamentos.
"""

RPO_SCENARIOS = {
    "Pessimista": 50.0,
    "Realista": 100.0,
    "Otimista": 150.0,
    "Teórico (100%)": 200.0,
}

RPO_REFERENCES = [
    ScientificReference(
        title="RPO mencionado como fração de RSU mas sem estudos dedicados",
        authors="Diversos",
        year=2024,
        doi=None,
        scopus_link=None,
        journal="Observação consolidada",
        relevance="Low",
        key_findings=[
            "GFW = 20% do OFMSW em Campinas",
            "Necessário: estudos BMP específicos"
        ]
    ),
]

RPO_DATA = ResidueData(
    name="RPO - Poda Urbana",
    category="Urbano",
    icon="🌳",
    generation="Dados em coleta | Estimativa: 20% da fração orgânica RSU",
    destination="A definir - aguardando estudos",
    chemical_params=RPO_CHEMICAL_PARAMS,
    availability=RPO_AVAILABILITY,
    operational=RPO_OPERATIONAL,
    justification=RPO_JUSTIFICATION,
    scenarios=RPO_SCENARIOS,
    references=RPO_REFERENCES
)

```

--- END OF FILE src/data/urbano/rpo.py ---

--- START OF FILE src/data/urbano/lodo.py ---

```python
"""
Lodo de Esgoto (ETE) - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Lodo de Esgoto (ETE) data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# LODO DE ESGOTO (ETE)
# ============================================================================


RPO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=0.0,
    bmp_unit="DADOS INSUFICIENTES - Aguardando estudos adicionais",
    ts=0.0,
    vs=0.0,
    vs_basis="Não disponível - Mencionado como 20% da fração orgânica RSU (GFW - Garden Food Waste)",
    moisture=0.0,
    cn_ratio=None,
    ph=None,
    ch4_content=None
)

RPO_AVAILABILITY = AvailabilityFactors(
    fc=0.0,
    fcp=0.0,
    fs=1.0,
    fl=0.0,
    final_availability=0.0
)

RPO_OPERATIONAL = OperationalParameters(
    hrt="Dados não disponíveis",
    temperature="Dados não disponíveis",
    reactor_type="Não caracterizado",
    olr="Dados não disponíveis"
)

RPO_JUSTIFICATION = """
**⚠️ DADOS INSUFICIENTES - AGUARDANDO ESTUDOS ADICIONAIS**

**Status**: Resíduos de poda urbana (folhas, galhos, aparas de árvores) são mencionados em estudos de RSU
como parte da fração orgânica (GFW - Garden Food Waste = ~20% do OFMSW em Campinas), mas **NÃO HÁ ESTUDOS
DEDICADOS** com caracterização BMP, físico-química ou fatores de correção específicos para RPO.

**Dados parciais identificados**:
- Campinas (Pacheco 2022): GFW = 20.0% do OFMSW (Green/Garden Food Waste)
- Campinas (Rodrigues 2022): Jardim/poda = 20.03% da fração orgânica total

**Necessidades para integração futura**:
1. Estudos BMP específicos para resíduos de poda (folhas vs galhos vs aparas)
2. Caracterização físico-química (lignina, celulose, hemicelulose)
3. Avaliação de pré-tratamentos (trituração, hidrólise)
4. Análise de sazonalidade (poda sazonal vs contínua)
5. Logística de coleta (descentralizada municipal)

**Recomendação**: Agrupar temporariamente com RSU ou aguardar estudos dedicados.
"""

RPO_SCENARIOS = {
    "Pessimista": 0.0,
    "Realista": 0.0,
    "Otimista": 0.0,
    "Teórico (100%)": 0.0
}

RPO_REFERENCES = [
    ScientificReference(
        title="Nota: RPO mencionado como fração de RSU mas sem estudos dedicados",
        authors="Diversos",
        year=2024,
        doi=None,
        scopus_link=None,
        journal="Observação do banco de dados RSU_RPO",
        relevance="Low",
        key_findings=[
            "GFW (Garden Food Waste) = 20% do OFMSW em Campinas (Pacheco 2022)",
            "Jardim/poda = 20.03% orgânico total Campinas (Rodrigues 2022)",
            "Necessário: estudos BMP específicos para resíduos de poda urbana"
        ]
    )
]

RPO_DATA = ResidueData(
    name="RPO - Poda Urbana",
    category="Urbano",
    icon="🌳",
    generation="DADOS INSUFICIENTES | Mencionado como ~20% fração orgânica RSU",
    destination="Aguardando caracterização e estudos BMP dedicados",
    chemical_params=RPO_CHEMICAL_PARAMS,
    availability=RPO_AVAILABILITY,
    operational=RPO_OPERATIONAL,
    justification=RPO_JUSTIFICATION,
    scenarios=RPO_SCENARIOS,
    references=RPO_REFERENCES
)


# =============================================================================
# 3. LODO DE ESGOTO (ETE) - PLACEHOLDER
# =============================================================================

LODO_ETE_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=0.0,
    bmp_unit="DADOS INSUFICIENTES - Apenas dados de co-digestão disponíveis",
    ts=0.0,
    vs=0.0,
    vs_basis="Não disponível - Mencionado apenas em co-digestão RSU+Lodo",
    moisture=0.0,
    cn_ratio=None,
    ph=None,
    ch4_content=None
)

LODO_ETE_AVAILABILITY = AvailabilityFactors(
    fc=0.0,
    fcp=0.0,
    fs=1.0,
    fl=0.0,
    final_availability=0.0
)

LODO_ETE_OPERATIONAL = OperationalParameters(
    hrt="Dados não disponíveis para mono-digestão",
    temperature="Dados não disponíveis",
    reactor_type="Não caracterizado",
    olr="Dados não disponíveis"
)

LODO_ETE_JUSTIFICATION = """
**⚠️ DADOS INSUFICIENTES - AGUARDANDO ESTUDOS MONO-DIGESTÃO**

**Status**: Lodo de esgoto (ETE) é mencionado em **co-digestão** com RSU/FW, mas **NÃO HÁ CARACTERIZAÇÃO
DEDICADA** para mono-digestão de lodo como resíduo standalone no banco de dados atual.

**Dados parciais identificados (co-digestão)**:
1. **Alves et al. 2022 (RJ)**: Co-digestão FW+Lodo (PS+FW)
   - BMP co-digestão: 236.1 mLCH4/gVS
   - BMP ternária (PS+FW+3% glicerol): 525.7 mLCH4/gVS
   - Lodo usado como co-substrato, não caracterizado isoladamente

2. **Crispim et al. 2024 (MG)**: Modelagem RSU+lodo em consórcios
   - Foco em biogás de aterro para H₂/amônia
   - Lodo mencionado apenas em geração total (RSU+lodo)

3. **Inóculo ETE Barueri**: Usado em D'Aquino 2022 (USP) como inóculo (8.7% SV)

**Necessidades para integração futura**:
1. Estudos BMP mono-digestão de lodo de ETE brasileiro
2. Caracterização físico-química completa (TS, VS, C/N, metais pesados)
3. Análise de tratamentos prévios do lodo (aeróbio, anaeróbio, digerido)
4. Avaliação de disponibilidade (geração por ETE, logística)
5. Fatores de correção específicos (FC, FCp, FL)

**Contexto Brasil**:
- Lodo de ETE tem grande potencial (milhões ton/ano)
- Legislação CONAMA requer tratamento adequado
- Co-digestão com RSU/FW pode otimizar C/N e estabilidade

**Recomendação**: Integrar dados quando disponíveis estudos mono-digestão brasileiros.
"""

LODO_ETE_SCENARIOS = {
    "Pessimista": 0.0,
    "Realista": 0.0,
    "Otimista": 0.0,
    "Teórico (100%)": 0.0
}

LODO_ETE_REFERENCES = [
    ScientificReference(
        title="Investigating the effect of crude glycerol from biodiesel industry on the anaerobic co-digestion of sewage sludge and food waste in ternary mixtures",
        authors="Alves, I.R.F.S.; Mahler, C.F.; Oliveira, L.B.; et al.",
        year=2022,
        doi="10.1016/j.energy.2021.122818",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85122101489&origin=inward",
        journal="Energy",
        relevance="Medium",
        key_findings=[
            "Co-digestão FW+Lodo (não mono-digestão de lodo isolado)",
            "BMP co-digestão PS+FW: 236.1 mLCH4/gVS",
            "BMP ternária PS+FW+3%GL: 525.7 mLCH4/gVS (otimizado)",
            "Lodo usado como co-substrato - caracterização parcial incluída"
        ]
    ),
    ScientificReference(
        title="An economic study of hydrogen and ammonia generation from the reforming of biogas from co-digestion of municipal solid waste and wastewater sludge in a Brazilian state",
        authors="Crispim, A.M.C.; Barros, R.M.; Tiago Filho, G.L.; et al.",
        year=2024,
        doi="10.1016/j.ijhydene.2024.04.108",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85191374697&origin=inward",
        journal="International Journal of Hydrogen Energy",
        relevance="Low",
        key_findings=[
            "RSU+lodo mencionado conjuntamente em geração consórcios MG",
            "Foco em biogás de aterro para H₂/amônia (não BMP lodo)",
            "Lodo não caracterizado separadamente"
        ]
    )
]

LODO_ETE_DATA = ResidueData(
    name="Lodo de Esgoto (ETE)",
    category="Urbano",
    icon="💧",
    generation="DADOS INSUFICIENTES | Mencionado apenas em co-digestão RSU+Lodo",
    destination="Aguardando estudos mono-digestão brasileiros | Potencial milhões ton/ano",
    chemical_params=LODO_ETE_CHEMICAL_PARAMS,
    availability=LODO_ETE_AVAILABILITY,
    operational=LODO_ETE_OPERATIONAL,
    justification=LODO_ETE_JUSTIFICATION,
    scenarios=LODO_ETE_SCENARIOS,
    references=LODO_ETE_REFERENCES
)



```

--- END OF FILE src/data/urbano/lodo.py ---

--- START OF FILE src/models/residue_models.py ---

```python
"""
Residue Data Models - Clean Data Structures (SOLID: Single Responsibility)
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

This module contains only dataclass definitions - no data, no business logic.
Follows the Single Responsibility Principle: defines structure only.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class ParameterRange:
    """Represents a parameter with min, mean, and max values"""
    min: Optional[float] = None
    mean: Optional[float] = None
    max: Optional[float] = None
    unit: Optional[str] = None

    def __post_init__(self):
        """Validate that at least mean is provided"""
        if self.mean is None and self.min is None and self.max is None:
            raise ValueError("At least one value (min, mean, or max) must be provided")

    def to_display(self) -> str:
        """Format range for display"""
        unit_str = f" {self.unit}" if self.unit else ""

        if self.min is not None and self.max is not None and self.mean is not None:
            return f"{self.min:.1f} - {self.mean:.1f} - {self.max:.1f}{unit_str}"
        elif self.min is not None and self.max is not None:
            return f"{self.min:.1f} - {self.max:.1f}{unit_str}"
        elif self.mean is not None:
            return f"{self.mean:.1f}{unit_str}"
        else:
            return "N/A"

    def has_range(self) -> bool:
        """Check if this parameter has range data (min/max)"""
        return self.min is not None or self.max is not None


@dataclass
class ChemicalParameters:
    """Chemical composition and methane potential parameters"""
    bmp: float
    bmp_unit: str
    ts: float
    vs: float
    vs_basis: str
    moisture: float
    cn_ratio: Optional[float] = None
    ph: Optional[float] = None
    cod: Optional[float] = None
    nitrogen: Optional[float] = None
    carbon: Optional[float] = None
    ch4_content: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    protein: Optional[float] = None
    toc: Optional[float] = None

    # Range data from literature validation
    bmp_range: Optional[ParameterRange] = None
    ts_range: Optional[ParameterRange] = None
    vs_range: Optional[ParameterRange] = None
    moisture_range: Optional[ParameterRange] = None
    cn_ratio_range: Optional[ParameterRange] = None
    ph_range: Optional[ParameterRange] = None
    cod_range: Optional[ParameterRange] = None
    nitrogen_range: Optional[ParameterRange] = None
    carbon_range: Optional[ParameterRange] = None
    ch4_content_range: Optional[ParameterRange] = None
    phosphorus_range: Optional[ParameterRange] = None
    potassium_range: Optional[ParameterRange] = None
    protein_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        result = {
            "BMP": f"{self.bmp} {self.bmp_unit}",
            "Sólidos Totais (TS)": f"{self.ts}%",
            "Sólidos Voláteis (VS)": f"{self.vs}% {self.vs_basis}",
            "Umidade": f"{self.moisture}%"
        }
        if self.cn_ratio: result["Relação C:N"] = f"{self.cn_ratio}"
        if self.ph: result["pH"] = f"{self.ph}"
        if self.cod: result["DQO"] = f"{self.cod} mg/L"
        if self.nitrogen: result["Nitrogênio (N)"] = f"{self.nitrogen}%"
        if self.carbon: result["Carbono (C)"] = f"{self.carbon}%"
        if self.ch4_content: result["Conteúdo CH₄"] = f"{self.ch4_content}%"
        return result

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert chemical parameters to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        param_mapping = [
            ("BMP", self.bmp, self.bmp_range, self.bmp_unit),
            ("Sólidos Totais (ST)", self.ts, self.ts_range, "%"),
            ("Sólidos Voláteis (SV)", self.vs, self.vs_range, "% ST"),
            ("Umidade", self.moisture, self.moisture_range, "%"),
            ("Relação C:N", self.cn_ratio, self.cn_ratio_range, ""),
            ("pH", self.ph, self.ph_range, ""),
            ("DQO", self.cod, self.cod_range, "mg/L"),
            ("Nitrogênio (N)", self.nitrogen, self.nitrogen_range, "%"),
            ("Carbono (C)", self.carbon, self.carbon_range, "%"),
            ("Conteúdo CH₄", self.ch4_content, self.ch4_content_range, "%"),
            ("Fósforo (P₂O₅)", self.phosphorus, self.phosphorus_range, "%"),
            ("Potássio (K₂O)", self.potassium, self.potassium_range, "%"),
            ("Proteína", self.protein, self.protein_range, "%"),
        ]

        for param_name, value, range_obj, unit in param_mapping:
            if value is None:
                continue

            if range_obj and range_obj.has_range():
                ranges_data.append({
                    "Parâmetro": param_name,
                    "Mínimo": f"{range_obj.min:.2f}" if range_obj.min is not None else "-",
                    "Média/Valor": f"{value:.2f}",
                    "Máximo": f"{range_obj.max:.2f}" if range_obj.max is not None else "-",
                    "Unidade": unit
                })
            else:
                # No range data, show only mean value
                ranges_data.append({
                    "Parâmetro": param_name,
                    "Mínimo": "-",
                    "Média/Valor": f"{value:.2f}",
                    "Máximo": "-",
                    "Unidade": unit
                })

        return ranges_data


@dataclass
class AvailabilityFactors:
    """Availability correction factors for residues"""
    fc: float
    fcp: float
    fs: float
    fl: float
    final_availability: float

    # Range data from literature validation
    fc_range: Optional[ParameterRange] = None
    fcp_range: Optional[ParameterRange] = None
    fs_range: Optional[ParameterRange] = None
    fl_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        return {
            "FC (Coleta)": f"{self.fc:.2f}",
            "FCp (Competição)": f"{self.fcp:.2f}",
            "FS (Sazonal)": f"{self.fs:.2f}",
            "FL (Logístico)": f"{self.fl:.2f}",
            "Disponibilidade Final": f"{self.final_availability:.1f}%"
        }

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert availability factors to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        param_mapping = [
            ("FC (Fator de Coleta)", self.fc, self.fc_range, "Eficiência de recolhimento"),
            ("FCp (Fator de Competição)", self.fcp, self.fcp_range, "Competição por usos alternativos"),
            ("FS (Fator Sazonal)", self.fs, self.fs_range, "Variação sazonal"),
            ("FL (Fator Logístico)", self.fl, self.fl_range, "Restrição por distância"),
        ]

        for param_name, value, range_obj, justification in param_mapping:
            if range_obj and range_obj.has_range():
                ranges_data.append({
                    "Fator": param_name,
                    "Mínimo": f"{range_obj.min:.2f}" if range_obj.min is not None else "-",
                    "Valor Adotado": f"{value:.2f}",
                    "Máximo": f"{range_obj.max:.2f}" if range_obj.max is not None else "-",
                    "Justificativa": justification
                })
            else:
                ranges_data.append({
                    "Fator": param_name,
                    "Mínimo": "-",
                    "Valor Adotado": f"{value:.2f}",
                    "Máximo": "-",
                    "Justificativa": justification
                })

        # Add final availability row
        ranges_data.append({
            "Fator": "Disponibilidade Final (SAF)",
            "Mínimo": "-",
            "Valor Adotado": f"{self.final_availability:.1f}%",
            "Máximo": "-",
            "Justificativa": "Produto de todos os fatores"
        })

        return ranges_data


@dataclass
class OperationalParameters:
    """Operational parameters for anaerobic digestion"""
    hrt: str
    temperature: str
    fi_ratio: Optional[float] = None
    olr: Optional[str] = None
    reactor_type: Optional[str] = None
    tan_threshold: Optional[str] = None
    vfa_limit: Optional[str] = None

    # Range data from literature validation (TRH in days, Temperature in °C)
    hrt_range: Optional[ParameterRange] = None
    temperature_range: Optional[ParameterRange] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        result = {
            "TRH (Tempo de Retenção Hidráulica)": self.hrt,
            "Temperatura": self.temperature,
        }
        if self.fi_ratio: result["Razão F/I"] = f"{self.fi_ratio}"
        if self.olr: result["TCO (Taxa de Carga Orgânica)"] = self.olr
        if self.reactor_type: result["Tipo de Reator"] = self.reactor_type
        if self.tan_threshold: result["Limite TAN"] = self.tan_threshold
        if self.vfa_limit: result["Limite AGV"] = self.vfa_limit
        return result

    def to_range_table(self) -> List[Dict[str, str]]:
        """
        Convert operational parameters to table format showing MIN/MEAN/MAX ranges
        Returns list of dicts for DataFrame display
        """
        ranges_data = []

        # TRH and Temperature with ranges
        if self.hrt_range and self.hrt_range.has_range():
            ranges_data.append({
                "Parâmetro": "TRH (Tempo de Retenção Hidráulica)",
                "Mínimo": f"{self.hrt_range.min:.0f} dias" if self.hrt_range.min else "-",
                "Valor Operacional": self.hrt,
                "Máximo": f"{self.hrt_range.max:.0f} dias" if self.hrt_range.max else "-",
            })
        else:
            ranges_data.append({
                "Parâmetro": "TRH (Tempo de Retenção Hidráulica)",
                "Mínimo": "-",
                "Valor Operacional": self.hrt,
                "Máximo": "-",
            })

        if self.temperature_range and self.temperature_range.has_range():
            ranges_data.append({
                "Parâmetro": "Temperatura",
                "Mínimo": f"{self.temperature_range.min:.0f}°C" if self.temperature_range.min else "-",
                "Valor Operacional": self.temperature,
                "Máximo": f"{self.temperature_range.max:.0f}°C" if self.temperature_range.max else "-",
            })
        else:
            ranges_data.append({
                "Parâmetro": "Temperatura",
                "Mínimo": "-",
                "Valor Operacional": self.temperature,
                "Máximo": "-",
            })

        # Other parameters (no ranges)
        if self.fi_ratio:
            ranges_data.append({
                "Parâmetro": "Razão F/I (Alimento/Inóculo)",
                "Mínimo": "-",
                "Valor Operacional": f"{self.fi_ratio}",
                "Máximo": "-",
            })

        if self.olr:
            ranges_data.append({
                "Parâmetro": "TCO (Taxa de Carga Orgânica)",
                "Mínimo": "-",
                "Valor Operacional": self.olr,
                "Máximo": "-",
            })

        if self.reactor_type:
            ranges_data.append({
                "Parâmetro": "Tipo de Reator",
                "Mínimo": "-",
                "Valor Operacional": self.reactor_type,
                "Máximo": "-",
            })

        return ranges_data


@dataclass
class ScientificReference:
    """Scientific paper reference"""
    title: str
    authors: str
    year: int
    doi: Optional[str] = None
    scopus_link: Optional[str] = None
    journal: Optional[str] = None
    relevance: str = "High"
    key_findings: List[str] = None
    data_type: str = "Literatura Científica"

    def __post_init__(self):
        if self.key_findings is None:
            self.key_findings = []


@dataclass
class ResidueData:
    """Complete residue data with validated factors"""
    name: str
    category: str
    icon: str
    generation: str
    destination: str
    chemical_params: ChemicalParameters
    availability: AvailabilityFactors
    operational: OperationalParameters
    justification: str
    scenarios: Dict[str, float]
    references: List[ScientificReference]
    top_municipalities: Optional[List[Dict]] = None
    validation_data: Optional[Dict] = None
    contribution_breakdown: Optional[Dict] = None
    sub_residues: Optional[List['ResidueData']] = None

    def __post_init__(self):
        """Validate residue data on initialization"""
        from src.utils.validators import validate_residue_data

        is_valid, errors = validate_residue_data(self)
        if not is_valid:
            print(f"[WARNING] Validation issues in {self.name}:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate complete residue data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        from src.utils.validators import validate_residue_data
        return validate_residue_data(self)

    def check_completeness(self) -> Dict[str, Any]:
        """
        Check data completeness.

        Returns:
            Dictionary with completeness metrics
        """
        from src.utils.validators import check_data_completeness
        return check_data_completeness(self)

    def to_summary_dict(self) -> Dict[str, Any]:
        """
        Convert to summary dictionary for display.

        Returns:
            Dictionary with key residue information
        """
        return {
            "name": self.name,
            "category": self.category,
            "icon": self.icon,
            "bmp": self.chemical_params.bmp,
            "bmp_unit": self.chemical_params.bmp_unit,
            "availability": self.availability.final_availability,
            "realistic_potential": self.scenarios.get("Realista", 0),
            "references_count": len(self.references)
        }

    def get_sub_residue(self, name: str) -> Optional['ResidueData']:
        """
        Get a sub-residue by name.

        Useful for accessing specific sub-components of composite residues.
        For example, getting "Palha" from Cana-de-açúcar.

        Args:
            name: Name of the sub-residue to find

        Returns:
            ResidueData object if found, None otherwise

        Example:
            >>> palha = cana_data.get_sub_residue("Palha de Cana-de-açúcar (Palhiço)")
            >>> if palha:
            ...     print(f"Found: {palha.name}")
        """
        if not self.sub_residues:
            return None

        for sub_residue in self.sub_residues:
            if sub_residue.name == name:
                return sub_residue

        return None

    def get_total_ch4(self, scenario: str = 'Realista') -> float:
        """
        Calculate total CH4 potential from all sub-residues.

        If the residue has sub-residues, returns their sum.
        If no sub-residues, returns the residue's own scenario value.

        Args:
            scenario: Which scenario to sum ('Pessimista', 'Realista', 'Otimista', 'Teórico')

        Returns:
            Total CH4 potential for the scenario

        Example:
            >>> total = cana_data.get_total_ch4('Realista')
            >>> total
            6077.0  # Sum of Bagaço + Palha + Vinhaça + Torta
        """
        if not self.sub_residues:
            # No sub-residues, return own value
            return self.scenarios.get(scenario, 0.0)

        # Sum sub-residues
        total = 0.0
        for sub_residue in self.sub_residues:
            sub_ch4 = sub_residue.scenarios.get(scenario, 0.0)
            total += sub_ch4

        return total

    def has_sub_residues(self) -> bool:
        """
        Check if this residue has sub-residues.

        Useful for conditional logic in UI components.

        Returns:
            True if sub_residues list exists and is not empty

        Example:
            >>> if cana_data.has_sub_residues():
            ...     print("This is a composite residue")
        """
        return self.sub_residues is not None and len(self.sub_residues) > 0

    def get_sub_residue_count(self) -> int:
        """
        Get the count of sub-residues.

        Returns:
            Number of sub-residues, 0 if none

        Example:
            >>> count = cana_data.get_sub_residue_count()
            >>> count
            4  # Bagaço, Palha, Vinhaça, Torta
        """
        if not self.sub_residues:
            return 0
        return len(self.sub_residues)

```

--- END OF FILE src/models/residue_models.py ---

--- START OF FILE src/data/residue_registry.py ---

```python
"""
Central Residue Registry - SOLID Architecture
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Central registry for all residues across all sectors
Provides backward-compatible API with the old research_data.py

Open/Closed Principle: Easy to add new sectors/residues without modifying existing code
"""

from typing import Dict, List, Optional
from src.models.residue_models import ResidueData

# Import all sector registries
from src.data.agricultura import AGRICULTURA_RESIDUES, AGRICULTURA_SECTOR_INFO
from src.data.pecuaria import PECUARIA_RESIDUES, PECUARIA_SECTOR_INFO
from src.data.urbano import URBANO_RESIDUES, URBANO_SECTOR_INFO
from src.data.industrial import INDUSTRIAL_RESIDUES, INDUSTRIAL_SECTOR_INFO


# ============================================================================
# UNIFIED REGISTRIES
# ============================================================================

# All residues across all sectors
RESIDUES_REGISTRY: Dict[str, ResidueData] = {
    **AGRICULTURA_RESIDUES,
    **PECUARIA_RESIDUES,
    **URBANO_RESIDUES,
    **INDUSTRIAL_RESIDUES,
}

# Category organization (old structure - backward compatibility)
CATEGORIES = {
    "Agricultura": list(AGRICULTURA_RESIDUES.keys()),
    "Pecuária": list(PECUARIA_RESIDUES.keys()),
    "Urbano": list(URBANO_RESIDUES.keys()),
    "Industrial": list(INDUSTRIAL_RESIDUES.keys()),
}

# Sector organization (new parallel structure)
SECTORS = {
    "Agricultura": AGRICULTURA_SECTOR_INFO,
    "Pecuária": PECUARIA_SECTOR_INFO,
    "Urbano": URBANO_SECTOR_INFO,
    "Industrial": INDUSTRIAL_SECTOR_INFO,
}


# ============================================================================
# PUBLIC API - Backward Compatible
# ============================================================================

def get_available_residues() -> List[str]:
    """Get list of all available residues"""
    return list(RESIDUES_REGISTRY.keys())


def get_residue_data(residue_name: str) -> Optional[ResidueData]:
    """Get complete data for a specific residue"""
    return RESIDUES_REGISTRY.get(residue_name)


def get_residues_by_category(category: str) -> List[str]:
    """Get list of residues by category (backward compatibility)"""
    return CATEGORIES.get(category, [])


def get_category_icon(category: str) -> str:
    """Get emoji icon for category (backward compatibility)"""
    icons = {
        "Agricultura": "🌾",
        "Pecuária": "🐄",
        "Urbano": "🏙️",
        "Industrial": "🏭",
    }
    return icons.get(category, "📊")


def get_residue_icon(residue_name: str) -> str:
    """Get emoji icon for specific residue"""
    residue = get_residue_data(residue_name)
    return residue.icon if residue else "📊"


# ============================================================================
# NEW API - Sector-based
# ============================================================================

def get_all_sectors() -> Dict[str, Dict]:
    """Get all parallel sectors with metadata"""
    return SECTORS


def get_sector_info(sector_name: str) -> Optional[Dict]:
    """Get metadata for a specific sector"""
    return SECTORS.get(sector_name)


def get_residues_by_sector(sector_name: str) -> List[str]:
    """Get list of residues for a specific parallel sector"""
    sector = SECTORS.get(sector_name)
    return sector.get("residues", []) if sector else []


def get_available_sectors() -> List[str]:
    """Get list of sector names with available residues"""
    return [name for name, info in SECTORS.items() if info.get("residues")]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_range_from_string(value_str: str) -> Optional[object]:
    """
    Parse range from string like "Range: 200-350" or "range: 70-80%"
    (Placeholder - implement if needed)
    """
    import re
    from src.models.residue_models import ParameterRange

    # Pattern to match "Range: min-max" or "range: min-max"
    pattern = r'[Rr]ange[:\s]+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
    match = re.search(pattern, value_str)

    if match:
        min_val = float(match.group(1))
        max_val = float(match.group(2))
        mean_val = (min_val + max_val) / 2

        # Extract unit if present
        unit_pattern = r'%|L|kg|m³|mg/L|g/L|°C|dias?|days?'
        unit_match = re.search(unit_pattern, value_str)
        unit = unit_match.group(0) if unit_match else None

        return ParameterRange(min=min_val, mean=mean_val, max=max_val, unit=unit)

    return None


# ============================================================================
# MODULE INFO
# ============================================================================

__all__ = [
    # Registries
    'RESIDUES_REGISTRY',
    'CATEGORIES',
    'SECTORS',

    # Backward-compatible API
    'get_available_residues',
    'get_residue_data',
    'get_residues_by_category',
    'get_category_icon',
    'get_residue_icon',

    # New sector-based API
    'get_all_sectors',
    'get_sector_info',
    'get_residues_by_sector',
    'get_available_sectors',

    # Utilities
    'parse_range_from_string',
]

```

--- END OF FILE src/data/residue_registry.py ---

--- START OF FILE src/data/pecuaria/bovinocultura.py ---

```python
"""
Dejetos de Bovinos (Leite + Corte) - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Dejetos de Bovinos (Leite + Corte) data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData,
    ParameterRange
)


# ============================================================================
# DEJETOS DE BOVINOS (LEITE + CORTE)
# ============================================================================



# ============================================================================
# DEJETOS DE BOVINOS (LEITE + CORTE)
# ============================================================================

DEJETOS_DE_BOVINOS_LEITE__CORTE_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=230.0,
    bmp_unit="L CH₄/kg VS",
    ts=22.0,  # Mean of 20-25% range
    vs=80.0,  # Mean value
    vs_basis="% of TS",
    moisture=78.0,  # 100 - 22 (TS)
    cn_ratio=14.7,  # Mean of 14-15.4
    ph=7.0,
    cod=174000.0,
    nitrogen=0.45,
    carbon=None,
    ch4_content=63.5,  # Mean of 62-65%
    phosphorus=0.65,
    potassium=1.21,
    protein=None,
    toc=None,
    # Range data from Cenario_Bovinocultura.md validation
    bmp_range=ParameterRange(min=40.0, mean=250.0, max=520.0, unit="L CH₄/kg SV"),
    ts_range=ParameterRange(min=18.0, mean=22.0, max=25.0, unit="%"),
    vs_range=ParameterRange(min=76.0, mean=80.0, max=81.0, unit="% ST"),
    moisture_range=ParameterRange(min=75.0, mean=78.0, max=82.0, unit="%"),
    cn_ratio_range=ParameterRange(min=14.0, mean=14.7, max=15.44, unit=""),
    ch4_content_range=ParameterRange(min=55.0, mean=63.5, max=81.48, unit="%")
)

DEJETOS_DE_BOVINOS_LEITE__CORTE_AVAILABILITY = AvailabilityFactors(
    fc=0.374,
    fcp=0.8,
    fs=1.0,
    fl=0.75,
    final_availability=33.60,
    # Range data from Cenario_Bovinocultura.md validation
    fc_range=ParameterRange(min=0.05, mean=0.37, max=0.80, unit=""),
    fcp_range=ParameterRange(min=0.70, mean=0.80, max=0.95, unit=""),
    fs_range=ParameterRange(min=0.60, mean=0.80, max=0.90, unit=""),
    fl_range=ParameterRange(min=0.50, mean=0.75, max=0.90, unit="")
)

DEJETOS_DE_BOVINOS_LEITE__CORTE_OPERATIONAL = OperationalParameters(
    hrt="30-32 dias",
    temperature="30-37°C mesofílica",
    fi_ratio=0.5,
    olr=None,
    reactor_type="CSTR, Canadense, Lagoa Coberta, Plug-flow",
    tan_threshold="NH₃ <3.000 mg/L",
    vfa_limit="pH 6,5-7,5",
    # Range data from Cenario_Bovinocultura.md validation
    hrt_range=ParameterRange(min=25.0, mean=31.0, max=60.0, unit="dias"),
    temperature_range=ParameterRange(min=18.2, mean=33.5, max=37.0, unit="°C")
)

DEJETOS_DE_BOVINOS_LEITE__CORTE_JUSTIFICATION = """
**Bovinocultura SP tem 33,6-50% disponível** (0,84-1,25 bilhões Nm³/ano) vs. 2,5 bilhões (teórico).

**Justificativa Técnica (35 papers 2017-2025):**
- **FCp=0,80**: BAIXA competição (dejetos sem valor comercial vs cama frango R$ 150-300/ton)
- 97% produtores não valorizam dejetos (Herrero 2018 Embrapa-SP)
- Custo oportunidade baixo: R$ 20-50/ton vs R$ 150-300/ton avicultura

**Co-digestão OBRIGATÓRIA:**
- C/N=14-15,4 (muito abaixo ótimo 25-30)
- Incrementos validados: +44,6% (batata-doce 50%), +138% (café 40%)

**Fatores (35 papers NIPE, UNESP, USP, Embrapa):**
- FC=0,374 | FCp=0,80 | FS=1,00 | FL=0,75
- Resultado: 0,84-1,25 bilhões Nm³/ano
"""

DEJETOS_DE_BOVINOS_LEITE__CORTE_SCENARIOS = {
    "Pessimista": 393.0,
    "Realista": 686.0,
    "Otimista": 1246.0,
    "Teórico (100%)": 2500.0,
}

DEJETOS_DE_BOVINOS_LEITE__CORTE_REFERENCES = [
    ScientificReference(
        title="An overview of the integrated biogas production - São Paulo state",
        authors="Mendes, F.B.; Volpi, M.P.C. et al.",
        year=2023,
        doi="10.1002/wene.454" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85167368558" if True else None,
        journal="WIREs Energy and Environment" if True else None,
        relevance="Very High",
        key_findings=[
            "Custos co-substratos: Vinhaça USD 3,75/ton SV | C/N=14,0 bovinos",
        ],
        data_type="NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Economic viability digester cattle confinement beef",
        authors="Montoro, S.B. et al.",
        year=2017,
        doi="10.1590/1809-4430-Eng.Agric.v37n2p353-365" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Engenharia Agrícola" if True else None,
        relevance="Very High",
        key_findings=[
            "TIR 26,6%, payback 6,2 anos | CAPEX R$ 10.339/kWe | BMP=0,27",
        ],
        data_type="UNESP-SP"
    ),
    ScientificReference(
        title="Dairy Manure Management: Perceptions South American",
        authors="Herrero, M.A.; Palhares, J.C.P. et al.",
        year=2018,
        doi="10.3389/fsufs.2018.00022" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Frontiers Sustainable Food Systems" if True else None,
        relevance="Very High",
        key_findings=[
            "97% potencial PERDIDO | FCon=0,40, FEq=0,31, FReg=0,49-0,76",
        ],
        data_type="Embrapa-SP"
    ),
    ScientificReference(
        title="Technical assessment mono-digestion co-digestion biogas Brazil",
        authors="Velásquez Piñas, J.A. et al.",
        year=2018,
        doi="10.1016/j.renene.2017.10.085" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Renewable Energy" if True else None,
        relevance="High",
        key_findings=[
            "BMP=0,28 Nm³/kg SV (padrão) | Range 0,18-0,52 | C/N=15,44",
        ],
        data_type="UNIFEI-MG"
    ),
    ScientificReference(
        title="Anaerobic co-digestion sweet potato dairy cattle manure",
        authors="Montoro, S.B. et al.",
        year=2019,
        doi="10.1016/j.jclepro.2019.04.148" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Journal of Cleaner Production" if True else None,
        relevance="Very High",
        key_findings=[
            "Co-digestão batata-doce +44,6% BMP | TIR 47-57%, payback 2-3 anos",
        ],
        data_type="UNESP-SP"
    ),
    ScientificReference(
        title="Economic holistic feasibility centralized decentralized biogas",
        authors="Velásquez Piñas, J.A. et al.",
        year=2019,
        doi="10.1016/j.renene.2019.02.053" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Renewable Energy" if True else None,
        relevance="Very High",
        key_findings=[
            "Mínimo viável ≥740 kWe (197 vacas) | TIR 18,2% sem subsídios",
        ],
        data_type="UNIFEI-MG"
    ),
    ScientificReference(
        title="Biogas potential biowaste Rio de Janeiro Brazil",
        authors="Oliveira, H.R. et al.",
        year=2024,
        doi="10.1016/j.renene.2023.119751" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Renewable Energy" if True else None,
        relevance="High",
        key_findings=[
            "BMP Embrapa: 0,210-0,230 Nm³/kg SV | Corte 43,9 L/dia, Leite 93,7 L/dia",
        ],
        data_type="UFRJ"
    ),
    ScientificReference(
        title="Life cycle assessment milk production anaerobic treatment manure",
        authors="Maciel, A.M. et al.",
        year=2022,
        doi="10.1016/j.seta.2022.102883" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Sustainable Energy Technologies" if True else None,
        relevance="High",
        key_findings=[
            "Redução GEE 25-54% | 65% CH₄ no biogás | TRH 32 dias plug-flow",
        ],
        data_type="Embrapa-MG"
    ),
    ScientificReference(
        title="Bioenergetic Potential Coffee Processing Residues Industrial Symbiosis",
        authors="Albarracin, L.T. et al.",
        year=2024,
        doi="10.3390/resources13020021" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Resources" if True else None,
        relevance="Very High",
        key_findings=[
            "Co-digestão café 40%: +138% BMP | TIR 60%, payback 2,1 anos",
        ],
        data_type="NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Milk production family agro-industries São Paulo Carbon balance",
        authors="Silva, M.C. et al.",
        year=2024,
        doi="10.1007/s11367-023-02157-x" if True else None,
        scopus_link="https://scopus.com/" if True else None,
        journal="Int. J. Life Cycle Assessment" if True else None,
        relevance="Very High",
        key_findings=[
            "Pegada 2.408 kg CO₂eq/1000 kg leite | Biodigestão -25-54%",
        ],
        data_type="ITAL-SP"
    ),
]

DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA = ResidueData(
    name="Dejetos de Bovinos (Leite + Corte)",
    category="Pecuária",
    icon="🐄",
    generation="13-21 kg/animal/dia | Confinamento: 20 kg/dia | Pasto: 10 kg/dia",
    destination="80% dispersão pasto + 20% uso fertilizante esporádico",
    chemical_params=DEJETOS_DE_BOVINOS_LEITE__CORTE_CHEMICAL_PARAMS,
    availability=DEJETOS_DE_BOVINOS_LEITE__CORTE_AVAILABILITY,
    operational=DEJETOS_DE_BOVINOS_LEITE__CORTE_OPERATIONAL,
    justification=DEJETOS_DE_BOVINOS_LEITE__CORTE_JUSTIFICATION,
    scenarios=DEJETOS_DE_BOVINOS_LEITE__CORTE_SCENARIOS,
    references=DEJETOS_DE_BOVINOS_LEITE__CORTE_REFERENCES
)


# ============================================================================

```

--- END OF FILE src/data/pecuaria/bovinocultura.py ---

---

### 📚 4. INFORMAÇÕES DE SUPORTE

Lembre-se que a principal forma de acessar os dados é através das funções em `src/data/residue_registry.py`, como `get_residue_data(name)` e `get_available_residues()`.
A estrutura de dados principal é a classe `ResidueData` definida em `src/models/residue_models.py`.
