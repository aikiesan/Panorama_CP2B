# CP2B Panorama Database - Schema & Update Guide

**Database**: `cp2b_panorama.db` (SQLite)
**Location**: `C:\Users\Lucas\Documents\CP2B\PanoramaCP2B\data\cp2b_panorama.db`
**Current Stats**: 674 papers | 8,648 parameters | 831 residue-paper links

---

## 📁 Database Location & Access

### Primary Database File
```
Path: data/cp2b_panorama.db
Type: SQLite 3
Size: ~50 MB (will grow with updates)
Encoding: UTF-8
```

### Backup Strategy
```
Backups: data/backups/cp2b_panorama_YYYY-MM-DD.db
Frequency: Before each major update
Retention: Keep last 5 backups minimum
```

---

## 📊 Database Schema (Core Tables)

### Table 1: `scientific_references` (674 rows)

**Purpose**: Stores all scientific papers with full bibliographic metadata

**Schema** (DO NOT CHANGE):
```sql
CREATE TABLE scientific_references (
    -- PRIMARY KEYS (IMMUTABLE)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER,  -- Link to validation database

    -- IDENTIFICATION (IMMUTABLE)
    codename TEXT NOT NULL UNIQUE,  -- Format: P####_SECTOR_RESIDUE_YEAR
    codename_short TEXT,            -- Format: SECTOR_RESIDUE_###

    -- FILE MANAGEMENT (CAN UPDATE paths)
    pdf_filename TEXT NOT NULL,
    pdf_path TEXT NOT NULL,
    original_filename TEXT,

    -- CLASSIFICATION (CAN UPDATE)
    sector TEXT,              -- AG_CANA, PEC_SUINO, UR_RSU, etc.
    sector_full TEXT,         -- "Agricultura - Cana-de-açúcar"
    primary_residue TEXT,     -- Main residue discussed
    query_folder TEXT,        -- Original search folder

    -- BIBLIOGRAPHIC METADATA (CAN UPDATE - validate data here!)
    authors TEXT,
    publication_year INTEGER,
    journal TEXT,
    volume TEXT,
    issue TEXT,
    pages TEXT,
    doi TEXT,
    title TEXT,
    abstract TEXT,
    keywords TEXT,            -- JSON array of keywords

    -- EXTERNAL IDENTIFIERS (CAN ADD)
    scopus_id TEXT,
    pubmed_id TEXT,
    google_scholar_link TEXT,

    -- QUALITY TRACKING (CAN UPDATE)
    data_quality TEXT DEFAULT 'Validated',  -- Validated, High, Medium, Low
    extraction_complete BOOLEAN DEFAULT 1,
    metadata_complete BOOLEAN DEFAULT 0,
    verified_by TEXT,

    -- TIMESTAMPS (AUTO-UPDATED)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- NOTES (CAN UPDATE)
    notes TEXT
);
```

**Fields You Can Safely UPDATE**:
- ✅ `authors`, `publication_year`, `journal`, `volume`, `issue`, `pages`
- ✅ `doi`, `title`, `abstract`, `keywords`
- ✅ `scopus_id`, `pubmed_id`, `google_scholar_link`
- ✅ `data_quality`, `verified_by`, `notes`
- ✅ `pdf_path` (if files moved)

**Fields You MUST NOT CHANGE**:
- ❌ `id` (breaks foreign keys)
- ❌ `codename` (breaks application references)
- ❌ `pdf_filename` (application expects this format)

---

### Table 2: `parameter_ranges` (8,648 rows)

**Purpose**: Stores chemical/physical parameters extracted from papers

**Schema** (DO NOT CHANGE structure):
```sql
CREATE TABLE parameter_ranges (
    -- PRIMARY KEY (IMMUTABLE)
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- RESIDUE LINK (CRITICAL - use database codes!)
    residue_codigo TEXT NOT NULL,  -- Database codes: VINHACA, DEJETOS_SUINO, etc.

    -- PARAMETER IDENTIFICATION (IMMUTABLE)
    parameter_name TEXT NOT NULL,  -- BMP, TS, VS, pH, COD, TAN, etc.
    parameter_category TEXT,       -- Chemical, Operational, Physical

    -- VALUE INFORMATION (CAN UPDATE - validate these!)
    value_min REAL,
    value_mean REAL,
    value_max REAL,
    unit TEXT NOT NULL,

    -- SAMPLE STATISTICS (CAN UPDATE)
    n_samples INTEGER,
    std_deviation REAL,

    -- SOURCE TRACEABILITY (CRITICAL - links to references)
    mean_reference_id INTEGER,     -- FK to scientific_references.id
    mean_page_number INTEGER,      -- Page where mean value found
    min_reference_id INTEGER,
    min_page_number INTEGER,
    max_reference_id INTEGER,
    max_page_number INTEGER,

    -- QUALITY INDICATORS (CAN UPDATE)
    data_quality TEXT DEFAULT 'Medium',  -- High, Medium, Low
    extraction_method TEXT,              -- Pass1, Pass2, Manual, etc.
    confidence_score REAL,               -- 0.0 to 1.0

    -- MEASUREMENT CONTEXT (CAN UPDATE)
    measurement_conditions TEXT,
    substrate_type TEXT,

    -- TIMESTAMPS (AUTO-UPDATED)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (mean_reference_id) REFERENCES scientific_references(id),
    FOREIGN KEY (min_reference_id) REFERENCES scientific_references(id),
    FOREIGN KEY (max_reference_id) REFERENCES scientific_references(id)
);
```

**Critical Database Codes** (MUST match these):
```
Top residues by parameter count:
- DEJETOS_SUINO    (1,246 parameters)
- VINHACA          (1,007 parameters)
- CASCA_CAFE       (982 parameters)
- VISCERAS         (953 parameters)
- LODO_SECUNDARIO  (875 parameters)
- CAMA_AVIARIO     (805 parameters)
- REJEITOS         (608 parameters)
- BAGACO           (396 parameters)
- CASCA_EUCALIPTO  (335 parameters)
- BAGACO_CITROS    (246 parameters)
```

**Fields You Can Safely UPDATE**:
- ✅ `value_min`, `value_mean`, `value_max`, `unit`
- ✅ `n_samples`, `std_deviation`
- ✅ `mean_page_number`, `min_page_number`, `max_page_number`
- ✅ `data_quality`, `extraction_method`, `confidence_score`
- ✅ `measurement_conditions`, `substrate_type`

**Fields You MUST NOT CHANGE**:
- ❌ `id` (breaks application)
- ❌ `residue_codigo` (unless correcting errors - use database codes!)
- ❌ `parameter_name` (unless correcting errors)
- ❌ `*_reference_id` (unless relinking to different paper)

---

### Table 3: `residue_references` (831 rows)

**Purpose**: Links residues to papers (many-to-many relationship)

**Schema**:
```sql
CREATE TABLE residue_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    residue_codigo TEXT NOT NULL,       -- Database code
    reference_id INTEGER NOT NULL,      -- FK to scientific_references.id
    parameter_count INTEGER DEFAULT 0,  -- How many parameters from this paper
    is_primary_source BOOLEAN DEFAULT 0, -- TRUE if provides 3+ parameters

    FOREIGN KEY (reference_id) REFERENCES scientific_references(id)
);
```

**This table is AUTO-GENERATED** when you add parameters. Don't edit manually.

---

## 🔄 How to Update the Database

### Option 1: SQLite Browser (Recommended for Small Updates)

1. **Download**: [DB Browser for SQLite](https://sqlitebrowser.org/)
2. **Open**: `data/cp2b_panorama.db`
3. **Browse Data** tab → Select table
4. **Double-click** cell to edit
5. **Write Changes** button to save

**Example: Update Paper Metadata**:
```sql
-- Fix author name
UPDATE scientific_references
SET authors = 'Silva, J.; Santos, M.; Oliveira, P.'
WHERE codename = 'P0001_AG_CANA_2003';

-- Update DOI
UPDATE scientific_references
SET doi = '10.1016/j.biortech.2023.123456'
WHERE id = 42;
```

**Example: Update Parameter Values**:
```sql
-- Correct BMP value for Vinhaça
UPDATE parameter_ranges
SET value_mean = 265.0,
    value_min = 240.0,
    value_max = 290.0
WHERE residue_codigo = 'VINHACA'
  AND parameter_name = 'BMP'
  AND mean_reference_id = 123;
```

---

### Option 2: Python Script (Recommended for Bulk Updates)

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('data/cp2b_panorama.db')

# Update multiple records
df = pd.read_csv('updates.csv')  # Your validation results
for _, row in df.iterrows():
    conn.execute("""
        UPDATE parameter_ranges
        SET value_mean = ?,
            data_quality = 'Validated',
            verified_by = 'Lucas',
            last_updated = CURRENT_TIMESTAMP
        WHERE residue_codigo = ?
          AND parameter_name = ?
          AND mean_reference_id = ?
    """, (row['new_value'], row['residue'], row['parameter'], row['ref_id']))

conn.commit()
conn.close()
```

---

### Option 3: Add New Papers (Full Workflow)

**Step 1**: Add paper to `scientific_references`:
```python
import sqlite3

conn = sqlite3.connect('data/cp2b_panorama.db')
cursor = conn.cursor()

# Insert new paper
cursor.execute("""
    INSERT INTO scientific_references (
        codename, pdf_filename, pdf_path,
        authors, publication_year, journal, title,
        sector, sector_full,
        data_quality, metadata_complete
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    'P0675_AG_CANA_2024',
    'P0675_AG_CANA_2024.pdf',
    'C:/Users/Lucas/Downloads/Artigos_Avicultura/P0675_AG_CANA_2024.pdf',
    'Oliveira, R.; Silva, M.',
    2024,
    'Renewable Energy',
    'Advanced biogas production from vinasse using UASB reactors',
    'AG_CANA',
    'Agricultura - Cana-de-açúcar',
    'High',
    True
))

new_paper_id = cursor.lastrowid
conn.commit()
```

**Step 2**: Extract and add parameters:
```python
# Add BMP parameter from new paper
cursor.execute("""
    INSERT INTO parameter_ranges (
        residue_codigo, parameter_name, parameter_category,
        value_mean, unit,
        mean_reference_id, mean_page_number,
        data_quality
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    'VINHACA',  # Database code!
    'BMP',
    'Chemical',
    275.0,
    'ml CH₄/g VS',
    new_paper_id,
    12,
    'High'
))

conn.commit()
conn.close()
```

**Step 3**: Verify in webapp:
- Navigate to Page 2
- Select Cana-de-açúcar → Vinhaça
- Click BMP tab
- Should see new source: "Oliveira et al. (2024), p. 12"

---

## ⚠️ CRITICAL: Residue Code Mapping

### Database Codes vs Webapp Codes

The database uses **simplified codes** but the webapp uses **hierarchical codes**.

**Mapping is handled automatically** in `src/data_handler.py::_map_residue_code_for_references()`.

**When adding NEW residues**, you must:

1. **Use database code** in `parameter_ranges.residue_codigo`:
   ```sql
   INSERT INTO parameter_ranges (residue_codigo, ...)
   VALUES ('VINHACA', ...);  -- ✅ Correct
   -- NOT 'CANA_VINHACA' ❌
   ```

2. **Add mapping** if webapp uses different code:
   ```python
   # In src/data_handler.py
   code_mapping = {
       # Add new mapping
       'NEW_WEBAPP_CODE': 'NEW_DB_CODE',
   }
   ```

### Current Mappings (Reference)
```python
{
    'CANA_VINHACA': 'VINHACA',
    'CANA_BAGACO': 'BAGACO',
    'SUINO_DEJETO': 'DEJETOS_SUINO',
    'AVES_CAMA': 'CAMA_AVIARIO',
    'CAFE_CASCA': 'CASCA_CAFE',
    'CITROS_BAGACO': 'BAGACO_CITROS',
    'LODO_ETE': 'LODO_SECUNDARIO',
    # ... see full list in data_handler.py
}
```

---

## 🔍 Validation Queries

### Check Data Quality
```sql
-- Count parameters by quality
SELECT data_quality, COUNT(*) as count
FROM parameter_ranges
GROUP BY data_quality;

-- Find papers missing metadata
SELECT codename, authors, title, metadata_complete
FROM scientific_references
WHERE metadata_complete = 0;
```

### Check Missing Page Numbers
```sql
-- Parameters without page traceability
SELECT residue_codigo, parameter_name, COUNT(*) as count
FROM parameter_ranges
WHERE mean_page_number IS NULL
GROUP BY residue_codigo, parameter_name;
```

### Verify Foreign Keys
```sql
-- Check for broken references
SELECT pr.id, pr.residue_codigo, pr.parameter_name
FROM parameter_ranges pr
LEFT JOIN scientific_references sr ON pr.mean_reference_id = sr.id
WHERE pr.mean_reference_id IS NOT NULL
  AND sr.id IS NULL;
```

---

## 🛡️ Backup Before Updates

**ALWAYS backup before making changes**:

### Windows Command Line:
```batch
cd C:\Users\Lucas\Documents\CP2B\PanoramaCP2B\data
copy cp2b_panorama.db backups\cp2b_panorama_%DATE:~-4,4%-%DATE:~-10,2%-%DATE:~-7,2%.db
```

### Python Script:
```python
import shutil
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
src = 'data/cp2b_panorama.db'
dst = f'data/backups/cp2b_panorama_{today}.db'
shutil.copy2(src, dst)
print(f"Backup created: {dst}")
```

---

## 📈 Database Growth Expectations

**Current Size**: ~50 MB
**Expected Growth**: +5-10 MB per 100 new papers
**Max Recommended Size**: 500 MB (10x current)

After 500 MB, consider:
- Archiving old/low-quality papers
- Splitting into year-based databases
- Using PostgreSQL for better performance

---

## 🚨 DO NOT Change These

### Immutable Fields:
- `scientific_references.id`
- `scientific_references.codename`
- `parameter_ranges.id`
- `residue_references.id`

### Immutable Structure:
- Table names
- Column names
- Column types
- Foreign key relationships
- Primary keys

**If you need structural changes**, create a new database version and migrate data.

---

## 📞 Questions?

If you need to:
- Add new parameter types
- Change database structure
- Migrate to PostgreSQL
- Add new tables
- Create complex queries

Contact the development team or check `CLAUDE.md` for architectural guidance.

---

**Last Updated**: 2025-10-23
**Database Version**: 1.0
**Contact**: CP2B Team, UNICAMP
