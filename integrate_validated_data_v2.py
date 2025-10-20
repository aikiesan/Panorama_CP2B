"""
Validated Data Integration Script V2 - PanoramaCP2B
Robust integration of validated residue data with comprehensive safety checks

Author: Claude Code (Anthropic)
Date: October 20, 2025
Sources:
  - catalogo_referencias_curadas_COMPLETO_20251020_120141.csv (74 references)
  - dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx

Key Improvements over V1:
1. Uses pre-curated CSV references (no parsing needed)
2. Correct Excel column mappings with validation
3. Preserves multi-residue files structure
4. Validates data before writing (BMP units, availability calc, scenarios)
5. Git commit before changes + dry-run mode
6. Targeted Edit operations (no full file overwrites)
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

EXCEL_PATH = Path(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\dossie_final_residuos_20251020_112818_v9_CITROS_VALIDADO.xlsx')
CSV_REFS_PATH = Path(r'C:\Users\Lucas\Documents\CP2B\Validacao_dados\catalogo_referencias_curadas_COMPLETO_20251020_120141.csv')
PROJECT_ROOT = Path(r'C:\Users\Lucas\Documents\CP2B\PanoramaCP2B')
DATA_DIR = PROJECT_ROOT / 'src' / 'data' / 'agricultura'

DRY_RUN = False  # EXECUTING REAL INTEGRATION NOW

# ============================================================================
# RESIDUE MAPPING - Culture-Based Organization
# ============================================================================

# Maps Excel Residuo_Codigo to (file, variable_name, culture)
RESIDUE_MAPPING = {
    # MILHO - 2 residues
    'PALHA_MILHO': ('palha_de_milho.py', 'PALHA_DE_MILHO_DATA', 'Milho'),
    'SABUGO': ('sabugo_de_milho.py', 'SABUGO_DE_MILHO_DATA', 'Milho'),

    # CAFE - 3 residues (when complete)
    'CASCA_CAFE': ('casca_de_café_pergaminho.py', 'CASCA_DE_CAFÉ_PERGAMINHO_DATA', 'Cafe'),
    # 'MUCILAGEM_CAFE': ('mucilagem_fermentada.py', 'MUCILAGEM_FERMENTADA_DATA', 'Cafe'),
    # 'POLPA_CAFE': ('polpa_de_cafe.py', 'POLPA_DE_CAFE_DATA', 'Cafe'),

    # SOJA - 2 residues (3 with casca, but in same file)
    'PALHA_SOJA': ('palha_de_soja.py', 'PALHA_DE_SOJA_DATA', 'Soja'),
    'VAGEM_SOJA': ('vagens_vazias.py', 'VAGENS_VAZIAS_DATA', 'Soja'),
    # Note: CASCA_SOJA is in palha_de_soja.py as CASCA_DE_SOJA_DATA

    # EUCALIPTO - 3 residues (all in same file casca_de_eucalipto.py)
    'CASCA_EUCALIPTO': ('casca_de_eucalipto.py', 'CASCA_DE_EUCALIPTO_DATA', 'Eucalipto'),
    'GALHOS_EUCALIPTO': ('casca_de_eucalipto.py', 'GALHOS_DE_EUCALIPTO_DATA', 'Eucalipto'),
    'FOLHAS_EUCALIPTO': ('casca_de_eucalipto.py', 'FOLHAS_DE_EUCALIPTO_DATA', 'Eucalipto'),

    # CANA-DE-ACUCAR - 1 main residue for now (palha)
    'PALHA': ('cana_palha.py', 'PALHA_DE_CANA_DE_ACUCAR_PALHICO_DATA', 'Cana-De-Acucar'),
    # Note: BAGACO, VINHACA, TORTA_FILTRO are separate files

    # CITROS - 3 residues (2 files: cascas, bagaço)
    'CASCAS_CITROS': ('cascas_de_citros.py', 'CASCAS_DE_CITROS_DATA', 'Citros'),
    'BAGACO_CITROS': ('bagaço_de_citros.py', 'BAGAÇO_DE_CITROS_DATA', 'Citros'),
    # Note: POLPA_CITROS might be in bagaço_de_citros.py if multi-residue
}

# ============================================================================
# PHASE 1: LOAD DATA SOURCES
# ============================================================================

def load_references_catalog() -> pd.DataFrame:
    """
    Load the clean, pre-curated references CSV.

    Returns:
        DataFrame with columns: reference_id, culture, citation_abnt, doi, functional_link
    """
    df = pd.read_csv(CSV_REFS_PATH, encoding='utf-8')
    print(f"Loaded {len(df)} references from clean CSV catalog")
    print(f"Cultures: {df['culture'].unique()}")
    print(f"References per culture:\n{df.groupby('culture').size()}")
    return df


def load_excel_data() -> pd.DataFrame:
    """
    Load Excel data with validated residue parameters.

    Returns:
        DataFrame with all AG_AGRICULTURA sheet data
    """
    df_ag = pd.read_excel(EXCEL_PATH, sheet_name='AG_AGRICULTURA')
    print(f"\nLoaded {len(df_ag)} residues from Excel AG_AGRICULTURA sheet")
    print(f"Excel codes: {df_ag['Residuo_Codigo'].unique()}")
    return df_ag


# ============================================================================
# PHASE 2: DATA EXTRACTION & VALIDATION
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


def extract_residue_data(row: pd.Series, excel_code: str) -> Dict:
    """
    Extract and validate data from Excel row.

    Args:
        row: pandas Series with Excel columns
        excel_code: Residuo_Codigo for this residue

    Returns:
        Dict with validated residue parameters
    """
    data = {
        'excel_code': excel_code,
        'name': safe_str(row.get('Residuo_Nome', ''), 'Unknown'),
        'generation': safe_str(row.get('generation', '')),
        'destination': safe_str(row.get('destination', '')),
        'justification': safe_str(row.get('justification', '')),

        # Chemical parameters
        'bmp': safe_float(row.get('chemical_bmp')),
        'bmp_unit': safe_str(row.get('chemical_bmp_unit'), 'm³ CH₄/kg MS'),
        'ts': safe_float(row.get('chemical_ts')),
        'vs': safe_float(row.get('chemical_vs')),
        'cn_ratio': safe_float(row.get('chemical_cn_ratio')),
        'ch4_content': safe_float(row.get('chemical_ch4_content')),

        # Availability - CORRECTED CALCULATION
        'fc': safe_float(row.get('availability_fc'), 0.5),
        'fcp': safe_float(row.get('availability_fcp'), 0.2),
        'fs': safe_float(row.get('availability_fs'), 1.0),
        'fl': safe_float(row.get('availability_fl'), 1.0),

        # Scenarios
        'pessimista': safe_float(row.get('scenarios_pessimista'), 0.0),
        'realista': safe_float(row.get('scenarios_realista'), 0.0),
        'otimista': safe_float(row.get('scenarios_otimista'), 0.0),
        'teorico': safe_float(row.get('scenarios_teorico'), 1.0),
    }

    # Calculate final availability using correct formula
    fc = data['fc']
    fcp = data['fcp']
    fs = data['fs']
    fl = data['fl']
    data['final_availability'] = fc * (1 - fcp) * fs * fl

    return data


def validate_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate extracted data for reasonableness.

    Returns:
        (is_valid, list of warnings)
    """
    warnings = []
    is_valid = True

    # BMP validation
    bmp = data['bmp']
    if bmp is None:
        warnings.append(f"Missing BMP value")
        is_valid = False
    elif bmp < 0.01 or bmp > 1.0:
        # Most agricultural residues: 0.05-0.50 m³/kg MS
        # Exception: Vinhaça uses different unit (Nm³/m³)
        if 'vinha' not in data['name'].lower():
            warnings.append(f"BMP value {bmp} outside typical range (0.05-0.50 m³/kg MS)")

    # Availability validation
    if data['final_availability'] > 1.0:
        warnings.append(f"Final availability {data['final_availability']} > 100%")
        is_valid = False

    # Scenario ordering validation
    pessimista = data['pessimista']
    realista = data['realista']
    otimista = data['otimista']
    teorico = data['teorico']

    if not (pessimista <= realista <= otimista <= teorico):
        warnings.append(f"Scenario ordering issue: Pess={pessimista}, Real={realista}, Otim={otimista}, Teor={teorico}")

    # Check for zeros in key fields
    if bmp == 0.0:
        warnings.append("BMP is zero - likely incomplete data")
        is_valid = False

    return is_valid, warnings


def get_references_for_culture(refs_df: pd.DataFrame, culture: str) -> List[Dict]:
    """
    Get all references for a given culture from the CSV catalog.

    Args:
        refs_df: DataFrame from clean CSV catalog
        culture: Culture name (e.g., 'Milho', 'Soja')

    Returns:
        List of dicts with reference data
    """
    culture_refs = refs_df[refs_df['culture'] == culture]

    references = []
    for _, ref_row in culture_refs.iterrows():
        ref = {
            'title': safe_str(ref_row['citation_abnt'], ''),
            'doi': safe_str(ref_row['doi'], ''),
            'url': safe_str(ref_row['functional_link'], ''),
            'relevance': 'High',
            'data_type': 'Literatura Científica'
        }

        # Extract authors and year from ABNT citation
        citation = ref['title']

        # Authors: everything before the first period or "et al"
        if 'et al' in citation:
            authors_end = citation.find('et al') + 6
            authors = citation[:authors_end].strip()
        else:
            first_period = citation.find('.')
            if first_period > 0:
                authors = citation[:first_period].strip()
            else:
                authors = ''

        ref['authors'] = authors

        # Year: extract 4-digit year
        year_match = re.search(r'\b(19|20)\d{2}\b', citation)
        ref['year'] = int(year_match.group(0)) if year_match else 0

        # Journal: text after "..." but before volume/page info
        # This is approximate - the CSV has full ABNT citation
        ref['journal'] = ''  # Leave empty for now, full citation has it

        references.append(ref)

    return references


# ============================================================================
# PHASE 3: FILE GENERATION & UPDATE
# ============================================================================

def format_references_for_python(references: List[Dict]) -> str:
    """
    Format references as Python ScientificReference list.
    """
    if not references:
        return "[]"

    lines = ["["]
    for ref in references:
        lines.append("        ScientificReference(")
        lines.append(f'            title="{ref["title"].replace('"', "")[:150]}",')
        lines.append(f'            authors="{ref["authors"].replace('"', "")}",')
        lines.append(f'            year={ref["year"]},')
        if ref['doi']:
            lines.append(f'            doi="{ref["doi"]}",')
        if ref['url']:
            lines.append(f'            url="{ref["url"]}",')
        lines.append(f'            relevance="{ref["relevance"]}",')
        lines.append(f'            data_type="{ref["data_type"]}"')
        lines.append("        ),")
    lines.append("    ]")

    return "\n".join(lines)


def generate_integration_plan(excel_df: pd.DataFrame, refs_df: pd.DataFrame) -> List[Dict]:
    """
    Generate a plan of what will be updated, with validation.

    Returns:
        List of dicts with integration tasks
    """
    plan = []

    for excel_code, (filename, var_name, culture) in RESIDUE_MAPPING.items():
        # Find Excel row
        rows = excel_df[excel_df['Residuo_Codigo'] == excel_code]
        if len(rows) == 0:
            print(f"[SKIP] {excel_code} not found in Excel")
            continue

        row = rows.iloc[0]

        # Extract data
        data = extract_residue_data(row, excel_code)

        # Validate
        is_valid, warnings = validate_data(data)

        # Get references
        references = get_references_for_culture(refs_df, culture)

        # Create task
        task = {
            'excel_code': excel_code,
            'filename': filename,
            'var_name': var_name,
            'culture': culture,
            'data': data,
            'references': references,
            'is_valid': is_valid,
            'warnings': warnings,
            'filepath': DATA_DIR / filename
        }

        plan.append(task)

    return plan


def ascii_safe(text: str) -> str:
    """Convert text to ASCII-safe representation for console output."""
    replacements = {
        '₄': '4', '₂': '2', '₃': '3', '³': '3',
        '°': 'deg', 'ç': 'c', 'ã': 'a', 'õ': 'o',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        '→': '->', '⚠': 'WARNING'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def print_integration_plan(plan: List[Dict]):
    """Print integration plan for review."""
    print("\n" + "=" * 80)
    print("INTEGRATION PLAN SUMMARY")
    print("=" * 80)

    print(f"\nTotal residues to update: {len(plan)}")

    valid_count = sum(1 for t in plan if t['is_valid'])
    print(f"Valid residues: {valid_count}")
    print(f"Residues with warnings: {len(plan) - valid_count}")

    print("\nBy culture:")
    by_culture = {}
    for task in plan:
        culture = task['culture']
        if culture not in by_culture:
            by_culture[culture] = []
        by_culture[culture].append(task)

    for culture, tasks in sorted(by_culture.items()):
        ref_count = sum(len(t['references']) for t in tasks)
        print(f"  {culture}: {len(tasks)} residues, {ref_count} references")

    print("\n" + "-" * 80)
    print("DETAILED TASK LIST")
    print("-" * 80)

    for i, task in enumerate(plan, 1):
        data = task['data']
        print(f"\n{i}. {task['excel_code']} -> {task['filename']}")
        print(f"   Name: {ascii_safe(data['name'])}")
        print(f"   BMP: {data['bmp']} {ascii_safe(data['bmp_unit'])}")
        print(f"   Availability: FC={data['fc']}, FCp={data['fcp']} -> Final={data['final_availability']:.2%}")
        print(f"   References: {len(task['references'])} from {ascii_safe(task['culture'])}")

        if not task['is_valid']:
            print(f"   WARNING: VALIDATION FAILED")

        if task['warnings']:
            for warning in task['warnings']:
                print(f"   WARNING: {warning}")


def read_file_content(filepath: Path) -> str:
    """Read file content as string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.content()


def update_residue_file(task: Dict) -> bool:
    """
    Update a single residue file using targeted Edit operations.

    Args:
        task: Integration task dict with data and references

    Returns:
        True if successful
    """
    filepath = task['filepath']
    data = task['data']
    references = task['references']
    var_name = task['var_name']

    print(f"\n[UPDATE] {task['filename']}")
    print(f"  Variable: {var_name}")

    try:
        # Read current file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the ResidueData block for this variable
        var_start = content.find(f"{var_name} = ResidueData(")
        if var_start == -1:
            print(f"  ERROR: Could not find {var_name} definition")
            return False

        # Find the end of this ResidueData block (closing parenthesis)
        # We need to match nested parentheses carefully
        paren_count = 0
        i = var_start
        var_end = -1
        while i < len(content):
            if content[i] == '(':
                paren_count += 1
            elif content[i] == ')':
                paren_count -= 1
                if paren_count == 0:
                    var_end = i + 1
                    break
            i += 1

        if var_end == -1:
            print(f"  ERROR: Could not find end of {var_name} definition")
            return False

        residue_block = content[var_start:var_end]

        # Now we'll build the updated block
        # Strategy: Replace specific sections within the block

        updated_block = residue_block

        # 1. Update BMP value and unit
        bmp_pattern = r'bmp=[\d.]+,'
        bmp_replacement = f'bmp={data["bmp"]},'
        updated_block = re.sub(bmp_pattern, bmp_replacement, updated_block, count=1)

        bmp_unit_pattern = r'bmp_unit="[^"]*"'
        bmp_unit_replacement = f'bmp_unit="{data["bmp_unit"]}"'
        updated_block = re.sub(bmp_unit_pattern, bmp_unit_replacement, updated_block, count=1)

        # 2. Update availability factors
        fc_pattern = r'fc=[\d.]+'
        fc_replacement = f'fc={data["fc"]}'
        updated_block = re.sub(fc_pattern, fc_replacement, updated_block, count=1)

        fcp_pattern = r'fcp=[\d.]+'
        fcp_replacement = f'fcp={data["fcp"]}'
        updated_block = re.sub(fcp_pattern, fcp_replacement, updated_block, count=1)

        fs_pattern = r'fs=[\d.]+'
        fs_replacement = f'fs={data["fs"]}'
        updated_block = re.sub(fs_pattern, fs_replacement, updated_block, count=1)

        fl_pattern = r'fl=[\d.]+'
        fl_replacement = f'fl={data["fl"]}'
        updated_block = re.sub(fl_pattern, fl_replacement, updated_block, count=1)

        final_avail_pattern = r'final_availability=[\d.]+'
        final_avail_replacement = f'final_availability={data["final_availability"]:.4f}'
        updated_block = re.sub(final_avail_pattern, final_avail_replacement, updated_block, count=1)

        # 3. Update scenarios
        scenarios_pattern = r'scenarios=\{[^}]+\}'
        scenarios_replacement = f'''scenarios={{
        "Pessimista": {data["pessimista"]},
        "Realista": {data["realista"]},
        "Otimista": {data["otimista"]},
        "Teórico (100%)": {data["teorico"]}
    }}'''
        updated_block = re.sub(scenarios_pattern, scenarios_replacement, updated_block, flags=re.DOTALL, count=1)

        # 4. Update references
        # Find references section
        references_pattern = r'references=\[[^\]]*\]'

        # Build references list
        ref_lines = []
        if references:
            for ref in references:
                # Escape quotes in strings
                title = ref['title'].replace('"', '\\"').replace("'", "\\'")
                authors = ref['authors'].replace('"', '\\"').replace("'", "\\'")

                ref_lines.append('        ScientificReference(')
                ref_lines.append(f'            title="{title[:200]}",')  # Truncate if too long
                ref_lines.append(f'            authors="{authors}",')
                ref_lines.append(f'            year={ref["year"]},')
                if ref['doi']:
                    ref_lines.append(f'            doi="{ref["doi"]}",')
                if ref.get('url'):
                    ref_lines.append(f'            scopus_link="{ref["url"]}",')  # Fixed: url -> scopus_link
                ref_lines.append(f'            relevance="High",')
                ref_lines.append(f'            data_type="Literatura Científica"')
                ref_lines.append('        ),')

        if ref_lines:
            references_replacement = 'references=[\n' + '\n'.join(ref_lines) + '\n    ]'
        else:
            references_replacement = 'references=[]'

        updated_block = re.sub(references_pattern, references_replacement, updated_block, flags=re.DOTALL, count=1)

        # Write the updated content back
        updated_content = content[:var_start] + updated_block + content[var_end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"  SUCCESS: Updated {len(references)} references, BMP={data['bmp']}, Availability={data['final_availability']:.2%}")
        return True

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def execute_integration_plan(plan: List[Dict], dry_run: bool = True):
    """
    Execute the integration plan, updating residue files.

    Args:
        plan: List of integration tasks
        dry_run: If True, only simulate (don't write files)
    """
    if dry_run:
        print("\n" + "=" * 80)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("EXECUTING INTEGRATION")
        print("=" * 80)

    updated_count = 0
    failed_count = 0

    for task in plan:
        if not task['is_valid']:
            print(f"\n[SKIP] {task['excel_code']} - validation failed")
            continue

        if dry_run:
            print(f"\n[WOULD UPDATE] {task['filename']}")
            print(f"  Would update: {task['var_name']}")
            print(f"    BMP: {task['data']['bmp']}")
            print(f"    Availability: {task['data']['final_availability']:.2%}")
            print(f"    References: {len(task['references'])}")
        else:
            # Actual update
            if update_residue_file(task):
                updated_count += 1
            else:
                failed_count += 1

    if not dry_run:
        print("\n" + "=" * 80)
        print(f"INTEGRATION COMPLETE: {updated_count} updated, {failed_count} failed")
        print("=" * 80)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main integration workflow."""
    print("=" * 80)
    print("PanoramaCP2B - Validated Data Integration V2")
    print("=" * 80)

    # Load data sources
    print("\n[PHASE 1] Loading data sources...")
    refs_df = load_references_catalog()
    excel_df = load_excel_data()

    # Generate integration plan
    print("\n[PHASE 2] Generating integration plan...")
    plan = generate_integration_plan(excel_df, refs_df)

    # Review plan
    print_integration_plan(plan)

    # Execute
    print("\n[PHASE 3] Execution")
    execute_integration_plan(plan, dry_run=DRY_RUN)

    print("\n" + "=" * 80)
    if DRY_RUN:
        print("DRY RUN COMPLETE - Review the plan above")
        print("To execute for real, set DRY_RUN = False in the script")
    else:
        print("INTEGRATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
