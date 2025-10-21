-- ═══════════════════════════════════════════════════════════════
-- FIX WEBAPP DATABASE - Direct UPDATE statements
-- Generated: 2025-10-21
-- Issue: Values were multiplied by 1000 twice
-- Solution: Direct UPDATE with correct values
-- ═══════════════════════════════════════════════════════════════

BEGIN TRANSACTION;

-- Update all corrupted residues (those with BMP > 1000)
-- Values are copied from the correct main database

UPDATE residuos SET bmp_medio = 850.0, bmp_min = 680.0, bmp_max = 1020.0 WHERE id = 33; -- Gordura e sebo
UPDATE residuos SET bmp_medio = 620.0, bmp_min = 200.0, bmp_max = 756.0 WHERE id = 24; -- Carcaças e mortalidade
UPDATE residuos SET bmp_medio = 450.0, bmp_min = 255.0, bmp_max = 600.0 WHERE id = 31; -- Sangue animal
UPDATE residuos SET bmp_medio = 420.0, bmp_min = 378.0, bmp_max = 462.0 WHERE id = 38; -- Levedura residual
UPDATE residuos SET bmp_medio = 400.0, bmp_min = 360.0, bmp_max = 440.0 WHERE id = 12; -- Casca de soja
UPDATE residuos SET bmp_medio = 350.0, bmp_min = 315.0, bmp_max = 385.0 WHERE id = 35; -- Aparas e refiles
UPDATE residuos SET bmp_medio = 320.0, bmp_min = 288.0, bmp_max = 352.0 WHERE id = 36; -- Rejeitos industriais orgânicos
UPDATE residuos SET bmp_medio = 300.0, bmp_min = 200.0, bmp_max = 400.0 WHERE id = 3; -- Vinhaça
UPDATE residuos SET bmp_medio = 290.0, bmp_min = 218.0, bmp_max = 400.0 WHERE id = 22; -- Cama de aviário
UPDATE residuos SET bmp_medio = 280.0, bmp_min = 252.0, bmp_max = 308.0 WHERE id = 34; -- Cascas diversas
UPDATE residuos SET bmp_medio = 250.0, bmp_min = 120.0, bmp_max = 400.0 WHERE id = 2; -- Torta de filtro
UPDATE residuos SET bmp_medio = 230.0, bmp_min = 207.0, bmp_max = 253.0 WHERE id = 27; -- Conteúdo ruminal
UPDATE residuos SET bmp_medio = 220.0, bmp_min = 150.0, bmp_max = 350.0 WHERE id = 5; -- Bagaço de citros
UPDATE residuos SET bmp_medio = 220.0, bmp_min = 198.0, bmp_max = 242.0 WHERE id = 37; -- Bagaço de malte
UPDATE residuos SET bmp_medio = 180.0, bmp_min = 162.0, bmp_max = 198.0 WHERE id = 6; -- Cascas de citros
UPDATE residuos SET bmp_medio = 170.0, bmp_min = 150.0, bmp_max = 200.0 WHERE id = 13; -- Palha de soja
UPDATE residuos SET bmp_medio = 170.0, bmp_min = 80.0, bmp_max = 250.0 WHERE id = 28; -- Lodo de frigoríficos
UPDATE residuos SET bmp_medio = 150.0, bmp_min = 130.0, bmp_max = 170.0 WHERE id = 4; -- Palha de cana
UPDATE residuos SET bmp_medio = 150.0, bmp_min = 135.0, bmp_max = 165.0 WHERE id = 7; -- Folhas de citros
UPDATE residuos SET bmp_medio = 150.0, bmp_min = 135.0, bmp_max = 165.0 WHERE id = 11; -- Palha de milho
UPDATE residuos SET bmp_medio = 120.0, bmp_min = 100.0, bmp_max = 150.0 WHERE id = 1; -- Bagaço de cana
UPDATE residuos SET bmp_medio = 115.0, bmp_min = 92.0, bmp_max = 138.0 WHERE id = 1; -- Bagaço de cana (corrected)
UPDATE residuos SET bmp_medio = 100.0, bmp_min = 90.0, bmp_max = 110.0 WHERE id = 18; -- Galhos e ponteiros
UPDATE residuos SET bmp_medio = 80.0, bmp_min = 72.0, bmp_max = 88.0 WHERE id = 17; -- Casca de eucalipto

COMMIT;
