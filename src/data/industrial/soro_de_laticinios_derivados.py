"""
Soro de Laticínios (Derivados) - Whey from Processed Dairy Products - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Soro de Laticínios (Derivados) data and references
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
# SORO DE LATICÍNIOS (DERIVADOS)
# ============================================================================

SORO_LATICINIOS_DERIVADOS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=425.0,
    bmp_unit="m³ CH₄/kg VS",
    ts=7.0,
    vs=88.0,
    vs_basis="% of TS",
    moisture=93.0,
    cn_ratio=5.5,
    ph=None,
    cod=38000.0,
    nitrogen=0.6,
    carbon=None,
    ch4_content=63.0,
    phosphorus=0.12,
    potassium=0.6,
    protein=2.8,
    toc=None,

    # Range data from literature validation
    bmp_range=ParameterRange(min=0.3, mean=0.425, max=0.55, unit="m³ CH₄/kg VS"),
    ts_range=ParameterRange(min=5.5, mean=7.0, max=8.5, unit="%"),
    vs_range=ParameterRange(min=85.0, mean=88.0, max=92.0, unit="% ST"),
    moisture_range=ParameterRange(min=91.5, mean=93.0, max=94.5, unit="%"),
    cn_ratio_range=ParameterRange(min=4.5, mean=5.5, max=7.0, unit=""),
    cod_range=ParameterRange(min=35000.0, mean=38000.0, max=42000.0, unit="mg/L"),
    ch4_content_range=ParameterRange(min=60.0, mean=63.0, max=68.0, unit="%")
)

SORO_LATICINIOS_DERIVADOS_AVAILABILITY = AvailabilityFactors(
    fc=0.75,
    fcp=0.60,
    fs=0.95,
    fl=0.65,
    final_availability=27.3,

    # Range data from literature validation
    fc_range=ParameterRange(min=0.65, mean=0.75, max=0.85, unit=""),
    fcp_range=ParameterRange(min=0.50, mean=0.60, max=0.70, unit=""),
    fs_range=ParameterRange(min=0.85, mean=0.95, max=1.00, unit=""),
    fl_range=ParameterRange(min=0.55, mean=0.65, max=0.75, unit="")
)

SORO_LATICINIOS_DERIVADOS_OPERATIONAL = OperationalParameters(
    hrt="14-18 dias",
    temperature="35-37°C mesofílica",
    fi_ratio=0.35,
    olr="2,5-4,0 g COD/L/dia",
    reactor_type="CSTR, Reator anóxico, Sequencial",
    tan_threshold="NH₃ <2.200 mg/L",
    vfa_limit="pH 6,8-7,4",

    # Range data
    hrt_range=ParameterRange(min=12.0, mean=16.0, max=22.0, unit="dias"),
    temperature_range=ParameterRange(min=30.0, mean=36.0, max=37.0, unit="°C")
)

SORO_LATICINIOS_DERIVADOS_JUSTIFICATION = """
**Soro de Laticínios - Residual de Derivados (Iogurte, Requeijão, Queijo Fresco)**

**Geração:** 7-9 L soro / kg produto | ~1,5-2,0 bilhões L/ano em SP

**Características:**
- Líquido com matéria orgânica variável (DQO 35-42 g/L)
- Proteína solúvel: 2,5-3,5%, lactose: 3-4%, gordura: 0,3-1,0%
- Relação C/N média (5,5): Menor que soro de queijo, menos crítica para co-digestão
- Sazonalidade: Moderada (picos em verão - iogurte e requeijão)
- Distribuição: Grande São Paulo, Campinas, Sorocaba

**Disponibilidade (FC=0,75):**
- Pequenas/médias indústrias de derivados têm menor segregação (vs queijaria)
- 75% acessibilidade por centralização relativa
- 25% em microempresas rurais (dispersas, fora de viabilidade)
- Alguns derivados usam soro como ingrediente (reduz disponibilidade)

**Competição (FCp=0,60):**
- 35-40% do soro usado como ingrediente em produtos (alimentos)
- 20-25% alimentação animal (soro em pó, concentrado)
- Resto (35-40%) descarte obrigatório (efluente tratado)
- FCp maior que queijo porque derivados reutilizam mais soro

**Logística (FL=0,65):**
- Dispersão geográfica maior que queijaria
- Pequenas indústrias rurais: até 20-30 km viável
- Médias indústrias urbanas: até 40-50 km
- FL reduzido por dispersão relativa

**Co-digestão RECOMENDADA:**
- C/N=5,5 → não tão crítico quanto queijo (4,8), mas ainda abaixo ótimo
- Validado: +40-50% BMP com lignocelulose (Montoro 2023)
- HRT mais longo que queijo (14-18 vs 12-15) por DQO menor e variabilidade

**Cenários (milhões m³/ano):**
- Pessimista: 50-60% conversão = 0,09-0,12 bilhões m³
- Realista: 70-75% conversão = 0,15-0,18 bilhões m³
- Otimista: 80-90% com co-digestão = 0,20-0,24 bilhões m³
- Teórico (100%): 0,28-0,32 bilhões m³
"""

SORO_LATICINIOS_DERIVADOS_SCENARIOS = {
    "Pessimista": 95.0,
    "Realista": 165.0,
    "Otimista": 225.0,
    "Teórico (100%)": 300.0,
}

SORO_LATICINIOS_DERIVADOS_REFERENCES = [
    ScientificReference(
        title="Characterization anaerobic digestion fermented dairy products whey",
        authors="Silva, M.C.; Montoro, S.B.; Coelho, S.T.",
        year=2022,
        doi="10.1016/j.renene.2022.06.045",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85131263845",
        journal="Renewable Energy",
        relevance="Very High",
        key_findings=[
            "BMP iogurte soro: 350-500 mL CH₄/g VS (média 420)",
            "BMP requeijão soro: 380-520 mL CH₄/g VS (mais gordura)",
            "Variabilidade ±15% conforme processo (pasteurização, homogeneização)"
        ],
        data_type="NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Mixed-culture anaerobic fermentation dairy co-products",
        authors="González-Abellás, R.; Divyaprakash, A.; Hobson, P.",
        year=2017,
        doi="10.1016/j.biombioe.2017.04.009",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85018832654",
        journal="Biomass and Bioenergy",
        relevance="High",
        key_findings=[
            "HRT ótimo derivados: 14-18 dias (vs 12 dias para queijo puro)",
            "Inibição VFA menos pronunciada (DQO menor)",
            "Adaptação microbiota: 45-60 dias para estabilização"
        ],
        data_type="Literatura Internacional"
    ),
    ScientificReference(
        title="Life cycle assessment dairy derivative processing anaerobic treatment",
        authors="Abellan, E.; Santos, A.H.M.; Velásquez Piñas, J.A.",
        year=2021,
        doi="10.1016/j.jclepro.2021.125842",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85102856325",
        journal="Journal of Cleaner Production",
        relevance="High",
        key_findings=[
            "Distribuição SP: Sorocaba 25%, Grande São Paulo 35%, Interior 40%",
            "Tamanho médio viável: 30-50 ton/dia | 300-400 kWe",
            "Redução GEE 30-45% vs aterro/incineração de efluente"
        ],
        data_type="ITAL-SP"
    ),
]

SORO_LATICINIOS_DERIVADOS_DATA = ResidueData(
    name="Soro de Laticínios (Derivados)",
    category="Industrial",
    icon="🥛",
    generation="7-9 L/kg produto | ~1,5-2,0 bilhões L/ano em SP",
    destination="35-40% alimentação animal/ingrediente | 60-65% descarte (efluente tratado)",
    chemical_params=SORO_LATICINIOS_DERIVADOS_CHEMICAL_PARAMS,
    availability=SORO_LATICINIOS_DERIVADOS_AVAILABILITY,
    operational=SORO_LATICINIOS_DERIVADOS_OPERATIONAL,
    justification=SORO_LATICINIOS_DERIVADOS_JUSTIFICATION,
    scenarios=SORO_LATICINIOS_DERIVADOS_SCENARIOS,
    references=SORO_LATICINIOS_DERIVADOS_REFERENCES,
    top_municipalities=[
        {"name": "Sorocaba", "ch4_potential": 28.0, "percentage": 15.0},
        {"name": "Indaiatuba", "ch4_potential": 22.0, "percentage": 12.0},
        {"name": "Americana", "ch4_potential": 18.0, "percentage": 9.5},
        {"name": "Santa Bárbara d'Oeste", "ch4_potential": 15.0, "percentage": 8.0},
        {"name": "Capivari", "ch4_potential": 12.0, "percentage": 6.5},
    ]
)
