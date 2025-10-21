"""
Ração não consumida - Residue Data
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

RAÇÃO_NÃO_CONSUMIDA_DATA = ResidueData(
    name="Ração não consumida",
    category="Agricultura",
    icon="🌾",
    generation="2-5% da ração fornecida",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=375.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=12.5,
        cn_ratio=6.0,
        ch4_content=66.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.3, mean=0.375, max=0.45, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=4.0,
            mean=6.0,
            max=8.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=62.0,
            mean=66.0,
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
    **Ração não consumida**

    **Geração:** 2-5% da ração fornecida
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Não necessário
    **Região Concentrada:** Vale do Ribeira

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
        # ['https://ojs.revistacontribuciones.com/ojs/index.php/clcs/article/view/890']
    ]
)
