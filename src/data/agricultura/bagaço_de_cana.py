"""
Bagaço de cana - Residue Data
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

BAGAÇO_DE_CANA_DATA = ResidueData(
    name="Bagaço de cana",
    category="Agricultura",
    icon="🌾",
    generation="250-280kg/ton",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=85.0,  # Phase 5: Updated from SAF analysis (Nm³/t)
        bmp_unit="Nm³ CH₄/t",
        ts=45.0,  # Typical TS for bagaço
        vs=80.0,  # Volatile solids percentage
        vs_basis="% TS",
        moisture=50.0,
        cn_ratio=65.0,
        ch4_content=55.0,

        # Ranges from literature
        bmp_range=ParameterRange(
            min=75.0,
            mean=85.0,
            max=95.0,
            unit="Nm³ CH₄/t"
        ),
        cn_ratio_range=ParameterRange(
            min=50.0,
            mean=65.0,
            max=80.0
        ),
        ch4_content_range=ParameterRange(
            min=55.0,
            mean=55.0,
            max=55.0,
            unit="%"
        ),
    ),

    availability=AvailabilityFactors(
        fc=0.95,  # Phase 5 SAF: Fator de Coleta (High - centralized processing)
        fcp=1.0,  # Phase 5 SAF: Fator de Competição (No competition - primary use is energy)
        fs=1.0,   # Phase 5 SAF: Fator Sazonalidade (Available year-round in mills)
        fl=1.0,   # Phase 5 SAF: Fator Logístico (On-site processing)
        final_availability=80.75  # Phase 5 SAF: Real availability factor
    ),

    operational=OperationalParameters(
        hrt="20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=20.0,
            mean=25.0,
            max=30.0,
            unit="dias"
        )
    ),

    justification="""
    **Bagaço de cana - FASE 5 VALIDAÇÃO SAF**

    **Geração:** 250-280 kg/ton cana processada
    **Sazonalidade:** Maio-Dezembro (safra)
    **Estado Físico:** Sólido fibroso
    **Pré-tratamento:** Compactação/armazenamento

    **Análise SAF (Surplus Availability Factor):**
    - SAF Real: 80.75% (EXCEPCIONAL - Rank 1)
    - FC=0.95: Coleta centralizada em usinas (alta eficiência)
    - FCp=1.0: Sem competição (energia é uso primário)
    - FS=1.0: Disponível contínuo em processamento
    - FL=1.0: No local da usina (transporte zero)

    **Viabilidade:** JÁ IMPLEMENTADO em muitas usinas de cana
    Potencial residual (complementar a biomassa existente): 10-15% adicional
    """,

    scenarios={
        "Pessimista": 2200.0,  # 70% de SAF × volume teórico
        "Realista": 3139.0,    # 80.75% de SAF (validado)
        "Otimista": 4200.0,    # 90% com otimizações logísticas
        "Teórico (100%)": 5236.0  # 100% - referência teórica
    },

    references=[],

    # Phase 5: SAF Validation Fields
    saf_real=80.75,
    priority_tier="EXCEPCIONAL",
    recommendation="JÁ IMPLEMENTADO - Potencial residual limitado (complementar usinas existentes)",
    saf_rank=1,
    fc_value=0.95,
    fcp_value=1.0,
    fs_value=1.0,
    fl_value=1.0,
    culture_group="Cana-de-Açúcar"
)
