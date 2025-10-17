"""
Soro de queijo - Residue Data
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

SORO_DE_QUEIJO_DATA = ResidueData(
    name="Soro de queijo",
    category="Industrial",
    icon="🧀",
    generation="9 L/kg queijo",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=500.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=94.5,
        cn_ratio=4.5,
        ch4_content=65.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=400.0,
            mean=500.0,
            max=600.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=3.0,
            mean=4.5,
            max=6.0
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
        hrt="12 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=10.0,
            mean=12.5,
            max=15.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Soro de queijo**

    **Geração:** 9 L/kg queijo
    **Sazonalidade:** Ano todo
    **Estado Físico:** Líquido
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
        # ['https://revistas.rcaap.pt/index.php/rca/article/view/16405']
    ]
)
