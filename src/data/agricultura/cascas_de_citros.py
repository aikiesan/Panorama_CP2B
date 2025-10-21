"""
Cascas de citros - Residue Data
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

CASCAS_DE_CITROS_DATA = ResidueData(
    name="Cascas de citros",
    category="Agricultura",
    icon="🍊",
    generation="440 kg MS/ton laranja (44% do fruto)",
    destination="92% para produtos de alto valor (óleo essencial, pectina)",

    chemical_params=ChemicalParameters(
        bmp=0.177,
        bmp_unit="m³ CH₄/kg MS",
        ts=21.3,  # TODO: Add from data source
        vs=87.5,  # TODO: Add from data source
        vs_basis="ST",
        moisture=75.0,
        cn_ratio=66.3,
        ch4_content=78.4,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.1, mean=0.15, max=0.2, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=20.0,
            mean=25.0,
            max=30.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=50.0,
            mean=60.0,
            max=70.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.9,  # TODO: Add actual availability factors
        fcp=0.08,
        fs=1.0,
        fl=1.0,
        final_availability=0.8280
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
    **Cascas de citros**

    **Geração:** 30-40% da fruta processada
    **Sazonalidade:** Maio-Outubro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração + extração limoneno
    **Região Concentrada:** Centro-Norte SP

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.0,
        "Realista": 0.08,
        "Otimista": 0.0,
        "Teórico (100%)": 1.0
    },

    references=[
        ScientificReference(
            title="WIKANDARI, R. et al. Improvement of Biogas Production from Orange Peel Waste by Leaching of Limonene. Biomedical Research International, v. 2015, 494182, 2015",
            authors="WIKANDARI, R. et al.",
            year=2015,
            doi="10.1155/2015/494182",
            scopus_link="https://pmc.ncbi.nlm.nih.gov/articles/PMC4383308/",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="WIKANDARI, R. et al. Biogas Production from Citrus Waste by Membrane Bioreactor. Membranes, v. 4, n. 3, p. 596-607, 2014",
            authors="WIKANDARI, R. et al.",
            year=2014,
            doi="10.3390/membranes4030596",
            scopus_link="https://pmc.ncbi.nlm.nih.gov/articles/PMC4194050/",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="ROSAS-MENDOZA, E. S. et al. Evaluation of bioenergy potential from citrus effluents... Renewable Energy, v. 163, p. 1229-1240, 2020",
            authors="ROSAS-MENDOZA, E. S. et al.",
            year=2020,
            doi="10.1016/j.renene.2020.09.040",
            scopus_link="https://doi.org/10.1016/j.renene.2020.09.040",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="CYPRIANO, D. Z.; DA SILVA, L. L.; TASIC, L. High value-added products from the orange juice industry waste. Waste Management, v. 79, p. 71-78, 2018",
            authors="CYPRIANO, D",
            year=2018,
            doi="10.1016/j.wasman.2018.07.028",
            scopus_link="https://doi.org/10.1016/j.wasman.2018.07.028",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="TEJADA-VÁZQUEZ, J. D. et al. Composting of Byproducts from the Orange... Revista Colombiana de Ciencia Animal, v. 12, n. 2, 2020",
            authors="TEJADA-VÁZQUEZ, J. D. et al.",
            year=2020,
            doi="10.24188/recia.v12.n2.2020.744",
            scopus_link="https://doi.org/10.24188/recia.v12.n2.2020.744",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="ROSALES-SAAVEDRA, T. et al. Carbon/Nitrogen Ratio Estimation for Urban Organic Waste... Revista Internacional de Contaminación Ambiental, v. 39, n. 3, p. 733-748, 2023",
            authors="ROSALES-SAAVEDRA, T. et al.",
            year=2023,
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="RUIZ, B. et al. Assessment of different pre-treatment methods for the removal of limonene... Waste Management & Research, v. 34, n. 12, p. 1249-1257, 2016",
            authors="RUIZ, B. et al.",
            year=2016,
            doi="10.1177/0734242X16661053",
            scopus_link="https://doi.org/10.1177/0734242X16661053",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="NEGRO, V. et al. Citrus waste as feedstock for bio-based products recovery... Bioresource Technology, v. 214, p. 806-815, 2016",
            authors="NEGRO, V. et al.",
            year=2016,
            doi="10.1016/j.biortech.2016.05.006",
            scopus_link="https://doi.org/10.1016/j.biortech.2016.05.006",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="VALENTI, F. et al. A GIS‐based model to estimate citrus pulp availability... Biofuels, Bioproducts and Biorefining, v. 11, n. 5, p. 789-799, 2017",
            authors="VALENTI, F. et al.",
            year=2017,
            doi="10.1002/bbb.1707",
            scopus_link="https://doi.org/10.1002/bbb.1707",
            relevance="High",
            data_type="Literatura Científica"
        ),
    ]
)
