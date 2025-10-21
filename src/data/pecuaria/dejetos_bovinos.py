"""
Dejetos bovinos - Residue Data
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

DEJETOS_BOVINOS_DATA = ResidueData(
    name="Dejetos bovinos",
    category="Pecuária",
    icon="🐄",
    generation="10 kg/cabeça/dia",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=225.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=88.5,
        cn_ratio=15.0,
        ch4_content=64.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.15, mean=0.225, max=0.3, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=10.0,
            mean=15.0,
            max=20.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=60.0,
            mean=64.0,
            max=68.0,
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
    **Dejetos bovinos**

    **Geração:** 10 kg/cabeça/dia
    **Sazonalidade:** Ano todo
    **Estado Físico:** Líquido/Semi-sólido
    **Pré-tratamento:** Não necessário
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
        # ['https://anaiscbens.emnuvens.com.br/cbens/article/download/611/611']
    ]
)
