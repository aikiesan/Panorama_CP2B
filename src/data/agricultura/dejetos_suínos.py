"""
Dejetos suínos - Residue Data
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

DEJETOS_SUÍNOS_DATA = ResidueData(
    name="Dejetos suínos",
    category="Agricultura",
    icon="🐖",
    generation="2,3 kg/cabeça/dia",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=550.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=92.5,
        cn_ratio=5.5,
        ch4_content=67.5,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=450.0,
            mean=550.0,
            max=650.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=3.0,
            mean=5.5,
            max=8.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=65.0,
            mean=67.5,
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
        hrt="16 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=12.0,
            mean=16.0,
            max=20.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Dejetos suínos**

    **Geração:** 2,3 kg/cabeça/dia
    **Sazonalidade:** Ano todo
    **Estado Físico:** Líquido
    **Pré-tratamento:** Separação sólido/líquido
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
        # ['https://sustenere.inf.br/index.php/rica/article/download/SPC2179-6858.2017.004.0013/1152/6644']
    ]
)
