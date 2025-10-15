"""
Dejeto de Codornas - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only Dejeto de Codornas data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# DEJETO DE CODORNAS
# ============================================================================


# ============================================================================
# DEJETO DE CODORNAS
# ============================================================================

DEJETO_DE_CODORNAS_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=0.0,
    bmp_unit="N/A",
    ts=24.5,
    vs=74.48,
    vs_basis="% of TS",
    moisture=75.5,
    cn_ratio=None,
    ph=6.01,
    cod=7640.0,
    nitrogen=663.32,
    carbon=None,
    ch4_content=None,
    phosphorus=0.24,
    potassium=225.0,
    protein=None,
    toc=None
)

DEJETO_DE_CODORNAS_AVAILABILITY = AvailabilityFactors(
    fc=0.6,
    fcp=0.9,
    fs=1.0,
    fl=0.7,
    final_availability=4.20
)

DEJETO_DE_CODORNAS_OPERATIONAL = OperationalParameters(
    hrt="N/A",
    temperature="N/A"
)

DEJETO_DE_CODORNAS_JUSTIFICATION = """
Validação cruzada avicultura
"""

DEJETO_DE_CODORNAS_SCENARIOS = {
    "Pessimista": 0.1,
    "Realista": 0.5,
    "Otimista": 1.2,
    "Teórico (100%)": 12.0,
}

DEJETO_DE_CODORNAS_REFERENCES = [
    ScientificReference(
        title="Chemical microbiological characterization quail wastes",
        authors="Sousa et al.",
        year=2012,
        doi="None" if False else None,
        scopus_link="None" if False else None,
        journal="ASABE Annual Meeting" if True else None,
        relevance="Medium",
        key_findings=[
            "TS=24,5% VS=74,5%TS pH=6,01",
        ],
        data_type="Experimental"
    ),
]

DEJETO_DE_CODORNAS_DATA = ResidueData(
    name="Dejeto de Codornas",
    category="Pecuária",
    icon="🐦",
    generation="TS: 24,5% | N: 663 mg/L",
    destination="90% fertilizante",
    chemical_params=DEJETO_DE_CODORNAS_CHEMICAL_PARAMS,
    availability=DEJETO_DE_CODORNAS_AVAILABILITY,
    operational=DEJETO_DE_CODORNAS_OPERATIONAL,
    justification=DEJETO_DE_CODORNAS_JUSTIFICATION,
    scenarios=DEJETO_DE_CODORNAS_SCENARIOS,
    references=DEJETO_DE_CODORNAS_REFERENCES
)


# ============================================================================
# URBANO - RESÍDUOS SÓLIDOS URBANOS
