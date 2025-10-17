"""
Vagens vazias - Residue Data
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

VAGENS_VAZIAS_DATA = ResidueData(
    name="Vagens vazias",
    category="Agricultura",
    icon="🌾",
    generation="0,8-1,2 ton/ha",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=210.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=20.0,
        cn_ratio=25.0,
        ch4_content=54.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=180.0,
            mean=210.0,
            max=240.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=20.0,
            mean=25.0,
            max=30.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=50.0,
            mean=54.0,
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
    **Vagens vazias**

    **Geração:** 0,8-1,2 ton/ha
    **Sazonalidade:** Fevereiro-Maio
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração
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
        # ['Zhang, W. et al. (2014)']
    ]
)
