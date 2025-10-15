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
    ResidueData
)


# ============================================================================
# DEJETOS DE BOVINOS (LEITE + CORTE)
# ============================================================================



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
