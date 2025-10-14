"""
Generate src/research_data.py from CP2B Complete Export
Converts JSON database export to Python dataclass format
"""

import json
from pathlib import Path

# Read the complete export
json_path = Path(__file__).parent.parent / "data" / "cp2b_complete_export.json"
with open(json_path, 'r', encoding='utf-8') as f:
    residues = json.load(f)

# Generate Python code
output_lines = []

# Header
output_lines.extend([
    '"""',
    'Research Data Module - Validated Chemical and Availability Data',
    'CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)',
    '',
    'Comprehensive database of residue characteristics, chemical parameters,',
    'availability factors, and scientific references for biogas production.',
    '',
    'AUTO-GENERATED FROM CP2B DATABASE v2.0',
    'Date: 2025-10-14',
    'Source: cp2b_panorama.db',
    'Residues: 7 | References: 50+',
    '"""',
    '',
    'from dataclasses import dataclass',
    'from typing import Dict, List, Optional, Any',
    '',
    ''
])

# Add dataclass definitions (from original file)
output_lines.extend([
    '# ============================================================================',
    '# DATA STRUCTURES',
    '# ============================================================================',
    '',
    '@dataclass',
    'class ChemicalParameters:',
    '    """Chemical composition and methane potential parameters"""',
    '    bmp: float',
    '    bmp_unit: str',
    '    ts: float',
    '    vs: float',
    '    vs_basis: str',
    '    moisture: float',
    '    cn_ratio: Optional[float] = None',
    '    ph: Optional[float] = None',
    '    cod: Optional[float] = None',
    '    nitrogen: Optional[float] = None',
    '    carbon: Optional[float] = None',
    '    ch4_content: Optional[float] = None',
    '    phosphorus: Optional[float] = None',
    '    potassium: Optional[float] = None',
    '    protein: Optional[float] = None',
    '    toc: Optional[float] = None',
    '',
    '    def to_dict(self) -> Dict[str, Any]:',
    '        """Convert to dictionary for display"""',
    '        result = {',
    '            "BMP": f"{self.bmp} {self.bmp_unit}",',
    '            "Sólidos Totais (TS)": f"{self.ts}%",',
    '            "Sólidos Voláteis (VS)": f"{self.vs}% {self.vs_basis}",',
    '            "Umidade": f"{self.moisture}%"',
    '        }',
    '        if self.cn_ratio: result["Relação C:N"] = f"{self.cn_ratio}"',
    '        if self.ph: result["pH"] = f"{self.ph}"',
    '        if self.cod: result["DQO"] = f"{self.cod} mg/L"',
    '        if self.nitrogen: result["Nitrogênio (N)"] = f"{self.nitrogen}%"',
    '        if self.carbon: result["Carbono (C)"] = f"{self.carbon}%"',
    '        if self.ch4_content: result["Conteúdo CH₄"] = f"{self.ch4_content}%"',
    '        return result',
    '',
    ''
])

# Add remaining dataclasses
output_lines.extend([
    '@dataclass',
    'class AvailabilityFactors:',
    '    """Availability correction factors for residues"""',
    '    fc: float',
    '    fcp: float',
    '    fs: float',
    '    fl: float',
    '    final_availability: float',
    '',
    '    def to_dict(self) -> Dict[str, str]:',
    '        """Convert to dictionary for display"""',
    '        return {',
    '            "FC (Coleta)": f"{self.fc:.2f}",',
    '            "FCp (Competição)": f"{self.fcp:.2f}",',
    '            "FS (Sazonal)": f"{self.fs:.2f}",',
    '            "FL (Logístico)": f"{self.fl:.2f}",',
    '            "Disponibilidade Final": f"{self.final_availability:.1f}%"',
    '        }',
    '',
    '',
    '@dataclass',
    'class OperationalParameters:',
    '    """Operational parameters for anaerobic digestion"""',
    '    hrt: str',
    '    temperature: str',
    '    fi_ratio: Optional[float] = None',
    '    olr: Optional[str] = None',
    '    reactor_type: Optional[str] = None',
    '    tan_threshold: Optional[str] = None',
    '    vfa_limit: Optional[str] = None',
    '',
    '    def to_dict(self) -> Dict[str, str]:',
    '        """Convert to dictionary for display"""',
    '        result = {',
    '            "TRH (Tempo de Retenção Hidráulica)": self.hrt,',
    '            "Temperatura": self.temperature,',
    '        }',
    '        if self.fi_ratio: result["Razão F/I"] = f"{self.fi_ratio}"',
    '        if self.olr: result["TCO (Taxa de Carga Orgânica)"] = self.olr',
    '        if self.reactor_type: result["Tipo de Reator"] = self.reactor_type',
    '        if self.tan_threshold: result["Limite TAN"] = self.tan_threshold',
    '        if self.vfa_limit: result["Limite AGV"] = self.vfa_limit',
    '        return result',
    '',
    '',
    '@dataclass',
    'class ScientificReference:',
    '    """Scientific paper reference"""',
    '    title: str',
    '    authors: str',
    '    year: int',
    '    doi: Optional[str] = None',
    '    scopus_link: Optional[str] = None',
    '    journal: Optional[str] = None',
    '    relevance: str = "High"',
    '    key_findings: List[str] = None',
    '    data_type: str = "Literatura Científica"',
    '',
    '    def __post_init__(self):',
    '        if self.key_findings is None:',
    '            self.key_findings = []',
    '',
    '',
    '@dataclass',
    'class ResidueData:',
    '    """Complete residue data with validated factors"""',
    '    name: str',
    '    category: str',
    '    icon: str',
    '    generation: str',
    '    destination: str',
    '    chemical_params: ChemicalParameters',
    '    availability: AvailabilityFactors',
    '    operational: OperationalParameters',
    '    justification: str',
    '    scenarios: Dict[str, float]',
    '    references: List[ScientificReference]',
    '    top_municipalities: Optional[List[Dict]] = None',
    '    validation_data: Optional[Dict] = None',
    '    contribution_breakdown: Optional[Dict] = None',
    '',
    ''
])

# Generate data for each residue
for idx, r in enumerate(residues, 1):
    residue_name = r['name'].replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace('+', '').replace('á', 'a').replace('ã', 'a').replace('ê', 'e').replace('í', 'i').replace('ú', 'u').replace('ç', 'c').upper()
    output_lines.extend([
        '# ============================================================================',
        f'# {r["name"].upper()}',
        '# ============================================================================',
        '',
        f'{residue_name}_CHEMICAL_PARAMS = ChemicalParameters(',
        f'    bmp={r["chemical"]["bmp"] or 0.0},',
        f'    bmp_unit="{r["chemical"]["bmp_unit"] or "N/A"}",',
        f'    ts={r["chemical"]["ts"] or 0.0},',
        f'    vs={r["chemical"]["vs"] or 0.0},',
        f'    vs_basis="{r["chemical"]["vs_basis"] or "% of TS"}",',
        f'    moisture={r["chemical"]["moisture"] or 0.0},',
        f'    cn_ratio={r["chemical"]["cn_ratio"]},',
        f'    ph={r["chemical"]["ph"]},',
        f'    cod={r["chemical"]["cod"]},',
        f'    nitrogen={r["chemical"]["nitrogen"]},',
        f'    carbon={r["chemical"]["carbon"]},',
        f'    ch4_content={r["chemical"]["ch4_content"]},',
        f'    phosphorus={r["chemical"]["phosphorus"]},',
        f'    potassium={r["chemical"]["potassium"]},',
        f'    protein={r["chemical"]["protein"]},',
        f'    toc={r["chemical"]["toc"]}',
        ')',
        '',
        f'{residue_name}_AVAILABILITY = AvailabilityFactors(',
        f'    fc={r["availability"]["fc"]},',
        f'    fcp={r["availability"]["fcp"]},',
        f'    fs={r["availability"]["fs"]},',
        f'    fl={r["availability"]["fl"]},',
        f'    final_availability={r["availability"]["final_availability"]:.2f}',
        ')',
        ''
    ])

    # Handle operational parameters (may be missing for some residues)
    if 'operational' in r and r['operational']:
        oper = r['operational']
        # Evaluate conditionals before generating strings
        olr_val = f'"{oper["olr"]}"' if oper.get("olr") is not None else 'None'
        reactor_type_val = f'"{oper["reactor_type"]}"' if oper.get("reactor_type") is not None else 'None'
        tan_threshold_val = f'"{oper["tan_threshold"]}"' if oper.get("tan_threshold") is not None else 'None'
        vfa_limit_val = f'"{oper["vfa_limit"]}"' if oper.get("vfa_limit") is not None else 'None'

        output_lines.extend([
            f'{residue_name}_OPERATIONAL = OperationalParameters(',
            f'    hrt="{oper.get("hrt", "N/A")}",',
            f'    temperature="{oper.get("temperature", "N/A")}",',
            f'    fi_ratio={oper.get("fi_ratio")},',
            f'    olr={olr_val},',
            f'    reactor_type={reactor_type_val},',
            f'    tan_threshold={tan_threshold_val},',
            f'    vfa_limit={vfa_limit_val}',
            ')',
            ''
        ])
    else:
        # Default operational parameters if missing
        output_lines.extend([
            f'{residue_name}_OPERATIONAL = OperationalParameters(',
            '    hrt="N/A",',
            '    temperature="N/A"',
            ')',
            ''
        ])

    # Add justification (escape quotes)
    just = r['justification'].replace('"', '\\"').replace('\n', '\\n')
    output_lines.append(f'{residue_name}_JUSTIFICATION = """')
    output_lines.append(r['justification'])
    output_lines.append('"""')
    output_lines.append('')

    # Add scenarios
    output_lines.append(f'{residue_name}_SCENARIOS = {{')
    for sc_name, sc_value in r['scenarios'].items():
        if sc_value is not None:
            output_lines.append(f'    "{sc_name}": {sc_value},')
    output_lines.append('}')
    output_lines.append('')

    # Add references
    output_lines.append(f'{residue_name}_REFERENCES = [')
    for ref in r['references']:
        output_lines.append('    ScientificReference(')
        output_lines.append(f'        title="{ref["title"]}",')
        output_lines.append(f'        authors="{ref["authors"]}",')
        output_lines.append(f'        year={ref["year"]},')
        output_lines.append(f'        doi="{ref["doi"]}" if {ref["doi"] is not None} else None,')
        output_lines.append(f'        scopus_link="{ref["scopus_link"]}" if {ref["scopus_link"] is not None} else None,')
        output_lines.append(f'        journal="{ref["journal"]}" if {ref["journal"] is not None} else None,')
        output_lines.append(f'        relevance="{ref["relevance"]}",')
        # Handle key_findings list
        if ref['key_findings']:
            output_lines.append('        key_findings=[')
            for finding in ref['key_findings']:
                # Escape and truncate if needed
                finding_esc = finding.replace('"', '\\"')
                if len(finding_esc) > 200:
                    finding_esc = finding_esc[:197] + '...'
                output_lines.append(f'            "{finding_esc}",')
            output_lines.append('        ],')
        else:
            output_lines.append('        key_findings=[],')
        output_lines.append(f'        data_type="{ref["data_type"]}"')
        output_lines.append('    ),')
    output_lines.append(']')
    output_lines.append('')

    # Create ResidueData object
    output_lines.extend([
        f'{residue_name}_DATA = ResidueData(',
        f'    name="{r["name"]}",',
        f'    category="{r["category"]}",',
        f'    icon="{r["icon"]}",',
        f'    generation="{r["generation"]}",',
        f'    destination="{r["destination"]}",',
        f'    chemical_params={residue_name}_CHEMICAL_PARAMS,',
        f'    availability={residue_name}_AVAILABILITY,',
        f'    operational={residue_name}_OPERATIONAL,',
        f'    justification={residue_name}_JUSTIFICATION,',
        f'    scenarios={residue_name}_SCENARIOS,',
        f'    references={residue_name}_REFERENCES',
        ')',
        '',
        ''
    ])

# Add registry and helper functions
output_lines.extend([
    '# ============================================================================',
    '# REGISTRY AND HELPER FUNCTIONS',
    '# ============================================================================',
    '',
    'RESIDUES_REGISTRY = {',
])

for r in residues:
    residue_name = r['name'].replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace('+', '').replace('á', 'a').replace('ã', 'a').replace('ê', 'e').replace('í', 'i').replace('ú', 'u').replace('ç', 'c').upper()
    output_lines.append(f'    "{r["name"]}": {residue_name}_DATA,')

output_lines.extend([
    '}',
    '',
    'CATEGORIES = {',
    '    "Agricultura": ["Vinhaça de Cana-de-açúcar", "Palha de Cana-de-açúcar (Palhiço)", "Torta de Filtro (Filter Cake)"],',
    '    "Pecuária": ["Dejeto de Aves (Cama de Frango)", "Dejetos de Bovinos (Leite + Corte)", "Dejetos de Suínos", "Dejeto de Codornas"]',
    '}',
    '',
    '',
    'def get_available_residues() -> List[str]:',
    '    """Get list of all available residues"""',
    '    return list(RESIDUES_REGISTRY.keys())',
    '',
    '',
    'def get_residue_data(residue_name: str) -> Optional[ResidueData]:',
    '    """Get complete data for a specific residue"""',
    '    return RESIDUES_REGISTRY.get(residue_name)',
    '',
    '',
    'def get_residues_by_category(category: str) -> List[str]:',
    '    """Get list of residues by category"""',
    '    return CATEGORIES.get(category, [])',
    '',
    '',
    'def get_category_icon(category: str) -> str:',
    '    """Get emoji icon for category"""',
    '    icons = {',
    '        "Agricultura": "🌾",',
    '        "Pecuária": "🐄",',
    '        "Urbano": "🏙️"',
    '    }',
    '    return icons.get(category, "📊")',
    '',
    '',
    'def get_residue_icon(residue_name: str) -> str:',
    '    """Get emoji icon for specific residue"""',
    '    residue = get_residue_data(residue_name)',
    '    return residue.icon if residue else "📊"',
    ''
])

# Write to output file
output_file = Path(__file__).parent.parent / "src" / "research_data_new.py"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Generated {len(residues)} residues with {sum(len(r['references']) for r in residues)} references")
print(f"Output: {output_file}")
