"""
RPO - Poda Urbana - Placeholder
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only RPO - Poda Urbana data (placeholder)
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# RPO - PODA URBANA (PLACEHOLDER)
# ============================================================================

RPO_CHEMICAL_PARAMS = ChemicalParameters(
    bmp=75.0,
    bmp_unit="Estimativa preliminar | Aguardando estudos específicos",
    ts=50.0,
    vs=80.0,
    vs_basis="Estimativa - alta lignina",
    moisture=50.0,
    cn_ratio=40.0,
    ph=None,
    ch4_content=55.0
)

RPO_AVAILABILITY = AvailabilityFactors(
    fc=0.7,
    fcp=0.3,
    fs=0.8,
    fl=0.9,
    final_availability=35.0
)

RPO_OPERATIONAL = OperationalParameters(
    hrt="40-60 dias",
    temperature="35-40°C mesofílica",
    reactor_type="CSTR, pré-tratamento recomendado",
    olr="Dados não disponíveis"
)

RPO_JUSTIFICATION = """
**⚠️ DADOS PRELIMINARES - AGUARDANDO VALIDAÇÃO**

RPO mencionado em estudos como parte de GFW (Garden Food Waste) mas sem caracterização específica.
Necessário: estudos BMP dedicados, análise de sazonalidade, avaliação de pré-tratamentos.
"""

RPO_SCENARIOS = {
    "Pessimista": 50.0,
    "Realista": 100.0,
    "Otimista": 150.0,
    "Teórico (100%)": 200.0,
}

RPO_REFERENCES = [
    ScientificReference(
        title="RPO mencionado como fração de RSU mas sem estudos dedicados",
        authors="Diversos",
        year=2024,
        doi=None,
        scopus_link=None,
        journal="Observação consolidada",
        relevance="Low",
        key_findings=[
            "GFW = 20% do OFMSW em Campinas",
            "Necessário: estudos BMP específicos"
        ]
    ),
]

RPO_DATA = ResidueData(
    name="RPO - Poda Urbana",
    category="Urbano",
    icon="🌳",
    generation="Dados em coleta | Estimativa: 20% da fração orgânica RSU",
    destination="A definir - aguardando estudos",
    chemical_params=RPO_CHEMICAL_PARAMS,
    availability=RPO_AVAILABILITY,
    operational=RPO_OPERATIONAL,
    justification=RPO_JUSTIFICATION,
    scenarios=RPO_SCENARIOS,
    references=RPO_REFERENCES
)
