"""
Database Inserters Module - Single Responsibility Principle

Handles all database INSERT/UPDATE operations with transaction support.
Each function performs ONE specific database operation.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from datetime import datetime
import shutil
import logging
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_engine(db_path: str = "data/cp2b_maps.db") -> Engine:
    """
    Create SQLAlchemy engine for database connection.

    Args:
        db_path: Path to SQLite database file

    Returns:
        Engine: SQLAlchemy database engine
    """
    # Convert to absolute path if relative
    if not Path(db_path).is_absolute():
        db_path = Path(__file__).parent.parent.parent / db_path

    engine = create_engine(f"sqlite:///{db_path}")
    logger.info(f"Connected to database: {db_path}")

    return engine


def backup_database(db_path: str = "data/cp2b_maps.db", backup_dir: Optional[str] = None) -> str:
    """
    Create timestamped backup of database file.

    Args:
        db_path: Path to database file to backup
        backup_dir: Optional directory for backups (default: same as db_path)

    Returns:
        str: Path to backup file

    Raises:
        FileNotFoundError: If database file doesn't exist
    """
    db_file = Path(db_path)

    if not db_file.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    if backup_dir is None:
        backup_dir = db_file.parent

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{db_file.stem}_backup_{timestamp}{db_file.suffix}"
    backup_path = Path(backup_dir) / backup_name

    shutil.copy2(db_file, backup_path)
    logger.info(f"Database backup created: {backup_path}")

    return str(backup_path)


def add_scenario_columns_if_missing(engine: Engine) -> None:
    """
    Add scenario columns to municipalities table if they don't exist.

    Args:
        engine: SQLAlchemy database engine
    """
    logger.info("Checking for scenario columns in municipalities table...")

    scenario_columns = {
        'ch4_theoretical': 'REAL',
        'ch4_pessimistic_agricultura': 'REAL',
        'ch4_pessimistic_pecuaria': 'REAL',
        'ch4_pessimistic_urbano': 'REAL',
        'ch4_pessimistic_total': 'REAL',
        'energia_pessimistic_mwh': 'REAL',
        'energia_pessimistic_tj': 'REAL',
        'ch4_realistic_agricultura': 'REAL',
        'ch4_realistic_pecuaria': 'REAL',
        'ch4_realistic_urbano': 'REAL',
        'ch4_realistic_total': 'REAL',
        'energia_realistic_mwh': 'REAL',
        'energia_realistic_tj': 'REAL',
        'ch4_optimistic_agricultura': 'REAL',
        'ch4_optimistic_pecuaria': 'REAL',
        'ch4_optimistic_urbano': 'REAL',
        'ch4_optimistic_total': 'REAL',
        'energia_optimistic_mwh': 'REAL',
        'energia_optimistic_tj': 'REAL',
    }

    with engine.connect() as conn:
        # Get existing columns
        result = conn.execute(text("PRAGMA table_info(municipalities)"))
        existing_cols = {row[1] for row in result}

        # Add missing columns
        for col_name, col_type in scenario_columns.items():
            if col_name not in existing_cols:
                alter_sql = f"ALTER TABLE municipalities ADD COLUMN {col_name} {col_type}"
                conn.execute(text(alter_sql))
                conn.commit()
                logger.info(f"  Added column: {col_name}")

    logger.info("Scenario columns check complete")


def update_municipalities_with_scenarios(engine: Engine, df: pd.DataFrame, backup: bool = True) -> Dict:
    """
    Update municipalities table with scenario data.

    Args:
        engine: SQLAlchemy database engine
        df: DataFrame with scenario data (must have codigo_municipio)
        backup: Whether to create backup before updating

    Returns:
        Dict: Operation report with success status and counts
    """
    logger.info("Updating municipalities with scenario data...")

    if backup:
        db_path = str(engine.url).replace('sqlite:///', '')
        backup_database(db_path)

    # Ensure scenario columns exist
    add_scenario_columns_if_missing(engine)

    # Get scenario columns from DataFrame
    scenario_cols = [col for col in df.columns
                     if any(col.startswith(prefix) for prefix in
                            ['ch4_pessimistic', 'ch4_realistic', 'ch4_optimistic',
                             'energia_pessimistic', 'energia_realistic', 'energia_optimistic',
                             'ch4_theoretical'])]

    if not scenario_cols:
        logger.warning("No scenario columns found in DataFrame")
        return {'success': False, 'error': 'No scenario columns found'}

    updated_count = 0
    failed_count = 0

    try:
        with engine.begin() as conn:  # Transaction context
            for idx, row in df.iterrows():
                codigo = row['codigo_municipio']

                # Build UPDATE query
                set_clauses = [f"{col} = :{col}" for col in scenario_cols]
                update_sql = f"""
                    UPDATE municipalities
                    SET {', '.join(set_clauses)}
                    WHERE codigo_municipio = :codigo_municipio
                """

                # Prepare parameters
                params = {'codigo_municipio': codigo}
                for col in scenario_cols:
                    params[col] = row[col] if pd.notna(row[col]) else None

                result = conn.execute(text(update_sql), params)

                if result.rowcount > 0:
                    updated_count += 1
                else:
                    failed_count += 1
                    logger.warning(f"  Municipality not found: {codigo}")

        logger.info(f"Successfully updated {updated_count} municipalities")

        if failed_count > 0:
            logger.warning(f"Failed to update {failed_count} municipalities (not found in database)")

        return {
            'success': True,
            'updated_count': updated_count,
            'failed_count': failed_count,
            'total_rows': len(df)
        }

    except Exception as e:
        logger.error(f"Error updating municipalities: {e}")
        return {'success': False, 'error': str(e)}


def insert_residues_by_sector(engine: Engine, sector_dfs: Dict[str, pd.DataFrame],
                               backup: bool = True) -> Dict:
    """
    Insert residue data into sector-specific tables.

    Args:
        engine: SQLAlchemy database engine
        sector_dfs: Dictionary mapping table names to DataFrames
                   (e.g., {'residuos_agricolas': df_agricola, ...})
        backup: Whether to create backup before inserting

    Returns:
        Dict: Operation report with success status and counts
    """
    logger.info("Inserting residues by sector...")

    if backup:
        db_path = str(engine.url).replace('sqlite:///', '')
        backup_database(db_path)

    results = {}

    try:
        for table_name, df in sector_dfs.items():
            logger.info(f"Processing table: {table_name} ({len(df)} rows)")

            # For now, we'll store residue metadata (not municipality-level data)
            # This is because the empty residue tables have municipality-specific schema
            # We need to check the actual schema first

            with engine.connect() as conn:
                # Check table schema
                result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                columns = {row[1] for row in result}

            # Map DataFrame columns to table columns
            # This mapping depends on the actual table schema
            # For now, log what we would insert
            logger.info(f"  Table {table_name} has columns: {columns}")
            logger.info(f"  DataFrame has columns: {list(df.columns)}")

            # Count as pending (will implement actual insert in next iteration)
            results[table_name] = {
                'status': 'pending',
                'rows': len(df),
                'message': 'Schema mapping needed'
            }

        return {
            'success': True,
            'tables_processed': len(sector_dfs),
            'results': results
        }

    except Exception as e:
        logger.error(f"Error inserting residues: {e}")
        return {'success': False, 'error': str(e)}


def verify_database_integrity(engine: Engine) -> Dict:
    """
    Verify database integrity after integration.

    Args:
        engine: SQLAlchemy database engine

    Returns:
        Dict: Integrity check report
    """
    logger.info("Verifying database integrity...")

    checks = {}

    try:
        with engine.connect() as conn:
            # Check municipalities count
            result = conn.execute(text("SELECT COUNT(*) FROM municipalities"))
            mun_count = result.fetchone()[0]
            checks['municipalities_count'] = mun_count

            # Check for NULL scenario totals
            result = conn.execute(text("""
                SELECT COUNT(*) FROM municipalities
                WHERE ch4_realistic_total IS NOT NULL
            """))
            scenario_count = result.fetchone()[0]
            checks['municipalities_with_scenarios'] = scenario_count

            # Check residue tables
            residue_tables = ['residuos_agricolas', 'residuos_pecuarios',
                              'residuos_urbanos', 'residuos_industriais']

            for table in residue_tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                checks[f'{table}_count'] = count

        logger.info("Database integrity check complete")
        return {'success': True, 'checks': checks}

    except Exception as e:
        logger.error(f"Error verifying database integrity: {e}")
        return {'success': False, 'error': str(e)}


def execute_sql_file(engine: Engine, sql_file: str) -> Dict:
    """
    Execute SQL commands from a file.

    Args:
        engine: SQLAlchemy database engine
        sql_file: Path to SQL file

    Returns:
        Dict: Execution report
    """
    logger.info(f"Executing SQL file: {sql_file}")

    path = Path(sql_file)
    if not path.exists():
        return {'success': False, 'error': f'SQL file not found: {sql_file}'}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            sql = f.read()

        with engine.begin() as conn:
            conn.execute(text(sql))

        logger.info("SQL file executed successfully")
        return {'success': True}

    except Exception as e:
        logger.error(f"Error executing SQL file: {e}")
        return {'success': False, 'error': str(e)}
