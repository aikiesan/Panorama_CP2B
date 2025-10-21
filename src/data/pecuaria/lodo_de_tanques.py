"""
Lodo de tanques - Residue Data
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

LODO_DE_TANQUES_DATA = ResidueData(
    name="Lodo de tanques",
    category="Pecuária",
    icon="💧",
    generation="50-100 kg/ton peixe",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=230.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=92.5,
        cn_ratio=9.0,
        ch4_content=63.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.18, mean=0.23, max=0.28, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=6.0,
            mean=9.0,
            max=12.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=58.0,
            mean=63.0,
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
    **Lodo de tanques**

    **Geração:** 50-100 kg/ton peixe
    **Sazonalidade:** Ano todo
    **Estado Físico:** Líquido espesso
    **Pré-tratamento:** Espessamento
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
        # ['https://periodicos.ufn.edu.br/index.php/disciplinarumNT/article/view/1327']
    ]
)
