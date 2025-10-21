"""
Torta de filtro - Residue Data
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

TORTA_DE_FILTRO_DATA = ResidueData(
    name="Torta de filtro",
    category="Agricultura",
    icon="🌾",
    generation="3-4 kg/ton cana",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=175.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=80.0,
        cn_ratio=10.0,
        ch4_content=60.0,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.15, mean=0.175, max=0.2, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=8.0,
            mean=10.0,
            max=12.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=58.0,
            mean=60.0,
            max=62.0,
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
    **Torta de filtro**

    **Geração:** 3-4 kg/ton cana
    **Sazonalidade:** Maio-Dezembro
    **Estado Físico:** Semi-sólido
    **Pré-tratamento:** Não necessário
    **Região Concentrada:** Centro-Oeste SP

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
        # ['https://repositorio.ifes.edu.br/bitstream/handle/123456789/4594/Tcc_Avalia%C3%A7%C3%A3o_do_Potencial.pdf?sequence=1&isAllowed=y']
    ]
)
