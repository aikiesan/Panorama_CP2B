"""
Complete Data Integration Script V3 - PanoramaCP2B
Updates ALL fields from Excel, not just references

Author: Claude Code (Anthropic)
Date: October 20, 2025
Improvements over V2:
- Updates generation, destination, justification text
- Updates TS, VS, C:N ratio, CH4 content
- Updates icons (with defaults if missing)
- Comprehensive field coverage
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from integrate_validated_data_v2 import (
    load_references_catalog,
    load_excel_data,
    RESIDUE_MAPPING,
    get_references_for_culture,
    safe_float,
    safe_str
)

# ============================================================================
# ICON DEFAULTS (if missing in Excel)
# ============================================================================

ICON_DEFAULTS = {
    'PALHA_MILHO': '🌽',
    'SABUGO': '🌽',
    'PALHA_SOJA': '🫘',
    'VAGEM_SOJA': '🫘',
    'CASCA_CAFE': '☕',
    'CASCA_EUCALIPTO': '🌳',
    'GALHOS_EUCALIPTO': '🌳',
    'FOLHAS_EUCALIPTO': '🌳',
    'PALHA': '🌾',
    'CASCAS_CITROS': '🍊',
    'BAGACO_CITROS': '🍊'
}

# ============================================================================
# COMPLETE DATA EXTRACTION
# ============================================================================

def extract_complete_residue_data(row: pd.Series, excel_code: str) -> Dict:
    """
    Extract ALL fields from Excel row.
    """
    data = {
        'excel_code': excel_code,

        # Basic info
        'name': safe_str(row.get('Residuo_Nome', ''), 'Unknown'),
        'generation': safe_str(row.get('generation', '')),
        'destination': safe_str(row.get('destination', '')),
        'justification': safe_str(row.get('justification', '')),
        'icon': safe_str(row.get('icon'), ICON_DEFAULTS.get(excel_code, '🌾')),

        # Chemical parameters
        'bmp': safe_float(row.get('chemical_bmp')),
        'bmp_unit': safe_str(row.get('chemical_bmp_unit'), 'm³ CH₄/kg MS'),
        'ts': safe_float(row.get('chemical_ts'), 0.0),  # Default to 0.0 if missing
        'vs': safe_float(row.get('chemical_vs'), 0.0),
        'cn_ratio': safe_float(row.get('chemical_cn_ratio')),
        'ch4_content': safe_float(row.get('chemical_ch4_content')),

        # Availability
        'fc': safe_float(row.get('availability_fc'), 0.5),
        'fcp': safe_float(row.get('availability_fcp'), 0.2),
        'fs': 1.0,  # Not in Excel, default
        'fl': 1.0,  # Not in Excel, default

        # Scenarios
        'pessimista': safe_float(row.get('scenarios_pessimista'), 0.0),
        'realista': safe_float(row.get('scenarios_realista'), 0.0),
        'otimista': safe_float(row.get('scenarios_otimista'), 0.0),
        'teorico': safe_float(row.get('scenarios_teorico'), 1.0),
    }

    # Calculate final availability
    data['final_availability'] = data['fc'] * (1 - data['fcp']) * data['fs'] * data['fl']

    return data


def update_complete_residue_file(filepath: Path, var_name: str, data: Dict, references: List[Dict]) -> bool:
    """
    Update ALL fields in a residue file.
    """
    print(f"\n[COMPLETE UPDATE] {filepath.name}")
    print(f"  Variable: {var_name}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the ResidueData block
        var_start = content.find(f"{var_name} = ResidueData(")
        if var_start == -1:
            print(f"  ERROR: Could not find {var_name}")
            return False

        # Find end of block
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
            print(f"  ERROR: Could not find end of {var_name}")
            return False

        residue_block = content[var_start:var_end]
        updated_block = residue_block

        # 1. Update name
        updated_block = re.sub(r'name="[^"]*"', f'name="{data["name"]}"', updated_block, count=1)

        # 2. Update icon
        updated_block = re.sub(r'icon="[^"]*"', f'icon="{data["icon"]}"', updated_block, count=1)

        # 3. Update generation
        generation_safe = data['generation'].replace('"', '\\"')
        updated_block = re.sub(r'generation="[^"]*"', f'generation="{generation_safe}"', updated_block, count=1)

        # 4. Update destination
        destination_safe = data['destination'].replace('"', '\\"')
        updated_block = re.sub(r'destination="[^"]*"', f'destination="{destination_safe}"', updated_block, count=1)

        # 5. Update BMP
        updated_block = re.sub(r'bmp=[\d.]+,', f'bmp={data["bmp"]},', updated_block, count=1)
        updated_block = re.sub(r'bmp_unit="[^"]*"', f'bmp_unit="{data["bmp_unit"]}"', updated_block, count=1)

        # 6. Update TS
        if data['ts'] and data['ts'] > 0:
            updated_block = re.sub(r'ts=[\d.]+,', f'ts={data["ts"]},', updated_block, count=1)

        # 7. Update VS
        if data['vs'] and data['vs'] > 0:
            updated_block = re.sub(r'vs=[\d.]+,', f'vs={data["vs"]},', updated_block, count=1)

        # 8. Update C:N ratio
        if data['cn_ratio']:
            # Add cn_ratio if not present
            if 'cn_ratio=' not in updated_block:
                # Insert after ch4_content or vs
                insert_pos = updated_block.find('ch4_content=')
                if insert_pos == -1:
                    insert_pos = updated_block.find('vs_basis=')
                if insert_pos > 0:
                    line_end = updated_block.find('\n', insert_pos)
                    updated_block = updated_block[:line_end+1] + f'        cn_ratio={data["cn_ratio"]},\n' + updated_block[line_end+1:]
            else:
                updated_block = re.sub(r'cn_ratio=[\d.]+', f'cn_ratio={data["cn_ratio"]}', updated_block, count=1)

        # 9. Update CH4 content
        if data['ch4_content']:
            if 'ch4_content=' not in updated_block:
                # Insert after cn_ratio
                insert_pos = updated_block.find('cn_ratio=')
                if insert_pos > 0:
                    line_end = updated_block.find('\n', insert_pos)
                    updated_block = updated_block[:line_end+1] + f'        ch4_content={data["ch4_content"]},\n' + updated_block[line_end+1:]
            else:
                updated_block = re.sub(r'ch4_content=[\d.]+', f'ch4_content={data["ch4_content"]}', updated_block, count=1)

        # 10. Update availability factors
        updated_block = re.sub(r'fc=[\d.]+', f'fc={data["fc"]}', updated_block, count=1)
        updated_block = re.sub(r'fcp=[\d.]+', f'fcp={data["fcp"]}', updated_block, count=1)
        updated_block = re.sub(r'final_availability=[\d.]+', f'final_availability={data["final_availability"]:.4f}', updated_block, count=1)

        # 11. Update scenarios
        scenarios_replacement = f'''scenarios={{
        "Pessimista": {data["pessimista"]},
        "Realista": {data["realista"]},
        "Otimista": {data["otimista"]},
        "Teórico (100%)": {data["teorico"]}
    }}'''
        updated_block = re.sub(r'scenarios=\{[^}]+\}', scenarios_replacement, updated_block, flags=re.DOTALL, count=1)

        # 12. Update justification
        if data['justification']:
            justification_safe = data['justification'].replace('"""', '\\"\\"\\"')
            justification_replacement = f'''justification="""
    {justification_safe}
    """'''
            updated_block = re.sub(r'justification="""[^"]*"""', justification_replacement, updated_block, flags=re.DOTALL, count=1)

        # 13. Update references
        ref_lines = []
        if references:
            for ref in references:
                title = ref['title'].replace('"', '\\"').replace("'", "\\'")
                authors = ref['authors'].replace('"', '\\"').replace("'", "\\'")

                ref_lines.append('        ScientificReference(')
                ref_lines.append(f'            title="{title[:200]}",')
                ref_lines.append(f'            authors="{authors}",')
                ref_lines.append(f'            year={ref["year"]},')
                if ref['doi']:
                    ref_lines.append(f'            doi="{ref["doi"]}",')
                if ref.get('url'):
                    ref_lines.append(f'            scopus_link="{ref["url"]}",')
                ref_lines.append(f'            relevance="High",')
                ref_lines.append(f'            data_type="Literatura Científica"')
                ref_lines.append('        ),')

        if ref_lines:
            references_replacement = 'references=[\n' + '\n'.join(ref_lines) + '\n    ]'
        else:
            references_replacement = 'references=[]'

        updated_block = re.sub(r'references=\[[^\]]*\]', references_replacement, updated_block, flags=re.DOTALL, count=1)

        # Write back
        updated_content = content[:var_start] + updated_block + content[var_end:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"  SUCCESS: Updated ALL fields")
        print(f"    Generation: {data['generation'][:50]}...")
        print(f"    TS: {data['ts']}, VS: {data['vs']}, C:N: {data['cn_ratio']}")
        print(f"    References: {len(references)}")
        return True

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("PanoramaCP2B - COMPLETE Data Integration V3")
    print("=" * 80)

    # Load data
    print("\n[PHASE 1] Loading data...")
    refs_df = load_references_catalog()
    excel_df = load_excel_data()

    # Process residues
    print("\n[PHASE 2] Processing residues...")

    updated_count = 0
    failed_count = 0

    for excel_code, (filename, var_name, culture) in RESIDUE_MAPPING.items():
        # Find Excel row
        rows = excel_df[excel_df['Residuo_Codigo'] == excel_code]
        if len(rows) == 0:
            print(f"\n[SKIP] {excel_code} not found in Excel")
            continue

        row = rows.iloc[0]

        # Extract complete data
        data = extract_complete_residue_data(row, excel_code)

        # Get references
        references = get_references_for_culture(refs_df, culture)

        # Update file
        filepath = Path('src/data/agricultura') / filename
        if update_complete_residue_file(filepath, var_name, data, references):
            updated_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 80)
    print(f"COMPLETE INTEGRATION: {updated_count} updated, {failed_count} failed")
    print("=" * 80)


if __name__ == '__main__':
    main()
