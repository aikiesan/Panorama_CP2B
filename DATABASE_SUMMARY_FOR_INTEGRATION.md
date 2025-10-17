# 📋 Database Architecture Summary - Quick Reference

**For Integration with External Validated Residue Databases**

---

## TL;DR - Critical Information

### Current Database Status:
- **Storage:** Python in-memory dataclasses (NO SQL database)
- **Residues:** 12 total (10 active, 2 placeholders)
- **Quality:** 87% average completeness
- **Structure:** 4 sectors, hierarchical registry system

### Key Files for Integration:
1. **Data Model:** `src/models/residue_models.py`
2. **Central Registry:** `src/data/residue_registry.py`
3. **CSV Import:** `src/utils/csv_importer.py`
4. **Validators:** `src/utils/validators.py`

---

## Database Architecture (30-Second Overview)

```
Your External DB
    ↓
CSV/JSON Adapter (to create)
    ↓
ResidueData Objects
    ↓
Registry System (src/data/residue_registry.py)
    ↓
Service Layer (calculations)
    ↓
UI Components
    ↓
Streamlit Web App
```

---

## Complete Data Model (Must Support This Schema)

### Minimum Required Fields:
```python
{
    'name': str,                    # Unique residue name
    'category': str,                # Agricultura|Pecuária|Urbano|Industrial
    'bmp': float,                   # Biochemical Methane Potential (PRIMARY)
    'ts': float,                    # Total Solids (%)
    'vs': float,                    # Volatile Solids (%)
    'moisture': float,              # Moisture (%)
    'fc': float,                    # Collection Factor (0-1)
    'fcp': float,                   # Competition Factor (0-1)
    'fs': float,                    # Seasonal Factor (0-1)
    'fl': float,                    # Logistic Factor (0-1)
    'final_availability': float,    # Calculated %
    'scenarios': {                  # 4 CH₄ potentials
        'Pessimista': float,
        'Realista': float,
        'Otimista': float,
        'Teórico (100%)': float
    },
    'references': [ScientificReference],  # Min 1
}
```

### Optional Fields (Enhance Data Quality):
- `cn_ratio`, `ph`, `cod` (chemical)
- `nitrogen`, `carbon`, `ch4_content` (composition)
- `phosphorus`, `potassium`, `protein` (nutrients)
- `hrt`, `temperature` (operational)
- `*_range` objects (MIN/MEAN/MAX validation)

---

## Current Residues by Sector

### ✅ Agricultura (3 residues - 87% quality)
- Vinhaça (100%) - 10 references
- Palha (92%) - 12 references
- Torta (96%) - 2 references

### ✅ Pecuária (4 residues - 92% quality)
- Bovinos (100%) - 10+ references
- Aves (95%) - 8 references
- Codornas (85%) - 2 references
- Suínos (90%) - 5 references

### ⚠️ Urbano (3 residues - 60% quality)
- RSU (96%) - 30+ references ✅
- RPO (20%) - Placeholder ❌
- Lodo ETE (20%) - Placeholder ❌

### ❌ Industrial (0 residues)
- Empty, awaiting implementation

---

## Validation Rules You Must Support

### Range Validation:
- ✅ `min ≤ mean ≤ max` (for all ranges)
- ✅ At least one value in range required

### Data Validation:
- ✅ BMP > 0
- ✅ 0 ≤ TS, VS, moisture ≤ 100
- ✅ 0 ≤ FC, FCp, FS, FL ≤ 1
- ✅ 0 ≤ final_availability ≤ 100
- ✅ Pessimista ≤ Realista ≤ Otimista ≤ Teórico
- ✅ Minimum 1 scientific reference
- ✅ Unique residue names per sector

### Quality Scoring:
- **80%+ = Complete** (all fields)
- **60-79% = Acceptable** (core fields)
- **<60% = Incomplete** (needs work)

---

## How Data Flows Through System

```
Your Data
    ↓ [Adapter Layer - TO CREATE]
ResidueData Objects
    ↓ [validate()]
Validation Layer (src/utils/validators.py)
    ↓ [RESIDUES_REGISTRY.update()]
Central Registry (src/data/residue_registry.py)
    ↓ [Sector aggregation]
Sector Registries (src/data/{sector}/__init__.py)
    ↓ [Services Layer]
- AvailabilityCalculator (available now)
- ScenarioManager (Phase 1.2)
- ContributionAnalyzer (Phase 1.3)
    ↓ [Visualization]
- availability_card.py
- scenario_selector.py
- contribution_chart.py
- municipality_ranking.py
- validation_panel.py
    ↓
Streamlit UI (app.py, pages/)
```

---

## Integration Checklist

### Pre-Integration:
- [ ] Format your data as JSON or CSV
- [ ] Validate: min ≤ mean ≤ max for all ranges
- [ ] Validate: Pessimista ≤ Realista ≤ Otimista ≤ Teórico
- [ ] Provide: Min 1-2 references per residue
- [ ] Target: 80%+ data completeness

### Integration Steps:
1. Create `src/utils/external_db_adapter.py`
2. Implement `adapt_external_residue()` function
3. Import your residues using adapter
4. Run validation suite
5. Test UI components
6. Verify all calculations work

### Post-Integration:
- [ ] Check registry size increased
- [ ] Verify sector counts updated
- [ ] Test all UI components work
- [ ] Check calculations are accurate
- [ ] Validate historical functionality maintained

---

## Key Metrics

### Current Data Quality:
| Sector | Residues | Quality | Status |
|--------|----------|---------|--------|
| Agricultura | 3 | 87% | ✅ Good |
| Pecuária | 4 | 92% | ✅ Good |
| Urbano | 3 | 60% | ⚠️ Needs work |
| Industrial | 0 | 0% | ❌ Not started |
| **TOTAL** | **10** | **87%** | **Acceptable** |

### Data Gaps:
- Industrial sector (0/4 residues)
- Urban sector incomplete (1/3 complete)
- COD values (sparse)
- Sub-residue aggregation (Cana)

---

## Critical API Functions

### Access Registry:
```python
from src.data.residue_registry import (
    get_residue_data,              # Get specific residue
    get_residues_by_sector,        # List all in sector
    get_available_sectors,         # List all sectors
    RESIDUES_REGISTRY              # Direct dict access
)
```

### Validate Data:
```python
from src.models.residue_models import ResidueData

residue = ResidueData(...)
is_valid, errors = residue.validate()
completeness = residue.check_completeness()
```

### Calculate Availability:
```python
from src.services.availability_calculator import AvailabilityCalculator

availability = AvailabilityCalculator.calculate(
    fc=0.80, fcp=0.65, fs=1.0, fl=0.90
)  # Returns: 25.2 (percentage)
```

---

## File Locations

### Data Files:
- `src/data/agricultura/` - 3 agriculture residues
- `src/data/pecuaria/` - 4 livestock residues
- `src/data/urbano/` - 3 urban residues (1 complete)
- `src/data/industrial/` - Empty (awaiting data)

### Models:
- `src/models/residue_models.py` - All dataclass definitions

### Access Layer:
- `src/data/residue_registry.py` - Central registry

### Utilities:
- `src/utils/csv_importer.py` - CSV parsing
- `src/utils/validators.py` - Data validation
- `src/utils/formatters.py` - Number formatting

### Services:
- `src/services/availability_calculator.py` - Core calculations

---

## What Your Database Must Provide

### Minimum:
- Residue name (unique per sector)
- BMP value + unit
- TS, VS, moisture (%)
- 4 availability factors (FC, FCp, FS, FL)
- 4 scenario potentials
- At least 1 scientific reference

### Recommended:
- ParameterRange data (min/mean/max)
- Chemical composition (C:N, pH, COD, N%, C%)
- Operational parameters (HRT, temperature)
- 2+ scientific references
- Multiple references per data point

---

## Quality Expectations

### Data Completeness:
- **Required:** ≥80% field completeness
- **Goal:** ≥90% field completeness

### Validation:
- All range data must: min ≤ mean ≤ max
- All factors must be: 0 ≤ value ≤ 1
- Scenarios must be: Pess ≤ Real ≤ Otim ≤ Teor

### References:
- Minimum: 1 reference per residue
- Preferred: 2-5 references
- Key references have: Title, Authors, Year, DOI

---

## Next Actions

1. **Prepare your data** in JSON or CSV format
2. **Map your schema** to ResidueData fields
3. **Create adapter** in `src/utils/external_db_adapter.py`
4. **Import residues** using registry API
5. **Validate results** with quality checks
6. **Test UI components** with new data

---

## Support Files Created

1. **DATABASE_ARCHITECTURE_COMPLETE.md** (12 sections)
   - Detailed data model specs
   - Complete schema documentation
   - Validation rules
   - Integration guide

2. **INTEGRATION_EXAMPLES.md** (5 examples)
   - JSON import example
   - CSV import example
   - Registry integration code
   - Validation examples
   - UI testing code

3. **This file** (Quick reference)
   - TL;DR overview
   - Critical info
   - Key metrics
   - Action checklist

---

**Status:** ✅ Ready for External Database Integration

**Questions?** Refer to DATABASE_ARCHITECTURE_COMPLETE.md for detailed specifications.
