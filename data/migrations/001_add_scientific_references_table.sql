-- Migration 001: Create scientific_references table
-- Date: 2025-10-23
-- Purpose: Support 600+ scientific papers with full metadata for research and systematic review

CREATE TABLE IF NOT EXISTS scientific_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Core metadata (REQUIRED)
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    year INTEGER NOT NULL,

    -- Publication details
    journal TEXT,
    volume TEXT,
    issue TEXT,
    pages TEXT,
    publisher TEXT,

    -- Unique identifiers
    doi TEXT UNIQUE,
    scopus_id TEXT,
    pubmed_id TEXT,
    isbn TEXT,
    arxiv_id TEXT,

    -- Auto-generated links
    doi_link TEXT,  -- https://doi.org/{doi}
    scopus_link TEXT,
    pubmed_link TEXT,
    google_scholar_link TEXT,

    -- Local resources
    pdf_local_path TEXT,  -- Path to PDF in your collection of 600 papers
    pdf_cloud_url TEXT,   -- Optional: Cloud storage URL

    -- Categorization for filtering
    sector TEXT,  -- Agricultura, Pecuária, Industrial, Urbano
    culture_group TEXT,  -- Cana-de-Açúcar, Café, Citros, etc.
    residue_names TEXT,  -- JSON array: ["Vinhaça", "Bagaço de cana"]
    keywords TEXT,  -- JSON array for advanced search: ["biogas", "BMP", "UASB"]
    research_type TEXT,  -- Experimental, Review, Meta-analysis, Field study, Modeling

    -- Quality metrics
    relevance_tier TEXT DEFAULT 'Medium',  -- Very High, High, Medium, Low
    citation_count INTEGER DEFAULT 0,
    impact_factor REAL,
    h_index INTEGER,

    -- Content (for search and display)
    abstract TEXT,
    key_findings TEXT,  -- JSON array of main findings
    methodology_summary TEXT,
    data_type TEXT,  -- Dados Experimentais, Literatura, Campo, Piloto, Industrial

    -- Geographic context
    country TEXT,
    region TEXT,  -- São Paulo, Brazil, Europe, etc.
    study_location TEXT,

    -- Administrative fields
    added_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT 0,  -- Manually verified for accuracy
    verified_by TEXT,
    notes TEXT,

    -- Data completeness score (0-100)
    completeness_score INTEGER DEFAULT 0,

    -- Language
    language TEXT DEFAULT 'en'  -- en, pt, es, etc.
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_ref_doi ON scientific_references(doi);
CREATE INDEX IF NOT EXISTS idx_ref_year ON scientific_references(year DESC);
CREATE INDEX IF NOT EXISTS idx_ref_sector ON scientific_references(sector);
CREATE INDEX IF NOT EXISTS idx_ref_culture ON scientific_references(culture_group);
CREATE INDEX IF NOT EXISTS idx_ref_relevance ON scientific_references(relevance_tier);
CREATE INDEX IF NOT EXISTS idx_ref_verified ON scientific_references(verified);

-- Full-text search index (for title, authors, keywords)
-- Note: This will be handled by application layer with LIKE queries or FTS5 extension

-- Trigger to auto-update last_updated timestamp
CREATE TRIGGER IF NOT EXISTS update_reference_timestamp
AFTER UPDATE ON scientific_references
BEGIN
    UPDATE scientific_references
    SET last_updated = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Trigger to auto-generate DOI link
CREATE TRIGGER IF NOT EXISTS generate_doi_link
AFTER INSERT ON scientific_references
WHEN NEW.doi IS NOT NULL AND NEW.doi_link IS NULL
BEGIN
    UPDATE scientific_references
    SET doi_link = 'https://doi.org/' || NEW.doi
    WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_doi_link
AFTER UPDATE OF doi ON scientific_references
WHEN NEW.doi IS NOT NULL
BEGIN
    UPDATE scientific_references
    SET doi_link = 'https://doi.org/' || NEW.doi
    WHERE id = NEW.id;
END;

-- Comments for documentation
-- This table supports:
-- 1. Full bibliographic management for systematic reviews
-- 2. Direct linking from parameter ranges to source papers
-- 3. Advanced search and filtering by multiple criteria
-- 4. Export to BibTeX, RIS, EndNote formats
-- 5. Quality assessment and verification tracking
