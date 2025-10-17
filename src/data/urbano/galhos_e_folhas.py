"""
Galhos e folhas - Residue Data
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

GALHOS_E_FOLHAS_DATA = ResidueData(
    name="Galhos e folhas",
    category="Urbano",
    icon="🏙️",
    generation="50-80 kg/hab/ano",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=35.0,
        bmp_unit="mL CH₄/g VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=55.0,
        cn_ratio=40.0,
        ch4_content=45.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=20.0,
            mean=35.0,
            max=50.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=30.0,
            mean=40.0,
            max=50.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=40.0,
            mean=45.0,
            max=50.0,
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
        hrt="52 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=45.0,
            mean=52.5,
            max=60.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Galhos e folhas**

    **Geração:** 50-80 kg/hab/ano
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração < 5mm + hidrólise alcalina + enzimática
    **Região Concentrada:** Região Metropolitana

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
        # ['https://periodicos.unicesumar.edu.br/index.php/rama/article/download/7840/6520/52558']
    ]
)
