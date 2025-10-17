"""
Palha de soja - Residue Data
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

PALHA_DE_SOJA_DATA = ResidueData(
    name="Palha de soja",
    category="Agricultura",
    icon="🫘",
    generation="2,5-3,0 ton/ha",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=190.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=15.0,
        cn_ratio=30.0,
        ch4_content=51.5,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=160.0,
            mean=190.0,
            max=220.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=25.0,
            mean=30.0,
            max=35.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=48.0,
            mean=51.5,
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
    **Palha de soja**

    **Geração:** 2,5-3,0 ton/ha
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
        # ['https://www.repositorio.ufal.br/bitstream/123456789/8792/1/Produ%C3%A7%C3%A3o%20de%20Hidrog%C3%AAnio%20a%20partir%20do%20Hidrolisado%20da%20Palha%20da%20Soja.pdf']
    ]
)
