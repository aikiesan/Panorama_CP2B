"""
Palha de soja - Residue Data
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

PALHA_DE_SOJA_DATA = ResidueData(
    name="Palha de soja",
    category="Agricultura",
    icon="🫘",
    generation="1210 kg MS/ton grão",
    destination="70% cobertura de solo (SPD), 10-15% combustível (briquetes)",

    chemical_params=ChemicalParameters(
        bmp=0.23,
        bmp_unit="m³ CH₄/kg MS",
        ts=88.5,  # TODO: Add from data source
        vs=87.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=15.0,
        cn_ratio=18.0,
        ch4_content=57.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.16, mean=0.19, max=0.22, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=25.0,
            mean=30.0,
            max=35.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=48.0,
            mean=51.5,
            max=55.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.3,  # TODO: Add actual availability factors
        fcp=0.1,
        fs=1.0,
        fl=1.0,
        final_availability=0.2700
    ),

    operational=OperationalParameters(
        hrt="30 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=25.0,
            mean=30.0,
            max=35.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Palha de soja**

    **Geração:** 2,5-3,0 ton/ha
    **Sazonalidade:** Fevereiro-Maio
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração
    **Região Concentrada:** Oeste SP

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.01,
        "Realista": 0.03,
        "Otimista": 0.08,
        "Teórico (100%)": 1.0
    },

    references=[
        ScientificReference(
            title="VEDOVATTO, Felipe et al. Production of biofuels from soybean straw and hull hydrolysates... Bioresource Technology, v. 340, 124837, 2021",
            authors="VEDOVATTO, Felipe et al.",
            year=2021,
            doi="10.1016/j.biortech.2021.124837",
            scopus_link="https://repositorio.ufsm.br/handle/1/23342",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="LÓPEZ-DÁVILA, Edelbis et al. Biochemical methane potential of agro-wastes... Ciencia y Tecnología Agropecuaria, v. 23, n. 1, e1890, 2022",
            authors="LÓPEZ-DÁVILA, Edelbis et al.",
            year=2022,
            doi="10.21930/rcta.vol23_num1_art:1890",
            scopus_link="http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0122-87062022000100002",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="BENTSEN, Niclas Scott et al. Agricultural residue production and potentials... Progress in Energy and Combustion Science, v. 40, p. 59-73, 2014",
            authors="BENTSEN, Niclas Scott et al.",
            year=2014,
            doi="10.1016/j.pecs.2013.09.003",
            scopus_link="http://macroecointern.dk/pdf-reprints/Bentsen_PECS_2014.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="CARVALHO, João Luís N. et al. Crop residue harvest for bioenergy production... Scientia Agricola, v. 74, n. 1, p. 66-80, 2017",
            authors="CARVALHO, João Luís N. et al.",
            year=2017,
            doi="10.1590/1678-992X-2016-0459",
            scopus_link="https://www.scielo.br/j/sa/a/mkjrJnJnFgxKhtZ9FSByDfh/?format=pdf&lang=en",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="SILESHI, Gudeta W. et al. Organic Matter Database (OMD)... Earth System Science Data, v. 17, p. 369-393, 2025",
            authors="SILESHI, Gudeta W. et al.",
            year=2025,
            doi="10.5194/essd-17-369-2025",
            scopus_link="https://essd.copernicus.org/articles/17/369/2025/essd-17-369-2025.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="DELAVALLADE, Clara et al. Understanding the contribution of soybean crop residues to soil nitrogen dynamics... PLOS ONE, v. 17, n. 6, e0270165, 2022",
            authors="DELAVALLADE, Clara et al.",
            year=2022,
            doi="10.1371/journal.pone.0270165",
            scopus_link="https://pmc.ncbi.nlm.nih.gov/articles/PMC9216555/",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="POPOVIĆ, Miroslav et al. Analysis of soybean production and biogas yield potential. Economics of Agriculture, v. 67, n. 4, p. 1053-1064, 2020",
            authors="POPOVIĆ, Miroslav et al.",
            year=2020,
            doi="10.5937/ekoPolj2004053P",
            scopus_link="https://scindeks.ceon.rs/article.aspx?artid=0352-34622004053P",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="KOOPMANS, Anja; KOPPEJAN, Jaap. Agricultural and forest residues - Generation, utilization and availability. FAO, 1997",
            authors="KOOPMANS, Anja; KOPPEJAN, Jaap",
            year=1997,
            scopus_link="https://www.fao.org/4/ad576e/ad576e00.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="EPE. Inventário Energético de Resíduos Rurais. Nota Técnica DEA 15/14. Rio de Janeiro, 2014",
            authors="EPE",
            year=2014,
            scopus_link="http://arquivos.ambiente.sp.gov.br/cpla/2016/12/DEA-15-14-Inventário-Energético-de-Resíduos-Rurais.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="ABiogás. Nota Técnica: Potencial de Biogás no Brasil. São Paulo, 2019",
            authors="ABiogás",
            year=2019,
            scopus_link="https://abiogas.org.br/publicacoes/",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="EMBRAPA. Tecnologias de Produção de Soja - Região Central do Brasil 2020. Sistemas de Produção, n. 17. Londrina, 2020",
            authors="EMBRAPA",
            year=2020,
            scopus_link="https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1123928/1/SP-17-2020-online-1.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="IBGE. Levantamento Sistemático da Produção Agrícola - LSPA 2019",
            authors="IBGE",
            year=2019,
            scopus_link="https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/9201-levantamento-sistematico-da-producao-agricola.html",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="CAO, Hongbing et al. Plant residue quality regulates mineral-associated organic carbon accumulation... Environmental Research, v. 267, 120593, 2025",
            authors="CAO, Hongbing et al.",
            year=2025,
            doi="10.1016/j.envres.2025.120593",
            scopus_link="https://doi.org/10.1016/j.envres.2025.120593",
            relevance="High",
            data_type="Literatura Científica"
        ),
    ]
)
