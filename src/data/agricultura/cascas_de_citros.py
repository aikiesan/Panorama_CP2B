"""
Cascas de citros - Residue Data
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

CASCAS_DE_CITROS_DATA = ResidueData(
    name="Cascas de citros",
    category="Agricultura",
    icon="🍊",
    generation="30-40% da fruta processada",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=150.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=75.0,
        cn_ratio=25.0,
        ch4_content=60.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=100.0,
            mean=150.0,
            max=200.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=20.0,
            mean=25.0,
            max=30.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=50.0,
            mean=60.0,
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
    **Cascas de citros**

    **Geração:** 30-40% da fruta processada
    **Sazonalidade:** Maio-Outubro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração + extração limoneno
    **Região Concentrada:** Centro-Norte SP

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
        # ['https://pmc.ncbi.nlm.nih.gov/articles/PMC4194050/', 'https://www.sciencedirect.com/science/article/abs/pii/S095965262030175X']
    ]
)
