"""
Vinhaça de Cana-de-açúcar - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Vinhaça data and references
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
    fc=0.80,
    fcp=1.0,
    fs=0.90,
    fl=0.95,
    final_availability=10.26,  # Aligned with Phase 5 SAF validation (10.26%)
    # Range data from Phase 5 SAF Validation Analysis
    fc_range=ParameterRange(min=0.55, mean=0.80, max=0.95, unit=""),
    fcp_range=ParameterRange(min=0.75, mean=1.0, max=1.5, unit=""),
    fs_range=ParameterRange(min=0.70, mean=0.90, max=1.0, unit=""),
    fl_range=ParameterRange(min=0.65, mean=0.95, max=1.0, unit="")
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
        doi="10.1016/j.scitotenv.2020.142717",
        scopus_link="https://www.scopus.com/",
        journal="Science of the Total Environment",
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
        doi="10.1016/j.rser.2020.110281",
        scopus_link="https://www.scopus.com/",
        journal="Renewable and Sustainable Energy Reviews",
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
        doi="10.1002/ese3.462",
        scopus_link="https://www.scopus.com/",
        journal="Energy Science & Engineering",
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
        doi="10.1016/j.biombioe.2012.03.011",
        scopus_link="https://www.scopus.com/",
        journal="Biomass and Bioenergy",
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
        doi="10.1111/gcbb.12292",
        scopus_link="https://www.scopus.com/",
        journal="GCB Bioenergy",
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
        doi="10.1016/j.geoderma.2013.02.009",
        scopus_link="https://www.scopus.com/",
        journal="Geoderma",
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
        doi="10.3390/en13174413",
        scopus_link="https://www.scopus.com/",
        journal="Energies",
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
        doi="10.1016/j.renene.2021.04.070",
        scopus_link="https://www.scopus.com/",
        journal="Renewable Energy",
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
        doi="10.1007/s12010-015-1856-z",
        scopus_link="https://www.scopus.com/",
        journal="Appl Biochem Biotechnol",
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
        doi="10.1007/s10163-020-01029-y",
        scopus_link="https://www.scopus.com/",
        journal="J Material Cycles Waste Management",
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
    references=VINHACA_DE_CANA_DE_ACUCAR_REFERENCES,

    # Phase 5: SAF Validation Fields
    saf_real=10.26,
    priority_tier="BOM",
    recommendation="Volume elevado; fertirrigação já estabelecida (co-digestão sinérgica com torta)",
    saf_rank=5,
    fc_value=0.80,
    fcp_value=1.0,
    fs_value=0.90,
    fl_value=0.95,
    culture_group="Cana-de-Açúcar"
)
