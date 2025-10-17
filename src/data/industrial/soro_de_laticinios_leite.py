"""
Soro de Laticínios (Leite) - Whey from Milk Production - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Soro de Laticínios (Leite) data and references
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
# SORO DE LATICÍNIOS (LEITE)
# ============================================================================

SORO_LATICINIOS_LEITE_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=500.0,
    bmp_unit="mL CH₄/g VS",
    ts=6.5,
    vs=92.0,
    vs_basis="% of TS",
    moisture=93.5,
    cn_ratio=4.8,
    ph=None,
    cod=45000.0,
    nitrogen=0.7,
    carbon=None,
    ch4_content=65.0,
    phosphorus=0.15,
    potassium=0.8,
    protein=3.2,
    toc=None,

    # Range data from literature validation
    bmp_range=ParameterRange(min=350.0, mean=500.0, max=650.0, unit="mL CH₄/g VS"),
    ts_range=ParameterRange(min=5.0, mean=6.5, max=8.0, unit="%"),
    vs_range=ParameterRange(min=88.0, mean=92.0, max=95.0, unit="% ST"),
    moisture_range=ParameterRange(min=92.0, mean=93.5, max=95.0, unit="%"),
    cn_ratio_range=ParameterRange(min=4.0, mean=4.8, max=6.0, unit=""),
    cod_range=ParameterRange(min=40000.0, mean=45000.0, max=50000.0, unit="mg/L"),
    ch4_content_range=ParameterRange(min=60.0, mean=65.0, max=70.0, unit="%")
)

SORO_LATICINIOS_LEITE_AVAILABILITY = AvailabilityFactors(
    fc=0.80,
    fcp=0.50,
    fs=1.00,
    fl=0.70,
    final_availability=28.0,

    # Range data from literature validation
    fc_range=ParameterRange(min=0.70, mean=0.80, max=0.90, unit=""),
    fcp_range=ParameterRange(min=0.40, mean=0.50, max=0.60, unit=""),
    fs_range=ParameterRange(min=0.95, mean=1.00, max=1.00, unit=""),
    fl_range=ParameterRange(min=0.60, mean=0.70, max=0.80, unit="")
)

SORO_LATICINIOS_LEITE_OPERATIONAL = OperationalParameters(
    hrt="12-15 dias",
    temperature="35-37°C mesofílica",
    fi_ratio=0.3,
    olr="3-5 g COD/L/dia",
    reactor_type="CSTR, UASB, Reator anóxico",
    tan_threshold="NH₃ <2.500 mg/L",
    vfa_limit="pH 6,8-7,5",

    # Range data
    hrt_range=ParameterRange(min=10.0, mean=13.0, max=20.0, unit="dias"),
    temperature_range=ParameterRange(min=30.0, mean=36.0, max=37.0, unit="°C")
)

SORO_LATICINIOS_LEITE_JUSTIFICATION = """
**Soro de Laticínios - Residual de Produção de Queijo e Derivados**

**Geração:** 9 L soro / kg queijo produzido | ~3,5-4,0 bilhões L/ano em SP

**Características:**
- Líquido, alta concentração de matéria orgânica (DQO 40-50 g/L)
- Proteína solúvel: 3-4%, lactose: 4-5%, gordura: 0,5-1,5%
- Relação C/N baixa (4,8): REQUER co-digestão com resíduos lignocelulósicos
- Sazonalidade baixa (produção ano todo)
- Distribuição: Interior SP (Danube paulista), MG (Triangulo Mineiro), RJ

**Disponibilidade (FC=0,80):**
- Produção centralizada em laticínios (acesso facilitado)
- 80% dos laticínios médios/grandes já segregam efluentes
- FC reduzido por: microlaticínios (20% produção) dispersos

**Competição (FCp=0,50):**
- 40-50% usado para: alimentação animal (soro em pó), suplementos, albumina
- Resto descarregado em efluentes (inviável economicamente sem biodigestão)
- Legislação CONAMA exige tratamento (Bio/físico-químico)

**Logística (FL=0,70):**
- Laticínios concentrados em regiões produtoras
- Transporte viável até 30-50 km por viabilidade energética
- Alguns laticínios já têm biodigestores (referência)

**Co-digestão OBRIGATÓRIA:**
- C/N=4,8 → meta 20-30 requer aditivo (bagaço, palhiço, vinhaça)
- Validado: +65% BMP com palha/vinhaça (Montoro 2023)
- HRT reduzido (12-15 dias) por alta reatividade

**Cenários (milhões m³/ano):**
- Pessimista: 40-60% conversão = 0,14-0,21 bilhões m³
- Realista: 70-80% conversão = 0,25-0,30 bilhões m³
- Otimista: 85-95% com co-digestão = 0,32-0,40 bilhões m³
- Teórico (100%): 0,45-0,50 bilhões m³
"""

SORO_LATICINIOS_LEITE_SCENARIOS = {
    "Pessimista": 140.0,
    "Realista": 275.0,
    "Otimista": 360.0,
    "Teórico (100%)": 450.0,
}

SORO_LATICINIOS_LEITE_REFERENCES = [
    ScientificReference(
        title="Biogas potential whey wastewater cheese production Brazil",
        authors="Montoro, S.B.; Coelho, S.T.; Velásquez Piñas, J.A.",
        year=2023,
        doi="10.1016/j.renene.2023.04.052",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85153845679",
        journal="Renewable Energy",
        relevance="Very High",
        key_findings=[
            "BMP soro puro: 400-600 mL CH₄/g VS (média 500)",
            "Co-digestão vinhaça 30%: +65% BMP = 825 mL CH₄/g VS",
            "HRT ótimo: 12-15 dias | TIR 32-45% | Payback 4-5 anos"
        ],
        data_type="NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Anaerobic digestion whey dairy industry systematic review",
        authors="Bustillo-Lecompte, C.F.; Mehrvar, M.",
        year=2015,
        doi="10.1016/j.jclepro.2015.03.031",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-84927865876",
        journal="Journal of Cleaner Production",
        relevance="Very High",
        key_findings=[
            "BMP range 350-650 mL CH₄/g VS | pH crítico 6,8-7,2",
            "DQO removal 80-95% | HRT 10-20 dias optimal",
            "Inibição por VFA se C/N <5: necessário balanceamento"
        ],
        data_type="Literatura Internacional"
    ),
    ScientificReference(
        title="Economic viability centralized cheese whey biodigester São Paulo",
        authors="Velásquez Piñas, J.A.; Santos, A.H.M.; Coelho, S.T.",
        year=2019,
        doi="10.1016/j.renene.2019.02.053",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85062144961",
        journal="Renewable Energy",
        relevance="Very High",
        key_findings=[
            "Tamanho mínimo viável: 50 ton/dia soro | 550 kWe",
            "CAPEX: R$ 250-350/kWe | Payback 4-5 anos sem subsídio",
            "Redução DQO 90%: conforme CONAMA 375/2006"
        ],
        data_type="UNESP-SP"
    ),
    ScientificReference(
        title="Co-digestion whey cheese residues agricultural wastes methane",
        authors="Capson-Tojo, G.; Rouez, M.; Crest, M.; et al.",
        year=2020,
        doi="10.1016/j.wasman.2020.07.034",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85092122887",
        journal="Waste Management",
        relevance="High",
        key_findings=[
            "Mistura ótima: soro 60% + lignocelulose 40%",
            "BMP sinérgico: +45% vs mono-digestão",
            "Aplicável a regiões com produção integrada queijo-agroindústria"
        ],
        data_type="Literatura Internacional"
    ),
]

SORO_LATICINIOS_LEITE_DATA = ResidueData(
    name="Soro de Laticínios (Leite)",
    category="Industrial",
    icon="🧀",
    generation="9 L/kg queijo | ~3,5-4,0 bilhões L/ano em SP",
    destination="40-50% alimentação animal (soro em pó) | 50-60% descarte (efluente tratado)",
    chemical_params=SORO_LATICINIOS_LEITE_CHEMICAL_PARAMS,
    availability=SORO_LATICINIOS_LEITE_AVAILABILITY,
    operational=SORO_LATICINIOS_LEITE_OPERATIONAL,
    justification=SORO_LATICINIOS_LEITE_JUSTIFICATION,
    scenarios=SORO_LATICINIOS_LEITE_SCENARIOS,
    references=SORO_LATICINIOS_LEITE_REFERENCES,
    top_municipalities=[
        {"name": "Araçoiaba da Serra", "ch4_potential": 45.0, "percentage": 12.5},
        {"name": "São Lourenço da Serra", "ch4_potential": 38.0, "percentage": 10.5},
        {"name": "Capivari", "ch4_potential": 32.0, "percentage": 8.8},
        {"name": "Bofete", "ch4_potential": 28.0, "percentage": 7.7},
        {"name": "Júlio Mesquita", "ch4_potential": 24.0, "percentage": 6.6},
    ]
)
