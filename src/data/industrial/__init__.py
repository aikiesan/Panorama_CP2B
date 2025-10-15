"""
Industrial Sector Registry
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Register all industrial residues
Currently: Placeholders for future implementation
"""

# Registry of all industrial residues (empty for now)
INDUSTRIAL_RESIDUES = {}

# Sector metadata
INDUSTRIAL_SECTOR_INFO = {
    "name": "Industrial",
    "icon": "🏭",
    "description": "Efluentes e resíduos industriais",
    "color": "#8b5cf6",
    "gradient": "linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%)",
    "border_color": "#8b5cf6",
    "residues": list(INDUSTRIAL_RESIDUES.keys())  # Empty list
}

__all__ = [
    'INDUSTRIAL_RESIDUES',
    'INDUSTRIAL_SECTOR_INFO',
]
