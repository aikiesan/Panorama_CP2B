# CP2B Database Structure Report

**Generated:** 2025-10-28
**Database:** `data/cp2b_maps.db` (SQLite)
**Status:** Comprehensive analysis of current structure and data requirements

---

## Executive Summary

The CP2B database contains **14 tables** with **645 municipalities** and comprehensive biogas potential calculations. However, **8 detailed tables remain EMPTY** and require population with granular time-series data from external sources.

### Database Health Status

| Category | Count | Status |
|----------|-------|--------|
| **Total Tables** | 14 | ✅ Complete |
| **Populated Tables** | 4 | ✅ Active (municipalities, conversion_factors, backups) |
| **Empty Tables** | 8 | ⚠️ Require Data Population |
| **Total Municipalities** | 645 | ✅ All São Paulo municipalities |
| **Custom Indexes** | 23 | ✅ Properly indexed |

---

## 1. TABLE INVENTORY

### 1.1 Active Tables (WITH DATA)

#### **municipalities** (645 rows)
**Purpose:** Main aggregated biogas potential calculations by municipality

**Key Columns (47 total):**
- **Identification:** nome_municipio, codigo_municipio, cd_mun
- **Geographic:** lat, lon, area_km2, populacao_2022, densidade_demografica
- **Biogas Potential by Culture:**
  - biogas_cana_m_ano (sugarcane)
  - biogas_soja_m_ano (soybean)
  - biogas_milho_m_ano (corn)
  - biogas_bovinos_m_ano (cattle)
  - biogas_cafe_m_ano (coffee)
  - biogas_citros_m_ano (citrus)
  - biogas_suino_m_ano (swine)
  - biogas_aves_m_ano (poultry)
  - biogas_piscicultura_m_ano (aquaculture)
  - biogas_silvicultura_m_ano (forestry)
- **Totals by Sector:**
  - total_agricola_m_ano
  - total_pecuaria_m_ano
  - total_urbano_m_ano
  - total_final_m_ano
- **Scenario Calculations (Pessimistic/Realistic/Optimistic):**
  - ch4_*_agricultura
  - ch4_*_pecuaria
  - ch4_*_urbano
  - ch4_*_total
  - energia_*_mwh
  - energia_*_tj

**Sample Data - Top 5 Municipalities by Total Potential:**
1. **Barretos**: 650.4 Mi m³/ano (639.3M agric + 6.7M pec + 4.5M urban)
2. **Morro Agudo**: 644.4 Mi m³/ano (641.1M agric + 2.3M pec + 1.1M urban)
3. **Guaíra**: 565.7 Mi m³/ano (561.2M agric + 3.1M pec + 1.4M urban)
4. **Jaboticabal**: 494.9 Mi m³/ano (491.2M agric + 1.0M pec + 2.7M urban)
5. **Rancharia**: 482.9 Mi m³/ano (466.2M agric + 15.4M pec + 1.2M urban)

**Indexes:**
- idx_nome_municipio
- idx_cd_mun
- idx_total_potential
- idx_lat_lon

---

#### **conversion_factors** (8 rows)
**Purpose:** Biogas conversion factors by category with literature validation

**Columns (12 total):**
- id, category, subcategory, factor_value, unit
- literature_reference, reference_url, real_data_validation
- safety_margin_percent, final_factor
- date_validated, notes

**Current Data:**

| Category | Subcategory | Factor | Final Factor | Unit |
|----------|-------------|--------|--------------|------|
| Pecuária | Bovinos | 135.00 | 130.00 | m³/cabeça/ano |
| Pecuária | Suínos | 461.00 | 380.00 | m³/cabeça/ano |
| Pecuária | Aves | 1.20 | 1.50 | m³/ave/ano |
| Culturas | Cana-de-açúcar | 94.00 | 85.00 | m³/ton |
| Culturas | Milho | 225.00 | 210.00 | m³/ton |
| Culturas | Soja | 215.00 | 200.00 | m³/ton |
| Culturas | Café | 310.00 | 280.00 | m³/ton |
| Culturas | Citros | 21.00 | 19.00 | m³/ton |

**Note:** These factors apply safety margins for conservative estimates.

---

#### **Backup Tables** (3 tables)
- municipalities_backup (645 rows)
- municipalities_backup_rsu_rpo (645 rows)
- municipalities_backup_focused_20250915_135355 (645 rows)

**Purpose:** Historical snapshots before major updates

---

### 1.2 Empty Tables (REQUIRE DATA POPULATION)

#### **residuos_agricolas** (0 rows) ⚠️
**Purpose:** Time-series agricultural production data by municipality and culture

**Schema (11 columns):**
```sql
CREATE TABLE residuos_agricolas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    cultura TEXT NOT NULL,  -- 'Cana-de-açúcar', 'Milho', 'Soja', etc.
    area_plantada_ha REAL DEFAULT 0,
    producao_ton REAL DEFAULT 0,
    produtividade_ton_ha REAL DEFAULT 0,
    valor_producao_mil_reais REAL DEFAULT 0,
    residuo_gerado_ton REAL DEFAULT 0,
    fator_residuo_cultura REAL DEFAULT 0,
    potencial_biogas_m3 REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_residuos_agricolas_mun, idx_residuos_agricolas_cultura, idx_residuos_agricolas_ano

**Data Source:** IBGE SIDRA API - Produção Agrícola Municipal (PAM)

**Expected Cultures:**
- Cana-de-açúcar, Milho, Soja, Café, Citros, Eucalipto

**Example Row:**
```
codigo_municipio: 354870 (Barretos)
ano: 2022
cultura: 'Cana-de-açúcar'
area_plantada_ha: 45000
producao_ton: 3600000
produtividade_ton_ha: 80
residuo_gerado_ton: 1008000  (vinhaça + bagaço + torta)
potencial_biogas_m3: 85680000  (usando conversion_factors)
```

---

#### **residuos_pecuarios** (0 rows) ⚠️
**Purpose:** Time-series livestock counts by municipality and animal type

**Schema (10 columns):**
```sql
CREATE TABLE residuos_pecuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    tipo_criacao TEXT NOT NULL,  -- 'Bovinos', 'Suínos', 'Aves', 'Piscicultura'
    num_cabecas REAL DEFAULT 0,
    peso_medio_kg REAL DEFAULT 0,
    residuo_kg_dia_cabeca REAL DEFAULT 0,
    residuo_ton_dia REAL DEFAULT 0,
    residuo_ton_ano REAL DEFAULT 0,
    potencial_biogas_m3_ano REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_residuos_pecuarios_mun, idx_residuos_pecuarios_tipo, idx_residuos_pecuarios_ano

**Data Source:**
- IBGE PPM (Pesquisa Pecuária Municipal)
- SEAPA (Defesa Agropecuária - GTA data)

**Expected Types:**
- Bovinos (leite + corte), Suínos, Aves (frango + postura), Piscicultura

**Example Row:**
```
codigo_municipio: 354870 (Barretos)
ano: 2022
tipo_criacao: 'Bovinos'
num_cabecas: 51200
peso_medio_kg: 450
residuo_kg_dia_cabeca: 12.5
residuo_ton_ano: 234000
potencial_biogas_m3_ano: 6656000  (130 m³/cabeça/ano)
```

---

#### **residuos_urbanos** (0 rows) ⚠️
**Purpose:** Urban waste generation data by municipality

**Schema (13 columns):**
```sql
CREATE TABLE residuos_urbanos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    populacao INTEGER DEFAULT 0,
    rsu_ton_ano REAL DEFAULT 0,
    rsu_per_capita_kg_dia REAL DEFAULT 0,
    coleta_seletiva_ton_ano REAL DEFAULT 0,
    organicos_ton_ano REAL DEFAULT 0,
    percentual_organicos REAL DEFAULT 0,
    aterro_sanitario BOOLEAN DEFAULT 0,
    poda_capina_ton_ano REAL DEFAULT 0,
    potencial_biogas_rsu_m3_ano REAL DEFAULT 0,
    potencial_biogas_poda_m3_ano REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_residuos_urbanos_mun, idx_residuos_urbanos_ano

**Data Source:** SNIS (Sistema Nacional de Informações sobre Saneamento)

**Example Row:**
```
codigo_municipio: 354870 (Barretos)
ano: 2022
populacao: 122485
rsu_ton_ano: 44700
rsu_per_capita_kg_dia: 1.0
organicos_ton_ano: 22350  (50% assumption)
potencial_biogas_rsu_m3_ano: 4470000  (100 m³/ton organic)
```

---

#### **residuos_industriais** (0 rows) ⚠️
**Purpose:** Industrial facility residue generation data

**Schema (10 columns):**
```sql
CREATE TABLE residuos_industriais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    setor_industrial TEXT NOT NULL,  -- 'Sucroalcooleiro', 'Frigorífico', 'Laticínio', etc.
    nome_estabelecimento TEXT,
    tipo_residuo TEXT,
    residuo_ton_ano REAL DEFAULT 0,
    composicao_organica_percentual REAL DEFAULT 0,
    potencial_biogas_m3_ano REAL DEFAULT 0,
    possui_tratamento BOOLEAN DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_residuos_industriais_mun, idx_residuos_industriais_setor

**Data Source:**
- CETESB (Inventário de Resíduos Industriais)
- Industry surveys
- Public datasets (UNICA for sugarcane mills, etc.)

**Expected Sectors:**
- Sucroalcooleiro, Frigorífico, Laticínio, Cervejaria, Citros

**Example Row:**
```
codigo_municipio: 354870 (Barretos)
ano: 2022
setor_industrial: 'Sucroalcooleiro'
nome_estabelecimento: 'Usina Barretos'
tipo_residuo: 'Vinhaça'
residuo_ton_ano: 1200000
potencial_biogas_m3_ano: 18000000  (15 m³/ton)
```

---

#### **dados_laboratoriais** (0 rows) ⚠️
**Purpose:** Laboratory analysis results for residue characterization

**Schema (11 columns):**
```sql
CREATE TABLE dados_laboratoriais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_residuo TEXT NOT NULL,
    parametro TEXT NOT NULL,  -- 'BMP', 'TS', 'VS', 'C/N', 'pH', etc.
    valor_tipico TEXT,
    valor_min REAL,
    valor_max REAL,
    unidade TEXT,
    metodo TEXT,  -- 'ISO 11734', 'APHA 2540', etc.
    referencia TEXT,
    observacoes TEXT,
    data_atualizacao DATE DEFAULT CURRENT_DATE
)
```

**Indexes:** idx_dados_lab_tipo, idx_dados_lab_parametro

**Data Source:** CP2B laboratory research data

**Example Row:**
```
tipo_residuo: 'Vinhaça de Cana-de-açúcar'
parametro: 'BMP'
valor_min: 12.0
valor_max: 18.0
valor_tipico: '15.0'
unidade: 'Nm³ CH₄/ton'
metodo: 'ISO 11734'
referencia: 'Silva et al. 2020'
```

---

#### **dados_socioeconomicos** (0 rows) ⚠️
**Purpose:** Socioeconomic indicators by municipality

**Schema (16 columns):**
```sql
CREATE TABLE dados_socioeconomicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    pib_mil_reais REAL DEFAULT 0,
    pib_per_capita REAL DEFAULT 0,
    pib_agropecuaria_mil_reais REAL DEFAULT 0,
    pib_industria_mil_reais REAL DEFAULT 0,
    pib_servicos_mil_reais REAL DEFAULT 0,
    populacao INTEGER DEFAULT 0,
    idhm REAL,
    idhm_renda REAL,
    idhm_longevidade REAL,
    idhm_educacao REAL,
    gini REAL,
    emprego_formal INTEGER DEFAULT 0,
    renda_media REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_socioeco_mun, idx_socioeco_ano

**Data Source:** IBGE, SEADE, Atlas Brasil

---

#### **uso_solo_mapbiomas** (0 rows) ⚠️
**Purpose:** Land use and cover classification by municipality

**Schema (10 columns):**
```sql
CREATE TABLE uso_solo_mapbiomas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    classe_uso TEXT NOT NULL,
    classe_nivel_1 TEXT,  -- 'Floresta', 'Agropecuária', 'Área não vegetada'
    classe_nivel_2 TEXT,  -- 'Lavoura temporária', 'Pastagem', etc.
    classe_nivel_3 TEXT,  -- Detailed classification
    area_km2 REAL DEFAULT 0,
    area_ha REAL DEFAULT 0,
    percentual_territorio REAL DEFAULT 0,
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_uso_solo_mun, idx_uso_solo_ano, idx_uso_solo_classe

**Data Source:** MapBiomas API (https://mapbiomas.org/)

---

#### **defesa_agropecuaria** (0 rows) ⚠️
**Purpose:** Agricultural defense and traceability data

**Schema (9 columns):**
```sql
CREATE TABLE defesa_agropecuaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    propriedades_cadastradas INTEGER DEFAULT 0,
    area_inspecionada_ha REAL DEFAULT 0,
    estabelecimentos_certificados INTEGER DEFAULT 0,
    producao_organica BOOLEAN DEFAULT 0,
    rastreabilidade_animal BOOLEAN DEFAULT 0,
    gtps_emitidas INTEGER DEFAULT 0,  -- Guias de Trânsito Animal
    FOREIGN KEY (codigo_municipio) REFERENCES municipalities(codigo_municipio)
)
```

**Indexes:** idx_defesa_agro_mun, idx_defesa_agro_ano

**Data Source:** SEAPA (Secretaria de Agricultura e Abastecimento)

---

## 2. DATA ARCHITECTURE

### 2.1 Two-Tier Data Model

The CP2B system uses **TWO SEPARATE DATA MODELS** that serve different purposes:

#### **Tier 1: Python Residue Registry** (Code-based)
**Location:** `src/data/residue_registry.py` and sector folders

**Content:** 40+ residue definitions with:
- Chemical parameters (BMP, TS, VS, C/N, pH)
- FDE factors (FC, FCp, FS, FL)
- Operational parameters (HRT, temperature, reactor type)
- Scientific references (DOI, papers)
- Priority rankings and recommendations

**Purpose:**
- Scientific characterization
- Biogas potential calculations
- UI display and filtering
- Research documentation

**Example:** `Bagaço de cana` with FDE=0%, BMP=85 Nm³/t, priority="NÃO DISPONÍVEL"

---

#### **Tier 2: Database Tables** (SQLite)
**Location:** `data/cp2b_maps.db`

**Content:** Time-series production/generation data:
- Municipality-level aggregations
- Annual production by culture/type
- Real-world generation quantities
- Geographic and economic context

**Purpose:**
- Historical trends analysis
- Geographic mapping
- Scenario modeling
- Municipality comparisons

**Example:** Barretos produced 3.6M ton sugarcane in 2022

---

### 2.2 Data Flow

```
External Sources (IBGE, SIDRA, MapBiomas)
    ↓
Empty Database Tables (residuos_*, dados_*)
    ↓
Aggregation + Calculations
    ↓
municipalities table (populated - 645 rows)
    ↓
Python Registry (residue definitions)
    ↓
Streamlit UI (user-facing application)
```

---

## 3. DATA UPDATE REQUIREMENTS

### 3.1 Critical Updates Needed

#### **Priority 1: Agricultural Production Data**
**Table:** `residuos_agricolas`
**Source:** IBGE SIDRA API
**Endpoint:** https://sidra.ibge.gov.br/api/
**Tables:** PAM (Produção Agrícola Municipal) - Table 1612

**Cultures to Import:**
1. Cana-de-açúcar (code 5457)
2. Milho (code 3001)
3. Soja (code 3004)
4. Café (code 2710)
5. Laranja (citros) (code 2711)

**Script Location:** `src/data_sources/sidra_handler.py`

**Expected Rows:** ~10,000 (645 municipalities × 5 cultures × 3 years)

---

#### **Priority 2: Livestock Census Data**
**Table:** `residuos_pecuarios`
**Source:** IBGE PPM (Pesquisa Pecuária Municipal)
**Endpoint:** https://sidra.ibge.gov.br/api/
**Tables:** PPM - Table 3939

**Animal Types:**
1. Bovinos (code 3940)
2. Suínos (code 3941)
3. Aves (code 3942)

**Script Location:** `src/data_sources/agro_handler.py`

**Expected Rows:** ~5,000 (645 municipalities × 3 types × 3 years)

---

#### **Priority 3: Urban Waste Data**
**Table:** `residuos_urbanos`
**Source:** SNIS (Sistema Nacional de Informações sobre Saneamento)
**Website:** http://app4.mdr.gov.br/serieHistorica/
**Format:** CSV download by municipality

**Key Fields:**
- RSU generation (ton/year)
- Per capita generation (kg/inhab/day)
- Selective collection (ton/year)
- Final disposal type

**Script Location:** Custom CSV importer needed

**Expected Rows:** ~2,000 (645 municipalities × 3 years)

---

#### **Priority 4: Laboratory Data**
**Table:** `dados_laboratoriais`
**Source:** CP2B internal research data
**Format:** Excel/CSV from lab reports

**Parameters per Residue:**
- BMP (Biochemical Methane Potential)
- TS (Total Solids)
- VS (Volatile Solids)
- C/N ratio
- pH
- COD (Chemical Oxygen Demand)

**Expected Rows:** ~240 (40 residues × 6 parameters)

---

### 3.2 Secondary Updates

#### **Priority 5: Industrial Data**
**Table:** `residuos_industriais`
**Sources:**
- UNICA (Sugarcane mills)
- CETESB (Industrial waste inventory)
- Industry associations

**Challenges:** Data is dispersed and often proprietary

---

#### **Priority 6: Socioeconomic Data**
**Table:** `dados_socioeconomicos`
**Sources:**
- IBGE (PIB Municipal)
- Atlas Brasil (IDHM)
- SEADE (São Paulo state statistics)

---

#### **Priority 7: Land Use Data**
**Table:** `uso_solo_mapbiomas`
**Source:** MapBiomas API
**Endpoint:** https://mapbiomas.org/
**Requirement:** API key needed

---

## 4. DATABASE CONSISTENCY CHECKS

### 4.1 Current Inconsistencies

✅ **FIXED:** Bagaço de Cana FDE values corrected from 80.75% to 0.0%

### 4.2 Validation Rules

**Foreign Key Integrity:**
- All `codigo_municipio` references must exist in `municipalities` table
- Current municipalities: 645 (all São Paulo)

**Data Range Validation:**
- Years: 2020-2024 (recommended range)
- Coordinates: lat ∈ [-25.3, -19.8], lon ∈ [-53.1, -44.2] (São Paulo bounds)
- Production values: > 0
- Percentages: [0, 100]

**Required Indexes:**
All tables have proper indexes created (23 total). No action needed.

---

## 5. RECOMMENDED ACTIONS

### 5.1 Immediate Actions

1. **Populate Agricultural Data** (Priority 1)
   - Run SIDRA API import for PAM data
   - Validate against current municipalities totals
   - Expected completion: 2-3 days

2. **Populate Livestock Data** (Priority 2)
   - Run SIDRA API import for PPM data
   - Cross-validate with Defesa Agropecuária data
   - Expected completion: 1-2 days

3. **Import Laboratory Data** (Priority 4)
   - Convert CP2B lab reports to standardized format
   - Populate dados_laboratoriais table
   - Link to Python registry residues
   - Expected completion: 1 day

### 5.2 Medium-term Actions

4. **Urban Waste Integration** (Priority 3)
   - Download SNIS historical data
   - Create CSV import script
   - Validate against current RSU calculations
   - Expected completion: 1 week

5. **Industrial Data Survey** (Priority 5)
   - Survey major industrial facilities
   - Import UNICA sugarcane mill data
   - Populate residuos_industriais
   - Expected completion: 2-4 weeks

### 5.3 Long-term Actions

6. **Socioeconomic Integration** (Priority 6)
   - IBGE PIB Municipal import
   - Atlas Brasil IDHM data
   - Expected completion: 1 week

7. **Land Use Integration** (Priority 7)
   - MapBiomas API integration
   - Annual land use classification
   - Expected completion: 2 weeks

---

## 6. DATA SOURCES REFERENCE

### 6.1 Primary Sources

| Source | Data | URL | Format | Update Frequency |
|--------|------|-----|--------|------------------|
| IBGE SIDRA | PAM (Agriculture) | https://sidra.ibge.gov.br/api/ | JSON/API | Annual |
| IBGE SIDRA | PPM (Livestock) | https://sidra.ibge.gov.br/api/ | JSON/API | Annual |
| SNIS | Urban Waste | http://app4.mdr.gov.br/serieHistorica/ | CSV | Annual |
| MapBiomas | Land Use | https://mapbiomas.org/ | API/WMS | Annual |
| CETESB | Industrial Waste | https://cetesb.sp.gov.br/ | PDF Reports | Periodic |
| UNICA | Sugarcane Mills | https://unicadata.com.br/ | CSV/Excel | Annual |
| CP2B | Lab Analysis | Internal | Excel/CSV | Ongoing |

### 6.2 API Examples

**SIDRA PAM (Sugarcane):**
```
https://apisidra.ibge.gov.br/values/t/1612/n6/all/v/216/p/2022/c81/5457
```

**SIDRA PPM (Cattle):**
```
https://apisidra.ibge.gov.br/values/t/3939/n6/all/v/284/p/2022/c79/3940
```

---

## 7. APPENDIX: SQL QUERIES

### 7.1 Check Data Completeness

```sql
-- Check empty tables
SELECT
    name as table_name,
    (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=t.name) as exists,
    (SELECT 'SELECT COUNT(*) FROM ' || name) as count_query
FROM sqlite_master t
WHERE type='table'
AND name NOT LIKE 'sqlite_%'
AND name NOT LIKE '%backup%';
```

### 7.2 Validate Municipality Coverage

```sql
-- Ensure all municipalities have basic data
SELECT
    nome_municipio,
    codigo_municipio,
    CASE
        WHEN total_final_m_ano IS NULL THEN 'Missing Total'
        WHEN total_final_m_ano = 0 THEN 'Zero Potential'
        ELSE 'OK'
    END as status
FROM municipalities
ORDER BY total_final_m_ano DESC NULLS LAST;
```

### 7.3 Sample Insert for Testing

```sql
-- Test insert into residuos_agricolas
INSERT INTO residuos_agricolas (
    codigo_municipio, ano, cultura,
    area_plantada_ha, producao_ton, produtividade_ton_ha,
    residuo_gerado_ton, fator_residuo_cultura, potencial_biogas_m3
) VALUES (
    354870, 2022, 'Cana-de-açúcar',
    45000, 3600000, 80,
    1008000, 0.28, 85680000
);
```

---

## 8. CONCLUSION

The CP2B database has a **solid foundation** with:
- ✅ Proper schema design with indexes and foreign keys
- ✅ Complete municipality-level aggregations (645 rows)
- ✅ Validated conversion factors
- ✅ Comprehensive scenario calculations

**Critical Gap:** 8 detailed tables remain empty and require population from external sources.

**Recommended Approach:**
1. Start with agricultural and livestock data (IBGE APIs) - **highest priority**
2. Add laboratory data from CP2B research - **validates Python registry**
3. Integrate urban waste data (SNIS) - **completes core sectors**
4. Expand with industrial, socioeconomic, and land use data - **enriches analysis**

**Timeline Estimate:** 4-8 weeks for complete data population

---

**Report Generated by:** Claude Code
**Last Updated:** 2025-10-28
**Version:** 1.0
