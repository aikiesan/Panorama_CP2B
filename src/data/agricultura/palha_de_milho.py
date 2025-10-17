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
        bmp=230.0,
        bmp_unit="mL CH₄/g VS",
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
        fc=0.80,  # TODO: Add actual availability factors
        fcp=0.50,
        fs=1.00,
        fl=0.70,
        final_availability=28.0
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
        "Pessimista": 0.0,  # TODO: Calculate
        "Realista": 0.0,    # TODO: Calculate
        "Otimista": 0.0,    # TODO: Calculate
        "Teórico (100%)": 0.0  # TODO: Calculate
    },

    references=[
        # TODO: Parse references from CSV
        # ['https://iris.unito.it/retrieve/handle/2318/151594/26398/Anaerobic%20digestion%20of%20corn%20stover%20fractions_Menardo.pdf']
    ]
)
