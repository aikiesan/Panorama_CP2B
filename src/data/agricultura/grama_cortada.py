"""
Grama cortada - Residue Data
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

GRAMA_CORTADA_DATA = ResidueData(
    name="Grama cortada",
    category="Agricultura",
    icon="🌿",
    generation="20-30 kg/hab/ano",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=65.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=77.5,
        cn_ratio=20.0,
        ch4_content=55.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=50.0,
            mean=65.0,
            max=80.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=50.0,
            mean=55.0,
            max=60.0,
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
    **Grama cortada**

    **Geração:** 20-30 kg/hab/ano
    **Sazonalidade:** Ano todo
    **Estado Físico:** Semi-sólido
    **Pré-tratamento:** Ensilagem + pré-compostagem parcial
    **Região Concentrada:** Região Metropolitana

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
        # ['https://bdta.abcd.usp.br/directbitstream/455ea227-59a6-4f35-952e-d944e9286fb3/PabloGomesPassaglia.pdf']
    ]
)
