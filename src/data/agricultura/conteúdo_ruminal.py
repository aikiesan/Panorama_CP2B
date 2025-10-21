"""
Conteúdo ruminal - Residue Data
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

CONTEÚDO_RUMINAL_DATA = ResidueData(
    name="Conteúdo ruminal",
    category="Agricultura",
    icon="🌾",
    generation="40-60 kg/cabeça",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=160.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=88.5,
        cn_ratio=20.0,
        ch4_content=58.5,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.12, mean=0.16, max=0.2, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=55.0,
            mean=58.5,
            max=62.0,
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
    **Conteúdo ruminal**

    **Geração:** 40-60 kg/cabeça
    **Sazonalidade:** Ano todo
    **Estado Físico:** Semi-sólido
    **Pré-tratamento:** Peneiramento
    **Região Concentrada:** Interior SP (geral)

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
        # ['Lovato, G. et al. (2017)']
    ]
)
