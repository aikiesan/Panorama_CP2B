"""
Cama de frango - Residue Data
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

CAMA_DE_FRANGO_DATA = ResidueData(
    name="Cama de frango",
    category="Agricultura",
    icon="🐔",
    generation="1,5-2,0 kg/ave/ciclo",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=230.0,
        bmp_unit="m³ CH₄/kg VS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=30.0,
        cn_ratio=12.5,
        ch4_content=62.5,

        # Ranges from CSV
        bmp_range=ParameterRange(min=0.18, mean=0.23, max=0.28, unit="m³ CH₄/kg VS") if True else None,
        cn_ratio_range=ParameterRange(
            min=10.0,
            mean=12.5,
            max=15.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=60.0,
            mean=62.5,
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
    **Cama de frango**

    **Geração:** 1,5-2,0 kg/ave/ciclo
    **Sazonalidade:** Ano todo
    **Estado Físico:** Sólido
    **Pré-tratamento:** Compostagem parcial
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
        # ['https://journals.ufrpe.br/index.php/geama/article/view/2691']
    ],

    # Phase 5: FDE Validation Fields
    fde_real=8.67,
    priority_tier="BOM",
    recommendation="PRIORIDADE MÉDIA-ALTA - Sistema bem estabelecido em granjas",
    fde_rank=8,
    fc_value=0.85,
    fcp_value=3.0,
    fs_value=1.0,
    fl_value=0.90,
    culture_group="Avicultura"
)
