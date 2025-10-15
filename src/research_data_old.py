"""
Research Data Module - Validated Chemical and Availability Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Comprehensive database of residue characteristics, chemical parameters,
availability factors, and scientific references for biogas production.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ChemicalParameters:
    """Chemical composition and methane potential parameters"""
    bmp: float  # Biochemical Methane Potential (m³ CH₄/ton or m³ CH₄/kg VS)
    bmp_unit: str  # Unit for BMP (e.g., "m³ CH₄/ton MS", "NL CH₄/kg VS")
    ts: float  # Total Solids (% of fresh weight)
    vs: float  # Volatile Solids (% of TS or % of fresh weight)
    vs_basis: str  # "% of TS" or "% of fresh weight"
    moisture: float  # Moisture content (%)
    cn_ratio: Optional[float] = None  # Carbon:Nitrogen ratio
    ph: Optional[float] = None  # pH value
    cod: Optional[float] = None  # Chemical Oxygen Demand (mg/L)
    nitrogen: Optional[float] = None  # Nitrogen content (%)
    carbon: Optional[float] = None  # Carbon content (%)
    ch4_content: Optional[float] = None  # Methane content in biogas (%)
    phosphorus: Optional[float] = None  # Phosphorus (P₂O₅) content (%)
    potassium: Optional[float] = None  # Potassium (K₂O) content (%)
    protein: Optional[float] = None  # Protein content (%)
    toc: Optional[float] = None  # Total Organic Carbon (%)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        return {
            'BMP': f"{self.bmp} {self.bmp_unit}",
            'Sólidos Totais (TS)': f"{self.ts}%",
            'Sólidos Voláteis (VS)': f"{self.vs}% {self.vs_basis}",
            'Umidade': f"{self.moisture}%",
            'Relação C:N': f"{self.cn_ratio}" if self.cn_ratio else "N/A",
            'pH': f"{self.ph}" if self.ph else "N/A",
            'DQO': f"{self.cod} mg/L" if self.cod else "N/A",
            'Nitrogênio (N)': f"{self.nitrogen}%" if self.nitrogen else "N/A",
            'Carbono (C)': f"{self.carbon}%" if self.carbon else "N/A",
            'Conteúdo CH₄': f"{self.ch4_content}%" if self.ch4_content else "N/A",
        }


@dataclass
class AvailabilityFactors:
    """Availability correction factors for residues"""
    fc: float  # Collection factor (0-1)
    fcp: float  # Competition factor (0-1)
    fs: float  # Seasonal factor (0-1)
    fl: float  # Logistic factor (0-1)
    final_availability: float  # Final availability percentage (0-100)

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        return {
            'FC (Coleta)': f"{self.fc:.2f}",
            'FCp (Competição)': f"{self.fcp:.2f}",
            'FS (Sazonal)': f"{self.fs:.2f}",
            'FL (Logístico)': f"{self.fl:.2f}",
            'Disponibilidade Final': f"{self.final_availability:.1f}%"
        }


@dataclass
class OperationalParameters:
    """Operational parameters for anaerobic digestion"""
    hrt: str  # Hydraulic Retention Time
    temperature: str  # Operating temperature (°C)
    fi_ratio: Optional[float] = None  # Food to Inoculum ratio
    olr: Optional[str] = None  # Organic Loading Rate (kg VS/m³/day)
    reactor_type: Optional[str] = None  # CSTR, UASB, etc.
    tan_threshold: Optional[str] = None  # Total Ammonia Nitrogen threshold
    vfa_limit: Optional[str] = None  # Volatile Fatty Acids limit

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        result = {
            'TRH (Tempo de Retenção Hidráulica)': self.hrt,
            'Temperatura': self.temperature,
        }
        if self.fi_ratio:
            result['Razão F/I'] = f"{self.fi_ratio}"
        if self.olr:
            result['TCO (Taxa de Carga Orgânica)'] = self.olr
        if self.reactor_type:
            result['Tipo de Reator'] = self.reactor_type
        if self.tan_threshold:
            result['Limite TAN'] = self.tan_threshold
        if self.vfa_limit:
            result['Limite AGV'] = self.vfa_limit
        return result


@dataclass
class ScientificReference:
    """Scientific paper reference"""
    title: str
    authors: str
    year: int
    doi: Optional[str] = None
    scopus_link: Optional[str] = None
    journal: Optional[str] = None
    relevance: str = "High"  # High/Medium/Low
    key_findings: List[str] = None
    data_type: str = "Literatura Científica"  # Primary/Literature/Remote Sensing/Norms

    def __post_init__(self):
        if self.key_findings is None:
            self.key_findings = []


@dataclass
class ResidueData:
    """Complete residue data with validated factors"""
    name: str
    category: str  # Agricultura/Pecuária/Urbano
    icon: str  # Emoji
    generation: str  # Generation rate description
    destination: str  # Current destination/use
    chemical_params: ChemicalParameters
    availability: AvailabilityFactors
    operational: OperationalParameters
    justification: str  # Technical justification for availability
    scenarios: Dict[str, float]  # Scenario name -> CH₄ potential (Mi m³/year)
    references: List[ScientificReference]

    # Optional fields for specific residues
    top_municipalities: Optional[List[Dict]] = None
    validation_data: Optional[Dict] = None
    contribution_breakdown: Optional[Dict] = None


# ============================================================================
# AVICULTURA (POULTRY) - Complete Data
# ============================================================================

AVICULTURA_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=291.39,
    bmp_unit="NL CH₄/kg VS (co-digestão)",
    ts=25.0,  # Average of 25-40% range
    vs=69.8,
    vs_basis="% of TS",
    moisture=65.0,  # Calculated from TS
    cn_ratio=7.85,
    ph=7.91,
    nitrogen=3.38,
    carbon=36.5,  # Average of 35-38%
    ch4_content=55.0,
    phosphorus=3.5,  # Average of range
    potassium=3.93,  # Average of range
    protein=9.22
)

AVICULTURA_AVAILABILITY = AvailabilityFactors(
    fc=0.90,
    fcp=0.50,
    fs=1.00,
    fl=0.90,
    final_availability=40.5
)

AVICULTURA_OPERATIONAL = OperationalParameters(
    hrt="60 dias (máxima produção)",
    temperature="35°C (mesofílica)",
    fi_ratio=0.5,
    olr="2.9-4.0 kg VS/m³/dia",
    reactor_type="CSTR (Reator Tanque Agitado Contínuo)",
    tan_threshold="<2 g/L (evitar inibição 3-6 g/L)",
    vfa_limit="Manter pH 6.8-7.2"
)

AVICULTURA_JUSTIFICATION = """
**Dejeto de aves tem 40,5% disponível** após competição com fertilizante.

**Justificativa Técnica:**
- Mercado consolidado de fertilizante orgânico (alto valor NPK)
- Guerini Filho (2019): exclui cama de frango da disponibilidade real
- Dos Santos (2023): valor econômico US$ 0,03/kg como fertilizante
- Linhares (2022): alto teor de N, P₂O₅, K₂O crucial para solos tropicais
- Redução da dependência de fertilizantes importados

**Co-digestão Obrigatória:**
- Relação C/N de 7,85 (muito baixa, ótimo: 25-30)
- Acúmulo de amônia (NH₃) inibe microrganismos metanogênicos
- Necessidade de substratos ricos em carbono (palha, bagaço)

**Fatores:**
- FC = 0.90: 90% coletável em sistemas confinados
- FCp = 0.50: 50% competido por fertilizante orgânico
- FS = 1.00: Geração contínua ao longo do ano
- FL = 0.90: 90% dentro de raio viável (20-30 km)

**Resultado:**
- Geração total: 3,12 milhões ton/ano
- **Disponível biogás: 1,25 milhões ton/ano (40,5%)**
- **Redução de 81,72% do potencial teórico**
"""

AVICULTURA_SCENARIOS = {
    'Pessimista': 509.7,
    'Realista': 728.2,
    'Otimista': 1164.5,
    'Teórico (100%)': 3983.2
}

AVICULTURA_REFERENCES = [
    ScientificReference(
        title="An overview of the integrated biogas production through agro-industrial and livestock residues in the Brazilian São Paulo state",
        authors="Mendes et al.",
        year=2023,
        doi="10.1002/wene.454",
        scopus_link="https://www.scopus.com/pages/publications/85167368558",
        journal="WIREs Energy and Environment",
        relevance="High",
        key_findings=[
            "Co-digestion with wheat straw: 330-600 L biogas/kg VS",
            "Economic valuation: US$ 37.74/ton fresh poultry manure",
            "Strong competition with organic fertilizer market"
        ]
    ),
    ScientificReference(
        title="Biomass availability assessment for biogas or methane production in Rio Grande do Sul, Brazil",
        authors="Guerini Filho et al.",
        year=2019,
        doi="10.1007/s10098-019-01710-3",
        relevance="Very High",
        key_findings=[
            "Broiler litter excluded in real scenario due to fertilizer competition",
            "Manure generation: 0.15 kg/animal/day (laying hens)",
            "Three-scenario approach: Theoretical → Practical → Real"
        ]
    ),
    ScientificReference(
        title="Methane production by co-digestion of poultry manure and lignocellulosic biomass",
        authors="Paranhos et al.",
        year=2020,
        doi="10.1016/j.biortech.2019.122588",
        key_findings=[
            "Best yield: 126.02 Nm³ CH₄/ton with corn cob co-digestion",
            "C/N ratio 7.85 requires co-digestion",
            "Can replace 53.2% of firewood in poultry farm heating"
        ]
    ),
    ScientificReference(
        title="Power generation potential in posture aviaries in Brazil in the context of a circular economy",
        authors="Ribeiro, Barros & Tiago Filho",
        year=2016,
        doi="10.1016/j.seta.2016.10.004",
        scopus_link="https://www.scopus.com/pages/publications/84994246776",
        relevance="High"
    ),
    ScientificReference(
        title="Feasibility of biogas and energy generation from poultry manure in Brazil",
        authors="Ribeiro et al.",
        year=2018,
        doi="10.1177/0734242X17751846",
        scopus_link="https://www.scopus.com/pages/publications/85042533812",
        relevance="High"
    )
]

AVICULTURA_TOP_MUNICIPALITIES = [
    {'rank': 1, 'name': 'Bastos', 'ch4': 180.5, 'electricity': 258, 'birds': 14500000},
    {'rank': 2, 'name': 'Salto', 'ch4': 48.2, 'electricity': 69, 'birds': 3850000},
    {'rank': 3, 'name': 'Tatuí', 'ch4': 42.1, 'electricity': 60, 'birds': 3360000},
    {'rank': 4, 'name': 'Ourinhos', 'ch4': 38.7, 'electricity': 55, 'birds': 3090000},
    {'rank': 5, 'name': 'Rancharia', 'ch4': 35.3, 'electricity': 50, 'birds': 2820000},
]

AVICULTURA_VALIDATION = {
    'total_birds': 58.4,  # Million birds
    'farms': 2850,
    'theoretical_reduction': 81.72,
    'coverage': 92,
    'municipalities': 387,
    'main_cluster': 'Bastos',
    'cluster_contribution': 24.8,
    'biofertilizer_coproduct': 1.25
}

AVICULTURA_DATA = ResidueData(
    name="Dejeto de Aves (Cama de Frango)",
    category="Pecuária",
    icon="🐔",
    generation="1,58 kg resíduo/kg produto | 0,15 kg/ave/dia",
    destination="50% fertilizante orgânico + 40% biodigestão disponível",
    chemical_params=AVICULTURA_CHEMICAL_PARAMS,
    availability=AVICULTURA_AVAILABILITY,
    operational=AVICULTURA_OPERATIONAL,
    justification=AVICULTURA_JUSTIFICATION,
    scenarios=AVICULTURA_SCENARIOS,
    references=AVICULTURA_REFERENCES,
    top_municipalities=AVICULTURA_TOP_MUNICIPALITIES,
    validation_data=AVICULTURA_VALIDATION
)


# ============================================================================
# PLACEHOLDER DATA FOR OTHER RESIDUES
# (To be expanded with complete data)
# ============================================================================

# Cana-de-açúcar (Sugar Cane) - Placeholder
CANA_DATA = ResidueData(
    name="Palha de Cana-de-açúcar",
    category="Agricultura",
    icon="🌾",
    generation="280 kg/ton cana (15% umidade)",
    destination="Retorno ao solo (sustentabilidade) + Recolhimento mecanizado",
    chemical_params=ChemicalParameters(
        bmp=200, bmp_unit="m³ CH₄/ton MS",
        ts=85.0, vs=90.0, vs_basis="% of TS", moisture=15.0
    ),
    availability=AvailabilityFactors(fc=0.80, fcp=0.65, fs=1.00, fl=0.90, final_availability=25.2),
    operational=OperationalParameters(hrt="30-45 dias", temperature="35-37°C (mesofílica)"),
    justification="Dados completos a serem adicionados - Ver referências FAPESP 2025/08745-2",
    scenarios={'Pessimista': 4354, 'Realista': 6077, 'Otimista': 10089, 'Teórico (100%)': 21000},
    references=[]
)


# ============================================================================
# REGISTRY AND HELPER FUNCTIONS
# ============================================================================

RESIDUES_REGISTRY = {
    'Avicultura': AVICULTURA_DATA,
    'Cana-de-açúcar': CANA_DATA,
    # More residues to be added
}

CATEGORIES = {
    'Agricultura': ['Cana-de-açúcar', 'Soja', 'Milho', 'Café', 'Citros', 'Silvicultura'],
    'Pecuária': ['Avicultura', 'Bovinocultura', 'Suinocultura', 'Piscicultura'],
    'Urbano': ['RSU', 'RPO', 'Esgoto']
}


def get_available_residues() -> List[str]:
    """Get list of all available residues"""
    return list(RESIDUES_REGISTRY.keys())


def get_residue_data(residue_name: str) -> Optional[ResidueData]:
    """Get complete data for a specific residue"""
    return RESIDUES_REGISTRY.get(residue_name)


def get_residues_by_category(category: str) -> List[str]:
    """Get list of residues by category"""
    return CATEGORIES.get(category, [])


def get_category_icon(category: str) -> str:
    """Get emoji icon for category"""
    icons = {
        'Agricultura': '🌾',
        'Pecuária': '🐄',
        'Urbano': '🏙️'
    }
    return icons.get(category, '📊')


def get_residue_icon(residue_name: str) -> str:
    """Get emoji icon for specific residue"""
    residue = get_residue_data(residue_name)
    return residue.icon if residue else '📊'
