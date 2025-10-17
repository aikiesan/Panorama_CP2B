"""
Bagaço de cana - Residue Data
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

BAGAÇO_DE_CANA_DATA = ResidueData(
    name="Bagaço de cana",
    category="Agricultura",
    icon="🌾",
    generation="250-280kg/ton",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=175.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=50.0,
        cn_ratio=65.0,
        ch4_content=55.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=175.0,
            mean=175.0,
            max=175.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=50.0,
            mean=65.0,
            max=80.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=55.0,
            mean=55.0,
            max=55.0,
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
        hrt="25 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=20.0,
            mean=25.0,
            max=30.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Bagaço de cana**

    **Geração:** 250-280kg/ton
    **Sazonalidade:** Maio-Dezembro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Pré-hidrólise
    **Região Concentrada:** Centro-Oeste SP

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
        # ['Moraes, B.S. et al. (2015)']
    ]
)
