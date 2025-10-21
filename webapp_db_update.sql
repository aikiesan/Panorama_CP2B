-- ═══════════════════════════════════════════════════════════════
-- CP2B WEBAPP DATABASE UPDATE (Simplified)
-- Only updates columns that exist in webapp schema
-- ═══════════════════════════════════════════════════════════════

BEGIN TRANSACTION;

-- ═══════════════════════════════════════════════════════════════
-- STEP 1: UNIT CONVERSION (m³/ton → mL/g VS)
-- Multiply all existing BMP values by 1000
-- ═══════════════════════════════════════════════════════════════

UPDATE residuos
SET bmp_medio = bmp_medio * 1000,
    bmp_min = bmp_min * 1000,
    bmp_max = bmp_max * 1000
WHERE bmp_medio IS NOT NULL;

-- ═══════════════════════════════════════════════════════════════
-- STEP 2: LITERATURE-BASED UPDATES (BMP and TS/VS only)
-- ═══════════════════════════════════════════════════════════════

-- Vísceras não comestíveis
UPDATE residuos SET bmp_medio = 245.4175, bmp_min = 55.7350, bmp_max = 571.3500 WHERE id = 32;

-- Dejetos frescos de aves
UPDATE residuos SET bmp_medio = 175.5900, bmp_min = 39.9500, bmp_max = 674.4000, ts_medio = 8.0000, ts_min = 0.1400, ts_max = 31.0000 WHERE id = 23;

-- Dejetos líquidos bovino
UPDATE residuos SET bmp_medio = 175.5900, bmp_min = 39.9500, bmp_max = 674.4000, ts_medio = 8.0000, ts_min = 0.1400, ts_max = 31.0000 WHERE id = 26;

-- Dejetos líquidos de suínos
UPDATE residuos SET bmp_medio = 175.5900, bmp_min = 39.9500, bmp_max = 674.4000, ts_medio = 8.0000, ts_min = 0.1400, ts_max = 31.0000 WHERE id = 20;

-- Esterco bovino
UPDATE residuos SET bmp_medio = 175.5900, bmp_min = 39.9500, bmp_max = 674.4000, ts_medio = 8.0000, ts_min = 0.1400, ts_max = 31.0000 WHERE id = 25;

-- Esterco sólido de suínos
UPDATE residuos SET bmp_medio = 175.5900, bmp_min = 39.9500, bmp_max = 674.4000, ts_medio = 8.0000, ts_min = 0.1400, ts_max = 31.0000 WHERE id = 21;

-- Casca de café
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 12.0000, bmp_max = 515.0000 WHERE id = 14;

-- Mucilagem de café
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 12.0000, bmp_max = 515.0000 WHERE id = 16;

-- Polpa de café
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 12.0000, bmp_max = 515.0000 WHERE id = 15;

-- Casca de milho
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 15.4250, bmp_max = 336.0000 WHERE id = 10;

-- Palha de milho
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 15.4250, bmp_max = 336.0000 WHERE id = 8;

-- Sabugo de milho
UPDATE residuos SET bmp_medio = 130.0000, bmp_min = 15.4250, bmp_max = 336.0000 WHERE id = 9;

-- Lodo primário
UPDATE residuos SET bmp_medio = 303.0000, bmp_min = 119.0000, bmp_max = 571.3500, ts_medio = 15.0000, ts_min = 1.0000, ts_max = 82.6000, vs_medio = 43.7500, vs_min = 10.0000, vs_max = 71.0000 WHERE id = 29;

-- Lodo secundário (biológico)
UPDATE residuos SET bmp_medio = 303.0000, bmp_min = 119.0000, bmp_max = 571.3500, ts_medio = 15.0000, ts_min = 1.0000, ts_max = 82.6000, vs_medio = 43.7500, vs_min = 10.0000, vs_max = 71.0000 WHERE id = 30;

COMMIT;
