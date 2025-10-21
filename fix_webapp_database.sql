-- ═══════════════════════════════════════════════════════════════
-- FIX WEBAPP DATABASE - Copy correct values from main database
-- Generated: 2025-10-21
-- Issue: Some values were multiplied by 1000 twice (corruption)
-- Solution: Copy all BMP/TS/VS values from main database
-- ═══════════════════════════════════════════════════════════════

BEGIN TRANSACTION;

-- Attach main database
ATTACH DATABASE 'data/cp2b_panorama.db' AS main_db;

-- Update all residues with correct values from main database
UPDATE residuos
SET
    bmp_medio = (SELECT bmp_medio FROM main_db.residuos WHERE id = residuos.id),
    bmp_min = (SELECT bmp_min FROM main_db.residuos WHERE id = residuos.id),
    bmp_max = (SELECT bmp_max FROM main_db.residuos WHERE id = residuos.id),
    ts_medio = (SELECT ts_medio FROM main_db.residuos WHERE id = residuos.id),
    ts_min = (SELECT ts_min FROM main_db.residuos WHERE id = residuos.id),
    ts_max = (SELECT ts_max FROM main_db.residuos WHERE id = residuos.id),
    vs_medio = (SELECT vs_medio FROM main_db.residuos WHERE id = residuos.id),
    vs_min = (SELECT vs_min FROM main_db.residuos WHERE id = residuos.id),
    vs_max = (SELECT vs_max FROM main_db.residuos WHERE id = residuos.id)
WHERE EXISTS (SELECT 1 FROM main_db.residuos WHERE id = residuos.id);

-- Detach main database
DETACH DATABASE main_db;

COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- VERIFICATION QUERIES (run these after to confirm fix)
-- ═══════════════════════════════════════════════════════════════
-- SELECT COUNT(*), MIN(bmp_medio), MAX(bmp_medio), AVG(bmp_medio) FROM residuos WHERE bmp_medio IS NOT NULL;
-- Expected: max ~850, avg ~241
--
-- SELECT nome, bmp_medio FROM residuos WHERE bmp_medio > 1000;
-- Expected: No rows (all values should be < 1000)
-- ═══════════════════════════════════════════════════════════════
