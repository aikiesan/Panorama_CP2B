"""
Sangue bovino - Residue Data
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

SANGUE_BOVINO_DATA = ResidueData(
    name="Sangue bovino",
    category="Agricultura",
    icon="🐄",
    generation="15-20 L/cabeça",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=275.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=85.0,
        cn_ratio=4.0,
        ch4_content=70.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.2, mean=0.275, max=0.35, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=3.0,
            mean=4.0,
            max=5.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=68.0,
            mean=70.0,
            max=72.0,
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
    **Sangue bovino**

    **Geração:** 15-20 L/cabeça
    **Sazonalidade:** Ano todo
    **Estado Físico:** Líquido viscoso
    **Pré-tratamento:** Coagulação
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
        # ['https://siambiental.ucs.br/congresso/getArtigo.php?id=404&ano=']
    ]
)
