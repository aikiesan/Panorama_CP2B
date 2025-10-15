"""
Dejetos de Suínos - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Dejetos de Suínos data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# DEJETOS DE SUÍNOS
# ============================================================================


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
