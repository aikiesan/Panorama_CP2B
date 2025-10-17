"""
Palha de cana - Residue Data
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

PALHA_DE_CANA_DATA = ResidueData(
    name="Palha de cana",
    category="Agricultura",
    icon="🌾",
    generation="280kg/ton",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=200.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=15.0,
        cn_ratio=100.0,
        ch4_content=53.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=200.0,
            mean=200.0,
            max=200.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=80.0,
            mean=100.0,
            max=120.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=53.0,
            mean=53.0,
            max=53.0,
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
    **Palha de cana**

    **Geração:** 280kg/ton
    **Sazonalidade:** Maio-Dezembro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração/Hidrólise
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
        # ['https://task37.ieabioenergy.com/wp-content/uploads/sites/32/2022/02/Update_Energy_crop_2011.pdf']
    ]
)
