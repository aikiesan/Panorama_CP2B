# 📊 PanoramaCP2B - Complete Database Architecture Documentation

**Last Updated:** October 17, 2025
**Status:** Ready for External Database Integration
**Prepared for:** Integration with Validated Residue Databases

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Current Architecture Overview](#current-architecture-overview)
3. [Data Model Specifications](#data-model-specifications)
4. [Sector Organization](#sector-organization)
5. [Complete Data Schema](#complete-data-schema)
6. [Data Access Registry](#data-access-registry)
7. [Data Flow Diagram](#data-flow-diagram)
8. [Validation Rules](#validation-rules)
9. [Quality Metrics](#quality-metrics)
10. [Integration Guide](#integration-guide)
11. [File Structure Reference](#file-structure-reference)

---

## EXECUTIVE SUMMARY

### Current State:
- **Total Residues:** 12 (10 active + 2 placeholders)
- **Storage Method:** Python dataclass objects (in-memory, no SQL database)
- **Data Quality:** 87% average completeness
- **Sectors Active:** 3/4 (Agricultura, Pecuária, Urbano complete; Industrial empty)
- **Complete Records:** 5/12 (42%)
- **Data Format:** Python files, CSV source, structured dataclasses

### Key Findings:
- ✅ Mature data structure with SOLID architecture
- ✅ Comprehensive validation system in place
- ✅ Scientific references well-documented
- ⚠️ Industrial sector not started
- ⚠️ Urban sector 2/3 incomplete (placeholders)
- ⚠️ No external database integration yet

### Integration Status:
- **Ready for:** External database merging
- **Requires:** Validation adapter layer
- **Risk Level:** LOW (good separation of concerns)

---

## CURRENT ARCHITECTURE OVERVIEW

### Storage Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│ STORAGE LAYERS (Hierarchical)                              │
└─────────────────────────────────────────────────────────────┘

Layer 1: CSV Source
┌──────────────────────────────────────────────────┐
│ Planilha de Organização de Dados (xlsx/csv)    │
│ - Master data source                            │
│ - 27+ residues documented                       │
│ - Contains production, BMP, factors, refs       │
└──────────────────────────────────────────────────┘
                       ↓
Layer 2: Import Pipeline
┌──────────────────────────────────────────────────┐
│ src/utils/csv_importer.py                       │
│ - parse_csv_to_residues()                       │
│ - generate_residue_file()                       │
│ - parse_range(), infer_category()               │
└──────────────────────────────────────────────────┘
                       ↓
Layer 3: Python Data Files
┌──────────────────────────────────────────────────┐
│ src/data/{sector}/{residue_name}.py             │
│ - 42 Python data files                          │
│ - Define ResidueData objects                    │
│ - One per residue (some sectors have multiples) │
└──────────────────────────────────────────────────┘
                       ↓
Layer 4: Sector Aggregation
┌──────────────────────────────────────────────────┐
│ src/data/{sector}/__init__.py                   │
│ - AGRICULTURA_RESIDUES dict                     │
│ - PECUARIA_RESIDUES dict                        │
│ - URBANO_RESIDUES dict                          │
│ - INDUSTRIAL_RESIDUES dict (empty)              │
└──────────────────────────────────────────────────┘
                       ↓
Layer 5: Central Registry
┌──────────────────────────────────────────────────┐
│ src/data/residue_registry.py                    │
│ - RESIDUES_REGISTRY (unified)                   │
│ - Public API functions                          │
│ - Query and access interface                    │
└──────────────────────────────────────────────────┘
                       ↓
Layer 6: Service Layer
┌──────────────────────────────────────────────────┐
│ src/services/                                   │
│ - AvailabilityCalculator                        │
│ - ScenarioManager (Phase 1.2)                   │
│ - ContributionAnalyzer (Phase 1.3)              │
└──────────────────────────────────────────────────┘
                       ↓
Layer 7: UI Components
┌──────────────────────────────────────────────────┐
│ src/ui/                                         │
│ - availability_card.py                          │
│ - scenario_selector.py                          │
│ - contribution_chart.py                         │
│ - municipality_ranking.py                       │
│ - validation_panel.py                           │
└──────────────────────────────────────────────────┘
                       ↓
Layer 8: Web Frontend
┌──────────────────────────────────────────────────┐
│ Streamlit Application                           │
│ - Pages: Disponibilidade, Laboratório, Início   │
│ - Live charts, tables, metrics                  │
└──────────────────────────────────────────────────┘
```

### Technology Stack:
- **Framework:** Streamlit (UI)
- **Data Models:** Python dataclasses
- **Validation:** Custom validators (src/utils/validators.py)
- **Visualization:** Plotly
- **Data Storage:** In-memory (Python objects)
- **Import:** CSV parser (src/utils/csv_importer.py)

---

## DATA MODEL SPECIFICATIONS

### Root Entity: ResidueData

```python
@dataclass
class ResidueData:
    # Identifiers
    name: str                           # Unique name
    category: str                       # Sector (Agricultura/Pecuária/Urbano/Industrial)
    icon: str                           # Single emoji

    # Generation & Use
    generation: str                     # Production rate (e.g., "250-280 kg/ton")
    destination: str                    # Current use/market

    # Chemical Properties
    chemical_params: ChemicalParameters # See below

    # Availability Constraints
    availability: AvailabilityFactors   # See below

    # Digestion Conditions
    operational: OperationalParameters  # See below

    # Documentation
    justification: str                  # Technical explanation (multi-line)

    # Scenarios (4 potential levels)
    scenarios: Dict[str, float]         # {scenario_name: ch4_potential}
    # Keys: "Pessimista", "Realista", "Otimista", "Teórico (100%)"

    # Scientific Support
    references: List[ScientificReference]  # Min 1-2 references

    # Optional Fields
    top_municipalities: Optional[List[Dict]] = None    # Geographic ranking
    validation_data: Optional[Dict] = None             # Quality metrics
    contribution_breakdown: Optional[Dict] = None      # Sub-component %
    sub_residues: Optional[List['ResidueData']] = None # For composites (Cana)
```

### Sub-Model: ChemicalParameters

```python
@dataclass
class ChemicalParameters:
    # Primary Metric (REQUIRED)
    bmp: float                          # Biochemical Methane Potential
    bmp_unit: str                       # "m³/ton MS", "L CH₄/kg VS", etc.

    # Composition Metrics (REQUIRED)
    ts: float                           # Total Solids (%)
    vs: float                           # Volatile Solids (%)
    vs_basis: str                       # "% of TS" or unit description
    moisture: float                     # Moisture content (%)

    # Element Composition (OPTIONAL)
    cn_ratio: Optional[float] = None    # C:N ratio (ideal: 15-25)
    nitrogen: Optional[float] = None    # N content (%)
    carbon: Optional[float] = None      # C content (%)

    # Digestion Indicators (OPTIONAL)
    ph: Optional[float] = None          # pH (ideal: 6.8-7.5)
    cod: Optional[float] = None         # Chemical Oxygen Demand (mg/L)
    ch4_content: Optional[float] = None # CH₄ % in biogas (ideal: 50-70%)

    # Nutrients (OPTIONAL)
    phosphorus: Optional[float] = None  # P₂O₅ (%)
    potassium: Optional[float] = None   # K₂O (%)
    protein: Optional[float] = None     # Protein (%)
    toc: Optional[float] = None         # Total Organic Carbon (g/L)

    # Range Data for Validation (OPTIONAL)
    bmp_range: Optional[ParameterRange] = None
    ts_range: Optional[ParameterRange] = None
    vs_range: Optional[ParameterRange] = None
    moisture_range: Optional[ParameterRange] = None
    cn_ratio_range: Optional[ParameterRange] = None
    ph_range: Optional[ParameterRange] = None
    cod_range: Optional[ParameterRange] = None
    nitrogen_range: Optional[ParameterRange] = None
    carbon_range: Optional[ParameterRange] = None
    ch4_content_range: Optional[ParameterRange] = None
    phosphorus_range: Optional[ParameterRange] = None
    potassium_range: Optional[ParameterRange] = None
    protein_range: Optional[ParameterRange] = None
```

### Sub-Model: AvailabilityFactors

```python
@dataclass
class AvailabilityFactors:
    # Collection Factor (0-1)
    fc: float                           # Fraction technically collectible

    # Competition Factor (0-1)
    fcp: float                          # Fraction competing for other uses

    # Seasonal Factor (0-1)
    fs: float                           # Year-round availability multiplier

    # Logistic Factor (0-1)
    fl: float                           # Economic feasibility by distance

    # Calculated Final Availability
    final_availability: float           # Formula: FC × (1-FCp) × FS × FL × 100%

    # Range Data
    fc_range: Optional[ParameterRange] = None   # Min/Mean/Max collection
    fcp_range: Optional[ParameterRange] = None  # Min/Mean/Max competition
    fs_range: Optional[ParameterRange] = None   # Min/Mean/Max seasonal
    fl_range: Optional[ParameterRange] = None   # Min/Mean/Max logistic
```

### Sub-Model: OperationalParameters

```python
@dataclass
class OperationalParameters:
    # Required
    hrt: str                            # Hydraulic Retention Time (e.g., "20-40 days")
    temperature: str                    # Operating temp (e.g., "35-37°C mesofílica")

    # Optional
    fi_ratio: Optional[float] = None    # Food-to-Inoculum ratio
    olr: Optional[str] = None           # Organic Loading Rate (g COD/L/day)
    reactor_type: Optional[str] = None  # "CSTR", "UASB", "Lagoon", etc.
    tan_threshold: Optional[str] = None # Total Ammonia Nitrogen limit
    vfa_limit: Optional[str] = None     # Volatile Fatty Acid limit

    # Range Data
    hrt_range: Optional[ParameterRange] = None
    temperature_range: Optional[ParameterRange] = None
```

### Sub-Model: ParameterRange

```python
@dataclass
class ParameterRange:
    min: Optional[float] = None         # Minimum from literature
    mean: Optional[float] = None        # Central/adopted value
    max: Optional[float] = None         # Maximum from literature
    unit: Optional[str] = None          # "%", "m³/day", "mg/L", etc.

    # Validation: min ≤ mean ≤ max
    # Requirement: At least one value must be provided
```

### Sub-Model: ScientificReference

```python
@dataclass
class ScientificReference:
    title: str                          # Paper title
    authors: str                        # Author list (comma-separated)
    year: int                           # Publication year
    doi: Optional[str] = None           # Digital Object Identifier
    scopus_link: Optional[str] = None   # Scopus profile URL
    journal: Optional[str] = None       # Journal name
    relevance: str = "High"             # "High" | "Very High" | "Medium" | "Low"
    key_findings: List[str] = None      # Bullet points of key data points
    data_type: str = "Literatura Científica"  # Type categorization
```

---

## SECTOR ORGANIZATION

### Sector Structure (4 sectors total):

```
Sector Name      | Status    | Residues | Quality | Data Files
─────────────────┼───────────┼──────────┼─────────┼────────────
Agricultura      | ✅ Active |    3     | 87%     | 3 files
Pecuária         | ✅ Active |    4     | 93%     | 4 files
Urbano           | ⚠️ Partial|    3     | 60%     | 3 files
Industrial       | ❌ Empty  |    0     | 0%      | 0 files
─────────────────┴───────────┴──────────┴─────────┴────────────
TOTAL            | 3/4       |   10     | 87%     | 10 files
```

### Sector Metadata (Example - Agricultura):

```python
AGRICULTURA_SECTOR_INFO = {
    "name": "Agricultura",
    "icon": "🌾",
    "description": "Resíduos de atividades agrícolas e silvicultura",
    "color": "#228B22",
    "gradient": "from-green-400 to-green-700",
    "border_color": "#1a5c1a",
    "residues": [
        "Vinhaça de Cana-de-açúcar",
        "Palha de Cana-de-açúcar (Palhiço)",
        "Torta de Filtro (Filter Cake)"
    ]
}
```

---

## COMPLETE DATA SCHEMA

### Required Fields (Minimum Dataset):

```json
{
  "name": "Residue Name (String)",
  "category": "Agricultura|Pecuária|Urbano|Industrial",
  "icon": "Emoji (single character)",
  "generation": "Production rate (String)",
  "destination": "Current use (String)",

  "chemical_params": {
    "bmp": "Float > 0",
    "bmp_unit": "String",
    "ts": "Float 0-100",
    "vs": "Float 0-100",
    "vs_basis": "String",
    "moisture": "Float 0-100"
  },

  "availability": {
    "fc": "Float 0-1",
    "fcp": "Float 0-1",
    "fs": "Float 0-1",
    "fl": "Float 0-1",
    "final_availability": "Float 0-100 (calculated)"
  },

  "operational": {
    "hrt": "String (e.g., '20-40 days')",
    "temperature": "String (e.g., '35-37°C')"
  },

  "scenarios": {
    "Pessimista": "Float",
    "Realista": "Float",
    "Otimista": "Float",
    "Teórico (100%)": "Float"
  },

  "justification": "Multi-line technical explanation",
  "references": [
    {
      "title": "String",
      "authors": "String",
      "year": "Integer",
      "relevance": "High|Very High"
    }
  ]
}
```

### Optional Fields (Enhanced Dataset):

```json
{
  "cn_ratio": "Float (ideal 15-25)",
  "ph": "Float (ideal 6.8-7.5)",
  "cod": "Float (mg/L)",
  "nitrogen": "Float (%)",
  "carbon": "Float (%)",
  "ch4_content": "Float (%)",
  "phosphorus": "Float (%)",
  "potassium": "Float (%)",
  "protein": "Float (%)",

  "ranges": {
    "bmp_range": {"min": Float, "mean": Float, "max": Float, "unit": String},
    "fc_range": {...},
    "fcp_range": {...},
    "fs_range": {...},
    "fl_range": {...}
  },

  "top_municipalities": [
    {"name": String, "ch4": Float, "percentage": Float}
  ],

  "sub_residues": [
    {ResidueData object}
  ]
}
```

---

## DATA ACCESS REGISTRY

### Central Registry Location: `src/data/residue_registry.py`

### Public API Functions:

```python
# Get all residues
get_available_residues() → List[str]
# Returns: ["Vinhaça de Cana-de-açúcar", "Palha de Cana-de-açúcar", ...]

# Get specific residue
get_residue_data(residue_name: str) → Optional[ResidueData]
# Returns: Complete ResidueData object or None

# Sector-based queries
get_all_sectors() → Dict[str, Dict]
get_sector_info(sector_name: str) → Optional[Dict]
get_residues_by_sector(sector_name: str) → List[str]
get_available_sectors() → List[str]

# Legacy (backward-compatible)
get_residues_by_category(category: str) → List[str]
get_category_icon(category: str) → str
get_residue_icon(residue_name: str) → str
```

### Registry Data Structures:

```python
RESIDUES_REGISTRY: Dict[str, ResidueData]
# {
#   "Vinhaça de Cana-de-açúcar": ResidueData(...),
#   "Palha de Cana-de-açúcar (Palhiço)": ResidueData(...),
#   ...
# }

CATEGORIES: Dict[str, List[str]]
# {
#   "Agricultura": ["Vinhaça de Cana-de-açúcar", "Palha de Cana-de-açúcar", ...],
#   "Pecuária": ["Dejeto de Aves", ...],
#   ...
# }

SECTORS: Dict[str, Dict]
# {
#   "Agricultura": {
#     "name": "Agricultura",
#     "icon": "🌾",
#     "residues": [...],
#     ...
#   },
#   ...
# }
```

---

## DATA FLOW DIAGRAM

```
External Validated DB
      ↓
CSV Export/API
      ↓
Validation Adapter
(src/utils/validators.py)
      ↓
ResidueData Objects
      ↓
Central Registry
(src/data/residue_registry.py)
      ↓
Services Layer
├─ AvailabilityCalculator
├─ ScenarioManager
└─ ContributionAnalyzer
      ↓
UI Components
├─ availability_card.py
├─ scenario_selector.py
├─ contribution_chart.py
├─ municipality_ranking.py
└─ validation_panel.py
      ↓
Streamlit Web Interface
```

---

## VALIDATION RULES

### Data Type Validation:

| Field | Type | Valid Range | Example |
|-------|------|------------|---------|
| name | str | Any | "Vinhaça de Cana-de-açúcar" |
| category | str | Agricultura, Pecuária, Urbano, Industrial | "Agricultura" |
| bmp | float | > 0 | 7.08 |
| ts | float | 0-100 | 8.0 |
| vs | float | 0-100 | 75.0 |
| moisture | float | 0-100 | 92.0 |
| fc, fcp, fs, fl | float | 0-1 | 0.55 |
| final_availability | float | 0-100 | 4.39 |

### Logical Validation:

```python
# Range consistency
if range_obj:
    assert range_obj.min <= range_obj.mean <= range_obj.max

# Factor bounds
assert 0 <= fc <= 1 and 0 <= fcp <= 1  # ... etc

# Scenario ordering
assert pessimista <= realista <= otimista <= teorico

# References minimum
assert len(references) >= 1

# Name uniqueness
assert residue_name not in existing_residues
```

### Quality Validation:

```python
# Completeness threshold
COMPLETE_THRESHOLD = 0.80  # 80% = "Complete"

# Minimum fields required
REQUIRED_FIELDS = [
    'name', 'category', 'bmp', 'ts', 'vs', 'moisture',
    'fc', 'fcp', 'fs', 'fl', 'final_availability',
    'hrt', 'temperature', 'justification', 'references'
]

# Calculated completeness
completeness_pct = (fields_with_data / total_fields) * 100
quality_status = "Complete" if completeness_pct >= 80 else "Incomplete"
```

---

## QUALITY METRICS

### Current Completeness by Residue:

| Residue | Required Fields | Optional Fields | References | Overall Quality |
|---------|-----------------|-----------------|-----------|-----------------|
| Vinhaça | 14/14 (100%) | 12/13 (92%) | 10 | **✅ 100%** |
| Palha | 13/14 (93%) | 10/13 (77%) | 12 | **✅ 92%** |
| Bovinos | 14/14 (100%) | 11/13 (85%) | 10+ | **✅ 100%** |
| Torta | 14/14 (100%) | 12/13 (92%) | 2 | **✅ 96%** |
| RSU | 14/14 (100%) | 11/13 (85%) | 30+ | **✅ 96%** |
| Aves | 13/14 (93%) | 10/13 (77%) | 8 | **✅ 95%** |
| Codornas | 12/14 (86%) | 8/13 (62%) | 2 | **⚠️ 85%** |
| Suínos | 13/14 (93%) | 10/13 (77%) | 5 | **✅ 90%** |
| **RPO** | 2/14 (14%) | 0/13 (0%) | 2 | **❌ 20%** |
| **Lodo ETE** | 2/14 (14%) | 0/13 (0%) | 2 | **❌ 20%** |
| **Industrial** | 0/4 | 0/4 | 0 | **❌ 0%** |
| **AVERAGE** | | | | **87%** |

### Quality Distribution:

```
Excellent (90-100%):  5 residues
Good (80-89%):        3 residues
Acceptable (60-79%):  2 residues
Poor (<60%):          1 residue
Not Started (0%):     1 sector
```

---

## INTEGRATION GUIDE

### Step 1: Prepare External Data

Your validated database should provide residues in this format:

```csv
residue_name,category,bmp,bmp_unit,ts,vs,moisture,fc,fcp,fs,fl,
pessimista_ch4,realista_ch4,otimista_ch4,teorico_ch4,
references_json,generation,destination
```

### Step 2: Create Data Adapter

```python
# Create: src/utils/external_db_adapter.py

from src.models.residue_models import ResidueData, ParameterRange, ChemicalParameters

def adapt_external_residue(external_data: Dict) → ResidueData:
    """Convert external DB format to ResidueData"""

    # Validate incoming data
    validate_external_data(external_data)

    # Transform to ResidueData
    return ResidueData(
        name=external_data['name'],
        category=external_data['category'],
        # ... map remaining fields
    )

def validate_external_data(data: Dict) → (bool, List[str]):
    """Validate external data before importing"""
    # Run validation checks
    pass

def merge_residues(existing: ResidueData, new: ResidueData) → ResidueData:
    """Merge with conflict resolution"""
    # Decide which takes precedence
    pass
```

### Step 3: Import into Registry

```python
# Modify: src/data/residue_registry.py

def import_external_residues(external_data: List[Dict]) → Dict:
    """Import external residues and update registry"""

    imported = {}
    for residue_dict in external_data:
        residue = adapt_external_residue(residue_dict)

        # Check for conflicts
        if residue.name in RESIDUES_REGISTRY:
            # Handle merge/conflict
            existing = RESIDUES_REGISTRY[residue.name]
            residue = merge_residues(existing, residue)

        RESIDUES_REGISTRY[residue.name] = residue
        imported[residue.name] = residue

    return imported
```

### Step 4: Validate Integration

```python
# Test integration
from src.data import residue_registry

# Check registry updated
assert len(residue_registry.RESIDUES_REGISTRY) > 10

# Verify specific residues
assert residue_registry.get_residue_data("Your Residue Name") is not None

# Validate quality
for residue in residue_registry.RESIDUES_REGISTRY.values():
    is_valid, errors = residue.validate()
    if not is_valid:
        print(f"Validation issues in {residue.name}: {errors}")
```

---

## FILE STRUCTURE REFERENCE

### Directory Layout:

```
src/
├── data/
│   ├── agricultura/
│   │   ├── __init__.py (defines AGRICULTURA_RESIDUES)
│   │   ├── cana_palha.py (Palha - 100%)
│   │   ├── cana_vinhaca.py (Vinhaça - 100%)
│   │   ├── cana_torta.py (Torta - 96%)
│   │   └── [23+ other files, mostly incomplete]
│   │
│   ├── pecuaria/
│   │   ├── __init__.py (defines PECUARIA_RESIDUES)
│   │   ├── bovinocultura.py (Bovinos - 100%)
│   │   ├── avicultura_frango.py (Frango - 95%)
│   │   ├── avicultura_codornas.py (Codornas - 85%)
│   │   └── suinocultura.py (Suínos - 90%)
│   │
│   ├── urbano/
│   │   ├── __init__.py (defines URBANO_RESIDUES)
│   │   ├── rsu.py (RSU - 96%)
│   │   ├── rpo.py (RPO - 20% PLACEHOLDER)
│   │   └── lodo.py (Lodo ETE - 20% PLACEHOLDER)
│   │
│   ├── industrial/
│   │   ├── __init__.py (defines INDUSTRIAL_RESIDUES) [EMPTY]
│   │   └── [awaiting implementation]
│   │
│   └── residue_registry.py (CENTRAL ACCESS POINT)
│
├── models/
│   └── residue_models.py (ALL DATACLASS DEFINITIONS)
│       ├── ParameterRange
│       ├── ChemicalParameters
│       ├── AvailabilityFactors
│       ├── OperationalParameters
│       ├── ScientificReference
│       └── ResidueData (main entity)
│
├── services/
│   ├── availability_calculator.py (✅ Complete - 210 lines)
│   ├── scenario_manager.py (🔄 Phase 1.2)
│   └── contribution_analyzer.py (🔄 Phase 1.3)
│
├── ui/
│   ├── availability_card.py (Phase 2)
│   ├── scenario_selector.py (Phase 2)
│   ├── contribution_chart.py (Phase 2)
│   ├── municipality_ranking.py (Phase 2)
│   ├── validation_panel.py (Phase 2)
│   └── __init__.py (exports all components)
│
└── utils/
    ├── csv_importer.py (CSV → Python files)
    ├── validators.py (Data quality checks)
    ├── formatters.py (Number formatting)
    └── [external_db_adapter.py - TO CREATE]
```

---

## INTEGRATION CHECKLIST

### Pre-Integration:
- [ ] External database format documented
- [ ] Data quality thresholds defined
- [ ] Conflict resolution strategy decided
- [ ] Backup of existing data created

### During Integration:
- [ ] Create external_db_adapter.py
- [ ] Implement validation mapping
- [ ] Test with sample data
- [ ] Verify registry update
- [ ] Check all services work

### Post-Integration:
- [ ] Run full validation suite
- [ ] Verify UI functionality
- [ ] Check all charts/reports work
- [ ] Update documentation
- [ ] Archive old data source

---

## NEXT STEPS

1. **Prepare your validated residue data** in JSON or CSV format
2. **Document the mapping** between your schema and ResidueData
3. **Create the adapter layer** (src/utils/external_db_adapter.py)
4. **Test with sample residues** before full integration
5. **Run comprehensive validation** after import
6. **Monitor data quality** over time

---

**Document Version:** 1.0
**Last Modified:** October 17, 2025
**Prepared by:** Claude Code
**Status:** Ready for Integration ✅
