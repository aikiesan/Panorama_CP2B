"""
Dejetos de postura - Residue Data
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

DEJETOS_DE_POSTURA_DATA = ResidueData(
    name="Dejetos de postura",
    category="Agricultura",
    icon="🌾",
    generation="0,15 kg/ave/dia",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=330.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=80.0,
        cn_ratio=10.0,
        ch4_content=63.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.28, mean=0.33, max=0.38, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=8.0,
            mean=10.0,
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
        hrt="22 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=18.0,
            mean=21.5,
            max=25.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Dejetos de postura**

    **Geração:** 0,15 kg/ave/dia
    **Sazonalidade:** Ano todo
    **Estado Físico:** Semi-sólido
    **Pré-tratamento:** Separação sólido/líquido
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
        # ['https://www.embrapa.br/documents/1355242/0/Biog%C3%A1sFert+-+Recupera%C3%A7%C3%A3o+energ%C3%A9tica+atrav%C3%A9s+da+produ%C3%A7%C3%A3o+de+metano+via+digest%C3%A3o+anaer%C3%B3bia+de+cama+de+frango+de+corte.pdf']
    ]
)
