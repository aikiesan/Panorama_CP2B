-- Migration 003: Add Scientific References and Parameter Traceability Tables
-- Date: 2025-10-23
-- Purpose: Enable full paper-parameter linkage for "click to see source" feature
-- Integration with: CP2B_Chemical_Parameters.db (674 papers, 8,519 parameters)

-- =============================================================================
-- TABLE 1: SCIENTIFIC REFERENCES
-- =============================================================================
-- Stores all 674 scientific papers with systematic naming (P[ID]_[SECTOR]_[YEAR].pdf)

CREATE TABLE IF NOT EXISTS scientific_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Link to validation database
    paper_id INTEGER UNIQUE,  -- Original ID from CP2B_Chemical_Parameters.db

    -- Systematic identification (from your renaming system)
    codename TEXT UNIQUE NOT NULL,  -- P0001_AG_CANA_2003
    codename_short TEXT,  -- AG_CANA_001

    -- File management
    pdf_filename TEXT UNIQUE NOT NULL,  -- P0001_AG_CANA_2003.pdf
    pdf_path TEXT NOT NULL,  -- C:\Users\Lucas\Documents\CP2B\Validacao_dados\02_LITERATURA\...
    original_filename TEXT,  -- Original before renaming

    -- Classification (from folder structure)
    sector TEXT,  -- AG_CANA, PEC_SUINO, etc.
    sector_full TEXT,  -- Agricultura - Cana-de-açúcar
    primary_residue TEXT,
    query_folder TEXT,  -- Cana, Citros, etc.

    -- Bibliographic metadata (TO BE POPULATED)
    authors TEXT,
    publication_year INTEGER,
    journal TEXT,
    volume TEXT,
    issue TEXT,
    pages TEXT,
    doi TEXT,
    title TEXT,
    abstract TEXT,
    keywords TEXT,  -- JSON array for search

    -- Additional identifiers
    scopus_id TEXT,
    pubmed_id TEXT,
    google_scholar_link TEXT,

    -- Quality tracking
    data_quality TEXT DEFAULT 'Validated',
    extraction_complete BOOLEAN DEFAULT 1,  -- All parameters extracted
    metadata_complete BOOLEAN DEFAULT 0,  -- Authors/DOI/Journal populated
    verified_by TEXT,

    -- Timestamps
    created_at TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Notes
    notes TEXT
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_ref_codename ON scientific_references(codename);
CREATE INDEX IF NOT EXISTS idx_ref_sector ON scientific_references(sector);
CREATE INDEX IF NOT EXISTS idx_ref_year ON scientific_references(publication_year DESC);
CREATE INDEX IF NOT EXISTS idx_ref_doi ON scientific_references(doi);
CREATE INDEX IF NOT EXISTS idx_ref_metadata_status ON scientific_references(metadata_complete);

-- Auto-update timestamp trigger
CREATE TRIGGER IF NOT EXISTS update_reference_timestamp
AFTER UPDATE ON scientific_references
BEGIN
    UPDATE scientific_references
    SET last_updated = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- =============================================================================
-- TABLE 2: PARAMETER RANGES (WITH SOURCE LINKAGE)
-- =============================================================================
-- Stores chemical parameter values with direct links to source papers
-- This enables "click min/max value to see source paper" feature

CREATE TABLE IF NOT EXISTS parameter_ranges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Residue linkage
    residue_codigo TEXT NOT NULL,  -- Links to residuos.codigo

    -- Parameter identification
    parameter_name TEXT NOT NULL,  -- BMP, TS, VS, pH, COD, TAN, CN_RATIO, etc.
    parameter_category TEXT,  -- Chemical, Operational, Physical

    -- Range values (from 5-pass extraction)
    value_min REAL,
    value_mean REAL,
    value_max REAL,
    unit TEXT NOT NULL,

    -- Sample statistics
    n_samples INTEGER,  -- Number of samples if available
    std_deviation REAL,

    -- SOURCE TRACEABILITY (CRITICAL FEATURE)
    -- Each value can come from different papers
    min_reference_id INTEGER,  -- FK to scientific_references.id
    mean_reference_id INTEGER,
    max_reference_id INTEGER,

    -- Page numbers where values were found
    min_page_number INTEGER,
    mean_page_number INTEGER,
    max_page_number INTEGER,

    -- Extraction quality (from your 5-pass extraction)
    data_quality TEXT,  -- High, Medium, Low
    extraction_method TEXT,  -- Pass1, Pass2, Pass3, Pass4, Pass5
    confidence_score REAL,  -- 0.0 to 1.0

    -- Measurement context
    measurement_conditions TEXT,  -- Temperature, pH range, etc.
    substrate_type TEXT,  -- Specific substrate variant

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys
    FOREIGN KEY (residue_codigo) REFERENCES residuos(codigo) ON DELETE CASCADE,
    FOREIGN KEY (min_reference_id) REFERENCES scientific_references(id),
    FOREIGN KEY (mean_reference_id) REFERENCES scientific_references(id),
    FOREIGN KEY (max_reference_id) REFERENCES scientific_references(id)
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_param_residue ON parameter_ranges(residue_codigo);
CREATE INDEX IF NOT EXISTS idx_param_name ON parameter_ranges(parameter_name);
CREATE INDEX IF NOT EXISTS idx_param_quality ON parameter_ranges(data_quality);
CREATE INDEX IF NOT EXISTS idx_param_min_ref ON parameter_ranges(min_reference_id);
CREATE INDEX IF NOT EXISTS idx_param_mean_ref ON parameter_ranges(mean_reference_id);
CREATE INDEX IF NOT EXISTS idx_param_max_ref ON parameter_ranges(max_reference_id);

-- =============================================================================
-- TABLE 3: RESIDUE-REFERENCE JUNCTION (MANY-TO-MANY)
-- =============================================================================
-- Links residues to all papers that provide data for them

CREATE TABLE IF NOT EXISTS residue_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    residue_codigo TEXT NOT NULL,
    reference_id INTEGER NOT NULL,

    -- Contribution details
    provides_parameters TEXT,  -- JSON array: ["BMP","TS","VS","pH"]
    parameter_count INTEGER DEFAULT 0,  -- How many parameters this paper provides

    -- Importance indicators
    is_primary_source BOOLEAN DEFAULT 0,  -- Main reference for this residue
    relevance_score INTEGER DEFAULT 5,  -- 1-10 scale

    -- Usage tracking
    times_cited INTEGER DEFAULT 0,  -- How often users clicked this reference

    -- Notes
    specific_findings TEXT,
    page_numbers TEXT,  -- Main pages with data

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (residue_codigo) REFERENCES residuos(codigo) ON DELETE CASCADE,
    FOREIGN KEY (reference_id) REFERENCES scientific_references(id) ON DELETE CASCADE,
    UNIQUE(residue_codigo, reference_id)
);

CREATE INDEX IF NOT EXISTS idx_resref_residue ON residue_references(residue_codigo);
CREATE INDEX IF NOT EXISTS idx_resref_reference ON residue_references(reference_id);
CREATE INDEX IF NOT EXISTS idx_resref_primary ON residue_references(is_primary_source);

-- =============================================================================
-- VIEW: PARAMETER SUMMARY WITH SOURCES
-- =============================================================================
-- Convenient view for querying parameters with their source information

CREATE VIEW IF NOT EXISTS v_parameters_with_sources AS
SELECT
    pr.id,
    pr.residue_codigo,
    r.nome as residue_name,
    r.setor as sector,
    pr.parameter_name,
    pr.value_min,
    pr.value_mean,
    pr.value_max,
    pr.unit,

    -- Min source
    sr_min.codename as min_source_code,
    sr_min.authors as min_source_authors,
    sr_min.publication_year as min_source_year,
    pr.min_page_number,

    -- Mean source
    sr_mean.codename as mean_source_code,
    sr_mean.authors as mean_source_authors,
    sr_mean.publication_year as mean_source_year,
    pr.mean_page_number,

    -- Max source
    sr_max.codename as max_source_code,
    sr_max.authors as max_source_authors,
    sr_max.publication_year as max_source_year,
    pr.max_page_number,

    pr.data_quality
FROM parameter_ranges pr
JOIN residuos r ON pr.residue_codigo = r.codigo
LEFT JOIN scientific_references sr_min ON pr.min_reference_id = sr_min.id
LEFT JOIN scientific_references sr_mean ON pr.mean_reference_id = sr_mean.id
LEFT JOIN scientific_references sr_max ON pr.max_reference_id = sr_max.id;

-- =============================================================================
-- STATISTICS VIEW: REFERENCE COVERAGE
-- =============================================================================

CREATE VIEW IF NOT EXISTS v_reference_statistics AS
SELECT
    sector,
    COUNT(DISTINCT id) as total_papers,
    COUNT(DISTINCT CASE WHEN metadata_complete = 1 THEN id END) as papers_with_metadata,
    COUNT(DISTINCT CASE WHEN doi IS NOT NULL THEN id END) as papers_with_doi,
    MIN(publication_year) as earliest_year,
    MAX(publication_year) as latest_year
FROM scientific_references
GROUP BY sector;

-- =============================================================================
-- COMMENTS
-- =============================================================================

-- This schema enables:
-- 1. Full traceability from every parameter value to source paper + page number
-- 2. "Click to see source" functionality in webapp UI
-- 3. Advanced reference search and filtering (by sector, year, metadata status)
-- 4. BibTeX/CSV export of filtered references
-- 5. PDF viewer integration (local file paths stored)
-- 6. Incremental metadata population tracking
-- 7. Many-to-many relationships between residues and papers

-- Migration from validation DB will be done in separate script (004_import_from_validation.sql)
