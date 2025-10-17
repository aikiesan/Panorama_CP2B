"""
CSV Importer Utility - Data Integration Tool
CP2B (Centro Paulista de Estudos em Biogás e Bioprodutos)

Converts CSV data to ResidueData objects and generates Python data files.
"""

import pandas as pd
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


def parse_range(value_str: str) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Parse range from string like "150-200", "55-65", etc.

    Args:
        value_str: String containing range (e.g., "150-200")

    Returns:
        Tuple of (min, mean, max) values
    """
    if pd.isna(value_str) or value_str == '':
        return None, None, None

    # Convert to string and clean
    value_str = str(value_str).strip()

    # Pattern to match "min-max"
    pattern = r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
    match = re.search(pattern, value_str)

    if match:
        min_val = float(match.group(1))
        max_val = float(match.group(2))
        mean_val = (min_val + max_val) / 2
        return min_val, mean_val, max_val

    # Try single value
    try:
        val = float(re.search(r'\d+\.?\d*', value_str).group())
        return val, val, val
    except:
        return None, None, None


def parse_percentage(value_str: str) -> Optional[float]:
    """
    Parse percentage from string, removing % symbol.

    Args:
        value_str: String like "45-60%" or "75%"

    Returns:
        Mean percentage value
    """
    if pd.isna(value_str) or value_str == '':
        return None

    min_val, mean_val, max_val = parse_range(str(value_str))
    return mean_val


def infer_category_from_fonte(fonte: str) -> str:
    """
    Infer category (sector) from "Fonte" column.

    Args:
        fonte: Source type (Cultura, Pecuária, RSU, etc.)

    Returns:
        Category name (Agricultura, Pecuária, Urbano, Industrial)
    """
    fonte = str(fonte).lower()

    if 'cultura' in fonte or 'agricultura' in fonte:
        return "Agricultura"
    elif 'pecuária' in fonte or 'pecuaria' in fonte or 'aqua' in fonte:
        return "Pecuária"
    elif 'rsu' in fonte or 'urbano' in fonte or 'poda' in fonte:
        return "Urbano"
    elif 'indústria' in fonte or 'industria' in fonte or 'frigorífico' in fonte or 'laticínio' in fonte:
        return "Industrial"
    else:
        return "Agricultura"  # Default


def get_residue_icon(residue_name: str, category: str) -> str:
    """
    Get appropriate emoji icon for residue.

    Args:
        residue_name: Name of the residue
        category: Category/sector

    Returns:
        Emoji icon
    """
    name_lower = residue_name.lower()

    # Agricultura
    if 'cana' in name_lower:
        return "🌾"
    elif 'café' in name_lower or 'cafe' in name_lower:
        return "☕"
    elif 'citros' in name_lower or 'laranja' in name_lower:
        return "🍊"
    elif 'milho' in name_lower:
        return "🌽"
    elif 'soja' in name_lower:
        return "🫘"
    elif 'eucalipto' in name_lower or 'silvicultura' in name_lower:
        return "🌳"

    # Pecuária
    elif 'bovino' in name_lower or 'gado' in name_lower or 'curral' in name_lower:
        return "🐄"
    elif 'suíno' in name_lower or 'suino' in name_lower or 'porco' in name_lower:
        return "🐖"
    elif 'frango' in name_lower or 'ave' in name_lower or 'galinha' in name_lower:
        return "🐔"
    elif 'peixe' in name_lower or 'piscicultura' in name_lower:
        return "🐟"

    # Urbano
    elif 'poda' in name_lower or 'grama' in name_lower:
        return "🌿"
    elif 'rsu' in name_lower or 'lixo' in name_lower or 'alimentício' in name_lower:
        return "🗑️"
    elif 'esgoto' in name_lower or 'lodo' in name_lower:
        return "💧"

    # Industrial
    elif 'queijo' in name_lower or 'soro' in name_lower or 'leite' in name_lower:
        return "🧀"
    elif 'cerveja' in name_lower or 'malte' in name_lower:
        return "🍺"
    elif 'sangue' in name_lower or 'frigorífico' in name_lower:
        return "🥩"

    # Default by category
    if category == "Agricultura":
        return "🌾"
    elif category == "Pecuária":
        return "🐄"
    elif category == "Urbano":
        return "🏙️"
    elif category == "Industrial":
        return "🏭"
    else:
        return "📊"


def parse_csv_to_residues(csv_path: str) -> List[Dict]:
    """
    Parse CSV file and convert to list of residue dictionaries.

    Args:
        csv_path: Path to CSV file

    Returns:
        List of residue data dictionaries
    """
    df = pd.read_csv(csv_path)

    residues = []

    for idx, row in df.iterrows():
        # Skip empty rows
        if pd.isna(row.get('Resíduo Principal')):
            continue

        # Extract data
        fonte = row.get('Fonte', 'Cultura')
        categoria = row.get('Categoria', '')
        residue_name = row.get('Resíduo Principal', '').strip()
        category = infer_category_from_fonte(fonte)

        if not residue_name:
            continue

        # Parse BMP
        bmp_str = str(row.get('Potencial Metanogênico (m³ CH₄/ton MS)', ''))
        bmp_min, bmp_mean, bmp_max = parse_range(bmp_str)

        # Parse CH4 content
        ch4_str = str(row.get('Concentração CH₄ (%)', ''))
        ch4_min, ch4_mean, ch4_max = parse_range(ch4_str)

        # Parse C/N ratio
        cn_str = str(row.get('Relação C/N', ''))
        cn_min, cn_mean, cn_max = parse_range(cn_str)

        # Parse moisture
        moisture = parse_percentage(str(row.get('Umidade (%)', '')))

        # Parse TRH
        trh_str = str(row.get('TRH (dias)', ''))
        trh_min, trh_mean, trh_max = parse_range(trh_str)

        # Get other data
        generation = str(row.get('Produção de Resíduos', 'Dados não disponíveis'))
        sazonalidade = str(row.get('Sazonalidade', 'Ano todo'))
        pre_tratamento = str(row.get('Pré-tratamento', 'Não necessário'))
        estado_fisico = str(row.get('Estado Físico', 'Variável'))
        regiao = str(row.get('Região SP Concentrada', 'Todo o estado'))
        referencias = str(row.get('Referências', ''))

        icon = get_residue_icon(residue_name, category)

        residue_data = {
            'name': residue_name,
            'category': category,
            'sub_category': categoria if categoria else category,
            'icon': icon,
            'generation': generation,
            'sazonalidade': sazonalidade,
            'pre_tratamento': pre_tratamento,
            'estado_fisico': estado_fisico,
            'regiao': regiao,
            'bmp': {
                'min': bmp_min,
                'mean': bmp_mean,
                'max': bmp_max,
                'unit': 'mL CH₄/g VS'
            },
            'ch4_content': {
                'min': ch4_min,
                'mean': ch4_mean,
                'max': ch4_max,
                'unit': '%'
            },
            'cn_ratio': {
                'min': cn_min,
                'mean': cn_mean,
                'max': cn_max
            },
            'moisture': moisture,
            'trh': {
                'min': trh_min,
                'mean': trh_mean,
                'max': trh_max,
                'unit': 'dias'
            },
            'referencias': referencias.split(' e ') if referencias else []
        }

        residues.append(residue_data)

    return residues


def generate_residue_file(residue_data: Dict, output_dir: Path) -> str:
    """
    Generate Python file with residue data.

    Args:
        residue_data: Dictionary with residue data
        output_dir: Output directory for the file

    Returns:
        Path to generated file
    """
    name = residue_data['name']
    category = residue_data['category']

    # Generate safe filename
    safe_name = re.sub(r'[^\w\s-]', '', name.lower())
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    filename = f"{safe_name}.py"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    # Generate Python code
    code = f'''"""
{name} - Residue Data
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

{name.upper().replace(' ', '_').replace('-', '_')}_DATA = ResidueData(
    name="{name}",
    category="{category}",
    icon="{residue_data['icon']}",
    generation="{residue_data['generation']}",
    destination="Biodigestão anaeróbia para produção de biogás",

    chemical_params=ChemicalParameters(
        bmp={residue_data['bmp']['mean'] or 0:.1f},
        bmp_unit="{residue_data['bmp']['unit']}",
        ts=0.0,  # TODO: Add from data source
        vs=0.0,  # TODO: Add from data source
        vs_basis="ST",
        moisture={residue_data['moisture'] or 0:.1f},
        cn_ratio={residue_data['cn_ratio']['mean'] if residue_data['cn_ratio']['mean'] else 'None'},
        ch4_content={residue_data['ch4_content']['mean'] if residue_data['ch4_content']['mean'] else 'None'},

        # Ranges from CSV
        bmp_range=ParameterRange(
            min={residue_data['bmp']['min'] if residue_data['bmp']['min'] else 'None'},
            mean={residue_data['bmp']['mean'] if residue_data['bmp']['mean'] else 'None'},
            max={residue_data['bmp']['max'] if residue_data['bmp']['max'] else 'None'},
            unit="{residue_data['bmp']['unit']}"
        ) if {residue_data['bmp']['mean'] is not None} else None,
        cn_ratio_range=ParameterRange(
            min={residue_data['cn_ratio']['min'] if residue_data['cn_ratio']['min'] else 'None'},
            mean={residue_data['cn_ratio']['mean'] if residue_data['cn_ratio']['mean'] else 'None'},
            max={residue_data['cn_ratio']['max'] if residue_data['cn_ratio']['max'] else 'None'}
        ) if {residue_data['cn_ratio']['mean'] is not None} else None,
        ch4_content_range=ParameterRange(
            min={residue_data['ch4_content']['min'] if residue_data['ch4_content']['min'] else 'None'},
            mean={residue_data['ch4_content']['mean'] if residue_data['ch4_content']['mean'] else 'None'},
            max={residue_data['ch4_content']['max'] if residue_data['ch4_content']['max'] else 'None'},
            unit="%"
        ) if {residue_data['ch4_content']['mean'] is not None} else None,
    ),

    availability=AvailabilityFactors(
        fc=0.80,  # TODO: Add actual availability factors
        fcp=0.50,
        fs=1.00,
        fl=0.70,
        final_availability=28.0
    ),

    operational=OperationalParameters(
        hrt="{residue_data['trh']['mean']:.0f} dias" if {residue_data['trh']['mean'] is not None} else "20-30 dias",
        temperature="35-37°C (mesofílico)",
        reactor_type="CSTR ou UASB",
        hrt_range=ParameterRange(
            min={residue_data['trh']['min'] if residue_data['trh']['min'] else 'None'},
            mean={residue_data['trh']['mean'] if residue_data['trh']['mean'] else 'None'},
            max={residue_data['trh']['max'] if residue_data['trh']['max'] else 'None'},
            unit="dias"
        ) if {residue_data['trh']['mean'] is not None} else None
    ),

    justification=f"""
    **{name}**

    **Geração:** {residue_data['generation']}
    **Sazonalidade:** {residue_data['sazonalidade']}
    **Estado Físico:** {residue_data['estado_fisico']}
    **Pré-tratamento:** {residue_data['pre_tratamento']}
    **Região Concentrada:** {residue_data['regiao']}

    Dados baseados em revisão de literatura científica.
    """,

    scenarios={{
        "Pessimista": 0.0,  # TODO: Calculate
        "Realista": 0.0,    # TODO: Calculate
        "Otimista": 0.0,    # TODO: Calculate
        "Teórico (100%)": 0.0  # TODO: Calculate
    }},

    references=[
        # TODO: Parse references from CSV
        # {repr(residue_data['referencias'])}
    ]
)
'''

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

    return str(filepath)


__all__ = [
    'parse_csv_to_residues',
    'generate_residue_file',
    'parse_range',
    'infer_category_from_fonte',
    'get_residue_icon'
]
