"""
Vinhaça - Residue Data
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

VINHAÇA_DATA = ResidueData(
    name="Vinhaça",
    category="Agricultura",
    icon="🌾",
    generation="10-15 m³/m³ etanol",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=20.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=97.0,
        cn_ratio=12.5,
        ch4_content=65.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.015, mean=0.02, max=0.025, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=10.0,
            mean=12.5,
            max=15.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=65.0,
            mean=65.0,
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
        hrt="20 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Vinhaça**

    **Geração:** 10-15 m³/m³ etanol
    **Sazonalidade:** Maio-Dezembro
    **Estado Físico:** Líquido
    **Pré-tratamento:** Concentração
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
