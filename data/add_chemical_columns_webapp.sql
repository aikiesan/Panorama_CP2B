-- Add chemical_cn_ratio and chemical_ch4_content columns to webapp database
-- Then copy values from main database

BEGIN TRANSACTION;

-- Add columns if they don't exist
ALTER TABLE residuos ADD COLUMN chemical_cn_ratio REAL;
ALTER TABLE residuos ADD COLUMN chemical_ch4_content REAL;

COMMIT;
