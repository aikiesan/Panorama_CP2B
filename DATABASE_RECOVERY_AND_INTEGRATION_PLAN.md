# Database Recovery & Integration Plan
**Date**: October 21, 2025
**Status**: ✅ RECOVERY COMPLETE | 📋 INTEGRATION PLANNED

---

## Executive Summary

Successfully recovered PanoramaCP2B database to working state from **October 20, 2025 at 13:11** (commit `521b61c`). The application is now functional with 645 municipalities and complete biogas potential data. This document provides a detailed, SOLID-principle-based plan for integrating validated data from Jupyter notebooks.

---

## Phase 1: Recovery Status ✅ COMPLETED

### Actions Taken

1. **Git Recovery**
   - Identified last working commit: `521b61c` (Oct 20, 13:11)
   - Created safety backup branch: `broken-state-backup`
   - Hard reset to working commit: `git reset --hard 521b61c`
   - Cleaned untracked files from failed fix attempts

2. **Configuration Restoration**
   - Created `.streamlit/secrets.toml` with database path
   - Verified database file exists: `data/cp2b_maps.db` (700KB)

3. **Verification Results**
   - ✅ Database loads successfully
   - ✅ 645 municipalities with biogas potential data
   - ✅ Total biogas potential: **48.8 billion m³/year**
   - ✅ All municipality aggregations working correctly
   - ❌ Residue detail tables empty (expected - to be populated in integration)

### Current Database State

**Working Tables:**
- `municipalities` - 645 rows, 28 columns (complete biogas potentials by sector)
- `conversion_factors` - Data conversion references
- `dados_laboratoriais` - Laboratory data
- `dados_socioeconomicos` - Socioeconomic data
- `uso_solo_mapbiomas` - Land use data

**Empty Tables (Ready for Population):**
- `residuos_agricolas` - 0 rows (schema: 11 columns)
- `residuos_pecuarios` - 0 rows
- `residuos_urbanos` - 0 rows
- `residuos_industriais` - 0 rows

---

## Phase 2: Validated Data Analysis ✅ COMPLETED

### Data Sources Located

**Primary Validated Data:**
1. `C:\Users\Lucas\Documents\CP2B\Validacao_dados\06_RESULTADO_FINAL_VALIDADO\`
   - `POTENCIAL_3CENARIOS_VALIDADO_20251020_151634.csv` (Main data)
   - Contains: 3 scenarios (Pessimistic, Realistic, Optimistic) with sector breakdowns

2. `C:\Users\Lucas\Documents\CP2B\Validacao_dados\05_RESULTADO_FINAL\`
   - `FATORES_DISPONIBILIDADE_COMPLETOS.csv` - **38 residues** with SAF factors
   - `FATORES_COMPLETOS_TODOS.csv` - Complete factor calculations
   - `POTENCIAL_3CENARIOS_20251020_150841.csv` - 3 scenario calculations
   - `POTENCIAL_COMPLETO_SP_20251020_150441.csv` - Complete SP state potential

3. `C:\Users\Lucas\Documents\CP2B\Validacao_dados\Referências_Organizadas_ABNT.ipynb`
   - ABNT-formatted scientific references

### Data Structure

**POTENCIAL_3CENARIOS_VALIDADO.csv Columns:**
- Municipality identifiers: `codigo_municipio`, `nome_municipio`, `area_km2`
- Theoretical potential: `ch4_teorico`
- Pessimistic scenario: `ch4_pes_agricultura`, `ch4_pes_pecuaria`, `ch4_pes_urbano`, `ch4_pes_total`, `energia_pes_mwh`, `energia_pes_tj`
- Realistic scenario: `ch4_rea_agricultura`, `ch4_rea_pecuaria`, `ch4_rea_urbano`, `ch4_rea_total`, `energia_rea_mwh`, `energia_rea_tj`
- Optimistic scenario: `ch4_oti_agricultura`, `ch4_oti_pecuaria`, `ch4_oti_urbano`, `ch4_oti_total`, `energia_oti_mwh`, `energia_oti_tj`

**FATORES_DISPONIBILIDADE_COMPLETOS.csv Columns:**
- Residue identifiers: `codigo`, `nome`, `setor`
- SAF factors: `bmp_medio`, `fc_medio`, `fcp_medio`, `fs_medio`, `fl_medio`, `fator_total`

---

## Phase 3: Integration Plan (DETAILED ROADMAP)

### Design Principles

This integration follows **SOLID principles** to prevent the issues that occurred yesterday:

1. **Single Responsibility (S)**: Each module has ONE clear purpose
2. **Open/Closed (O)**: Extend functionality without modifying existing code
3. **Liskov Substitution (L)**: Data models are interchangeable
4. **Interface Segregation (I)**: Focused interfaces for data operations
5. **Dependency Inversion (D)**: Business logic independent of data sources

### Integration Architecture

```
scripts/
└── database_integration/        # New folder for integration scripts
    ├── __init__.py
    ├── data_loaders.py          # S: Load CSV/Excel files
    ├── data_validators.py       # S: Validate data quality
    ├── data_transformers.py     # S: Transform to database schema
    ├── database_inserters.py    # S: Insert into SQLite (with transactions)
    └── integration_runner.py    # Orchestrates the pipeline
```

### Step-by-Step Integration Process

#### Step 1: Create Integration Infrastructure (1 hour)

**Objective**: Build reusable, testable modules following SOLID

**Files to Create:**
1. `scripts/database_integration/__init__.py` - Package marker
2. `scripts/database_integration/data_loaders.py`
   - `load_scenario_data(file_path: str) -> pd.DataFrame`
   - `load_availability_factors(file_path: str) -> pd.DataFrame`
   - `load_references(notebook_path: str) -> pd.DataFrame`

3. `scripts/database_integration/data_validators.py`
   - `validate_municipality_codes(df: pd.DataFrame) -> bool`
   - `validate_saf_factors(df: pd.DataFrame) -> bool`
   - `validate_numeric_columns(df: pd.DataFrame, columns: list) -> bool`
   - `generate_validation_report(df: pd.DataFrame) -> dict`

4. `scripts/database_integration/data_transformers.py`
   - `transform_scenario_to_municipalities(df: pd.DataFrame) -> pd.DataFrame`
   - `transform_factors_to_residues(df: pd.DataFrame) -> dict`
   - `normalize_residue_names(df: pd.DataFrame) -> pd.DataFrame`

5. `scripts/database_integration/database_inserters.py`
   - `insert_municipalities_with_scenarios(engine, df: pd.DataFrame, backup=True)`
   - `insert_availability_factors(engine, df: pd.DataFrame, backup=True)`
   - `insert_references(engine, df: pd.DataFrame, backup=True)`
   - Uses **transactions**: commit on success, rollback on error

6. `scripts/database_integration/integration_runner.py`
   - `run_integration(dry_run=True, backup=True, step='all')`
   - Orchestrates entire pipeline
   - Provides detailed logging and progress tracking

**Key Features:**
- All functions have type hints
- All functions have docstrings (Args, Returns, Raises)
- Each module < 200 lines of code (SOLID SRP)
- No circular dependencies
- Easy to test individually

#### Step 2: Dry Run Integration (30 minutes)

**Objective**: Validate data WITHOUT touching database

**Actions:**
1. Run `integration_runner.py --dry-run`
2. Generate validation report:
   - Municipality code matches: Current DB vs Validated CSV
   - Residue name mismatches (current vs validated)
   - Missing data indicators
   - Data type inconsistencies
3. Review report and fix mapping issues

**Expected Output:**
```
=== DRY RUN INTEGRATION REPORT ===
✓ Loaded 645 municipalities from validated data
✓ Loaded 38 residue availability factors
✓ Municipality codes: 645/645 matched (100%)
⚠ Residue name mismatches: 3 found
  - "Bagaco de cana" vs "Bagaço de cana-de-açúcar"
  - "RSU" vs "Resíduos Sólidos Urbanos"
  - "RPO" vs "Resíduos de Processamento de Origem Animal"
✓ Numeric columns validated: 22/22 passed
✓ SAF factors validated: 38/38 passed

RECOMMENDATION: Create name mapping file before proceeding
```

#### Step 3: Create Name Mapping (15 minutes)

**Objective**: Standardize residue names between systems

**File to Create:**
`scripts/database_integration/residue_name_mapping.json`
```json
{
  "BAGACO": "Bagaço de cana-de-açúcar",
  "RSU": "Resíduos Sólidos Urbanos",
  "RPO": "Resíduos de Processamento de Origem Animal",
  ...
}
```

**Update:**
- `data_transformers.py` to use this mapping
- Run dry-run again to verify 100% match

#### Step 4: Database Backup (5 minutes)

**Objective**: Multiple safety backups before integration

**Actions:**
1. Manual backup: `cp data/cp2b_maps.db data/cp2b_maps_backup_$(date +%Y%m%d_%H%M%S).db`
2. Automated backup in script: `database_inserters.py` creates timestamped backup
3. Git commit current state: `git add . && git commit -m "chore: Pre-integration checkpoint"`

#### Step 5: Phased Integration (1 hour)

**Objective**: Integrate data incrementally with validation checkpoints

**Phase 5.1: Scenario Data Integration**
```bash
python scripts/database_integration/integration_runner.py --step scenarios --backup
```
- Updates `municipalities` table with 3 scenarios
- Adds columns: `scenario_pessimistic`, `scenario_realistic`, `scenario_optimistic`
- Validates: Sum of sectors equals total for each scenario
- **Checkpoint**: Run Streamlit app, verify municipalities page works

**Phase 5.2: Availability Factors Integration**
```bash
python scripts/database_integration/integration_runner.py --step factors --backup
```
- Populates `residuos_agricolas`, `residuos_pecuarios`, `residuos_urbanos`, `residuos_industriais`
- Inserts 38 residues with complete SAF factors (FC, FCp, FS, FL)
- Validates: All factors in valid range (0-1)
- **Checkpoint**: Query database, verify residue counts

**Phase 5.3: References Integration**
```bash
python scripts/database_integration/integration_runner.py --step references --backup
```
- Updates `references` table from ABNT notebook
- Links references to residues via foreign keys
- Validates: All referenced residues exist
- **Checkpoint**: Run references page in Streamlit

**Phase 5.4: Full Validation**
```bash
python scripts/database_integration/integration_runner.py --step validate
```
- Runs comprehensive database integrity checks
- Verifies all foreign keys
- Checks for orphaned records
- Validates data ranges and types
- Generates final integration report

#### Step 6: Streamlit App Testing (30 minutes)

**Objective**: Verify all pages work with integrated data

**Test Cases:**
1. **Homepage (app.py)**
   - ✓ Loads without errors
   - ✓ Displays updated KPIs

2. **Page 1: Disponibilidade**
   - ✓ Municipality selector works
   - ✓ Scenario selector shows 3 scenarios (Pessimistic, Realistic, Optimistic)
   - ✓ Charts render correctly
   - ✓ Municipality ranking displays

3. **Page 2: Parametros Quimicos**
   - ✓ Residue selector shows 38 residues
   - ✓ Chemical parameters display correctly
   - ✓ SAF factors visible (FC, FCp, FS, FL)

4. **Page 3: Referencias Cientificas**
   - ✓ References organized by sector
   - ✓ ABNT formatting correct
   - ✓ Links to residues work

5. **Page 4: Comparacao Laboratorial**
   - ✓ Lab data comparison works
   - ✓ Charts render correctly

**If ANY test fails:**
- STOP immediately
- Run: `git reset --hard HEAD^` (undo integration commit)
- Restore database backup
- Review error logs
- Fix issue in integration scripts
- Re-run from Step 2 (Dry Run)

#### Step 7: Documentation & Commit (20 minutes)

**Objective**: Document successful integration for future reference

**Actions:**
1. Generate final integration report: `INTEGRATION_SUCCESS_REPORT.md`
2. Update `CLAUDE.md` with new database schema
3. Update `DATABASE_ARCHITECTURE_COMPLETE.md`
4. Git commit with detailed message:
```bash
git add .
git commit -m "feat: Integrate validated biogas potential data with 3 scenarios

- Add 38 residues with complete SAF factors (FC, FCp, FS, FL)
- Integrate municipality data with pessimistic, realistic, optimistic scenarios
- Populate residue tables (agricolas, pecuarios, urbanos, industriais)
- Add ABNT-formatted scientific references
- Update database schema with scenario columns

Closes #[issue-number] (if applicable)
Validated with: 645 municipalities, 38 residues, 100% data integrity"
```

---

## Phase 4: Post-Integration Maintenance

### Monitoring Checklist

- [ ] Database file size (should be ~2-3MB after integration)
- [ ] Query performance (municipalities page < 2s load time)
- [ ] Cache hit rates (Streamlit @st.cache_data effectiveness)
- [ ] Error logs (check for any data access issues)

### Rollback Procedure

**If integration causes issues AFTER commit:**

1. **Immediate Rollback:**
   ```bash
   git reset --hard 521b61c  # Return to current working state
   cp data/cp2b_maps_backup_YYYYMMDD_HHMMSS.db data/cp2b_maps.db
   ```

2. **Investigation:**
   - Review integration logs
   - Check validation reports
   - Identify root cause

3. **Fix & Retry:**
   - Update integration scripts
   - Run dry-run again
   - Re-attempt integration

---

## Risk Assessment & Mitigation

### Risks Identified

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Residue name mismatch | HIGH | HIGH | Name mapping file (Step 3) + validation |
| Data type incompatibility | MEDIUM | MEDIUM | Type validation in data_validators.py |
| Foreign key violations | LOW | HIGH | Referential integrity checks in Step 5.4 |
| Database corruption | LOW | CRITICAL | Multiple backups (manual + automated) |
| Cache invalidation issues | MEDIUM | LOW | Clear Streamlit cache after integration |
| SOLID principle violations | MEDIUM | HIGH | Code review before each step |

### Success Criteria

✅ Integration is successful when:
1. All 645 municipalities load in Disponibilidade page
2. All 38 residues display in Parametros Quimicos page
3. 3 scenarios (Pessimistic, Realistic, Optimistic) selectable
4. No errors in Streamlit console
5. Database size < 5MB
6. All Streamlit pages load in < 3 seconds
7. No SOLID principle violations (verified by code review)

---

## Timeline Estimate

| Phase | Estimated Time | Complexity |
|-------|---------------|------------|
| Step 1: Create Infrastructure | 1 hour | MEDIUM |
| Step 2: Dry Run | 30 minutes | LOW |
| Step 3: Name Mapping | 15 minutes | LOW |
| Step 4: Backup | 5 minutes | LOW |
| Step 5: Phased Integration | 1 hour | HIGH |
| Step 6: Testing | 30 minutes | MEDIUM |
| Step 7: Documentation | 20 minutes | LOW |
| **TOTAL** | **~3.5 hours** | **MEDIUM-HIGH** |

---

## Next Steps

**Immediate Actions:**
1. ✅ Review this integration plan
2. ⏳ Confirm approach with stakeholder (you!)
3. ⏳ Begin Step 1: Create integration infrastructure
4. ⏳ Execute phased integration with checkpoints

**Questions for Stakeholder:**
1. Do you want to proceed with this integration plan immediately?
2. Should we create a separate feature branch for integration (`feature/data-integration`)?
3. Any specific data validations or business rules to add?
4. Do you want step-by-step progress updates or just final report?

---

## Appendix: File Locations Reference

**Current Working Database:**
- `C:\Users\Lucas\Documents\CP2B\PanoramaCP2B\data\cp2b_maps.db`

**Validated Data Sources:**
- `C:\Users\Lucas\Documents\CP2B\Validacao_dados\06_RESULTADO_FINAL_VALIDADO\POTENCIAL_3CENARIOS_VALIDADO_20251020_151634.csv`
- `C:\Users\Lucas\Documents\CP2B\Validacao_dados\05_RESULTADO_FINAL\FATORES_DISPONIBILIDADE_COMPLETOS.csv`
- `C:\Users\Lucas\Documents\CP2B\Validacao_dados\Referências_Organizadas_ABNT.ipynb`

**Backup Locations:**
- Git backup branch: `broken-state-backup`
- Current working commit: `521b61c`

---

**Document Version**: 1.0
**Last Updated**: October 21, 2025
**Status**: ✅ Ready for execution pending stakeholder approval
