"""
Bagaço de citros - Residue Data
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

BAGAÇO_DE_CITROS_DATA = ResidueData(
    name="Bagaço de citros",
    category="Agricultura",
    icon="🍊",
    generation="45-60% da fruta processada",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=115.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=80.0,
        cn_ratio=15.0,
        ch4_content=55.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=80.0,
            mean=115.0,
            max=150.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=12.0,
            mean=15.0,
            max=18.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=45.0,
            mean=55.0,
            max=65.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.80,  # TODO: Add actual availability factors
        fcp=0.50,
        fs=1.00,
        fl=0.70,
        final_availability=28.0
    ),

    operational=OperationalParameters(
        hrt="35 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=30.0,
            mean=35.0,
            max=40.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Bagaço de citros**

    **Geração:** 45-60% da fruta processada
    **Sazonalidade:** Maio-Outubro
    **Estado Físico:** Semi-sólido
    **Pré-tratamento:** Desidratação + remoção limoneno
    **Região Concentrada:** Centro-Norte SP

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.0,  # TODO: Calculate
        "Realista": 0.0,    # TODO: Calculate
        "Otimista": 0.0,    # TODO: Calculate
        "Teórico (100%)": 0.0  # TODO: Calculate
    },

    references=[
        # TODO: Parse references from CSV
        # ['https://pmc.ncbi.nlm.nih.gov/articles/PMC4383308/']
    ]
)
