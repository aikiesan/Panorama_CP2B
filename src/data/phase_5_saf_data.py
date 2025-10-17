"""
Phase 5 SAF (Surplus Availability Factor) Validation Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Maps validated SAF data from cp2b_analise_fatores_residuos.md to residues
Format: {residue_name: {saf_real, priority_tier, fc, fcp, fs, fl, rank, culture, recommendation}}
"""

# Complete SAF ranking from cp2b_analise_fatores_residuos.md
# Sorted by SAF_REAL (descending)
SAF_VALIDATION_DATA = {
    # ===== RANK 1: EXCEPCIONAL (SAF > 30%) =====
    "Bagaço de cana": {
        "saf_real": 80.75,
        "priority_tier": "EXCEPCIONAL",
        "fc": 0.95,
        "fcp": 1.0,
        "fs": 1.0,
        "fl": 1.0,
        "bmp": 85,
        "saf_rank": 1,
        "culture_group": "Cana-de-Açúcar",
        "recommendation": "JÁ IMPLEMENTADO - Potencial residual limitado (10-15% complementar)"
    },
    "Soro de queijo": {
        "saf_real": 30.40,
        "priority_tier": "EXCELENTE",
        "fc": 0.95,
        "fcp": 1.5,
        "fs": 1.0,
        "fl": 0.80,
        "bmp": 500,
        "saf_rank": 2,
        "culture_group": "Laticínios",
        "recommendation": "MÁXIMA PRIORIDADE - Melhor oportunidade (exceto bagaço cana)"
    },

    # ===== RANK 3-8: EXCELENTE/BOM (SAF > 8%) =====
    "Torta de Filtro (Filter Cake)": {
        "saf_real": 12.88,
        "priority_tier": "MUITO BOM",
        "fc": 0.90,
        "fcp": 2.5,
        "fs": 0.95,
        "fl": 0.85,
        "bmp": 40,
        "saf_rank": 3,
        "culture_group": "Cana-de-Açúcar",
        "recommendation": "Integrar com bagaço em usinas existentes"
    },
    "Mucilagem fermentada": {
        "saf_real": 11.90,
        "priority_tier": "MUITO BOM",
        "fc": 0.85,
        "fcp": 1.5,
        "fs": 0.70,
        "fl": 0.75,
        "bmp": 350,
        "saf_rank": 4,
        "culture_group": "Café",
        "recommendation": "OPORTUNIDADE REAL - Contactar beneficiadores (sazonalidade crítica 4 meses/ano)"
    },
    "Vinhaça de Cana-de-açúcar": {
        "saf_real": 10.26,
        "priority_tier": "BOM",
        "fc": 0.80,
        "fcp": 1.0,
        "fs": 0.90,
        "fl": 0.95,
        "bmp": 15,
        "saf_rank": 5,
        "culture_group": "Cana-de-Açúcar",
        "recommendation": "Volume elevado; fertirrigação já estabelecida"
    },
    "RSU urbano": {
        "saf_real": 9.88,
        "priority_tier": "BOM",
        "fc": 0.65,
        "fcp": 2.5,
        "fs": 1.0,
        "fl": 0.95,
        "bmp": 40,
        "saf_rank": 6,
        "culture_group": "Urbano",
        "recommendation": "Potencial em RMSP; coleta seletiva necessária"
    },
    "Resíduo alimentício": {
        "saf_real": 9.33,
        "priority_tier": "BOM",
        "fc": 0.70,
        "fcp": 3.0,
        "fs": 1.0,
        "fl": 0.80,
        "bmp": 400,
        "saf_rank": 7,
        "culture_group": "Urbano",
        "recommendation": "Oportunidade real em restaurantes/indústria"
    },
    "Cama de frango": {
        "saf_real": 8.67,
        "priority_tier": "BOM",
        "fc": 0.85,
        "fcp": 3.0,
        "fs": 1.0,
        "fl": 0.90,
        "bmp": 230,
        "saf_rank": 8,
        "culture_group": "Avicultura",
        "recommendation": "PRIORIDADE MÉDIA-ALTA - Sistema bem estabelecido"
    },

    # ===== RANK 9-15: RAZOÁVEL (SAF 4-8%) =====
    "Bagaço de malte": {
        "saf_real": 6.69,
        "priority_tier": "RAZOÁVEL",
        "fc": 0.90,
        "fcp": 4.0,
        "fs": 1.0,
        "fl": 0.85,
        "bmp": 115,
        "saf_rank": 9,
        "culture_group": "Cervejaria",
        "recommendation": "Parcerias com grandes cervejarias (RMSP)"
    },
    "Dejetos de postura": {
        "saf_real": 5.83,
        "priority_tier": "RAZOÁVEL",
        "fc": 0.80,
        "fcp": 3.5,
        "fs": 1.0,
        "fl": 0.85,
        "bmp": 330,
        "saf_rank": 10,
        "culture_group": "Avicultura",
        "recommendation": "Co-digestão com cama de frango"
    },
    "Conteúdo ruminal": {
        "saf_real": 5.46,
        "priority_tier": "REGULAR",
        "fc": 0.85,
        "fcp": 3.5,
        "fs": 1.0,
        "fl": 0.75,
        "bmp": 160,
        "saf_rank": 11,
        "culture_group": "Frigorífico",
        "recommendation": "Casos específicos em grandes frigoríficos"
    },
    "Lodo de lagoas": {
        "saf_real": 4.76,
        "priority_tier": "REGULAR",
        "fc": 0.70,
        "fcp": 2.5,
        "fs": 1.0,
        "fl": 0.85,
        "bmp": 350,
        "saf_rank": 12,
        "culture_group": "Suinocultura",
        "recommendation": "Co-digestão sinérgica com dejetos frescos"
    },
    "Cama de curral": {
        "saf_real": 4.25,
        "priority_tier": "REGULAR",
        "fc": 0.80,
        "fcp": 4.0,
        "fs": 1.0,
        "fl": 0.85,
        "bmp": 250,
        "saf_rank": 13,
        "culture_group": "Bovinocultura",
        "recommendation": "Apenas em confinamentos estabelecidos"
    },
    "Lodo tanques": {
        "saf_real": 4.10,
        "priority_tier": "REGULAR",
        "fc": 0.70,
        "fcp": 2.5,
        "fs": 0.90,
        "fl": 0.65,
        "bmp": 25,
        "saf_rank": 14,
        "culture_group": "Piscicultura",
        "recommendation": "Agregar múltiplas unidades (Vale Ribeira)"
    },
    "Ração não consumida": {
        "saf_real": 3.78,
        "priority_tier": "REGULAR",
        "fc": 0.60,
        "fcp": 2.0,
        "fs": 0.90,
        "fl": 0.70,
        "bmp": 375,
        "saf_rank": 15,
        "culture_group": "Piscicultura",
        "recommendation": "Agregar múltiplas unidades (Vale Ribeira)"
    },

    # ===== RANK 16-26: BAIXO/CRÍTICO (SAF 1-4%) =====
    "Dejetos suínos": {
        "saf_real": 3.67,
        "priority_tier": "REGULAR",
        "fc": 0.80,
        "fcp": 3.0,
        "fs": 1.0,
        "fl": 0.90,
        "bmp": 550,
        "saf_rank": 16,
        "culture_group": "Suinocultura",
        "recommendation": "INTEGRAR com lodo de lagoas em complexos"
    },
    "Cascas de citros": {
        "saf_real": 3.26,
        "priority_tier": "REGULAR",
        "fc": 0.85,
        "fcp": 5.2,
        "fs": 0.80,
        "fl": 0.85,
        "bmp": 30,
        "saf_rank": 17,
        "culture_group": "Citros",
        "recommendation": "Análise caso-a-caso; pré-tratamento (limoneno) necessário"
    },
    "Casca de café (pergaminho)": {
        "saf_real": 2.67,
        "priority_tier": "BAIXO",
        "fc": 0.80,
        "fcp": 4.5,
        "fs": 0.75,
        "fl": 0.80,
        "bmp": 25,
        "saf_rank": 18,
        "culture_group": "Café",
        "recommendation": "Competição moderada-alta; viabilidade limitada"
    },
    "Dejetos bovinos (confinamento)": {
        "saf_real": 2.55,
        "priority_tier": "BAIXO",
        "fc": 0.75,
        "fcp": 5.0,
        "fs": 1.0,
        "fl": 0.85,
        "bmp": 20,
        "saf_rank": 19,
        "culture_group": "Bovinocultura",
        "recommendation": "Complemento em complexos integrados"
    },
    "Bagaço de citros": {
        "saf_real": 2.33,
        "priority_tier": "BAIXO",
        "fc": 0.90,
        "fcp": 5.2,
        "fs": 0.80,
        "fl": 0.85,
        "bmp": 20,
        "saf_rank": 20,
        "culture_group": "Citros",
        "recommendation": "Baixa prioridade; competição forte com ração"
    },
    "Sabugo de milho": {
        "saf_real": 2.25,
        "priority_tier": "BAIXO",
        "fc": 0.75,
        "fcp": 6.0,
        "fs": 0.80,
        "fl": 0.75,
        "bmp": 30,
        "saf_rank": 21,
        "culture_group": "Milho",
        "recommendation": "Potencial limitado; co-digestão com nitrogenados"
    },
    "Palha de milho": {
        "saf_real": 1.96,
        "priority_tier": "BAIXO",
        "fc": 0.70,
        "fcp": 8.5,
        "fs": 0.80,
        "fl": 0.80,
        "bmp": 35,
        "saf_rank": 22,
        "culture_group": "Milho",
        "recommendation": "Potencial limitado; alto C/N requer co-digestão obrigatória"
    },
    "Poda urbana": {
        "saf_real": 1.53,
        "priority_tier": "CRÍTICO",
        "fc": 0.75,
        "fcp": 5.0,
        "fs": 0.80,
        "fl": 0.85,
        "bmp": 15,
        "saf_rank": 23,
        "culture_group": "Urbano",
        "recommendation": "BMP mínimo (15); competição compostagem - NÃO PRIORIZAR"
    },
    "Vagens vazias": {
        "saf_real": 1.37,
        "priority_tier": "CRÍTICO",
        "fc": 0.70,
        "fcp": 7.5,
        "fs": 0.75,
        "fl": 0.70,
        "bmp": 25,
        "saf_rank": 24,
        "culture_group": "Soja",
        "recommendation": "NÃO PRIORIZAR - mesmos fatores que palha"
    },
    "Palha de soja": {
        "saf_real": 1.36,
        "priority_tier": "CRÍTICO",
        "fc": 0.65,
        "fcp": 9.0,
        "fs": 0.75,
        "fl": 0.75,
        "bmp": 30,
        "saf_rank": 25,
        "culture_group": "Soja",
        "recommendation": "NÃO PRIORIZAR - fixação N solo é mais crítica"
    },
    "Palha de Cana-de-açúcar (Palhiço)": {
        "saf_real": 1.18,
        "priority_tier": "CRÍTICO",
        "fc": 0.75,
        "fcp": 13.7,
        "fs": 0.85,
        "fl": 0.85,
        "bmp": 30,
        "saf_rank": 26,
        "culture_group": "Cana-de-Açúcar",
        "recommendation": "NÃO PRIORIZAR - competição impossível (60% solo + 20% etanol 2G + 10% ração)"
    },

    # ===== RANK 27-29: INVIÁVEL (SAF < 1%) =====
    "Dejetos de pastagem": {
        "saf_real": 0.99,
        "priority_tier": "INVIÁVEL",
        "fc": 0.70,
        "fcp": 8.5,
        "fs": 1.0,
        "fl": 0.80,
        "bmp": 15,
        "saf_rank": 27,
        "culture_group": "Bovinocultura",
        "recommendation": "NÃO COLETAR - dispersão impossível"
    },
    "Casca de eucalipto": {
        "saf_real": 0.95,
        "priority_tier": "INVIÁVEL",
        "fc": 0.60,
        "fcp": 6.0,
        "fs": 0.85,
        "fl": 0.70,
        "bmp": 100,
        "saf_rank": 28,
        "culture_group": "Silvicultura",
        "recommendation": "NÃO PRIORIZAR - biomassa energética estabelecida"
    },
    "Resíduos de colheita": {
        "saf_real": 0.74,
        "priority_tier": "INVIÁVEL",
        "fc": 0.55,
        "fcp": 7.0,
        "fs": 0.85,
        "fl": 0.65,
        "bmp": 90,
        "saf_rank": 29,
        "culture_group": "Silvicultura",
        "recommendation": "NÃO COLETAR - deixado no solo é estratégico"
    },
}

def get_saf_data(residue_name: str) -> dict:
    """
    Get SAF validation data for a residue.

    Args:
        residue_name: Name of the residue

    Returns:
        Dictionary with SAF data or empty dict if not found
    """
    return SAF_VALIDATION_DATA.get(residue_name, {})

def apply_saf_to_residue(residue_data, residue_name: str) -> None:
    """
    Apply SAF validation data to a ResidueData object.
    Modifies the object in-place.

    Args:
        residue_data: ResidueData object to update
        residue_name: Name of the residue
    """
    saf_data = get_saf_data(residue_name)
    if not saf_data:
        return  # Residue not in SAF analysis yet

    # Apply Phase 5 fields
    residue_data.saf_real = saf_data.get("saf_real")
    residue_data.priority_tier = saf_data.get("priority_tier")
    residue_data.saf_rank = saf_data.get("saf_rank")
    residue_data.recommendation = saf_data.get("recommendation")
    residue_data.fc_value = saf_data.get("fc")
    residue_data.fcp_value = saf_data.get("fcp")
    residue_data.fs_value = saf_data.get("fs")
    residue_data.fl_value = saf_data.get("fl")
    residue_data.culture_group = saf_data.get("culture_group")

def get_residues_by_priority(priority_tier: str) -> list:
    """
    Get all residues with a specific priority tier.

    Args:
        priority_tier: One of "EXCEPCIONAL", "EXCELENTE", "BOM", "REGULAR", "BAIXO", "CRÍTICO", "INVIÁVEL"

    Returns:
        List of residue names
    """
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("priority_tier") == priority_tier
    ]

def get_residues_by_culture(culture_group: str) -> list:
    """
    Get all residues from a specific culture group.

    Args:
        culture_group: Culture name (e.g., "Cana-de-Açúcar", "Café")

    Returns:
        List of residue names
    """
    return [
        name for name, data in SAF_VALIDATION_DATA.items()
        if data.get("culture_group") == culture_group
    ]

if __name__ == "__main__":
    # Test
    print("SAF Validation Data Loaded")
    print(f"Total residues: {len(SAF_VALIDATION_DATA)}")
    print(f"\nExcepcional (SAF > 30%): {get_residues_by_priority('EXCEPCIONAL')}")
    print(f"Cana-de-Açúcar group: {get_residues_by_culture('Cana-de-Açúcar')}")
