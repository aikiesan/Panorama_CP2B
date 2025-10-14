"""
Research Data Module - Validated Chemical and Availability Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Comprehensive database of residue characteristics, chemical parameters,
availability factors, and scientific references for biogas production.

AUTO-GENERATED FROM CP2B DATABASE v2.0
Date: 2025-10-14
Source: cp2b_panorama.db
Residues: 7 | References: 50+
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


# ============================================================================
# DATA STRUCTURES
# ============================================================================

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


@dataclass
class AvailabilityFactors:
    """Availability correction factors for residues"""
    fc: float
    fcp: float
    fs: float
    fl: float
    final_availability: float

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for display"""
        return {
            "FC (Coleta)": f"{self.fc:.2f}",
            "FCp (Competição)": f"{self.fcp:.2f}",
            "FS (Sazonal)": f"{self.fs:.2f}",
            "FL (Logístico)": f"{self.fl:.2f}",
            "Disponibilidade Final": f"{self.final_availability:.1f}%"
        }


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


# ============================================================================
# DEJETO DE AVES (CAMA DE FRANGO)
# ============================================================================

DEJETO_DE_AVES_CAMA_DE_FRANGO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=275.0,
    bmp_unit="L CH₄/kg VS | Range: 200-350 | Paper [2] | Alta variabilidade cama",
    ts=42.5,
    vs=75.0,
    vs_basis="75% of TS (range: 70-80%)",
    moisture=57.5,
    cn_ratio=11.5,
    ph=7.4,
    cod=296900.0,
    nitrogen=2.75,
    carbon=36.5,
    ch4_content=57.5,
    phosphorus=3.5,
    potassium=3.93,
    protein=9.22,
    toc=None
)

DEJETO_DE_AVES_CAMA_DE_FRANGO_AVAILABILITY = AvailabilityFactors(
    fc=0.9,
    fcp=0.5,
    fs=1.0,
    fl=0.9,
    final_availability=40.50
)

DEJETO_DE_AVES_CAMA_DE_FRANGO_OPERATIONAL = OperationalParameters(
    hrt="42-60 dias (Papers #8, #11, #12: 80% produção em 30d, máximo 60d)",
    temperature="35-37°C mesofílica (Paper #11, #12: máximo 36-40°C)",
    fi_ratio=0.5,
    olr="2.9-4.0 kg VS/m³/dia (Paper #1 USP case)",
    reactor_type="CSTR (Reator Tanque Agitado Contínuo) ou Batch Indian (Paper #10, #12)",
    tan_threshold="<2 g/L ideal, inibição 3-6 g/L (Papers #8, #11, #15)",
    vfa_limit="Manter pH 6.8-7.2, correção Ca(OH)₂ se <6.0 (Papers #11, #12)"
)

DEJETO_DE_AVES_CAMA_DE_FRANGO_JUSTIFICATION = """
**Avicultura SP tem 40,5% disponível** (728,2 Mi m³ CH₄/ano cenário realista vs 3.983,2 Mi m³ teórico).

**Justificativa Técnica (15 papers validados):**
- FCp=0,50: Mercado consolidado fertilizante orgânico (US$ 37,74/ton) compete diretamente
- Brasil 3º produtor mundial, importa fertilizantes da Rússia, solo tropical deficiente NPK
- Cama de frango: 41,5 g/kg N + 43-49 g/kg P₂O₅ + 45-53 g/kg K₂O = alto valor agronômico

**Co-digestão OBRIGATÓRIA:**
- C/N=4,66-11,55 (muito baixo, ótimo 20-35) → risco inibição amônia (TAN >3-6 g/L)
- Requer mistura palha cana (C/N~75-150), sabugo milho (C/N~50-80), bagaço laranja
- BMP aumenta 2-3x com co-digestão: 101-291 NL CH₄/kg VS vs 86-99 sozinho

**Fatores (validados Paper #10, #13 NIPE-UNICAMP):**
- FC=0,90: 85% produção em grandes integrações (sistemas confinados)
- FCp=0,50: 50% comercializado como fertilizante (NSWP Lei 12.305/2010)
- FS=1,00: Produção contínua (aviários climatizados, ciclo 42 dias)
- FL=0,90: Concentração Bastos-SP (24,8% produção estadual) facilita logística 10-30km

**Resultado:** 284.400 ton/ano geração SP (13% market share nacional) × 40,5% = **115.182 ton disponível biogás**
"""

DEJETO_DE_AVES_CAMA_DE_FRANGO_SCENARIOS = {
    "Pessimista": 509.7,
    "Realista": 728.2,
    "Otimista": 1164.5,
    "Teórico (100%)": 3983.2,
}

DEJETO_DE_AVES_CAMA_DE_FRANGO_REFERENCES = [
    ScientificReference(
        title="An overview of the integrated biogas production through agro-industrial and livestock residues in the Brazilian São Paulo state",
        authors="Mendes, F.B.; Volpi, M.P.C. et al.",
        year=2023,
        doi="10.1002/bbb.2461" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85167368558" if True else None,
        journal="Biofuels, Bioproducts and Biorefining" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP co-digestão palha trigo: 330-600 L biogás/kg VS | Valoração econômica: US$ 37,74/ton cama de frango | Competição forte com mercado fertilizante orgânico | C/N ótimo 20-35, cama frango 7,85 requ...",
        ],
        data_type="Literatura Científica - NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Biomass availability assessment for biogas or methane production in Rio Grande do Sul, Brazil",
        authors="Guerini Filho, M. et al.",
        year=2019,
        doi="10.1007/s10098-019-01710-3" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85066622173" if True else None,
        journal="Clean Technologies and Environmental Policy" if True else None,
        relevance="Very High",
        key_findings=[
            "METODOLOGIA 3 CENÁRIOS validada: Teórico-Prático-Real | FC=0,20 sistemas extensivos | FCp: cama frango EXCLUÍDA Cenário III por competição fertilizante | Taxa geração: 0,15 kg/ave/dia | TS=18%, VS=...",
        ],
        data_type="Literatura Científica - Metodologia Cenários"
    ),
    ScientificReference(
        title="Methane production by co-digestion of poultry manure and lignocellulosic biomass: Kinetic and energy assessment",
        authors="Paranhos, A.G.O. et al.",
        year=2020,
        doi="10.1016/j.biortech.2019.122588" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85077067274" if True else None,
        journal="Bioresource Technology" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP EXPERIMENTAL Brasil: 291,39 NL CH₄/kg VS (sabugo milho+cama) vs 99,3 (cama sozinha) | HRT=60 dias máxima produção | C/N=7,85 | TAN <2 g/L ideal, inibição 3-6 g/L | Temp=35°C | F/I=0,5 ótimo | G...",
        ],
        data_type="Literatura Científica - BMP Experimental"
    ),
    ScientificReference(
        title="Energy potential of poultry litter for the production of biogas",
        authors="Onofre, T.G. et al.",
        year=2015,
        doi="10.5897/AJAR2015.9932" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/" if True else None,
        journal="African Journal of Agricultural Research" if True else None,
        relevance="High",
        key_findings=[
            "CAMPO Paraná: 0,643-3,285 m³ biogás/kg cama (conservador-ótimo) | 60-70% CH₄ | HRT=56 dias | 51,2 Mi kg/ano geração regional | Biodigestor Indian batch | Temp 15-37°C ambiente",
        ],
        data_type="Dados Experimentais - Campo"
    ),
    ScientificReference(
        title="Policy, regulatory issues, and case studies of full-scale projects",
        authors="Various authors",
        year=2025,
        doi="None" if False else None,
        scopus_link="https://www.scopus.com/pages/publications/105005901393" if True else None,
        journal="Elsevier Book Chapter" if True else None,
        relevance="High",
        key_findings=[
            "Potencial técnico Brasil: 81,8-84,6 bilhões m³ biogás/ano | Produção atual 2021-22: 2,3-2,8 bi m³ | Projeção 2030: 6,9 bi m³ | Gado+aves: 16,8 bi m³ | Cana vinhaça: 39,8 bi m³ | OLR planta USP-SP: ...",
        ],
        data_type="Política Pública"
    ),
    ScientificReference(
        title="Biorefinery study of availability of agriculture residues and wastes for integrated biorefineries in Brazil",
        authors="Forster-Carneiro, T. et al.",
        year=2013,
        doi="10.1016/j.resconrec.2013.05.007" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/84880027508" if True else None,
        journal="Resources, Conservation and Recycling" if True else None,
        relevance="Very High",
        key_findings=[
            "GP INDEX = 1,58 t resíduo/t produto avícola (METODOLOGIA BASELINE CP2B) | Geração nacional 2009: 18,36 Mi ton | Projeção 2020: 26,27 Mi ton (+43%) | Sistemas confinados únicos viáveis | Múltiplos u...",
        ],
        data_type="Literatura Científica - Metodologia GP"
    ),
    ScientificReference(
        title="Determination of methane generation potential and evaluation of kinetic models in poultry wastes",
        authors="Silva, T.H.L. et al.",
        year=2021,
        doi="10.1016/j.bcab.2021.101936" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85100656962" if True else None,
        journal="Biocatalysis and Agricultural Biotechnology" if True else None,
        relevance="High",
        key_findings=[
            "BMP=101,4 NmL CH₄/g VS | Modelo Gompertz R²=0,89-1,00 | k hidról=0,02-0,10/dia | Fase lag=0,79-6,62 dias | pH 7,7-8,8 com NaHCO₃ | Condutividade 7669-14130 µS/cm final | HRT=47 dias",
        ],
        data_type="Literatura Científica - Cinética"
    ),
    ScientificReference(
        title="Reducing the environmental impacts of Brazilian chicken meat production using different waste recovery strategies",
        authors="Santos, R.A. et al.",
        year=2023,
        doi="10.1016/j.jenvman.2023.118021" if True else None,
        scopus_link="https://www.scopus.com/pages/publications/85153949561" if True else None,
        journal="Journal of Environmental Management" if True else None,
        relevance="High",
        key_findings=[
            "VALIDAÇÃO FCp: Valor econômico cama US$ 0,03/kg | Mercado total US$ 235.413/ano (2,49% produção) | Alocação econômica 16,08% com biodigestão | 50,35% acidificação terrestre se uso direto fertilizan...",
        ],
        data_type="ACV - Competição Fertilizante"
    ),
]

DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA = ResidueData(
    name="Dejeto de Aves (Cama de Frango)",
    category="Pecuária",
    icon="🐔",
    generation="1,58 kg resíduo/kg produto (GP Index) | 0,14-0,18 kg/ave/dia",
    destination="50% fertilizante orgânico (NPK: 3,38% N, 3,5% P, 3,93% K) + 40% biodigestão disponível",
    chemical_params=DEJETO_DE_AVES_CAMA_DE_FRANGO_CHEMICAL_PARAMS,
    availability=DEJETO_DE_AVES_CAMA_DE_FRANGO_AVAILABILITY,
    operational=DEJETO_DE_AVES_CAMA_DE_FRANGO_OPERATIONAL,
    justification=DEJETO_DE_AVES_CAMA_DE_FRANGO_JUSTIFICATION,
    scenarios=DEJETO_DE_AVES_CAMA_DE_FRANGO_SCENARIOS,
    references=DEJETO_DE_AVES_CAMA_DE_FRANGO_REFERENCES
)


# ============================================================================
# DEJETOS DE BOVINOS (LEITE + CORTE)
# ============================================================================

DEJETOS_DE_BOVINOS_LEITE__CORTE_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=230.0,
    bmp_unit="L CH₄/kg VS | Range: 180-280 | Paper [2] | Conservador",
    ts=11.5,
    vs=82.5,
    vs_basis="82,5% of TS (range: 80-85%)",
    moisture=88.5,
    cn_ratio=20.0,
    ph=7.0,
    cod=174000.0,
    nitrogen=0.45,
    carbon=None,
    ch4_content=60.0,
    phosphorus=0.65,
    potassium=1.21,
    protein=None,
    toc=None
)

DEJETOS_DE_BOVINOS_LEITE__CORTE_AVAILABILITY = AvailabilityFactors(
    fc=0.374,
    fcp=0.8,
    fs=1.0,
    fl=0.75,
    final_availability=33.60
)

DEJETOS_DE_BOVINOS_LEITE__CORTE_OPERATIONAL = OperationalParameters(
    hrt="30-32 dias",
    temperature="30-37°C mesofílica",
    fi_ratio=0.5,
    olr=None,
    reactor_type="CSTR, Canadense, Lagoa Coberta, Plug-flow",
    tan_threshold="NH₃ <3.000 mg/L",
    vfa_limit="pH 6,5-7,5"
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
# VINHAÇA DE CANA-DE-AÇÚCAR
# ============================================================================

VINHACA_DE_CANA_DE_ACUCAR_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=7.08,
    bmp_unit="Nm³ biogas/m³ vinhaça | Range: 6,6-7,5 | Papers [9,11] | MCF: 0,225 Nm³/kg COD",
    ts=8.0,
    vs=75.0,
    vs_basis="75% of TS (range: 70-80%)",
    moisture=92.0,
    cn_ratio=32.5,
    ph=4.25,
    cod=30000.0,
    nitrogen=0.95,
    carbon=32.5,
    ch4_content=72.5,
    phosphorus=0.13,
    potassium=3.5,
    protein=None,
    toc=1.99
)

VINHACA_DE_CANA_DE_ACUCAR_AVAILABILITY = AvailabilityFactors(
    fc=0.55,
    fcp=0.88,
    fs=0.7,
    fl=0.95,
    final_availability=4.39
)

VINHACA_DE_CANA_DE_ACUCAR_OPERATIONAL = OperationalParameters(
    hrt="58 dias (batch) | 20-30 dias (contínuo UASB)",
    temperature="30-37.5°C mesofílico",
    fi_ratio=None,
    olr=None,
    reactor_type="UASB, Lagoa Anaeróbia Coberta, AnSBBR (Sequencing Batch with Biomass)",
    tan_threshold="pH baixo requer correção 6,5-7,5",
    vfa_limit=None
)

VINHACA_DE_CANA_DE_ACUCAR_JUSTIFICATION = """
**Vinhaça SP tem 20-30% disponível** após competição com fertirrigação.

**Justificativa Técnica (15 papers 2011-2024):**
- **FCp=0,75**: ALTA competição com fertirrigação (CETESB NP 4231 obriga aplicação solo)
- Composição rica NPK (K2O: 1.400 mg/L, N: 414 mg/kg) valorizada na lavoura
- Custo aplicação fertirrigação: R$ 3,75/ton VS (Mendes 2023)
- 95% vinhaça aplicada diretamente no canavial (raio 3-5 km usina)

**Co-digestão:**
- C/N=16,78 (adequado 15-25) → possível mono-digestão
- pH=4,67 (ácido) → correção para 6,5-7,5 necessária
- COD=20.866 mg/L (alto potencial energético)

**Fatores (validados Buller 2021, Silva Neto 2021):**
- FC=0,90: Alta eficiência coleta (sistema fechado usina)
- FCp=0,75: Competição forte fertirrigação (CETESB)
- FS=0,85: Sazonalidade safra abril-novembro
- FL=0,95: Raio curto usina-biodigestor (<1 km)

**Resultado:** 8 bilhões L/ano × 7,08 Nm³ CH₄/m³ × FC × FCp × FS × FL = **10-15 bilhões Nm³/ano potencial teórico**
"""

VINHACA_DE_CANA_DE_ACUCAR_SCENARIOS = {
    "Pessimista": 1132.8,
    "Realista": 2485.9296000000004,
    "Otimista": 5664.0,
    "Teórico (100%)": 56640.0,
}

VINHACA_DE_CANA_DE_ACUCAR_REFERENCES = [
    ScientificReference(
        title="A spatially explicit assessment of sugarcane vinasse as a sustainable by-product",
        authors="Buller, L.S.; Romero, C.W.; Lamparelli, R.A.C. et al.",
        year=2021,
        doi="10.1016/j.scitotenv.2020.142717" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Science of the Total Environment" if True else None,
        relevance="Very High",
        key_findings=[
            "Vinhaça in natura: TS=3,69%, VS=61,16%TS, COD=20.866 mg/L, C/N=16,78, pH=4,67 | CH₄=49% (dia 58) | Potencial elétrico 0,0028 MWh/m³",
        ],
        data_type="Dados Experimentais - UNICAMP"
    ),
    ScientificReference(
        title="Potential impacts vinasse biogas replacing fossil oil power generation",
        authors="Silva Neto, J.V.; Gallo, W.L.R.",
        year=2021,
        doi="10.1016/j.rser.2020.110281" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Renewable and Sustainable Energy Reviews" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP=7,08 Nm³ CH₄/m³ vinhaça (COD=31,5 kg/m³, MCF=0,225) | Substitução combustível fóssil SP | Geração elétrica potencial",
        ],
        data_type="Literatura Científica"
    ),
    ScientificReference(
        title="Assessment agricultural biomass residues replace fossil fuel hydroelectric",
        authors="Romero, C.W.; Berni, M.D.; Figueiredo, G.K. et al.",
        year=2019,
        doi="10.1002/ese3.462" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Energy Science & Engineering" if True else None,
        relevance="Very High",
        key_findings=[
            "FC=0,60 para palha (fração sustentável de 14 Mg/ha) | Lignina 25%, Celulose 40%, Hemicelulose 30% | Co-digestão vinhaça",
        ],
        data_type="Literatura Científica - UNICAMP"
    ),
    ScientificReference(
        title="Long-term decomposition sugarcane harvest residues São Paulo",
        authors="Fortes, C.; Trivelin, P.C.O.; Vitti, A.C.",
        year=2012,
        doi="10.1016/j.biombioe.2012.03.011" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Biomass and Bioenergy" if True else None,
        relevance="High",
        key_findings=[
            "Post-Harvest Trash: C=44,4%, N=0,41%, C/N=108 | Lignina=24,6%, Celulose=43,9%, Hemi=26,4% | Decomposição lenta",
        ],
        data_type="Dados de Campo - SP"
    ),
    ScientificReference(
        title="Contribution N from green harvest residues sugarcane nutrition Brazil",
        authors="Ferreira, D.A.; Franco, H.C.J.; Otto, R. et al.",
        year=2016,
        doi="10.1111/gcbb.12292" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="GCB Bioenergy" if True else None,
        relevance="High",
        key_findings=[
            "C/N=100 típico palha | Apenas 16,2% N recuperado pela cultura (3 ciclos) | C=39-45%, N=0,46-0,65%",
        ],
        data_type="Dados de Campo - SP"
    ),
    ScientificReference(
        title="Soil GHG fluxes vinasse burnt unburnt sugarcane",
        authors="Oliveira, B.G.; Carvalho, J.L.N. et al.",
        year=2013,
        doi="10.1016/j.geoderma.2013.02.009" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Geoderma" if True else None,
        relevance="Very High",
        key_findings=[
            "N₂O EF: 0.68% (burnt) 0.44% (unburnt) | CO₂eq: 0.491/0.314 kg/m³ | C/N=8.65 | TOC=1.99 g/L",
        ],
        data_type="Dados Campo - SP"
    ),
    ScientificReference(
        title="Economic viability biogas vinasse sugarcane",
        authors="Pereira, L.G.; Cavalett, O.; Bonomi, A.",
        year=2020,
        doi="10.3390/en13174413" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Energies" if True else None,
        relevance="Very High",
        key_findings=[
            "LCOE: 55.8-133.7 USD/MWh | BMP: 0.39 m³/kg COD | Viável >8.058 ha | NPV positivo escala",
        ],
        data_type="Economia - CTBE"
    ),
    ScientificReference(
        title="Centralized distributed biogas hubs vinasse",
        authors="Pavan, M.C.; Aniceto, J.P.S.; Silva, R.C.",
        year=2021,
        doi="10.1016/j.renene.2021.04.070" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Renewable Energy" if True else None,
        relevance="High",
        key_findings=[
            "UASB: 77.9 USD/m³ | Generator: 549.8 USD/kW | Centralizado vs Distribuído | CH₄=60%",
        ],
        data_type="Economia"
    ),
    ScientificReference(
        title="Anaerobic Biological Treatment Vinasse Environmental Compliance Methane",
        authors="Albanez, R. et al.",
        year=2016,
        doi="10.1007/s12010-015-1856-z" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Appl Biochem Biotechnol" if True else None,
        relevance="Very High",
        key_findings=[
            "AnSBBR reactor: BMP=9,47 mol CH₄/kg COD | CH₄=77% | OLR=5,54 g COD/L/dia | T=30°C | Scale-up: 17 MW energia",
        ],
        data_type="Dados Experimentais - Brasil"
    ),
    ScientificReference(
        title="Biogas biofertilizer from vinasse making sugarcane ethanol sustainable",
        authors="Sica, P.; Carvalho, R. et al.",
        year=2020,
        doi="10.1007/s10163-020-01029-y" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="J Material Cycles Waste Management" if True else None,
        relevance="Very High",
        key_findings=[
            "UASB: BMP=0,19-0,25 L CH₄/g COD | pH neutralizado 4,5→7,0 | COD=23-41 g/L | T=37,5°C | Vinhaça:Etanol=12,5:1",
        ],
        data_type="Dados Experimentais - Brasil"
    ),
]

VINHACA_DE_CANA_DE_ACUCAR_DATA = ResidueData(
    name="Vinhaça de Cana-de-açúcar",
    category="Agricultura",
    icon="🍶",
    generation="10-15 L vinhaça/L etanol | 350 L/ton cana (média) | SP: ~8 bilhões L/ano",
    destination="95% fertirrigação (CETESB NP 4231) + 5% biodigestão disponível",
    chemical_params=VINHACA_DE_CANA_DE_ACUCAR_CHEMICAL_PARAMS,
    availability=VINHACA_DE_CANA_DE_ACUCAR_AVAILABILITY,
    operational=VINHACA_DE_CANA_DE_ACUCAR_OPERATIONAL,
    justification=VINHACA_DE_CANA_DE_ACUCAR_JUSTIFICATION,
    scenarios=VINHACA_DE_CANA_DE_ACUCAR_SCENARIOS,
    references=VINHACA_DE_CANA_DE_ACUCAR_REFERENCES
)


# ============================================================================
# PALHA DE CANA-DE-AÇÚCAR (PALHIÇO)
# ============================================================================

PALHA_DE_CANA_DE_ACUCAR_PALHICO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=300.0,
    bmp_unit="L CH₄/kg VS | Range: 250-350 | Papers [15,17,24] | Pré-tratamento recomendado",
    ts=88.5,
    vs=90.5,
    vs_basis="90,5% of TS (range: 88-93%)",
    moisture=11.5,
    cn_ratio=100.0,
    ph=None,
    cod=None,
    nitrogen=0.5,
    carbon=47.5,
    ch4_content=52.5,
    phosphorus=0.03,
    potassium=0.47,
    protein=None,
    toc=None
)

PALHA_DE_CANA_DE_ACUCAR_PALHICO_AVAILABILITY = AvailabilityFactors(
    fc=0.6,
    fcp=0.4,
    fs=0.85,
    fl=0.85,
    final_availability=36.00
)

PALHA_DE_CANA_DE_ACUCAR_PALHICO_OPERATIONAL = OperationalParameters(
    hrt="40-60 dias",
    temperature="35-55°C (mesofílica ou termofílica)",
    fi_ratio=None,
    olr=None,
    reactor_type="CSTR, Semi-contínuo | Pré-tratamento necessário (mecânico/químico/biológico)",
    tan_threshold=None,
    vfa_limit=None
)

PALHA_DE_CANA_DE_ACUCAR_PALHICO_JUSTIFICATION = """
**Palha SP tem 36% disponível** (Romero 2019 FC=0,60 sustentável).

**Justificativa Técnica (15 papers 2011-2024):**
- **FCp=0,40**: MÉDIA competição E2G (etanol 2G) + cobertura solo obrigatória
- Romero 2019: 60% de 14 ton/ha pode ser explorado sustentavelmente
- Cobertura solo: previne erosão, conserva umidade, recicla 16,2% N (Ferreira 2016)
- E2G: mercado emergente mas ainda pequena escala comercial

**Composição Lignocelulósica:**
- Lignina: 24,6-26,8% (alta recalcitrância)
- Celulose: 29,7-43,9%
- Hemicelulose: 22,5-26,4%
- C/N=71-108 (MUITO ALTO) → co-digestão obrigatória

**Fatores (validados Romero 2019, Fortes 2012, Nogueira 2023):**
- FC=0,60: Sustentabilidade agronômica (Romero 2019)
- FCp=0,40: Competição E2G + cobertura
- FS=0,85: Sazonalidade safra
- FL=0,85: Raio 30 km usina-biodigestor

**Resultado:** 25 Mi ton MS/ano × 0,36 disponibilidade = **9 Mi ton MS disponível**
"""

PALHA_DE_CANA_DE_ACUCAR_PALHICO_SCENARIOS = {
    "Pessimista": 1800.0,
    "Realista": 2250.0,
    "Otimista": 3200.0,
    "Teórico (100%)": 6250.0,
}

PALHA_DE_CANA_DE_ACUCAR_PALHICO_REFERENCES = [
    ScientificReference(
        title="A spatially explicit assessment of sugarcane vinasse as a sustainable by-product",
        authors="Buller, L.S.; Romero, C.W.; Lamparelli, R.A.C. et al.",
        year=2021,
        doi="10.1016/j.scitotenv.2020.142717" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Science of the Total Environment" if True else None,
        relevance="Very High",
        key_findings=[
            "Vinhaça in natura: TS=3,69%, VS=61,16%TS, COD=20.866 mg/L, C/N=16,78, pH=4,67 | CH₄=49% (dia 58) | Potencial elétrico 0,0028 MWh/m³",
        ],
        data_type="Dados Experimentais - UNICAMP"
    ),
    ScientificReference(
        title="Potential impacts vinasse biogas replacing fossil oil power generation",
        authors="Silva Neto, J.V.; Gallo, W.L.R.",
        year=2021,
        doi="10.1016/j.rser.2020.110281" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Renewable and Sustainable Energy Reviews" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP=7,08 Nm³ CH₄/m³ vinhaça (COD=31,5 kg/m³, MCF=0,225) | Substitução combustível fóssil SP | Geração elétrica potencial",
        ],
        data_type="Literatura Científica"
    ),
    ScientificReference(
        title="Assessment agricultural biomass residues replace fossil fuel hydroelectric",
        authors="Romero, C.W.; Berni, M.D.; Figueiredo, G.K. et al.",
        year=2019,
        doi="10.1002/ese3.462" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Energy Science & Engineering" if True else None,
        relevance="Very High",
        key_findings=[
            "FC=0,60 para palha (fração sustentável de 14 Mg/ha) | Lignina 25%, Celulose 40%, Hemicelulose 30% | Co-digestão vinhaça",
        ],
        data_type="Literatura Científica - UNICAMP"
    ),
    ScientificReference(
        title="Long-term decomposition sugarcane harvest residues São Paulo",
        authors="Fortes, C.; Trivelin, P.C.O.; Vitti, A.C.",
        year=2012,
        doi="10.1016/j.biombioe.2012.03.011" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Biomass and Bioenergy" if True else None,
        relevance="High",
        key_findings=[
            "Post-Harvest Trash: C=44,4%, N=0,41%, C/N=108 | Lignina=24,6%, Celulose=43,9%, Hemi=26,4% | Decomposição lenta",
        ],
        data_type="Dados de Campo - SP"
    ),
    ScientificReference(
        title="Contribution N from green harvest residues sugarcane nutrition Brazil",
        authors="Ferreira, D.A.; Franco, H.C.J.; Otto, R. et al.",
        year=2016,
        doi="10.1111/gcbb.12292" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="GCB Bioenergy" if True else None,
        relevance="High",
        key_findings=[
            "C/N=100 típico palha | Apenas 16,2% N recuperado pela cultura (3 ciclos) | C=39-45%, N=0,46-0,65%",
        ],
        data_type="Dados de Campo - SP"
    ),
    ScientificReference(
        title="GHG emissions sugarcane straw removal levels",
        authors="Vasconcelos, A.L.S.; Cherubin, M.R. et al.",
        year=2018,
        doi="10.1016/j.biombioe.2018.03.002" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Biomass and Bioenergy" if True else None,
        relevance="Very High",
        key_findings=[
            "C/N=51.2 | N₂O: 0.14-0.72% | T½: 147-231 dias | GHG neutral: 3.5 Mg/ha | C=42%, N=0.82%",
        ],
        data_type="Dados Experimentais - SP"
    ),
    ScientificReference(
        title="Economic evaluation baling sugarcane straw",
        authors="Lemos, S.V.; Ferreira, M.C.; Almeida-Cortez, J.S.",
        year=2014,
        doi="10.1016/j.biombioe.2014.03.047" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Biomass and Bioenergy" if True else None,
        relevance="Very High",
        key_findings=[
            "Coleta: 56-58 USD/ha | Round: 7.81 ton/ha | Square: 6.41 ton/ha | Preço: 32.68 USD/ton",
        ],
        data_type="Economia - Campo"
    ),
    ScientificReference(
        title="Evolution GHG emissions sugarcane harvesting 1990-2009",
        authors="Capaz, R.S.; Carvalho, J.L.N.; Nogueira, L.A.H.",
        year=2013,
        doi="10.1016/j.apenergy.2012.08.040" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Applied Energy" if True else None,
        relevance="High",
        key_findings=[
            "Redução 39.3% GEE (1990-2009) | Straw/stalk: 18% | Yield: 14.4 Mg/ha | Range SP: 12.5-24.9",
        ],
        data_type="Análise Histórica"
    ),
    ScientificReference(
        title="Soil carbon stocks burned vs unburned sugarcane",
        authors="Galdos, M.V.; Cerri, C.C.; Cerri, C.E.P.",
        year=2009,
        doi="10.1016/j.geoderma.2009.08.025" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Geoderma" if True else None,
        relevance="High",
        key_findings=[
            "Green cane: aumento C solo | Litter layer: CMB alto | Valida importância cobertura palha",
        ],
        data_type="Solos - SP"
    ),
    ScientificReference(
        title="Sugarcane straw removal effects Ultisols Oxisols south-central Brazil",
        authors="Satiro, L.S. et al.",
        year=2017,
        doi="10.1016/j.geodrs.2017.10.005" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Geoderma Regional" if True else None,
        relevance="High",
        key_findings=[
            "Cenários remoção: 0%=15,6 Mg/ha | 50%=8,7 Mg/ha (sustentável Oxisol) | Impacto Ca, Mg, K",
        ],
        data_type="Dados Campo - SP"
    ),
    ScientificReference(
        title="Prediction Sugarcane Yield NDVI Leaf-Tissue Nutrients Straw Removal",
        authors="Lisboa, I.P. et al.",
        year=2018,
        doi="10.3390/agronomy8090196" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Agronomy" if True else None,
        relevance="High",
        key_findings=[
            "C=44,5%, N=0,39%, C/N=114 (range 73-177) | P=0,04%, K=0,15% | Straw 0% removal: 16,2 Mg/ha",
        ],
        data_type="Dados Campo - SP"
    ),
]

PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA = ResidueData(
    name="Palha de Cana-de-açúcar (Palhiço)",
    category="Agricultura",
    icon="🌾",
    generation="120-140 kg MS/ton cana | 14 ton MS/ha | SP: ~25-30 Mi ton MS/ano",
    destination="40% cobertura solo (obrigatório sustentabilidade) + 60% disponível (E2G/bioenergia)",
    chemical_params=PALHA_DE_CANA_DE_ACUCAR_PALHICO_CHEMICAL_PARAMS,
    availability=PALHA_DE_CANA_DE_ACUCAR_PALHICO_AVAILABILITY,
    operational=PALHA_DE_CANA_DE_ACUCAR_PALHICO_OPERATIONAL,
    justification=PALHA_DE_CANA_DE_ACUCAR_PALHICO_JUSTIFICATION,
    scenarios=PALHA_DE_CANA_DE_ACUCAR_PALHICO_SCENARIOS,
    references=PALHA_DE_CANA_DE_ACUCAR_PALHICO_REFERENCES
)


# ============================================================================
# TORTA DE FILTRO (FILTER CAKE)
# ============================================================================

TORTA_DE_FILTRO_FILTER_CAKE_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=357.5,
    bmp_unit="L CH₄/kg VS | Range: 300-415 | Papers [10,11] | Co-digestão otimiza",
    ts=25.0,
    vs=77.5,
    vs_basis="75% of TS (range: 70-80%)",
    moisture=75.0,
    cn_ratio=20.0,
    ph=7.0,
    cod=400000.0,
    nitrogen=1.25,
    carbon=25.0,
    ch4_content=60.0,
    phosphorus=2.25,
    potassium=0.75,
    protein=None,
    toc=None
)

TORTA_DE_FILTRO_FILTER_CAKE_AVAILABILITY = AvailabilityFactors(
    fc=0.85,
    fcp=0.85,
    fs=0.85,
    fl=0.95,
    final_availability=12.30
)

TORTA_DE_FILTRO_FILTER_CAKE_OPERATIONAL = OperationalParameters(
    hrt="40-60 dias",
    temperature="35-55°C",
    fi_ratio=None,
    olr=None,
    reactor_type="CSTR, Co-digestão com vinhaça recomendada",
    tan_threshold=None,
    vfa_limit=None
)

TORTA_DE_FILTRO_FILTER_CAKE_JUSTIFICATION = """
**Torta de Filtro tem 10-15% disponível** para bioenergia.

**Justificativa (30 papers 2011-2025):**
- **FCp=0,85**: ALTA competição fertilizante (torta rica P, Ca, N orgânico)
- Valor agronômico alto: substitui 30-50% fertilizante fosfatado
- Composição: 1,5-2% P₂O₅, 1-1,5% N, 0,5-1% K₂O, 25-30% matéria orgânica
- Uso tradicional: aplicação direta solo (150-200 kg/ha)

**Potencial Energético:**
- C/N: 15-25 (adequado para biodigestão)
- TS: 25-30% (intermediário palha/vinhaça)
- BMP: 200-300 m³ CH₄/ton MS (literatura internacional)

**Co-digestão Sinérgica:**
- Torta + Vinhaça: balanceia nutrientes (torta rica P/Ca, vinhaça rica K)
- Torta + Palha: ajusta umidade e C/N
- Errera 2025: Vinhaça+Torta = 39,8 bilhões Nm³/ano (Brasil)

**Fatores:**
- FC=0,85: Alta coleta (processo industrial centralizado)
- FCp=0,85: Competição forte fertilizante
- FS=0,85: Sazonalidade safra
- FL=0,95: Usina-biodigestor <1 km

**Resultado:** 1,35 Mi ton/ano × FC × (1-FCp) × FS × FL = **150-200 Mi Nm³/ano SP**
"""

TORTA_DE_FILTRO_FILTER_CAKE_SCENARIOS = {
    "Pessimista": 120.0,
    "Realista": 170.0,
    "Otimista": 250.0,
    "Teórico (100%)": 337.5,
}

TORTA_DE_FILTRO_FILTER_CAKE_REFERENCES = [
    ScientificReference(
        title="Policy regulatory issues full-scale biogas projects Brazil",
        authors="Errera, M.R. et al.",
        year=2025,
        doi="10.1016/B978-0-443-16084-4.00020-1" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="From Crops Wastes to Bioenergy" if True else None,
        relevance="Very High",
        key_findings=[
            "Vinhaça+Torta: 39,8 bilhões Nm³/ano Brasil | Setor açúcar-álcool principal fonte biogás",
        ],
        data_type="Análise Nacional"
    ),
]

TORTA_DE_FILTRO_FILTER_CAKE_DATA = ResidueData(
    name="Torta de Filtro (Filter Cake)",
    category="Agricultura",
    icon="🍰",
    generation="30-40 kg/ton cana | 4-5% da moagem | SP: ~1,2-1,5 Mi ton/ano",
    destination="85% fertilizante direto (rico NPK) + 15% biodigestão/compostagem",
    chemical_params=TORTA_DE_FILTRO_FILTER_CAKE_CHEMICAL_PARAMS,
    availability=TORTA_DE_FILTRO_FILTER_CAKE_AVAILABILITY,
    operational=TORTA_DE_FILTRO_FILTER_CAKE_OPERATIONAL,
    justification=TORTA_DE_FILTRO_FILTER_CAKE_JUSTIFICATION,
    scenarios=TORTA_DE_FILTRO_FILTER_CAKE_SCENARIOS,
    references=TORTA_DE_FILTRO_FILTER_CAKE_REFERENCES
)


# ============================================================================
# DEJETOS DE SUÍNOS
# ============================================================================

DEJETOS_DE_SUINOS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=300.0,
    bmp_unit="NL CH₄/kg SV | Range: 170-642 (fase-dependente) | Média ciclo: 300-360 | Papers: Amaral 2016 (#3), Ribeiro 2013 (#1)",
    ts=3.0,
    vs=70.0,
    vs_basis="70% of TS (range: 60-80% - ALTA variação por fase)",
    moisture=97.0,
    cn_ratio=12.5,
    ph=7.0,
    cod=30000.0,
    nitrogen=3.23,
    carbon=15.0,
    ch4_content=67.5,
    phosphorus=3.64,
    potassium=2.64,
    protein=None,
    toc=None
)

DEJETOS_DE_SUINOS_AVAILABILITY = AvailabilityFactors(
    fc=0.65,
    fcp=0.8,
    fs=0.7,
    fl=0.8,
    final_availability=7.28
)

DEJETOS_DE_SUINOS_OPERATIONAL = OperationalParameters(
    hrt="25-35 dias",
    temperature="35-37°C mesofílica",
    fi_ratio=None,
    olr=None,
    reactor_type="CSTR, Lagoa Coberta, Canadense",
    tan_threshold="NH₃ <3.000 mg/L",
    vfa_limit=None
)

DEJETOS_DE_SUINOS_JUSTIFICATION = """
**Suinocultura SP: 25-30% disponível** para biodigestão.

**Justificativa (8 papers):**
- FCp=0,70: Competição média fertilizante
- BMP: 350-450 NL CH₄/kg SV (alto potencial)
- C/N: 8-15 (adequado mono/co-digestão)
- Clusters SP: Holambra, Amparo, Bragança Paulista

**Fatores:** FC=0,50 | FCp=0,70 | FS=1,00 | FL=0,80
"""

DEJETOS_DE_SUINOS_SCENARIOS = {
    "Pessimista": 2548.7999999999997,
    "Realista": 618.5088,
    "Otimista": 2124.0,
    "Teórico (100%)": 8496.0,
}

DEJETOS_DE_SUINOS_REFERENCES = [
    ScientificReference(
        title="Swine waste biogas production São Paulo",
        authors="Análise 1-8 papers consolidados",
        year=2024,
        doi="None" if False else None,
        scopus_link="None" if False else None,
        journal="Revista Técnica" if True else None,
        relevance="High",
        key_findings=[
            "BMP: 350-450 NL/kg SV | TS: 2,5-10% | C/N: 8-15 | Clusters SP identificados",
        ],
        data_type="Papers Consolidados"
    ),
    ScientificReference(
        title="Características químicas solo aplicação esterco líquido suínos pastagem",
        authors="Ceretta, C.A.; Durigon, R. et al.",
        year=2003,
        doi="None" if False else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Pesquisa Agropecuária Brasileira" if True else None,
        relevance="Very High",
        key_findings=[
            "FCp=1,00 (100% aplicação direta) | N=3,23 kg/m³ P=3,64 kg/m³ (2-3× típico) | Baseline pré-biodigestores | Perdas N: 47-65%",
        ],
        data_type="Campo - RS Baseline"
    ),
    ScientificReference(
        title="Potentialities energy generation waste feedstock agricultural sector Brazil Paraná",
        authors="Ribeiro, M.F.S.; Raiher, A.P.",
        year=2013,
        doi="None" if False else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Energy Policy" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP=0,29 Nm³/kg SV | RPR=5,90 m³/dia/cabeça | FC=0,70 (plantel comercial) | FS=0,88 (320 dias/ano) | 39,4% usinas PR escala viável",
        ],
        data_type="Análise Paraná"
    ),
    ScientificReference(
        title="Application cleaner production methodology evaluate generation bioenergy small swine farm",
        authors="Leite, S.A.F. et al.",
        year=2014,
        doi="10.3303/CET1439099" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Chemical Engineering Transactions" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP=0,30 Nm³/kg SV (validado SV e DBO) | Variação sazonal SV: 2,4× | Pequena propriedade 323 cabeças | Barreira investimento USD 250/suíno",
        ],
        data_type="Pequena Propriedade"
    ),
    ScientificReference(
        title="Life cycle assessment swine production Brazil comparison four manure management systems",
        authors="Cherubini, E. et al.",
        year=2015,
        doi="10.1016/j.jclepro.2014.10.035" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Journal of Cleaner Production" if True else None,
        relevance="Very High",
        key_findings=[
            "FCp=0,80 VALIDADO (80% lagoas abertas) | <1% CHP energia | Paradoxo NH₃: biodigestão +8% acidificação | ACV completa",
        ],
        data_type="LCA - Validação FCp"
    ),
    ScientificReference(
        title="Influence solid-liquid separation strategy biogas yield stratified swine production system",
        authors="Amaral, A.C.; Kunz, A. et al.",
        year=2016,
        doi="10.1016/j.jenvman.2015.12.014" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Journal of Environmental Management" if True else None,
        relevance="Very High",
        key_findings=[
            "BMP fase: Creche 642, Terminação 303, Gestação 170 NmL/g SV | Média ciclo: 0,36 Nm³/kg SV VALIDA CP2B | Armazenamento >15d: SV <1%",
        ],
        data_type="Experimental - Estratificação Fase"
    ),
    ScientificReference(
        title="Effect storage time swine manure solid separation efficiency screening",
        authors="Kunz, A.; Steinmetz, R.L.R. et al.",
        year=2009,
        doi="10.1016/j.biortech.2008.09.022" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Bioresource Technology" if True else None,
        relevance="Very High",
        key_findings=[
            "FC TEMPORAL: <7d FC=0,90 | 8-15d FC=0,65 | >15d FC=0,50 | DQO solubilização +76% em 29 dias | Ammonificação 24 mg/L/dia",
        ],
        data_type="Validação FC Temporal"
    ),
    ScientificReference(
        title="Eficiência energética sistema produção suínos tratamento resíduos biodigestor",
        authors="Angonese, A.R. et al.",
        year=2006,
        doi="None" if False else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Rev. Bras. Eng. Agrícola Ambiental" if True else None,
        relevance="High",
        key_findings=[
            "SAF=16,5% (energia biogás+biofertilizante) VALIDA CP2B 15,3% | BMP implícito 0,30 | TRH 10 dias (curto) | 650 terminação",
        ],
        data_type="Baseline SAF Validação"
    ),
    ScientificReference(
        title="Utility specific biomarkers assess safety swine manure biofertilizing purposes",
        authors="Fongaro, G. et al.",
        year=2014,
        doi="10.1016/j.scitotenv.2014.02.004" if True else None,
        scopus_link="https://www.scopus.com/" if True else None,
        journal="Science of the Total Environment" if True else None,
        relevance="High",
        key_findings=[
            "FS SAZONALIDADE: Temperatura 1,6-1,8× | NH₃ 2,3-2,9× verão vs inverno | Salmonella 2,7× verão | 93,5% PCV2 infeccioso pós-biodigestão",
        ],
        data_type="Sazonalidade + Biossegurança"
    ),
]

DEJETOS_DE_SUINOS_DATA = ResidueData(
    name="Dejetos de Suínos",
    category="Pecuária",
    icon="🐷",
    generation="4-5 kg/animal/dia (média) | Terminação: 5,5-8,6 kg/dia | Lactação: 2,35-4,0 kg/dia",
    destination="70% uso esporádico fertilizante + 30% biodigestão disponível",
    chemical_params=DEJETOS_DE_SUINOS_CHEMICAL_PARAMS,
    availability=DEJETOS_DE_SUINOS_AVAILABILITY,
    operational=DEJETOS_DE_SUINOS_OPERATIONAL,
    justification=DEJETOS_DE_SUINOS_JUSTIFICATION,
    scenarios=DEJETOS_DE_SUINOS_SCENARIOS,
    references=DEJETOS_DE_SUINOS_REFERENCES
)


# ============================================================================
# DEJETO DE CODORNAS
# ============================================================================

DEJETO_DE_CODORNAS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=0.0,
    bmp_unit="N/A",
    ts=24.5,
    vs=74.48,
    vs_basis="% of TS",
    moisture=75.5,
    cn_ratio=None,
    ph=6.01,
    cod=7640.0,
    nitrogen=663.32,
    carbon=None,
    ch4_content=None,
    phosphorus=0.24,
    potassium=225.0,
    protein=None,
    toc=None
)

DEJETO_DE_CODORNAS_AVAILABILITY = AvailabilityFactors(
    fc=0.6,
    fcp=0.9,
    fs=1.0,
    fl=0.7,
    final_availability=4.20
)

DEJETO_DE_CODORNAS_OPERATIONAL = OperationalParameters(
    hrt="N/A",
    temperature="N/A"
)

DEJETO_DE_CODORNAS_JUSTIFICATION = """
Validação cruzada avicultura
"""

DEJETO_DE_CODORNAS_SCENARIOS = {
    "Pessimista": 0.1,
    "Realista": 0.5,
    "Otimista": 1.2,
    "Teórico (100%)": 12.0,
}

DEJETO_DE_CODORNAS_REFERENCES = [
    ScientificReference(
        title="Chemical microbiological characterization quail wastes",
        authors="Sousa et al.",
        year=2012,
        doi="None" if False else None,
        scopus_link="None" if False else None,
        journal="ASABE Annual Meeting" if True else None,
        relevance="Medium",
        key_findings=[
            "TS=24,5% VS=74,5%TS pH=6,01",
        ],
        data_type="Experimental"
    ),
]

DEJETO_DE_CODORNAS_DATA = ResidueData(
    name="Dejeto de Codornas",
    category="Pecuária",
    icon="🐦",
    generation="TS: 24,5% | N: 663 mg/L",
    destination="90% fertilizante",
    chemical_params=DEJETO_DE_CODORNAS_CHEMICAL_PARAMS,
    availability=DEJETO_DE_CODORNAS_AVAILABILITY,
    operational=DEJETO_DE_CODORNAS_OPERATIONAL,
    justification=DEJETO_DE_CODORNAS_JUSTIFICATION,
    scenarios=DEJETO_DE_CODORNAS_SCENARIOS,
    references=DEJETO_DE_CODORNAS_REFERENCES
)


# ============================================================================
# REGISTRY AND HELPER FUNCTIONS
# ============================================================================

RESIDUES_REGISTRY = {
    "Dejeto de Aves (Cama de Frango)": DEJETO_DE_AVES_CAMA_DE_FRANGO_DATA,
    "Dejetos de Bovinos (Leite + Corte)": DEJETOS_DE_BOVINOS_LEITE__CORTE_DATA,
    "Vinhaça de Cana-de-açúcar": VINHACA_DE_CANA_DE_ACUCAR_DATA,
    "Palha de Cana-de-açúcar (Palhiço)": PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA,
    "Torta de Filtro (Filter Cake)": TORTA_DE_FILTRO_FILTER_CAKE_DATA,
    "Dejetos de Suínos": DEJETOS_DE_SUINOS_DATA,
    "Dejeto de Codornas": DEJETO_DE_CODORNAS_DATA,
}

CATEGORIES = {
    "Agricultura": ["Vinhaça de Cana-de-açúcar", "Palha de Cana-de-açúcar (Palhiço)", "Torta de Filtro (Filter Cake)"],
    "Pecuária": ["Dejeto de Aves (Cama de Frango)", "Dejetos de Bovinos (Leite + Corte)", "Dejetos de Suínos", "Dejeto de Codornas"]
}

# Parallel sectors structure for UI organization
SECTORS = {
    "Agricultura": {
        "name": "Agricultura",
        "icon": "🌾",
        "description": "Resíduos agrícolas e agroindustriais",
        "color": "#059669",
        "gradient": "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)",
        "border_color": "#059669",
        "residues": ["Vinhaça de Cana-de-açúcar", "Palha de Cana-de-açúcar (Palhiço)", "Torta de Filtro (Filter Cake)"]
    },
    "Pecuária": {
        "name": "Pecuária",
        "icon": "🐄",
        "description": "Dejetos animais e resíduos pecuários",
        "color": "#ea580c",
        "gradient": "linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)",
        "border_color": "#ea580c",
        "residues": ["Dejeto de Aves (Cama de Frango)", "Dejetos de Bovinos (Leite + Corte)", "Dejetos de Suínos", "Dejeto de Codornas"]
    },
    "Urbano": {
        "name": "Urbano",
        "icon": "🏙️",
        "description": "Resíduos sólidos urbanos e lodo de esgoto",
        "color": "#6366f1",
        "gradient": "linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)",
        "border_color": "#6366f1",
        "residues": []  # Para futuro
    },
    "Industrial": {
        "name": "Industrial",
        "icon": "🏭",
        "description": "Efluentes e resíduos industriais",
        "color": "#8b5cf6",
        "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%)",
        "border_color": "#8b5cf6",
        "residues": []  # Para futuro
    }
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
        "Agricultura": "🌾",
        "Pecuária": "🐄",
        "Urbano": "🏙️"
    }
    return icons.get(category, "📊")


def get_residue_icon(residue_name: str) -> str:
    """Get emoji icon for specific residue"""
    residue = get_residue_data(residue_name)
    return residue.icon if residue else "📊"


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


def parse_range_from_string(value_str: str) -> Optional[ParameterRange]:
    """
    Parse range from string like "Range: 200-350" or "range: 70-80%"

    Args:
        value_str: String containing range information

    Returns:
        ParameterRange object or None if no range found
    """
    import re

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
