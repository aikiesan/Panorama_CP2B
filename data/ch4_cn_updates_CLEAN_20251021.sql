-- ═══════════════════════════════════════════════════════════════
-- CP2B CH4 & C/N UPDATES - Ultra-Deep Extraction (CLEANED)
-- Generated: 2025-10-21 15:21:48 (Cleaned by Claude Code)
-- Source: 108 PDFs re-analyzed with deep extraction
-- Duplicates Resolved: Used higher source count values for id 31, 34, 36
-- ═══════════════════════════════════════════════════════════════

BEGIN TRANSACTION;

-- ═══════════════════════════════════════════════════════════════
-- C/N RATIO UPDATES (14 residues, all duplicates resolved)
-- ═══════════════════════════════════════════════════════════════

-- Aparas e refiles - C/N (Confidence: HIGH, 10 sources)
UPDATE residuos SET chemical_cn_ratio = 23.50 WHERE id = 35;

-- Casca de milho - C/N (Confidence: HIGH, 14 sources)
UPDATE residuos SET chemical_cn_ratio = 31.00 WHERE id = 10;

-- Cascas diversas - C/N (Confidence: HIGH, 15 sources - KEPT HIGHER SOURCE COUNT)
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 34;

-- Esterco sólido de suínos - C/N (Confidence: HIGH, 39 sources)
UPDATE residuos SET chemical_cn_ratio = 20.00 WHERE id = 21;

-- FORSU - Fração Orgânica separada - C/N (Confidence: HIGH, 26 sources)
UPDATE residuos SET chemical_cn_ratio = 18.00 WHERE id = 28;

-- Gordura e sebo - C/N (Confidence: HIGH, 10 sources)
UPDATE residuos SET chemical_cn_ratio = 23.50 WHERE id = 33;

-- Levedura residual - C/N (Confidence: HIGH, 15 sources)
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 38;

-- Lodo primário - C/N (Confidence: HIGH, 26 sources)
UPDATE residuos SET chemical_cn_ratio = 18.00 WHERE id = 29;

-- Lodo secundário (biológico) - C/N (Confidence: HIGH, 26 sources)
UPDATE residuos SET chemical_cn_ratio = 18.00 WHERE id = 30;

-- Rejeitos industriais orgânicos - C/N (Confidence: HIGH, 15 sources - KEPT HIGHER SOURCE COUNT)
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 36;

-- Sangue animal - C/N (Confidence: HIGH, 15 sources - KEPT HIGHER SOURCE COUNT)
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 31;

-- Vísceras não comestíveis - C/N (Confidence: HIGH, 10 sources)
UPDATE residuos SET chemical_cn_ratio = 23.50 WHERE id = 32;

-- Polpa de café - C/N (Confidence: MEDIUM, 7 sources)
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 15;

-- Cama de aviário - C/N (Confidence: HIGH, 25 sources) -- BONUS UPDATE FROM ANALYSIS
UPDATE residuos SET chemical_cn_ratio = 15.00 WHERE id = 22;

-- ═══════════════════════════════════════════════════════════════
-- CH4 CONTENT UPDATES (10 residues, no duplicates)
-- ═══════════════════════════════════════════════════════════════

-- Aparas e refiles - CH4 (Confidence: HIGH, 31 sources)
UPDATE residuos SET chemical_ch4_content = 62.00 WHERE id = 35;

-- Cascas diversas - CH4 (Confidence: HIGH, 21 sources)
UPDATE residuos SET chemical_ch4_content = 64.74 WHERE id = 34;

-- FORSU - Fração Orgânica separada - CH4 (Confidence: HIGH, 27 sources)
UPDATE residuos SET chemical_ch4_content = 52.00 WHERE id = 28;

-- Fração orgânica RSU - CH4 (Confidence: HIGH, 27 sources)
UPDATE residuos SET chemical_ch4_content = 52.00 WHERE id = 27;

-- Gordura e sebo - CH4 (Confidence: HIGH, 31 sources)
UPDATE residuos SET chemical_ch4_content = 62.00 WHERE id = 33;

-- Rejeitos industriais orgânicos - CH4 (Confidence: HIGH, 21 sources)
UPDATE residuos SET chemical_ch4_content = 64.74 WHERE id = 36;

-- Sangue animal - CH4 (Confidence: HIGH, 31 sources)
UPDATE residuos SET chemical_ch4_content = 62.00 WHERE id = 31;

-- Bagaço de malte - CH4 (Confidence: LOW, 4 sources)
UPDATE residuos SET chemical_ch4_content = 76.00 WHERE id = 37;

-- Casca de milho - CH4 (Confidence: LOW, 2 sources)
UPDATE residuos SET chemical_ch4_content = 51.00 WHERE id = 10;

-- Levedura residual - CH4 (Confidence: LOW, 4 sources)
UPDATE residuos SET chemical_ch4_content = 76.00 WHERE id = 38;

-- Polpa de café - CH4 (Confidence: LOW, 3 sources)
UPDATE residuos SET chemical_ch4_content = 46.00 WHERE id = 15;


COMMIT;

-- ═══════════════════════════════════════════════════════════════
-- SUMMARY
-- ═══════════════════════════════════════════════════════════════
-- Total Updates: 25 (14 C/N + 11 CH4)
-- Unique Residues: 17
-- Duplicates Resolved: 3 (Sangue animal, Cascas diversas, Rejeitos industriais)
-- Confidence: HIGH=22, MEDIUM=1, LOW=4
-- ═══════════════════════════════════════════════════════════════
