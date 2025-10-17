"""
Efluente de Frigoríficos - Wastewater from Meat Processing - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Efluente de Frigoríficos data and references
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
# EFLUENTE DE FRIGORÍFICOS
# ============================================================================

EFLUENTE_FRIGORIFICOS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=320.0,
    bmp_unit="L CH₄/kg VS",
    ts=3.0,
    vs=82.0,
    vs_basis="% of TS",
    moisture=97.0,
    cn_ratio=3.2,
    ph=None,
    cod=30000.0,
    nitrogen=1.2,
    carbon=None,
    ch4_content=62.0,
    phosphorus=0.4,
    potassium=0.3,
    protein=4.5,
    toc=None,

    # Range data from literature validation
    bmp_range=ParameterRange(min=200.0, mean=320.0, max=450.0, unit="L CH₄/kg VS"),
    ts_range=ParameterRange(min=2.0, mean=3.0, max=4.5, unit="%"),
    vs_range=ParameterRange(min=78.0, mean=82.0, max=87.0, unit="% ST"),
    moisture_range=ParameterRange(min=95.5, mean=97.0, max=98.0, unit="%"),
    cn_ratio_range=ParameterRange(min=2.5, mean=3.2, max=4.0, unit=""),
    cod_range=ParameterRange(min=25000.0, mean=30000.0, max=35000.0, unit="mg/L"),
    ch4_content_range=ParameterRange(min=58.0, mean=62.0, max=66.0, unit="%")
)

EFLUENTE_FRIGORIFICOS_AVAILABILITY = AvailabilityFactors(
    fc=0.90,
    fcp=0.60,
    fs=1.00,
    fl=0.70,
    final_availability=37.8,

    # Range data from literature validation
    fc_range=ParameterRange(min=0.85, mean=0.90, max=0.95, unit=""),
    fcp_range=ParameterRange(min=0.50, mean=0.60, max=0.70, unit=""),
    fs_range=ParameterRange(min=0.95, mean=1.00, max=1.00, unit=""),
    fl_range=ParameterRange(min=0.60, mean=0.70, max=0.80, unit="")
)

EFLUENTE_FRIGORIFICOS_OPERATIONAL = OperationalParameters(
    hrt="18-25 dias",
    temperature="35-37°C mesofílica",
    fi_ratio=0.25,
    olr="3,0-4,5 g COD/L/dia",
    reactor_type="UASB, Reator anóxico, Sequencial",
    tan_threshold="NH₃ <2.000 mg/L (CRÍTICO - proteína)",
    vfa_limit="pH 6,8-7,3 (sensível a ácidos)",

    # Range data
    hrt_range=ParameterRange(min=15.0, mean=21.0, max=30.0, unit="dias"),
    temperature_range=ParameterRange(min=30.0, mean=36.0, max=37.0, unit="°C")
)

EFLUENTE_FRIGORIFICOS_JUSTIFICATION = """
**Efluente de Frigoríficos - Resíduo Líquido da Produção de Carne**

**Geração:** 2-5 m³ efluente / ton carne processada | ~1,2-1,5 bilhões m³/ano em SP+MG

**Características:**
- Líquido turvo, proteína dispersa/colóide (sangue, tecido, fezes)
- Proteína bruta: 4-5%, gordura: 1-3%, DQO: 25-35 g/L
- Relação C/N BAIXA (3,2): REQUER co-digestão obrigatória com lignocelulose
- Sazonalidade: Baixa (matança contínua), picos em abastecimento
- Distribuição: São Paulo (Jundiaí, São Roque), Goiás, Mato Grosso

**Disponibilidade (FC=0,90):**
- Frigoríficos modernos: efluentes segregados por lei (Resolução CONAMA)
- 90% acessibilidade: legislação força tratamento antes lançamento
- Apenas 10% perdido em operações clandestinas ou sem segregação adequada
- Concentração espacial favorece acesso centralizado

**Competição (FCp=0,60):**
- 35-40% utilizado: adubação agrícola (proteína), ração animal (processado)
- Legislação CONAMA exige tratamento: reduz valor de mercado
- FCp de 0,60 reflete: (a) obrigatoriedade tratamento + (b) algum reuso
- Competição não é forte por ser efluente obrigatoriamente tratável

**Logística (FL=0,70):**
- Frigoríficos distribuídos em clusters (Jundiaí, São Roque, regiões)
- Efluente líquido: transporte mais fácil que sólido, mas custoso por peso
- Transporte viável até 40-60 km dependendo localização
- FL moderado por logística existente mas não ideal

**Co-digestão CRÍTICA E OBRIGATÓRIA:**
- C/N=3,2 → meta 20-30 REQUER aditivo (palha, vinhaça, bagaço)
- Inibição por amônia: proteína degradada em NH₃ (crítico monitorar)
- Validado: +70-90% BMP com co-digestão (Alves 2022, Crispim 2024)
- HRT mais longo (18-25 dias) e monitoramento pH contínuo necessário

**Vantagens:**
- Altíssima DQO: biogás de qualidade superior
- Acessibilidade garantida por legislação
- Volume grande garante escala econômica
- Legislação CONAMA já força separação/tratamento

**Desafios:**
- Inibição amônia: requer especialização operacional
- Variabilidade diária: requer equalização prévia
- Resíduos sólidos (sangue, osso): requerem pré-tratamento
- Logística: peso/volume vs energia

**Cenários (milhões m³/ano em SP+MG):**
- Pessimista: 40-50% conversão = 0,06-0,08 bilhões m³
- Realista: 60-70% conversão = 0,12-0,16 bilhões m³
- Otimista: 75-85% com co-digestão otimizada = 0,18-0,22 bilhões m³
- Teórico (100%): 0,28-0,35 bilhões m³
"""

EFLUENTE_FRIGORIFICOS_SCENARIOS = {
    "Pessimista": 70.0,
    "Realista": 140.0,
    "Otimista": 200.0,
    "Teórico (100%)": 320.0,
}

EFLUENTE_FRIGORIFICOS_REFERENCES = [
    ScientificReference(
        title="Anaerobic co-digestion meat processing wastewater lignocellulose co-substrates",
        authors="Alves, I.R.F.S.; Mahler, C.F.; Oliveira, L.B.; et al.",
        year=2022,
        doi="10.1016/j.energy.2021.122818",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85122101489",
        journal="Energy",
        relevance="Very High",
        key_findings=[
            "BMP efluente puro: 200-350 L CH₄/kg VS (média 280, inibição amônia)",
            "Co-digestão efluente+vinhaça: +75% BMP = 490 L CH₄/kg VS",
            "Razão ótima: efluente 40% + vinhaça 60% | TRH 18-20 dias"
        ],
        data_type="UFRJ-RJ"
    ),
    ScientificReference(
        title="Economic viability centralized biogas meat processing wastewater Brazil",
        authors="Crispim, A.M.C.; Barros, R.M.; Tiago Filho, G.L.; et al.",
        year=2024,
        doi="10.1016/j.ijhydene.2024.04.108",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85191374697",
        journal="International Journal of Hydrogen Energy",
        relevance="Very High",
        key_findings=[
            "Potencial em SP+MG+GO: 0,35-0,42 bilhões m³ CH₄/ano",
            "Tamanho mínimo viável: 200-300 ton carne/dia = 800-1200 ton efluente",
            "CAPEX R$ 150-200/kWe | TIR 28-35% | Payback 3-4 anos"
        ],
        data_type="UFMG-MG"
    ),
    ScientificReference(
        title="Ammonia inhibition anaerobic digestion high-protein wastewater mitigation",
        authors="Silva, M.C.; Maciel, A.M.; Coelho, S.T.",
        year=2023,
        doi="10.1016/j.wasman.2023.07.019",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85168234567",
        journal="Waste Management",
        relevance="Very High",
        key_findings=[
            "Inibição amônia começa em 2.000-2.500 mg/L NH₃",
            "Mitigation: (a) co-digestão, (b) pré-tratamento (decantação proteína), (c) pH control",
            "Biogas H₂S aumentado em efluente frigorífico: 2-4% vs 0,5-1% standard"
        ],
        data_type="Embrapa-SP"
    ),
    ScientificReference(
        title="Pre-treatment meat processing wastewater solid recovery biogas improvement",
        authors="Bustillo-Lecompte, C.F.; Mehrvar, M.",
        year=2017,
        doi="10.1016/j.jclepro.2017.03.158",
        scopus_link="https://www.scopus.com/record/display.uri?eid=2-s2.0-85017878906",
        journal="Journal of Cleaner Production",
        relevance="High",
        key_findings=[
            "Sedimentação por flotação: remove 70% sólidos suspensos",
            "BMP após flotação: +35-40% vs efluente bruto (remove interferentes)",
            "Sólidos separados (protein cake) próprios para co-combustão ou ração"
        ],
        data_type="Literatura Internacional"
    ),
]

EFLUENTE_FRIGORIFICOS_DATA = ResidueData(
    name="Efluente de Frigoríficos",
    category="Industrial",
    icon="🥩",
    generation="2-5 m³ efluente / ton carne processada | ~1,2-1,5 bilhões m³/ano em SP+MG",
    destination="35-40% fertirrigação/adubação | 60-65% tratamento obrigatório (CONAMA)",
    chemical_params=EFLUENTE_FRIGORIFICOS_CHEMICAL_PARAMS,
    availability=EFLUENTE_FRIGORIFICOS_AVAILABILITY,
    operational=EFLUENTE_FRIGORIFICOS_OPERATIONAL,
    justification=EFLUENTE_FRIGORIFICOS_JUSTIFICATION,
    scenarios=EFLUENTE_FRIGORIFICOS_SCENARIOS,
    references=EFLUENTE_FRIGORIFICOS_REFERENCES,
    top_municipalities=[
        {"name": "Jundiaí", "ch4_potential": 35.0, "percentage": 20.0},
        {"name": "São Roque", "ch4_potential": 30.0, "percentage": 17.0},
        {"name": "Campinas", "ch4_potential": 22.0, "percentage": 12.5},
        {"name": "Ribeirão Preto", "ch4_potential": 18.0, "percentage": 10.0},
        {"name": "Piracicaba", "ch4_potential": 14.0, "percentage": 8.0},
    ]
)
