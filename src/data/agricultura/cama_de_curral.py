"""
Cama de curral - Residue Data
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

CAMA_DE_CURRAL_DATA = ResidueData(
    name="Cama de curral",
    category="Agricultura",
    icon="🐄",
    generation="2-3 kg/cabeça/dia",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=250.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=67.5,
        cn_ratio=20.0,
        ch4_content=61.5,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.2, mean=0.25, max=0.3, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=58.0,
            mean=61.5,
            max=65.0,
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
    **Cama de curral**

    **Geração:** 2-3 kg/cabeça/dia
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Homogeneização
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
        # ['https://sustenere.inf.br/index.php/rica/article/download/SPC2179-6858.2017.004.0013/1152/6644']
    ]
)
