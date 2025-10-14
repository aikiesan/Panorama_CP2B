"""
Extract CP2B Database and Convert to Python Dataclass Format
"""

import sqlite3
import json
from pathlib import Path

# Connect to database
db_path = Path(__file__).parent.parent / "data" / "cp2b_panorama.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row  # Access columns by name
cursor = conn.cursor()

# Extract all residues with complete data
residues_data = []

cursor.execute("SELECT * FROM residues")
residues = cursor.fetchall()

for residue in residues:
    residue_id = residue['id']
    residue_dict = {
        'id': residue_id,
        'name': residue['name'],
        'category': residue['category'],
        'icon': residue['icon'],
        'generation': residue['generation'],
        'destination': residue['destination']
    }

    # Get chemical parameters
    cursor.execute("SELECT * FROM chemical_params WHERE residue_id = ?", (residue_id,))
    chem = cursor.fetchone()
    if chem:
        residue_dict['chemical'] = {
            'bmp': chem['bmp'],
            'bmp_unit': chem['bmp_unit'],
            'ts': chem['ts'],
            'vs': chem['vs'],
            'vs_basis': chem['vs_basis'],
            'moisture': chem['moisture'],
            'cn_ratio': chem['cn_ratio'],
            'ph': chem['ph'],
            'cod': chem['cod'],
            'nitrogen': chem['nitrogen'],
            'carbon': chem['carbon'],
            'ch4_content': chem['ch4_content'],
            'phosphorus': chem['phosphorus'],
            'potassium': chem['potassium'],
            'protein': chem['protein'],
            'toc': chem['toc']
        }

    # Get availability factors
    cursor.execute("SELECT * FROM availability_factors WHERE residue_id = ?", (residue_id,))
    avail = cursor.fetchone()
    if avail:
        residue_dict['availability'] = {
            'fc': avail['fc'],
            'fcp': avail['fcp'],
            'fs': avail['fs'],
            'fl': avail['fl'],
            'final_availability': avail['final_availability']
        }

    # Get operational parameters
    cursor.execute("SELECT * FROM operational_params WHERE residue_id = ?", (residue_id,))
    oper = cursor.fetchone()
    if oper:
        residue_dict['operational'] = {
            'hrt': oper['hrt'],
            'temperature': oper['temperature'],
            'fi_ratio': oper['fi_ratio'],
            'olr': oper['olr'],
            'reactor_type': oper['reactor_type'],
            'tan_threshold': oper['tan_threshold'],
            'vfa_limit': oper['vfa_limit']
        }

    # Get scenarios
    cursor.execute("SELECT * FROM scenarios WHERE residue_id = ?", (residue_id,))
    scenarios = cursor.fetchone()
    if scenarios:
        residue_dict['scenarios'] = {
            'Pessimista': scenarios['pessimista'],
            'Realista': scenarios['realista'],
            'Otimista': scenarios['otimista'],
            'Teórico (100%)': scenarios['teorico']
        }

    # Get justification from residues table
    residue_dict['justification'] = residue['justification']

    # Get scientific references
    cursor.execute("SELECT * FROM scientific_references WHERE residue_id = ?", (residue_id,))
    refs = cursor.fetchall()
    residue_dict['references'] = []
    for ref in refs:
        # Parse key_findings safely
        key_findings = []
        if ref['key_findings']:
            try:
                key_findings = json.loads(ref['key_findings'])
            except (json.JSONDecodeError, TypeError):
                # If not JSON, treat as a single string or split by newlines
                key_findings = [ref['key_findings']]

        residue_dict['references'].append({
            'title': ref['title'],
            'authors': ref['authors'],
            'year': ref['year'],
            'doi': ref['doi'],
            'scopus_link': ref['scopus_link'],
            'journal': ref['journal'],
            'relevance': ref['relevance'],
            'key_findings': key_findings,
            'data_type': ref['data_type']
        })

    residues_data.append(residue_dict)

# Export to JSON
output_path = Path(__file__).parent.parent / "data" / "cp2b_complete_export.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(residues_data, f, indent=2, ensure_ascii=False)

print(f"[OK] Extracted {len(residues_data)} residues")
print(f"[OK] Total references: {sum(len(r['references']) for r in residues_data)}")
print(f"[OK] Export saved to: {output_path}")

# Print summary
for r in residues_data:
    print(f"\n{r['name']}")
    print(f"  Category: {r['category']}")
    print(f"  BMP: {r['chemical']['bmp']} {r['chemical']['bmp_unit']}")
    print(f"  Availability: {r['availability']['final_availability']}%")
    print(f"  References: {len(r['references'])} papers")
    if r['scenarios']['Realista']:
        print(f"  Realistic Potential: {r['scenarios']['Realista']} Mi m³/ano")

conn.close()
