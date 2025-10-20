"""
Casca de café (pergaminho) - Residue Data
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

CASCA_DE_CAFÉ_PERGAMINHO_DATA = ResidueData(
    name="Casca de café (pergaminho)",
    category="Agricultura",
    icon="☕",
    generation="0,18 kg/kg café beneficiado",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp=0.12,
        bmp_unit="m³ CH₄/kg MS",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture=50.0,
        cn_ratio=20.0,
        ch4_content=60.0,

        # Ranges from CSV
        bmp_range=ParameterRange(
            min=150.0,
            mean=175.0,
            max=200.0,
            unit="mL CH₄/g VS"
        ) if True else None,
        cn_ratio_range=ParameterRange(
            min=15.0,
            mean=20.0,
            max=25.0
        ) if True else None,
        ch4_content_range=ParameterRange(
            min=55.0,
            mean=60.0,
            max=65.0,
            unit="%"
        ) if True else None,
    ),

    availability=AvailabilityFactors(
        fc=0.5,  # TODO: Add actual availability factors
        fcp=0.15,
        fs=1.0,
        fl=1.0,
        final_availability=0.4250
    ),

    operational=OperationalParameters(
        hrt="35 dias" if True else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min=30.0,
            mean=35.0,
            max=40.0,
            unit="dias"
        ) if True else None
    ),

    justification=f"""
    **Casca de café (pergaminho)**

    **Geração:** 0,18 kg/kg café beneficiado
    **Sazonalidade:** Maio-Setembro
    **Estado Físico:** Sólido
    **Pré-tratamento:** Trituração
    **Região Concentrada:** Sul SP, Mogiana

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={
        "Pessimista": 0.0,
        "Realista": 0.0,
        "Otimista": 0.0,
        "Teórico (100%)": 1.0
    },

    references=[
        ScientificReference(
            title="CZEKAŁA, Wojciech et al. Waste-to-energy: Biogas potential of waste from coffee production and consumption. Energy, v. 276, 127604, 2023",
            authors="CZEKAŁA, Wojciech et al.",
            year=2023,
            doi="10.1016/j.energy.2023.127604",
            scopus_link="https://doi.org/10.1016/j.energy.2023.127604",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="PAES, Juliana L. et al. Biogas production by anaerobic digestion of coffee husks and cattle manure. Engenharia Agrícola, v. 43, e20220126, 2023",
            authors="PAES, Juliana L. et al.",
            year=2023,
            doi="10.1590/1809-4430-Eng.Agric.v43nepe20220126/2023",
            scopus_link="https://doi.org/10.1590/1809-4430-Eng.Agric.v43nepe20220126/2023",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="PASSOS, Fabiana et al. Anaerobic co-digestion of coffee husks and microalgal biomass... Bioresource Technology, v. 253, p. 49-54, 2018",
            authors="PASSOS, Fabiana et al.",
            year=2018,
            doi="10.1016/j.biortech.2017.12.045",
            scopus_link="https://doi.org/10.1016/j.biortech.2017.12.045",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="TEIXEIRA, Roberta Arléu et al. Biochemical Methane Potential of Spent Coffee Grounds... BioEnergy Research, v. 17, p. 1133-1145, 2021",
            authors="TEIXEIRA, Roberta Arléu et al.",
            year=2021,
            doi="10.1007/s12155-020-10240-y",
            scopus_link="https://doi.org/10.1007/s12155-020-10240-y",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="DU, Nan et al. Study on the biogas potential of anaerobic digestion of coffee husks... Waste Management & Research, v. 39, n. 2, p. 273-280, 2021",
            authors="DU, Nan et al.",
            year=2021,
            doi="10.1177/0734242X20939619",
            scopus_link="https://doi.org/10.1177/0734242X20939619",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="RODRIGUES, Caroline Varella et al. Towards a circular bioeconomy to produce methane... Chemosphere, v. 351, 141177, 2024",
            authors="RODRIGUES, Caroline Varella et al.",
            year=2024,
            doi="10.1016/j.chemosphere.2024.141177",
            scopus_link="https://doi.org/10.1016/j.chemosphere.2024.141177",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="FERNANDES, Matheus Augusto de Oliveira et al. LCA-based carbon footprint analysis... Renewable and Sustainable Energy Reviews, v. 189, 113967, 2025",
            authors="FERNANDES, Matheus Augusto de Oliveira et al.",
            year=2025,
            doi="10.1016/j.rser.2023.113967",
            scopus_link="https://doi.org/10.1016/j.rser.2023.113967",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="KIM, Danbee; CHOI, Jaewoo; LEE, Changsoo. Enhanced methane production with co-feeding spent coffee grounds... Scientific Reports, v. 14, 3990, 2024",
            authors="KIM, Danbee; CHOI, Jaewoo; LEE, Changsoo",
            year=2024,
            doi="10.1038/s41598-024-54411-0",
            scopus_link="https://doi.org/10.1038/s41598-024-54411-0",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="PRADO, Maria Angélica Cardoso do; CAMPOS, Carlos Magno Moreira de. Estudo da variação da concentração de metano no biogás... Coffee Science, v. 5, n. 1, p. 87-98, 2010",
            authors="PRADO, Maria Angélica Cardoso do; CAMPOS, Carlos Magno Moreira de",
            year=2010,
            doi="10.25186/cs.v5i1.213",
            scopus_link="https://doi.org/10.25186/cs.v5i1.213",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="ZOCA, Samuel Menegatti et al. Coffee processing residues as a soil potassium amendment... International Journal of Recycling of Organic Waste in Agriculture, v. 3, n. 4, p. 155-165, 2014",
            authors="ZOCA, Samuel Menegatti et al.",
            year=2014,
            doi="10.1007/s40093-014-0078-7",
            scopus_link="https://doi.org/10.1007/s40093-014-0078-7",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="SILVA, Cintia Caroline Gouveia da et al. Coffee waste as an eco-friendly and low-cost alternative for biochar production... Bragantia, v. 80, e2121, 2021",
            authors="SILVA, Cintia Caroline Gouveia da et al.",
            year=2021,
            doi="10.1590/1678-4499.20210004",
            scopus_link="https://doi.org/10.1590/1678-4499.20210004",
            relevance="High",
            data_type="Literatura Científica"
        ),
        ScientificReference(
            title="BUDIYONO, Budiyono; SYAICHURROZI, Ignasius; SUMARDIONO, Siswo. Effect of Pretreatment and C/N Ratio in Anaerobic Digestion... International Journal of Renewable Energy Development, v. 12, n. 1, p. 24-",
            authors="BUDIYONO, Budiyono; SYAICHURROZI, Ignasius; SUMARDIONO, Siswo",
            year=2023,
            doi="10.14710/ijred.2023.49298",
            scopus_link="https://doi.org/10.14710/ijred.2023.49298",
            relevance="High",
            data_type="Literatura Científica"
        ),
    ]
)
