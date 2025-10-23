"""
Database Migration Script - CP2B Validation DB → Webapp DB
Safely migrates 674 papers and 8,519 parameters with rollback capability

Usage:
    python scripts/run_database_migration.py --step all
    python scripts/run_database_migration.py --step 1  # Tables only
    python scripts/run_database_migration.py --step 2  # Import papers
    python scripts/run_database_migration.py --step 3  # Import parameters
    python scripts/run_database_migration.py --dry-run  # Test without commit
"""

import sqlite3
import os
import shutil
from datetime import datetime
from pathlib import Path
import argparse
import json

# Paths
VALIDATION_DB = r"C:\Users\Lucas\Documents\CP2B\Validacao_dados\CP2B_Chemical_Parameters.db"
WEBAPP_DB = r"C:\Users\Lucas\Documents\CP2B\PanoramaCP2B\data\cp2b_panorama.db"
MIGRATIONS_DIR = Path(__file__).parent.parent / "data" / "migrations"
BACKUP_DIR = Path(__file__).parent.parent / "data" / "backups"

# Migration files
MIGRATION_FILES = [
    "003_add_reference_tables.sql",
    "004_import_from_validation_db.sql"
]


def create_backup(db_path: str) -> str:
    """Create timestamped backup of database"""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_name = Path(db_path).stem
    backup_path = BACKUP_DIR / f"{db_name}_backup_{timestamp}.db"

    print(f"📦 Creating backup: {backup_path.name}")
    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup created: {backup_path}")

    return str(backup_path)


def verify_databases():
    """Verify both databases exist and are accessible"""
    print("\n🔍 Verifying databases...")

    if not os.path.exists(VALIDATION_DB):
        raise FileNotFoundError(f"Validation DB not found: {VALIDATION_DB}")

    if not os.path.exists(WEBAPP_DB):
        raise FileNotFoundError(f"Webapp DB not found: {WEBAPP_DB}")

    # Check validation DB structure
    conn = sqlite3.connect(VALIDATION_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = ['scientific_papers', 'residue_types', 'chemical_parameters']
    missing = set(expected_tables) - set(tables)

    if missing:
        raise ValueError(f"Validation DB missing tables: {missing}")

    # Get counts
    cursor.execute("SELECT COUNT(*) FROM scientific_papers")
    paper_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chemical_parameters")
    param_count = cursor.fetchone()[0]

    conn.close()

    print(f"✅ Validation DB verified:")
    print(f"   📄 {paper_count} papers")
    print(f"   🧪 {param_count} parameters")

    # Check webapp DB
    conn = sqlite3.connect(WEBAPP_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM residuos")
    residue_count = cursor.fetchone()[0]

    conn.close()

    print(f"✅ Webapp DB verified:")
    print(f"   🌾 {residue_count} residues")


def run_migration_step_1():
    """Step 1: Create new tables"""
    print("\n📋 Step 1: Creating reference tables...")

    sql_file = MIGRATIONS_DIR / "003_add_reference_tables.sql"

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    conn = sqlite3.connect(WEBAPP_DB)
    cursor = conn.cursor()

    try:
        # Execute SQL (split by semicolon for multiple statements)
        cursor.executescript(sql)
        conn.commit()

        # Verify tables created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%reference%'")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"✅ Tables created: {', '.join(tables)}")

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to create tables: {e}")
    finally:
        conn.close()


def run_migration_step_2(dry_run=False):
    """Step 2: Import papers and parameters"""
    print(f"\n📥 Step 2: Importing data (dry_run={dry_run})...")

    conn_webapp = sqlite3.connect(WEBAPP_DB)
    cursor_webapp = conn_webapp.cursor()

    try:
        # Attach validation database
        cursor_webapp.execute(f"ATTACH DATABASE '{VALIDATION_DB}' AS validation")

        # Import papers
        print("   📄 Importing scientific papers...")
        cursor_webapp.execute("""
            INSERT OR IGNORE INTO scientific_references (
                paper_id, codename, codename_short, pdf_filename, pdf_path,
                original_filename, sector, sector_full, primary_residue,
                query_folder, publication_year, data_quality,
                extraction_complete, metadata_complete, created_at
            )
            SELECT
                paper_id, codename, codename_short, pdf_filename, pdf_path,
                original_filename, sector, sector_full, primary_residue,
                query_folder, publication_year, 'Validated',
                1, 0, created_at
            FROM validation.scientific_papers
        """)

        papers_imported = cursor_webapp.rowcount
        print(f"      ✅ {papers_imported} papers imported")

        # Create residue mapping temp table
        print("   🗺️  Creating residue mapping...")
        cursor_webapp.execute("""
            CREATE TEMP TABLE IF NOT EXISTS temp_residue_mapping (
                validation_residue_id INTEGER,
                validation_residue_code TEXT,
                validation_residue_name TEXT,
                webapp_residue_codigo TEXT,
                match_confidence TEXT
            )
        """)

        # Attempt automatic mapping
        cursor_webapp.execute("""
            INSERT INTO temp_residue_mapping (
                validation_residue_id, validation_residue_code,
                validation_residue_name, webapp_residue_codigo, match_confidence
            )
            SELECT
                vr.residue_id, vr.residue_code, vr.residue_name,
                wr.codigo,
                CASE
                    WHEN LOWER(vr.residue_name) = LOWER(wr.nome) THEN 'Exact'
                    WHEN LOWER(vr.residue_name) LIKE '%' || LOWER(wr.nome) || '%' THEN 'Partial'
                    WHEN LOWER(wr.nome) LIKE '%' || LOWER(vr.residue_name) || '%' THEN 'Partial'
                    ELSE 'Manual_Review'
                END
            FROM validation.residue_types vr
            LEFT JOIN residuos wr ON
                LOWER(REPLACE(vr.residue_name, '_', ' ')) = LOWER(REPLACE(wr.nome, '_', ' '))
        """)

        # Check mapping quality
        cursor_webapp.execute("""
            SELECT match_confidence, COUNT(*) as count
            FROM temp_residue_mapping
            GROUP BY match_confidence
        """)

        print("      Residue mapping results:")
        for confidence, count in cursor_webapp.fetchall():
            print(f"         {confidence}: {count} residues")

        # Export mapping to JSON for review
        cursor_webapp.execute("SELECT * FROM temp_residue_mapping WHERE match_confidence = 'Manual_Review'")
        manual_review = cursor_webapp.fetchall()

        if manual_review:
            mapping_file = BACKUP_DIR / f"residue_mapping_review_{datetime.now().strftime('%Y%m%d')}.json"
            BACKUP_DIR.mkdir(exist_ok=True)

            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump([{
                    'validation_id': row[0],
                    'validation_code': row[1],
                    'validation_name': row[2],
                    'webapp_codigo': row[3],
                    'confidence': row[4]
                } for row in manual_review], f, indent=2, ensure_ascii=False)

            print(f"      ⚠️  {len(manual_review)} residues need manual review")
            print(f"      📄 Saved to: {mapping_file}")

        # Import parameters (only confident matches)
        print("   🧪 Importing chemical parameters...")
        cursor_webapp.execute("""
            INSERT OR IGNORE INTO parameter_ranges (
                residue_codigo, parameter_name, value_min, value_mean, value_max, unit,
                min_reference_id, mean_reference_id, max_reference_id,
                min_page_number, mean_page_number, max_page_number,
                data_quality, extraction_method, created_at
            )
            SELECT
                trm.webapp_residue_codigo, UPPER(vcp.parameter_name),
                vcp.value_min, vcp.value_mean, vcp.value_max, vcp.unit,
                sr.id, sr.id, sr.id,
                vcp.page_number, vcp.page_number, vcp.page_number,
                vcp.data_quality, vcp.extraction_method, vcp.created_at
            FROM validation.chemical_parameters vcp
            JOIN temp_residue_mapping trm ON vcp.residue_id = trm.validation_residue_id
            JOIN scientific_references sr ON sr.paper_id = vcp.paper_id
            WHERE trm.match_confidence IN ('Exact', 'Partial')
              AND trm.webapp_residue_codigo IS NOT NULL
        """)

        params_imported = cursor_webapp.rowcount
        print(f"      ✅ {params_imported} parameters imported")

        # Create residue-reference links
        print("   🔗 Creating residue-reference links...")
        cursor_webapp.execute("""
            INSERT OR IGNORE INTO residue_references (
                residue_codigo, reference_id, provides_parameters, parameter_count, is_primary_source
            )
            SELECT
                pr.residue_codigo, pr.mean_reference_id,
                '[' || GROUP_CONCAT(DISTINCT '"' || pr.parameter_name || '"') || ']',
                COUNT(DISTINCT pr.parameter_name),
                CASE WHEN COUNT(DISTINCT pr.parameter_name) >= 3 THEN 1 ELSE 0 END
            FROM parameter_ranges pr
            WHERE pr.mean_reference_id IS NOT NULL
            GROUP BY pr.residue_codigo, pr.mean_reference_id
        """)

        links_created = cursor_webapp.rowcount
        print(f"      ✅ {links_created} residue-paper links created")

        if not dry_run:
            conn_webapp.commit()
            print("\n✅ Migration committed successfully!")
        else:
            conn_webapp.rollback()
            print("\n🔄 Dry run complete - changes rolled back")

        # Detach validation DB
        cursor_webapp.execute("DETACH DATABASE validation")

    except Exception as e:
        conn_webapp.rollback()
        raise Exception(f"Migration failed: {e}")
    finally:
        conn_webapp.close()


def print_summary():
    """Print migration summary"""
    print("\n📊 Migration Summary:")

    conn = sqlite3.connect(WEBAPP_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scientific_references")
    paper_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM parameter_ranges")
    param_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM residue_references")
    link_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT parameter_name) FROM parameter_ranges")
    param_types = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scientific_references WHERE metadata_complete = 1")
    complete_metadata = cursor.fetchone()[0]

    conn.close()

    print(f"""
    📄 Scientific Papers: {paper_count}
       └─ With complete metadata: {complete_metadata} ({complete_metadata/paper_count*100:.1f}%)

    🧪 Chemical Parameters: {param_count}
       └─ Parameter types: {param_types}

    🔗 Residue-Paper Links: {link_count}
    """)


def main():
    parser = argparse.ArgumentParser(description="CP2B Database Migration Tool")
    parser.add_argument('--step', choices=['all', '1', '2'], default='all',
                       help='Migration step to run (1=tables, 2=import, all=both)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Test migration without committing changes')

    args = parser.parse_args()

    print("🚀 CP2B Database Migration Tool")
    print("=" * 60)

    try:
        # Verify databases
        verify_databases()

        # Create backup
        backup_path = create_backup(WEBAPP_DB)

        # Run migration steps
        if args.step in ['all', '1']:
            run_migration_step_1()

        if args.step in ['all', '2']:
            run_migration_step_2(dry_run=args.dry_run)

        # Print summary
        if not args.dry_run:
            print_summary()

        print("\n✅ Migration completed successfully!")
        print(f"💾 Backup saved at: {backup_path}")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"💾 Restore from backup if needed: {backup_path}")
        raise


if __name__ == "__main__":
    main()
