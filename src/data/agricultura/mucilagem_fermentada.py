"""
Mucilagem fermentada - Residue Data
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

MUCILAGEM_FERMENTADA_DATA = ResidueData(
    name="Mucilagem fermentada",
    category="Agricultura",
    icon="🌾",
    generation="0,05 kg/kg café beneficiado",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=350.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=87.5,
        cn_ratio=10.0,
        ch4_content=65.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=300.0,
            mean=350.0,
            max=400.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=8.0,
            mean=10.0,
            max=12.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=60.0,
            mean=65.0,
            max=70.0,
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
    **Mucilagem fermentada**

    **Geração:** 0,05 kg/kg café beneficiado
    **Sazonalidade:** Maio-Setembro
    **Estado Físico:** Líquido
    **Pré-tratamento:** Não necessário
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
        # ['https://www.scielo.br/j/eagri/a/HMtY4DxjrLXKWsSV5tLczms/?format=pdf&lang=en']
    ]
)
