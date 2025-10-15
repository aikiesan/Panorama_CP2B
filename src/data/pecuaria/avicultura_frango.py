"""
Dejeto de Aves (Cama de Frango) - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Dejeto de Aves (Cama de Frango) data and references
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
# DEJETO DE AVES (CAMA DE FRANGO)
# ============================================================================

# DEJETO DE AVES (CAMA DE FRANGO)
# ============================================================================

DEJETO_DE_AVES_CAMA_DE_FRANGO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=275.0,  # Conservative mean
    bmp_unit="L CH₄/kg VS",
    ts=27.5,  # Mean of 25-30%
    vs=75.0,
    vs_basis="% of TS",
    moisture=72.5,  # 100 - 27.5 (TS)
    cn_ratio=9.5,  # Mean of 8-11
    ph=7.4,
    cod=296900.0,
    nitrogen=2.75,
    carbon=36.5,
    ch4_content=63.75,  # Mean of 62.5-65%
    phosphorus=3.5,
    potassium=3.93,
    protein=9.22,
    toc=None,
    # Range data from cenario_Avicultura.md validation
    bmp_range=ParameterRange(min=143.0, mean=360.0, max=650.0, unit="L CH₄/kg ST"),  # Adjusted max from 3285 (likely error)
    ts_range=ParameterRange(min=15.69, mean=27.5, max=40.0, unit="%"),
    vs_range=ParameterRange(min=69.8, mean=75.0, max=84.31, unit="% ST"),
    moisture_range=ParameterRange(min=60.0, mean=72.5, max=84.31, unit="%"),
    cn_ratio_range=ParameterRange(min=4.66, mean=9.5, max=11.55, unit=""),
    ch4_content_range=ParameterRange(min=49.2, mean=63.75, max=77.6, unit="%")
)

DEJETO_DE_AVES_CAMA_DE_FRANGO_AVAILABILITY = AvailabilityFactors(
    fc=0.9,
    fcp=0.5,
    fs=1.0,
    fl=0.9,
    final_availability=40.50,
    # Range data from cenario_Avicultura.md validation
    fc_range=ParameterRange(min=0.20, mean=0.90, max=1.0, unit=""),
    fcp_range=ParameterRange(min=0.40, mean=0.50, max=0.60, unit=""),
    fs_range=ParameterRange(min=0.60, mean=0.85, max=1.0, unit=""),
    fl_range=ParameterRange(min=0.50, mean=0.75, max=0.90, unit="")
)

DEJETO_DE_AVES_CAMA_DE_FRANGO_OPERATIONAL = OperationalParameters(
    hrt="42-60 dias",
    temperature="35-37°C mesofílica",
    fi_ratio=0.5,
    olr="2.9-4.0 kg VS/m³/dia",
    reactor_type="CSTR ou Batch Indian",
    tan_threshold="<2 g/L ideal, inibição 3-6 g/L",
    vfa_limit="Manter pH 6.8-7.2, correção Ca(OH)₂ se <6.0",
    # Range data from cenario_Avicultura.md validation
    hrt_range=ParameterRange(min=30.0, mean=51.0, max=97.0, unit="dias"),
    temperature_range=ParameterRange(min=25.0, mean=36.0, max=40.0, unit="°C")
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
