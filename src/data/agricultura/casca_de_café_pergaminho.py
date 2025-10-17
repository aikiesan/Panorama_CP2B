"""
Casca de café (pergaminho) - Residue Data
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

CASCA_DE_CAFÉ_(PERGAMINHO)_DATA = ResidueData(
    name="Casca de café (pergaminho)",
    category="Agricultura",
    icon="☕",
    generation="0,18 kg/kg café beneficiado",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=175.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=50.0,
        cn_ratio=20.0,
        ch4_content=60.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=150.0,
            mean=175.0,
            max=200.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=55.0,
            mean=60.0,
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
    **Casca de café (pergaminho)**

    **Geração:** 0,18 kg/kg café beneficiado
    **Sazonalidade:** Maio-Setembro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração
    **Região Concentrada:** Sul SP, Mogiana

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
        # ['https://www.sciencedirect.com/science/article/abs/pii/S0360544223009982']
    ]
)
