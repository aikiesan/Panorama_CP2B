"""
Migration Script: Split research_data.py into SOLID architecture
Extracts each residue into its own focused file
"""

import re
from pathlib import Path

# Residue definitions and their target locations
RESIDUES = {
    'DEJETO_DE_AVES_CAMA_DE_FRANGO': {
        'target': 'src/data/pecuaria/avicultura_frango.py',
        'name': 'Dejeto de Aves (Cama de Frango)',
        'start_line': 173,  # Line where DEJETO_DE_AVES starts
        'end_line': 360,    # Approximate end (before next section)
    },
    'DEJETO_DE_CODORNAS': {
        'target': 'src/data/pecuaria/avicultura_codornas.py',
        'name': 'Dejeto de Codornas',
        'start_line': 1330,
        'end_line': 1410,
    },
    'DEJETOS_DE_BOVINOS': {
        'target': 'src/data/pecuaria/bovinocultura.py',
        'name': 'Dejetos de Bovinos (Leite + Corte)',
        'start_line': 362,
        'end_line': 577,
    },
    'DEJETOS_DE_SUINOS': {
        'target': 'src/data/pecuaria/suinocultura.py',
        'name': 'Dejetos de Suínos',
        'start_line': 1135,
        'end_line': 1328,
    },
    'PALHA_DE_CANA': {
        'target': 'src/data/agricultura/cana_palha.py',
        'name': 'Palha de Cana-de-açúcar (Palhiço)',
        'start_line': 796,
        'end_line': 1027,
    },
    'TORTA_DE_FILTRO': {
        'target': 'src/data/agricultura/cana_torta.py',
        'name': 'Torta de Filtro (Filter Cake)',
        'start_line': 1029,
        'end_line': 1134,
    },
    'RSU': {
        'target': 'src/data/urbano/rsu.py',
        'name': 'RSU - Resíduo Sólido Urbano',
        'start_line': 1412,
        'end_line': 1600,
    },
    'RPO': {
        'target': 'src/data/urbano/rpo.py',
        'name': 'RPO - Poda Urbana',
        'start_line': 1602,
        'end_line': 1720,
    },
    'LODO_ETE': {
        'target': 'src/data/urbano/lodo.py',
        'name': 'Lodo de Esgoto (ETE)',
        'start_line': 1530,
        'end_line': 1735,
    },
}


def extract_residue(source_file: str, start_line: int, end_line: int, target_file: str, residue_name: str):
    """Extract residue data from source and write to target file"""

    # Read source
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract relevant section
    section = lines[start_line-1:end_line]

    # Create header
    header = f'''"""
{residue_name} - Validated Research Data
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Single Responsibility: Contains only {residue_name} data and references
"""

from src.models.residue_models import (
    ChemicalParameters,
    AvailabilityFactors,
    OperationalParameters,
    ScientificReference,
    ResidueData
)


# ============================================================================
# {residue_name.upper()}
# ============================================================================

'''

    # Write to target
    target_path = Path(target_file)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.writelines(section)

    print(f"Created: {target_file} ({len(section)} lines)")


if __name__ == "__main__":
    source = "src/research_data.py"

    print("Starting migration...")
    print(f"Source: {source}\n")

    for key, config in RESIDUES.items():
        extract_residue(
            source,
            config['start_line'],
            config['end_line'],
            config['target'],
            config['name']
        )

    print("\nMigration complete!")
    print(f"Created {len(RESIDUES)} residue files")
