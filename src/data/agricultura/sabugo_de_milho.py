"""
Sabugo de milho - Residue Data
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

SABUGO_DE_MILHO_DATA = ResidueData(
    name="Sabugo de milho",
    category="Agricultura",
    icon="🌽",
    generation="2,5 ton/ha",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=185.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=15.0,
        cn_ratio=50.0,
        ch4_content=52.5,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=150.0,
            mean=185.0,
            max=220.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=40.0,
            mean=50.0,
            max=60.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=50.0,
            mean=52.5,
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
    **Sabugo de milho**

    **Geração:** 2,5 ton/ha
    **Sazonalidade:** Fevereiro-Julho
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração e pré-tratamento hidrotérmico
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
        # ['https://open.metu.edu.tr/handle/11511/89580']
    ]
)
