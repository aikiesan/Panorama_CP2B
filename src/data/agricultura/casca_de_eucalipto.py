"""
Casca de eucalipto - Residue Data
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

CASCA_DE_EUCALIPTO_DATA = ResidueData(
    name="Casca de eucalipto",
    category="Agricultura",
    icon="🌳",
    generation="150 kg MS/ton madeira (RPR ~0.15)",
    destination="60% adubo, 20% biomassa térmica",

    chemical_params=ChemicalParameters(
        bmp=0.08,
        bmp_unit="m³ CH₄/kg MS",
        ts=89.0,  # TODO: Add from data source
        vs=60.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=50.0,
        cn_ratio=80.0,
        ch4_content=50.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.06, mean=0.09, max=0.12, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=80.0,
            mean=100.0,
            max=120.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=45.0,
            mean=50.0,
            max=55.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.25,  # TODO: Add actual availability factors
        fcp=0.1,
        fs=1.0,
        fl=1.0,
        final_availability=0.2250
    ),

    operational=OperationalParameters(
        hrt="45 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=40.0,
            mean=45.0,
            max=50.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Casca de eucalipto**

    **Geração:** 15-20 m³/ha/ciclo
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração + hidrólise alcalina
    **Região Concentrada:** Vale do Paraíba, Litoral

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.01,
        "Realista": 0.025,
        "Otimista": 0.05,
        "Teórico (100%)": 1.0
    },

    references=[
        ScientificReference(
            title="PINCELLI, Ana Lúcia Sodero Martins et al. Quantificação dos resíduos da colheita em florestas de Eucalyptus grandis... Scientia Forestalis, v. 45, n. 115, p. 519-526, 2017",
            authors="PINCELLI, Ana Lúcia Sodero Martins et al.",
            year=2017,
            doi="10.18671/scifor.v45n115.09",
            scopus_link="https://www.ipef.br/publicacoes/scientia/nr115/cap09.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="FOELKEL, Celso. Gestão ecoeficiente dos resíduos florestais lenhosos da eucaliptocultura. Eucalyptus Online Book & Newsletter, 2007",
            authors="FOELKEL, Celso",
            year=2007,
            scopus_link="https://www.eucalyptus.com.br/capitulos/PT07_residuoslenhosos.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="IBÁ - Indústria Brasileira de Árvores. Anuário 2016: ano base 2015. São Paulo: Ibá, 2016",
            authors="IBÁ - Indústria Brasileira de Árvores",
            year=2016,
            scopus_link="https://iba.org/datafiles/publicacoes/relatorios/",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="EPE - Empresa de Pesquisa Energética. Inventário Energético de Resíduos Rurais. Nota Técnica DEA 15/14. Rio de Janeiro, 2014",
            authors="EPE - Empresa de Pesquisa Energética",
            year=2014,
            scopus_link="http://arquivos.ambiente.sp.gov.br/cpla/2016/12/DEA-15-14-Inventário-Energético-de-Resíduos-Rurais.pdf",
            relevance="High",
            data_type="Literatura Científica"
        ),
    ]
)
