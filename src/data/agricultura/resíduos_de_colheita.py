"""
Resíduos de colheita - Residue Data
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

RESÍDUOS_DE_COLHEITA_DATA = ResidueData(
    name="Resíduos de colheita",
    category="Agricultura",
    icon="🌾",
    generation="10-15 m³/ha/ciclo",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=110.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=40.0,
        cn_ratio=80.0,
        ch4_content=53.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.08, mean=0.11, max=0.14, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=60.0,
            mean=80.0,
            max=100.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=48.0,
            mean=53.0,
            max=58.0,
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
        hrt="40 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=35.0,
            mean=40.0,
            max=45.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Resíduos de colheita**

    **Geração:** 10-15 m³/ha/ciclo
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração + hidrólise alcalina
    **Região Concentrada:** Vale do Paraíba, Litoral

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
        # ['https://www.eucalyptus.com.br/eucaliptos/PT35_Compostagem_Residuos_Biogas.pdf']
    ]
)
