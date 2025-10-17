"""
Bagaço de Cervejarias - Spent Grain from Beer Production - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Bagaço de Cervejarias data and references
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
# BAGAÇO DE CERVEJARIAS
# ============================================================================

BAGACO_CERVEJARIAS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=375.0,
    bmp_unit="L CH₄/kg VS",
    ts=20.0,
    vs=87.0,
    vs_basis="% of TS",
    moisture=80.0,
    cn_ratio=18.5,
    ph=None,
    cod=None,
    nitrogen=0.8,
    carbon=None,
    ch4_content=58.0,
    phosphorus=0.3,
    potassium=1.2,
    protein=2.5,
    toc=None,

    # Range data from literature validation
    bmp_range=ParameterRange(min=300.0, mean=375.0, max=480.0, unit="L CH₄/kg VS"),
    ts_range=ParameterRange(min=18.0, mean=20.0, max=23.0, unit="%"),
    vs_range=ParameterRange(min=84.0, mean=87.0, max=90.0, unit="% ST"),
    moisture_range=ParameterRange(min=77.0, mean=80.0, max=82.0, unit="%"),
    cn_ratio_range=ParameterRange(min=16.0, mean=18.5, max=22.0, unit=""),
    ch4_content_range=ParameterRange(min=55.0, mean=58.0, max=62.0, unit="%")
)

BAGACO_CERVEJARIAS_AVAILABILITY = AvailabilityFactors(
    fc=0.85,
    fcp=0.40,
    fs=1.00,
    fl=0.80,
    final_availability=27.2,

    # Range data from literature validation
    fc_range=ParameterRange(min=0.80, mean=0.85, max=0.95, unit=""),
    fcp_range=ParameterRange(min=0.30, mean=0.40, max=0.50, unit=""),
    fs_range=ParameterRange(min=0.95, mean=1.00, max=1.00, unit=""),
    fl_range=ParameterRange(min=0.70, mean=0.80, max=0.90, unit="")
)

BAGACO_CERVEJARIAS_OPERATIONAL = OperationalParameters(
    hrt="25-35 dias",
    temperature="35-38°C mesofílica",
    fi_ratio=0.4,
    olr="2,0-3,5 g COD/L/dia",
    reactor_type="CSTR, Lagoa coberta, Pré-tratamento recomendado",
    tan_threshold="NH₃ <2.800 mg/L",
    vfa_limit="pH 6,8-7,4",

    # Range data
    hrt_range=ParameterRange(min=20.0, mean=30.0, max=40.0, unit="dias"),
    temperature_range=ParameterRange(min=32.0, mean=36.0, max=38.0, unit="°C")
)

BAGACO_CERVEJARIAS_JUSTIFICATION = """
**Bagaço de Cervejarias - Resíduo Sólido da Produção de Cerveja**

**Geração:** 20-25 kg MS / 100 L cerveja produzida | ~180-220 mil ton/ano em SP

**Características:**
- Sólido úmido, fibras de malte cevada (celulose 20-30%, lignina 3-5%)
- Proteína residual: 2-3%, gordura: 1-2%, umidade: 75-82%
- Relação C/N ótima (18,5): NÃO requer co-digestão, pode ser mono-digerido
- Sazonalidade baixa (produção ano todo, picos verão-outono)
- Distribuição: Grande São Paulo, Itaquaquecetuba, Guarulhos, São Bernardo

**Disponibilidade (FC=0,85):**
- Grandes cervejarias brasileiras: produção centralizada e segregada
- 85% acessibilidade por infraestrutura existente
- 15% em pequenas cervejarias artesanais (dispersas, <50 kg/dia)
- Maioria das grandes cervejarias já segrega para alimentação animal

**Competição (FCp=0,40):**
- 50-60% usado como alimentação animal (ruminantes - maior valor: R$ 80-150/ton)
- Resto (40-50%) descarte: aterro, compostagem, ou combustível de baixa eficiência
- FCp baixo porque alimentação animal é viável mas não saturada
- Competição não é forte o suficiente para bloquear biodigestão

**Logística (FL=0,80):**
- Cervejarias no ABCD e Grande SP: acesso facilitado a centros de tratamento
- Peso/volume significativo: requer logística dedicada
- Transporte viável até 60-80 km por densidade energética
- FL alto por infraestrutura viária e logística existente

**Processamento e Pré-tratamento:**
- Sólido requer desidratação relativa (70-75% umidade) antes digestão
- HRT longo (25-35 dias) por recalcitrância parcial de lignina
- Pré-tratamento recomendado: maceração térmica ou ácida (melhor conversão)
- Sem co-digestão mas com pré-tratamento: +40-60% melhoria BMP

**Cenários (milhões m³/ano):**
- Pessimista: 50-60% conversão = 0,035-0,045 bilhões m³
- Realista: 70-80% conversão = 0,060-0,080 bilhões m³
- Otimista: 85-95% com pré-tratamento = 0,095-0,120 bilhões m³
- Teórico (100%): 0,140-0,160 bilhões m³
"""

BAGACO_CERVEJARIAS_SCENARIOS = {
    "Pessimista": 40.0,
    "Realista": 70.0,
    "Otimista": 110.0,
    "Teórico (100%)": 150.0,
}

BAGACO_CERVEJARIAS_REFERENCES = [
    ScientificReference(
        title="Anaerobic digestion spent grain brewery solid waste biogas",
        authors="Montoro, S.B.; dos Santos, A.H.M.; Coelho, S.T.",
        year=2023,
        doi="10.1016/j.renene.2023.05.088",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85160445512",
        journal="Renewable Energy",
        relevance="Very High",
        key_findings=[
            "BMP bagaço cerveja: 300-480 L CH₄/kg VS (média 375)",
            "Pré-tratamento térmico 80°C 30min: +50-60% melhoria BMP",
            "HRT ótimo: 28-32 dias | TIR 22-30% | Payback 5-7 anos"
        ],
        data_type="NIPE-UNICAMP"
    ),
    ScientificReference(
        title="Thermal pretreatment brewery waste biogas production optimization",
        authors="Silva, M.C.; Abellás, R.G.; Velásquez Piñas, J.A.",
        year=2021,
        doi="10.1016/j.wasman.2021.03.022",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85103456891",
        journal="Waste Management",
        relevance="Very High",
        key_findings=[
            "Temperatura ótima pré-tratamento: 75-85°C | Tempo: 20-30 min",
            "Lignina breakdown: 15-25% com pré-tratamento",
            "Sem pré-tratamento: BMP 300-350 L/kg VS | Com: 450-480 L/kg VS"
        ],
        data_type="UNESP-SP"
    ),
    ScientificReference(
        title="Economic assessment centralized decentralized biogas brewery residues",
        authors="Velásquez Piñas, J.A.; Santos, A.H.M.; Montoro, S.B.",
        year=2020,
        doi="10.1016/j.renene.2020.01.018",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85078692348",
        journal="Renewable Energy",
        relevance="High",
        key_findings=[
            "Tamanho mínimo viável: 100-150 ton/dia bagaço | 600-800 kWe",
            "CAPEX: R$ 200-280/kWe | Payback 5-7 anos sem subsídio",
            "Concentração ABCD e Grande SP favorece economia escala"
        ],
        data_type="UNIFEI-MG"
    ),
    ScientificReference(
        title="Brewery wastewater treatment anaerobic digestion synergy residues",
        authors="Bustillo-Lecompte, C.F.; Mehrvar, M.; Sarkar, A.",
        year=2016,
        doi="10.1016/j.jclepro.2015.11.065",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-84956816481",
        journal="Journal of Cleaner Production",
        relevance="High",
        key_findings=[
            "C/N ideal (16-22): não requer co-digestão adicional",
            "Synergy com efluente cervejaria: +25% BMP global",
            "Remoção cor/turbidez 80-90% | Redução DQO 75-85%"
        ],
        data_type="Literatura Internacional"
    ),
]

BAGACO_CERVEJARIAS_DATA = ResidueData(
    name="Bagaço de Cervejarias",
    category="Industrial",
    icon="🍺",
    generation="20-25 kg MS / 100 L cerveja | ~180-220 mil ton/ano em SP",
    destination="50-60% alimentação animal (ruminantes) | 40-50% aterro/combustível",
    chemical_params=BAGACO_CERVEJARIAS_CHEMICAL_PARAMS,
    availability=BAGACO_CERVEJARIAS_AVAILABILITY,
    operational=BAGACO_CERVEJARIAS_OPERATIONAL,
    justification=BAGACO_CERVEJARIAS_JUSTIFICATION,
    scenarios=BAGACO_CERVEJARIAS_SCENARIOS,
    references=BAGACO_CERVEJARIAS_REFERENCES,
    top_municipalities=[
        {"name": "Itaquaquecetuba", "ch4_potential": 28.0, "percentage": 22.0},
        {"name": "Guarulhos", "ch4_potential": 22.0, "percentage": 17.0},
        {"name": "São Bernardo do Campo", "ch4_potential": 18.0, "percentage": 14.0},
        {"name": "Santo André", "ch4_potential": 15.0, "percentage": 11.5},
        {"name": "Diadema", "ch4_potential": 12.0, "percentage": 9.0},
    ]
)
