-- Migration 004: Import Data from Validation Database
-- Date: 2025-10-23
-- Source: C:\Users\Lucas\Documents\CP2B\Validacao_dados\CP2B_Chemical_Parameters.db
-- Target: cp2b_panorama.db
-- Purpose: Migrate 674 papers and 8,519 chemical parameters with full traceability

-- =============================================================================
-- PREREQUISITES
-- =============================================================================
-- 1. Run migration 003_add_reference_tables.sql first
-- 2. Attach validation database before running this script:
--    ATTACH DATABASE 'C:\Users\Lucas\Documents\CP2B\Validacao_dados\CP2B_Chemical_Parameters.db' AS validation;

-- =============================================================================
-- STEP 1: IMPORT SCIENTIFIC PAPERS (674 records)
-- =============================================================================

INSERT OR IGNORE INTO scientific_references (
    paper_id,
    codename,
    codename_short,
    pdf_filename,
    pdf_path,
    original_filename,
    sector,
    sector_full,
    primary_residue,
    query_folder,
    publication_year,
    data_quality,
    extraction_complete,
    metadata_complete,
    created_at
)
SELECT
    paper_id,
    codename,
    codename_short,
    pdf_filename,
    pdf_path,
    original_filename,
    sector,
    sector_full,
    primary_residue,
    query_folder,
    publication_year,
    'Validated' as data_quality,
    1 as extraction_complete,
    CASE
        WHEN authors IS NOT NULL AND authors != '' THEN 1
        ELSE 0
    END as metadata_complete,
    created_at
FROM validation.scientific_papers;

-- Log import results
SELECT
    COUNT(*) as papers_imported,
    COUNT(DISTINCT sector) as sectors,
    MIN(publication_year) as earliest_year,
    MAX(publication_year) as latest_year
FROM scientific_references;

-- =============================================================================
-- STEP 2: CREATE TEMPORARY RESIDUE CODE MAPPING
-- =============================================================================
-- Map validation DB residue_types to webapp residuos.codigo

-- This temporary table helps map between validation DB and webapp DB
CREATE TEMP TABLE IF NOT EXISTS temp_residue_mapping (
    validation_residue_id INTEGER,
    validation_residue_code TEXT,
    validation_residue_name TEXT,
    webapp_residue_codigo TEXT,
    match_confidence TEXT
);

-- Automatic mapping attempt (by name similarity)
-- NOTE: This will need manual review/adjustment
INSERT INTO temp_residue_mapping (
    validation_residue_id,
    validation_residue_code,
    validation_residue_name,
    webapp_residue_codigo,
    match_confidence
)
SELECT
    vr.residue_id,
    vr.residue_code,
    vr.residue_name,
    wr.codigo,
    CASE
        WHEN LOWER(vr.residue_name) = LOWER(wr.nome) THEN 'Exact'
        WHEN LOWER(vr.residue_name) LIKE '%' || LOWER(wr.nome) || '%' THEN 'Partial'
        WHEN LOWER(wr.nome) LIKE '%' || LOWER(vr.residue_name) || '%' THEN 'Partial'
        ELSE 'Manual_Review_Needed'
    END as match_confidence
FROM validation.residue_types vr
LEFT JOIN residuos wr ON
    LOWER(REPLACE(vr.residue_name, '_', ' ')) = LOWER(REPLACE(wr.nome, '_', ' '));

-- Export mapping for manual review
SELECT * FROM temp_residue_mapping
ORDER BY match_confidence, validation_residue_code;

-- =============================================================================
-- STEP 3: IMPORT CHEMICAL PARAMETERS (8,519 records)
-- =============================================================================
-- Only import parameters where residue mapping is confident

INSERT OR IGNORE INTO parameter_ranges (
    residue_codigo,
    parameter_name,
    value_min,
    value_mean,
    value_max,
    unit,
    min_reference_id,
    mean_reference_id,
    max_reference_id,
    min_page_number,
    mean_page_number,
    max_page_number,
    data_quality,
    extraction_method,
    created_at
)
SELECT
    trm.webapp_residue_codigo as residue_codigo,
    UPPER(vcp.parameter_name) as parameter_name,  -- Standardize to uppercase
    vcp.value_min,
    vcp.value_mean,
    vcp.value_max,
    vcp.unit,

    -- Link to references (using paper_id mapping)
    sr.id as min_reference_id,
    sr.id as mean_reference_id,
    sr.id as max_reference_id,

    -- Page numbers (same source for min/mean/max in this extraction)
    vcp.page_number as min_page_number,
    vcp.page_number as mean_page_number,
    vcp.page_number as max_page_number,

    vcp.data_quality,
    vcp.extraction_method,
    vcp.created_at
FROM validation.chemical_parameters vcp
JOIN temp_residue_mapping trm ON vcp.residue_id = trm.validation_residue_id
JOIN scientific_references sr ON sr.paper_id = vcp.paper_id
WHERE trm.match_confidence IN ('Exact', 'Partial')  -- Only import confident matches
  AND trm.webapp_residue_codigo IS NOT NULL;

-- Log import results
SELECT
    COUNT(*) as parameters_imported,
    COUNT(DISTINCT residue_codigo) as residues_with_params,
    COUNT(DISTINCT parameter_name) as parameter_types,
    COUNT(DISTINCT mean_reference_id) as papers_referenced
FROM parameter_ranges;

-- Parameter type breakdown
SELECT
    parameter_name,
    COUNT(*) as count,
    COUNT(DISTINCT residue_codigo) as residues
FROM parameter_ranges
GROUP BY parameter_name
ORDER BY count DESC;

-- =============================================================================
-- STEP 4: POPULATE RESIDUE-REFERENCE JUNCTION TABLE
-- =============================================================================
-- Create many-to-many links between residues and papers

INSERT OR IGNORE INTO residue_references (
    residue_codigo,
    reference_id,
    provides_parameters,
    parameter_count,
    is_primary_source
)
SELECT
    pr.residue_codigo,
    pr.mean_reference_id as reference_id,
    '[' || GROUP_CONCAT(DISTINCT '"' || pr.parameter_name || '"') || ']' as provides_parameters,
    COUNT(DISTINCT pr.parameter_name) as parameter_count,
    CASE
        WHEN COUNT(DISTINCT pr.parameter_name) >= 3 THEN 1  -- Primary if provides 3+ parameters
        ELSE 0
    END as is_primary_source
FROM parameter_ranges pr
WHERE pr.mean_reference_id IS NOT NULL
GROUP BY pr.residue_codigo, pr.mean_reference_id;

-- Log junction table results
SELECT
    COUNT(*) as total_links,
    COUNT(DISTINCT residue_codigo) as residues_linked,
    COUNT(DISTINCT reference_id) as papers_linked,
    SUM(CASE WHEN is_primary_source = 1 THEN 1 ELSE 0 END) as primary_sources
FROM residue_references;

-- =============================================================================
-- STEP 5: DATA QUALITY CHECKS
-- =============================================================================

-- Check 1: Papers without any parameters
SELECT
    'Papers without parameters' as check_name,
    COUNT(*) as count
FROM scientific_references sr
LEFT JOIN parameter_ranges pr ON sr.id = pr.mean_reference_id
WHERE pr.id IS NULL;

-- Check 2: Parameters without source papers
SELECT
    'Parameters without source' as check_name,
    COUNT(*) as count
FROM parameter_ranges
WHERE mean_reference_id IS NULL;

-- Check 3: Residues without any parameters
SELECT
    'Residues without parameters' as check_name,
    COUNT(*) as count
FROM residuos r
LEFT JOIN parameter_ranges pr ON r.codigo = pr.residue_codigo
WHERE pr.id IS NULL;

-- Check 4: Unmapped residues from validation DB
SELECT
    'Unmapped validation residues' as check_name,
    COUNT(*) as count
FROM temp_residue_mapping
WHERE webapp_residue_codigo IS NULL
   OR match_confidence = 'Manual_Review_Needed';

-- =============================================================================
-- STEP 6: UPDATE RESIDUE STATISTICS IN MAIN TABLE
-- =============================================================================
-- Update residuos table with reference counts

UPDATE residuos
SET references_count = (
    SELECT COUNT(DISTINCT rr.reference_id)
    FROM residue_references rr
    WHERE rr.residue_codigo = residuos.codigo
)
WHERE codigo IN (SELECT DISTINCT residue_codigo FROM residue_references);

-- =============================================================================
-- FINAL SUMMARY REPORT
-- =============================================================================

SELECT '=== IMPORT SUMMARY ===' as report;

SELECT
    'Total Papers Imported' as metric,
    COUNT(*) as value
FROM scientific_references
UNION ALL
SELECT
    'Papers with Complete Metadata',
    COUNT(*)
FROM scientific_references
WHERE metadata_complete = 1
UNION ALL
SELECT
    'Total Parameters Imported',
    COUNT(*)
FROM parameter_ranges
UNION ALL
SELECT
    'Unique Parameter Types',
    COUNT(DISTINCT parameter_name)
FROM parameter_ranges
UNION ALL
SELECT
    'Residues with Parameters',
    COUNT(DISTINCT residue_codigo)
FROM parameter_ranges
UNION ALL
SELECT
    'Total Residue-Paper Links',
    COUNT(*)
FROM residue_references;

-- =============================================================================
-- CLEANUP
-- =============================================================================

-- Keep temp_residue_mapping for manual review
-- Detach validation database
-- DETACH DATABASE validation;

-- =============================================================================
-- POST-MIGRATION TASKS
-- =============================================================================
-- TODO:
-- 1. Review temp_residue_mapping for Manual_Review_Needed entries
-- 2. Run metadata enrichment script to populate authors/DOI/journal
-- 3. Verify PDF paths are accessible from webapp
-- 4. Create backup of database after successful migration
-- 5. Update webapp UI to use new parameter_ranges table
