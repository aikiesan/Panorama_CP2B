"""
Database Update Script - PanoramaCP2B
Integrates validated residue data from Excel into Python dataclass files

Author: Claude Code
Date: October 20, 2025
Source: dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

EXCEL_PATH = r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx'
PROJECT_ROOT = Path(r'C:\Users\Lucas\Documents\CP2B\PanoramaCP2B')
DATA_DIR = PROJECT_ROOT / 'src' / 'data'

# ============================================================================
# PHASE 1: MAPPING & CODE MATCHING
# ============================================================================

# Manual mapping between Excel codes and Python file names
# Format: 'EXCEL_CODE': ('sector_folder', 'python_file.py', 'VARIABLE_NAME')
# Only including residues with GOOD data quality (6/6 complete fields)
RESIDUE_MAPPING = {
    # Cana-de-açúcar (1 complete sub-residue)
    'PALHA': ('agricultura', 'cana_palha.py', 'PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA'),

    # Citros (3 complete sub-residues - 100% validated)
    'BAGACO_CITROS': ('agricultura', 'bagaço_de_citros.py', 'BAGACO_DE_CITROS_DATA'),
    'CASCAS_CITROS': ('agricultura', 'cascas_de_citros.py', 'CASCAS_DE_CITROS_DATA'),
    'POLPA_CITROS': ('agricultura', 'bagaço_de_citros.py', 'POLPA_CITROS_DATA'),  # Separate variable

    # Milho (2 complete sub-residues)
    'PALHA_MILHO': ('agricultura', 'palha_de_milho.py', 'PALHA_DE_MILHO_DATA'),
    'SABUGO': ('agricultura', 'sabugo_de_milho.py', 'SABUGO_DE_MILHO_DATA'),

    # Soja (3 complete sub-residues - 100% validated)
    'PALHA_SOJA': ('agricultura', 'palha_de_soja.py', 'PALHA_DE_SOJA_DATA'),
    'CASCA_SOJA': ('agricultura', 'palha_de_soja.py', 'CASCA_SOJA_DATA'),  # Separate variable if needed
    'VAGEM_SOJA': ('agricultura', 'vagens_vazias.py', 'VAGENS_VAZIAS_DATA'),

    # Eucalipto (3 complete sub-residues - 100% validated)
    'CASCA_EUCALIPTO': ('agricultura', 'casca_de_eucalipto.py', 'CASCA_DE_EUCALIPTO_DATA'),
    'GALHOS_EUCALIPTO': ('agricultura', 'casca_de_eucalipto.py', 'GALHOS_EUCALIPTO_DATA'),
    'FOLHAS_EUCALIPTO': ('agricultura', 'casca_de_eucalipto.py', 'FOLHAS_EUCALIPTO_DATA'),
}

# ============================================================================
# PHASE 2: REFERENCE PARSER
# ============================================================================

def parse_reference_string(ref_string: str) -> Optional[Dict]:
    """
    Parse a single reference string into structured data.

    Example input:
    "ROQUE, A.P.; DIAS, R.S. et al. Title of paper. **Journal Name**, v. 71, n. 1-3,
     p. 243-249, 2007. Disponível em: <https://doi.org/10.1016/j.smallrumres.2006.07.004>."

    Returns:
        Dict with keys: authors, title, journal, year, doi, scopus_link
    """
    if pd.isna(ref_string) or not ref_string or ref_string.strip() == '':
        return None

    ref_string = ref_string.strip()

    # Initialize result
    result = {
        'authors': '',
        'title': '',
        'journal': '',
        'year': 0,
        'doi': '',
        'scopus_link': '',
        'relevance': 'High',  # Default for validated data
        'data_type': 'Literatura Científica',
        'key_findings': []
    }

    # Extract year (4 digits, possibly with .0 after it)
    year_match = re.search(r',\s*(19\d{2}|20\d{2})(?:\.0)?\.', ref_string)
    if year_match:
        result['year'] = int(year_match.group(1))

    # Extract DOI
    doi_match = re.search(r'(?:DOI:|doi:|https?://doi\.org/|<https?://doi\.org/)([^>\s]+)', ref_string, re.IGNORECASE)
    if doi_match:
        result['doi'] = doi_match.group(1).rstrip('>.')

    # Extract journal (text between ** ** markers)
    journal_match = re.search(r'\*\*([^*]+)\*\*', ref_string)
    if journal_match:
        result['journal'] = journal_match.group(1).strip()

        # Extract authors (everything before title, which is before journal)
        # Pattern: AUTHORS.. TITLE. **JOURNAL**
        before_journal = ref_string[:journal_match.start()].strip()

        # Find the last double period (..) which typically ends the author list
        author_end = before_journal.rfind('..')
        if author_end > 0:
            authors_part = before_journal[:author_end]
            title_part = before_journal[author_end+2:].strip()
            # Remove trailing period from title
            title_part = title_part.rstrip('.')
        else:
            # Fallback: split on first period after authors
            parts = before_journal.split('.', 1)
            if len(parts) == 2:
                authors_part = parts[0]
                title_part = parts[1].strip()
            else:
                authors_part = before_journal
                title_part = ""

        result['authors'] = authors_part.strip()
        result['title'] = title_part.strip()
    else:
        # No journal marker found - try basic parsing
        # Assume: AUTHORS. Title. Rest of citation.
        parts = ref_string.split('.')
        if len(parts) >= 2:
            result['authors'] = parts[0].strip()
            result['title'] = parts[1].strip()
        else:
            result['title'] = ref_string[:100] + '...' if len(ref_string) > 100 else ref_string

    # If title is still empty, use a truncated version of the string
    if not result['title']:
        result['title'] = ref_string[:100] + '...' if len(ref_string) > 100 else ref_string

    # Clean up extra spaces and normalize
    result['authors'] = ' '.join(result['authors'].split())
    result['title'] = ' '.join(result['title'].split())
    if result['journal']:
        result['journal'] = ' '.join(result['journal'].split())

    return result


def parse_all_references(row: pd.Series) -> List[Dict]:
    """
    Extract all references from a row's reference columns.

    Columns to check:
    - BMP_Referencias_Literatura
    - TS_Referencias_Literatura
    - VS_Referencias_Literatura
    - CN_Referencias_Literatura
    - CH4_CONTEUDO_Referencias_Literatura
    """
    all_refs = []
    seen_refs = set()  # To avoid duplicates

    ref_columns = [
        'BMP_Referencias_Literatura',
        'TS_Referencias_Literatura',
        'VS_Referencias_Literatura',
        'CN_Referencias_Literatura',
        'CH4_CONTEUDO_Referencias_Literatura'
    ]

    for col in ref_columns:
        if col not in row:
            continue

        ref_string = row[col]
        if pd.isna(ref_string) or not ref_string or ref_string.strip() == '':
            continue

        # Split by common separators (newlines, semicolons)
        # Some references may be concatenated
        ref_parts = re.split(r';\s*(?=[A-Z])|(?<=\.)\s+(?=[A-Z][A-Z])', str(ref_string))

        for ref_part in ref_parts:
            ref_part = ref_part.strip()
            if not ref_part:
                continue

            # Create a hash to detect duplicates
            ref_hash = ref_part[:50]  # Use first 50 chars as identifier
            if ref_hash in seen_refs:
                continue

            seen_refs.add(ref_hash)
            parsed = parse_reference_string(ref_part)
            if parsed and parsed['title']:
                all_refs.append(parsed)

    return all_refs


def format_references_as_python(references: List[Dict]) -> str:
    """
    Format parsed references as Python code for ScientificReference objects.
    """
    if not references:
        return "[]"

    ref_lines = ["["]
    for ref in references:
        ref_lines.append("        ScientificReference(")
        ref_lines.append(f"            title=\"{ref['title'].replace(chr(34), chr(39))}\",")
        ref_lines.append(f"            authors=\"{ref['authors'].replace(chr(34), chr(39))}\",")
        ref_lines.append(f"            year={ref['year']},")
        if ref['doi']:
            ref_lines.append(f"            doi=\"{ref['doi']}\",")
        if ref['journal']:
            ref_lines.append(f"            journal=\"{ref['journal'].replace(chr(34), chr(39))}\",")
        ref_lines.append(f"            relevance=\"{ref['relevance']}\",")
        ref_lines.append(f"            data_type=\"{ref['data_type']}\"")
        ref_lines.append("        ),")
    ref_lines.append("    ]")

    return "\n".join(ref_lines)


# ============================================================================
# PHASE 3: DATA TRANSFORMATION
# ============================================================================

def parse_resumo_literatura(resumo_str: str) -> Optional[Tuple[float, float, float]]:
    """
    Parse literature summary strings like:
    "Média: 250.5 | Min: 200.0 | Max: 300.0 (n=15)"

    Returns:
        Tuple of (min, mean, max) or None
    """
    if pd.isna(resumo_str) or not resumo_str:
        return None

    try:
        mean_match = re.search(r'M[ée]dia:\s*([\d.]+)', resumo_str)
        min_match = re.search(r'Min:\s*([\d.]+)', resumo_str)
        max_match = re.search(r'Max:\s*([\d.]+)', resumo_str)

        mean_val = float(mean_match.group(1)) if mean_match else None
        min_val = float(min_match.group(1)) if min_match else None
        max_val = float(max_match.group(1)) if max_match else None

        if mean_val is not None:
            return (min_val, mean_val, max_val)
    except:
        pass

    return None


def build_mapping_report():
    """Generate a report of which residues will be updated."""
    print("=" * 80)
    print("RESIDUE MAPPING REPORT")
    print("=" * 80)

    # Load Excel
    df_ag = pd.read_excel(EXCEL_PATH, sheet_name='AG_AGRICULTURA')
    df_pc = pd.read_excel(EXCEL_PATH, sheet_name='PC_PECUARIA')
    df_ur = pd.read_excel(EXCEL_PATH, sheet_name='UR_URBANO')
    df_in = pd.read_excel(EXCEL_PATH, sheet_name='IN_INDUSTRIAL')

    all_df = pd.concat([df_ag, df_pc, df_ur, df_in], ignore_index=True)
    excel_codes = set(all_df['Residuo_Codigo'].unique())

    print(f"\nTotal residues in Excel: {len(excel_codes)}")
    print(f"Total residues in mapping: {len(RESIDUE_MAPPING)}")

    # Matched residues
    matched = []
    for code in excel_codes:
        if code in RESIDUE_MAPPING:
            sector, filename, var = RESIDUE_MAPPING[code]
            filepath = DATA_DIR / sector / filename
            exists = filepath.exists()
            matched.append({
                'code': code,
                'file': filename,
                'exists': exists
            })

    print(f"\nResidues to be updated: {len(matched)}")
    print("\nMatched residues:")
    for item in matched:
        status = "[EXISTS]" if item['exists'] else "[NOT FOUND]"
        print(f"  {item['code']:20s} -> {item['file']:40s} {status}")

    # Not matched
    not_matched = excel_codes - set(RESIDUE_MAPPING.keys())
    if not_matched:
        print(f"\nResidues in Excel but NOT in mapping (will be skipped): {len(not_matched)}")
        for code in sorted(not_matched):
            print(f"  - {code}")

    return matched


# ============================================================================
# PHASE 4: FILE UPDATE LOGIC
# ============================================================================

def safe_float(val, default=None):
    """Safely convert to float, return default if NaN or invalid."""
    if pd.isna(val):
        return default
    try:
        return float(val)
    except:
        return default


def safe_str(val, default=""):
    """Safely convert to string, return default if NaN."""
    if pd.isna(val) or val is None:
        return default
    return str(val).strip()


def generate_updated_residue_code(row: pd.Series, references: List[Dict]) -> str:
    """
    Generate complete Python code for a ResidueData object from Excel row.

    Args:
        row: Pandas Series with all Excel columns
        references: List of parsed reference dicts

    Returns:
        String containing Python code for ResidueData definition
    """
    # Extract basic fields
    residue_name = safe_str(row.get('Residuo_Nome', ''), 'Unknown Residue')
    generation = safe_str(row.get('generation', ''))
    destination = safe_str(row.get('destination', ''))
    justification = safe_str(row.get('justification', ''))
    icon = safe_str(row.get('icon', '🌾'))

    # Chemical parameters
    bmp = safe_float(row.get('chemical_bmp'))
    bmp_unit = safe_str(row.get('chemical_bmp_unit'), 'L CH₄/kg VS')
    ts = safe_float(row.get('chemical_ts'))
    vs = safe_float(row.get('chemical_vs'))
    cn_ratio = safe_float(row.get('chemical_cn_ratio'))
    ch4_content = safe_float(row.get('chemical_ch4_content'))

    # Availability
    fc = safe_float(row.get('availability_fc'), 0.8)
    fcp = safe_float(row.get('availability_fcp'), 0.5)
    final_avail = safe_float(row.get('availability_final_availability'), 50.0)

    # Scenarios
    pessimista = safe_float(row.get('scenarios_pessimista'), 0.0)
    realista = safe_float(row.get('scenarios_realista'), 0.0)
    otimista = safe_float(row.get('scenarios_otimista'), 0.0)
    teorico = safe_float(row.get('scenarios_teorico'), 0.0)

    # Parse literature summaries for ranges
    bmp_resumo = parse_resumo_literatura(safe_str(row.get('BMP_Resumo_Literatura')))
    ts_resumo = parse_resumo_literatura(safe_str(row.get('TS_Resumo_Literatura')))
    vs_resumo = parse_resumo_literatura(safe_str(row.get('VS_Resumo_Literatura')))
    cn_resumo = parse_resumo_literatura(safe_str(row.get('CN_Resumo_Literatura')))
    ch4_resumo = parse_resumo_literatura(safe_str(row.get('CH4_CONTEUDO_Resumo_Literatura')))

    # Build code
    code_lines = []
    code_lines.append('"""')
    code_lines.append(f'{residue_name} - Validated Residue Data')
    code_lines.append('CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)')
    code_lines.append('')
    code_lines.append('Updated from validated database: dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx')
    code_lines.append(f'Update date: October 20, 2025')
    code_lines.append('"""')
    code_lines.append('')
    code_lines.append('from src.models.residue_models import (')
    code_lines.append('    ResidueData,')
    code_lines.append('    ChemicalParameters,')
    code_lines.append('    AvailabilityFactors,')
    code_lines.append('    OperationalParameters,')
    code_lines.append('    ScientificReference,')
    code_lines.append('    ParameterRange')
    code_lines.append(')')
    code_lines.append('')

    # Variable name (uppercase with underscores)
    var_name = residue_name.upper().replace(' ', '_').replace('-', '_').replace('Ç', 'C').replace('Ã', 'A')
    var_name = ''.join(c for c in var_name if c.isalnum() or c == '_') + '_DATA'

    code_lines.append(f'{var_name} = ResidueData(')
    code_lines.append(f'    name="{residue_name}",')
    code_lines.append(f'    category="Agricultura",  # TODO: Verify sector')
    code_lines.append(f'    icon="{icon}",')
    code_lines.append(f'    generation="{generation}",')
    code_lines.append(f'    destination="{destination}",')
    code_lines.append('')

    # Chemical parameters
    code_lines.append('    chemical_params=ChemicalParameters(')
    if bmp is not None:
        code_lines.append(f'        bmp={bmp},')
    else:
        code_lines.append('        bmp=0.0,  # TODO: Add BMP value')
    code_lines.append(f'        bmp_unit="{bmp_unit}",')
    if ts is not None:
        code_lines.append(f'        ts={ts},')
    else:
        code_lines.append('        ts=0.0,  # TODO: Add TS value')
    if vs is not None:
        code_lines.append(f'        vs={vs},')
    else:
        code_lines.append('        vs=0.0,  # TODO: Add VS value')
    code_lines.append('        vs_basis="% TS",')
    code_lines.append('        moisture=50.0,  # TODO: Add moisture value')
    if cn_ratio is not None:
        code_lines.append(f'        cn_ratio={cn_ratio},')
    if ch4_content is not None:
        code_lines.append(f'        ch4_content={ch4_content},')

    # Add ranges
    if bmp_resumo:
        min_v, mean_v, max_v = bmp_resumo
        code_lines.append('        bmp_range=ParameterRange(')
        if min_v: code_lines.append(f'            min={min_v},')
        code_lines.append(f'            mean={mean_v},')
        if max_v: code_lines.append(f'            max={max_v},')
        code_lines.append(f'            unit="{bmp_unit}"')
        code_lines.append('        ),')

    if ts_resumo:
        min_v, mean_v, max_v = ts_resumo
        code_lines.append('        ts_range=ParameterRange(')
        if min_v: code_lines.append(f'            min={min_v},')
        code_lines.append(f'            mean={mean_v},')
        if max_v: code_lines.append(f'            max={max_v},')
        code_lines.append('            unit="%"')
        code_lines.append('        ),')

    # TODO: Add VS, CN, CH4 ranges similarly

    code_lines.append('    ),')
    code_lines.append('')

    # Availability
    code_lines.append('    availability=AvailabilityFactors(')
    code_lines.append(f'        fc={fc},')
    code_lines.append(f'        fcp={fcp},')
    code_lines.append('        fs=1.0,  # TODO: Add FS value from validated data')
    code_lines.append('        fl=1.0,  # TODO: Add FL value from validated data')
    code_lines.append(f'        final_availability={final_avail}')
    code_lines.append('    ),')
    code_lines.append('')

    # Operational (placeholder)
    code_lines.append('    operational=OperationalParameters(')
    code_lines.append('        hrt="20-30 dias",')
    code_lines.append('        temperature="35-37°C (mesofílico)"')
    code_lines.append('    ),')
    code_lines.append('')

    # Justification
    code_lines.append(f'    justification="""')
    code_lines.append(f'    {justification}')
    code_lines.append('    """,')
    code_lines.append('')

    # Scenarios
    code_lines.append('    scenarios={')
    code_lines.append(f'        "Pessimista": {pessimista},')
    code_lines.append(f'        "Realista": {realista},')
    code_lines.append(f'        "Otimista": {otimista},')
    code_lines.append(f'        "Teórico (100%)": {teorico}')
    code_lines.append('    },')
    code_lines.append('')

    # References
    if references:
        code_lines.append('    references=[')
        for ref in references:
            code_lines.append('        ScientificReference(')
            # Escape quotes in strings
            title = ref['title'].replace('"', '\\"')
            authors = ref['authors'].replace('"', '\\"')
            journal = ref['journal'].replace('"', '\\"') if ref['journal'] else ''

            code_lines.append(f'            title="{title}",')
            code_lines.append(f'            authors="{authors}",')
            code_lines.append(f'            year={ref["year"]},')
            if ref['doi']:
                code_lines.append(f'            doi="{ref["doi"]}",')
            if journal:
                code_lines.append(f'            journal="{journal}",')
            code_lines.append(f'            relevance="{ref["relevance"]}",')
            code_lines.append(f'            data_type="{ref["data_type"]}"')
            code_lines.append('        ),')
        code_lines.append('    ]')
    else:
        code_lines.append('    references=[]')

    code_lines.append(')')
    code_lines.append('')

    return '\n'.join(code_lines)


def update_single_residue(excel_code: str, sector: str, filename: str, var_name: str):
    """
    Update a single residue file from Excel data.

    Args:
        excel_code: Residuo_Codigo from Excel
        sector: Sector folder name
        filename: Python filename
        var_name: Variable name in Python file
    """
    # Load all Excel sheets
    df_ag = pd.read_excel(EXCEL_PATH, sheet_name='AG_AGRICULTURA')
    df_pc = pd.read_excel(EXCEL_PATH, sheet_name='PC_PECUARIA')
    df_ur = pd.read_excel(EXCEL_PATH, sheet_name='UR_URBANO')
    df_in = pd.read_excel(EXCEL_PATH, sheet_name='IN_INDUSTRIAL')

    all_df = pd.concat([df_ag, df_pc, df_ur, df_in], ignore_index=True)

    # Find the row
    rows = all_df[all_df['Residuo_Codigo'] == excel_code]
    if len(rows) == 0:
        print(f"  [SKIP] {excel_code} not found in Excel")
        return False

    row = rows.iloc[0]

    # Parse references
    references = parse_all_references(row)

    # Generate code
    updated_code = generate_updated_residue_code(row, references)

    # Write to file
    filepath = DATA_DIR / sector / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_code)

    print(f"  [UPDATED] {filename} ({len(references)} references)")
    return True


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("PanoramaCP2B Database Update Script")
    print("=" * 80)

    # Phase 1: Generate mapping report
    matched_residues = build_mapping_report()

    print("\n" + "=" * 80)
    print("Starting File Updates")
    print("=" * 80)

    updated_count = 0
    for code, (sector, filename, var_name) in RESIDUE_MAPPING.items():
        print(f"\nProcessing {code}...")
        if update_single_residue(code, sector, filename, var_name):
            updated_count += 1

    print("\n" + "=" * 80)
    print(f"Update Complete: {updated_count} files updated")
    print("=" * 80)
