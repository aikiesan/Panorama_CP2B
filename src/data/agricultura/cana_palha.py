"""
Palha de Cana-de-açúcar (Palhiço) - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Palha de Cana-de-açúcar (Palhiço) data and references
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
# PALHA DE CANA-DE-AÇÚCAR (PALHIÇO)
# ============================================================================

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
    final_availability=36.00,
    # Range data from Cenario_Cana.md validation
    fc_range=ParameterRange(min=0.60, mean=0.80, max=0.80, unit=""),
    fcp_range=ParameterRange(min=0.40, mean=0.65, max=0.65, unit=""),
    fs_range=ParameterRange(min=0.70, mean=0.85, max=1.0, unit=""),
    fl_range=ParameterRange(min=0.80, mean=0.90, max=0.90, unit="")
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
    name="Palha de cana",
    category="Agricultura",
    icon="🌾",
    generation="140 kg MS/ton colhida (14% MS) | 96,52% área temporária SP",
    destination="30% cobertura solo (obrigatório) + 70% disponível E2G/biogas",
    chemical_params=PALHA_DE_CANA_DE_ACUCAR_PALHICO_CHEMICAL_PARAMS,
    availability=PALHA_DE_CANA_DE_ACUCAR_PALHICO_AVAILABILITY,
    operational=PALHA_DE_CANA_DE_ACUCAR_PALHICO_OPERATIONAL,
    justification=PALHA_DE_CANA_DE_ACUCAR_PALHICO_JUSTIFICATION,
    scenarios=PALHA_DE_CANA_DE_ACUCAR_PALHICO_SCENARIOS,
    references=PALHA_DE_CANA_DE_ACUCAR_PALHICO_REFERENCES
)

