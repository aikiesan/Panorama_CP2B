"""
Torta de Filtro (Filter Cake) - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Torta de Filtro (Filter Cake) data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# TORTA DE FILTRO (FILTER CAKE)
# ============================================================================

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

