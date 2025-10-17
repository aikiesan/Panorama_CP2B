"""
Casca de eucalipto - Residue Data
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

CASCA_DE_EUCALIPTO_DATA = ResidueData(
    name="Casca de eucalipto",
    category="Agricultura",
    icon="🌳",
    generation="15-20 m³/ha/ciclo",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=90.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=50.0,
        cn_ratio=100.0,
        ch4_content=50.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=60.0,
            mean=90.0,
            max=120.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=80.0,
            mean=100.0,
            max=120.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=45.0,
            mean=50.0,
            max=55.0,
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
        hrt="45 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=40.0,
            mean=45.0,
            max=50.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Casca de eucalipto**

    **Geração:** 15-20 m³/ha/ciclo
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
        # ['Carneiro, A.C.O. et al. (2016)']
    ]
)
