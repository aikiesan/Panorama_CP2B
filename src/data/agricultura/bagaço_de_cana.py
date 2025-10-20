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
        fc=0.95,  # Fator de Coleta (High - centralized processing in mills)
        fcp=1.0,  # Fator de Competição (100% competition - ALL used in cogeneration)
        fs=1.0,   # Fator Sazonalidade (Available year-round in mills)
        fl=1.0,   # Fator Logístico (On-site processing)
        final_availability=0.0  # CORRECTED: 0% available - 100% used in cogeneration (cogeração)
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
    **Bagaço de cana - 0% Disponível para Biogás**

    **Geração:** 250-280 kg/ton cana processada
    **Sazonalidade:** Maio-Dezembro (safra)
    **Estado Físico:** Sólido fibroso
    **Situação:** 100% comprometido em cogeração elétrica e vapor

    **Análise de Disponibilidade:**
    - **Disponibilidade Real: 0%** (ZERO available for biogas)
    - FC=0.95: Coleta centralizada eficiente em usinas
    - FCp=1.0: **100% competição com cogeração** (uso prioritário já estabelecido)
    - FS=1.0: Disponível durante todo processamento
    - FL=1.0: No local da usina (transporte zero)

    **Justificativa:** 
    Bagaço é queimado em caldeiras para geração de vapor de processo e eletricidade.
    Este uso já está consolidado e é economicamente essencial para operação das usinas.
    
    **Fórmula de Disponibilidade:**
    D_final = FC × (1 - FCp) × FS × FL × 100%
    D_final = 0.95 × (1 - 1.0) × 1.0 × 1.0 × 100% = **0%**
    
    **Impacto:** Não contribui para cenários de biogás. Todo potencial já explorado em cogeração.
    
    **Referência:** Ver análise agregada em "Cana-de-Açúcar" para contexto completo do setor.
    """,

    scenarios={
        "Pessimista": 0.0,  # 0% - All used in cogeneration
        "Realista": 0.0,    # 0% - All used in cogeneration
        "Otimista": 0.0,    # 0% - All used in cogeneration
        "Teórico (100%)": 5236.0  # 100% theoretical (if cogeneration didn't exist)
    },

    references=[],

    # SAF Validation Fields - CORRECTED
    saf_real=0.0,
    priority_tier="NÃO DISPONÍVEL",
    recommendation="NÃO VIÁVEL - 100% usado em cogeração. Sem potencial adicional para biogás.",
    saf_rank=None,  # Not ranked - not available
    fc_value=0.95,
    fcp_value=1.0,  # 100% competition
    fs_value=1.0,
    fl_value=1.0,
    culture_group="Cana-de-Açúcar"
)
