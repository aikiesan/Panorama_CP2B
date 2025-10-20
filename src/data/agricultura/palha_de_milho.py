"""
Palha de milho - Residue Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Auto-generated from CSV import
"""

from src.models.residue_models import (
    ResidueData,
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ParameterRange
)

PALHA_DE_MILHO_DATA = ResidueData(
    name="Palha de milho",
    category="Agricultura",
    icon="🌽",
    generation="8-12 ton/ha",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=0.22,
        bmp_unit="m³ CH₄/kg MS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=20.0,
        cn_ratio=42.5,
        ch4_content=55.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=200.0,
            mean=230.0,
            max=260.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=35.0,
            mean=42.5,
            max=50.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=52.0,
            mean=55.0,
            max=58.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.35,  # TODO: Add actual availability factors
        fcp=0.12,
        fs=1.0,
        fl=1.0,
        final_availability=0.3080
    ),

    operational=OperationalParameters(
        hrt="28 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=25.0,
            mean=27.5,
            max=30.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Palha de milho**

    **Geração:** 8-12 ton/ha
    **Sazonalidade:** Fevereiro-Julho
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração/Ensilagem
    **Região Concentrada:** Oeste SP

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.02,
        "Realista": 0.05,
        "Otimista": 0.1,
        "Teórico (100%)": 1.0
    },

    references=[
        ScientificReference(
            title="FERNÁNDEZ-RODRÍGUEZ, María José et al. Evaluation and modelling of methane production from corn stover... Waste Management & Research, v. 40, n. 6, p. 737-748, 2022",
            authors="FERNÁNDEZ-RODRÍGUEZ, María José et al.",
            year=2022,
            doi="10.1177/0734242X211038185",
            scopus_link="https://doi.org/10.1177/0734242X211038185",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="MENARDO, Salvatore et al. Potential biogas and methane yield of maize stover fractions... Biosystems Engineering, v. 129, p. 352-359, 2015",
            authors="MENARDO, Salvatore et al.",
            year=2015,
            doi="10.1016/j.biosystemseng.2014.11.007",
            scopus_link="https://doi.org/10.1016/j.biosystemseng.2014.11.007",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="LIU, Chunmei et al. Improving Biomethane Production... PLOS ONE, v. 10, n. 6, e0129025, 2015",
            authors="LIU, Chunmei et al.",
            year=2015,
            doi="10.1371/journal.pone.0129025",
            scopus_link="https://doi.org/10.1371/journal.pone.0129025",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="BRUNI, Enrico; JENSEN, Anders Peter; ANGELIDAKI, Irini. Anaerobic digestion of maize focusing on variety, harvest time and pretreatment. Applied Energy, v. 87, n. 7, p. 2212-2217, 2010",
            authors="BRUNI, Enrico; JENSEN, Anders Peter; ANGELIDAKI, Irini",
            year=2010,
            doi="10.1016/j.apenergy.2010.01.004",
            scopus_link="https://doi.org/10.1016/j.apenergy.2010.01.004",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="ALI, Shahid et al. Exploring lignocellulosic biomass for bio-methane potential... Energy, Environment, and Sustainability, v. 1, n. 1, p. 5-13, 2018",
            authors="ALI, Shahid et al.",
            year=2018,
            doi="10.1177/0958305X18759009",
            scopus_link="https://doi.org/10.1177/0958305X18759009",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="WEI, Wei et al. Enhanced high-quality biomethane production from anaerobic digestion... Bioresource Technology, v. 306, 123159, 2020",
            authors="WEI, Wei et al.",
            year=2020,
            doi="10.1016/j.biortech.2020.123159",
            scopus_link="https://doi.org/10.1016/j.biortech.2020.123159",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="NUNES, Márcio R. et al. Science-based maize stover removal can be sustainable. Agronomy Journal, v. 113, n. 5, p. 4100-4115, 2021",
            authors="NUNES, Márcio R. et al.",
            year=2021,
            doi="10.1002/agj2.20724",
            scopus_link="https://doi.org/10.1002/agj2.20724",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="JOHARI, Siti Aisyah Mohamad et al. Enhancing biogas production in anaerobic co-digestion of fresh chicken manure and corn stover. SN Applied Sciences, v. 2, n. 7, 1260, 2020",
            authors="JOHARI, Siti Aisyah Mohamad et al.",
            year=2020,
            doi="10.1007/s42452-020-3061-0",
            scopus_link="https://doi.org/10.1007/s42452-020-3061-0",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="AMARO, Bianca Ramos et al. Chemical composition of maize stover fraction versus methane yield... Energy, v. 198, 117322, 2020",
            authors="AMARO, Bianca Ramos et al.",
            year=2020,
            doi="10.1016/j.energy.2020.117322",
            scopus_link="https://doi.org/10.1016/j.energy.2020.117322",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="CARVALHO, João Luís N. et al. Crop residue harvest for bioenergy production... Scientia Agricola, v. 74, n. 1, p. 66-80, 2017",
            authors="CARVALHO, João Luís N. et al.",
            year=2017,
            doi="10.1590/1678-992X-2016-0459",
            scopus_link="https://doi.org/10.1590/1678-992X-2016-0459",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="IBGE. Produção Agrícola Municipal 2018... Agência IBGE Notícias, 04 set. 2019",
            authors="IBGE",
            year=2018,
            scopus_link="https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/25371-pam-2018-valor-da-producao-agricola-nacional-cresce-8-3-e-atinge-recorde-de-r-343-5-bilhoes",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="IEA. Disponibilidade e utilização de resíduos gerados no beneficiamento do milho. Informações Econômicas, São Paulo, v. 24, n. 1, 1994",
            authors="IEA",
            year=1994,
            scopus_link="https://iea.agricultura.sp.gov.br/ftpiea/ie/1994/tec1-0194.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="TORRES-MAYANGA, Paola C. et al. Decomposição da palhada e liberação de nitrogênio e fósforo... Pesquisa Agropecuária Brasileira, v. 49, n. 12, p. 1009-1017, 2014",
            authors="TORRES-MAYANGA, Paola C. et al.",
            year=2014,
            doi="10.1590/S0100-204X2014001200012",
            scopus_link="https://doi.org/10.1590/S0100-204X2014001200012",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="CERRI, Carlos Eduardo P. et al. Utilização do nitrogênio da palha de milho... Revista Brasileira de Ciência do Solo, v. 32, n. 6, p. 2853-2861, 2008",
            authors="CERRI, Carlos Eduardo P. et al.",
            year=2008,
            doi="10.1590/S0100-06832008000600034",
            scopus_link="https://doi.org/10.1590/S0100-06832008000600034",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="GRAHAM, Robert L. et al. Current and potential U.S. corn stover supplies. Agronomy Journal, v. 99, n. 1, p. 1-11, 2007",
            authors="GRAHAM, Robert L. et al.",
            year=2007,
            doi="10.2134/agronj2005.0222",
            scopus_link="https://doi.org/10.2134/agronj2005.0222",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="PURDUE UNIVERSITY. Corn Stover for Bioenergy Production... Extension Publication RE-3-W, 2003",
            authors="PURDUE UNIVERSITY",
            year=2003,
            scopus_link="https://www.extension.purdue.edu/extmedia/ec/re-3-w.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="IOWA STATE UNIVERSITY. How Much Crop Residue to Remove. Crop News, 2024",
            authors="IOWA STATE UNIVERSITY",
            year=2024,
            scopus_link="https://crops.extension.iastate.edu/cropnews/2012/04/how-much-crop-residue-remove",
            relevance="High",
            data_type="Literatura Científica"
        ),
    ]
)
