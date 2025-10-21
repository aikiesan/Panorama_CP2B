"""
Integration Runner - Orchestrator

Orchestrates the complete data integration pipeline following SOLID principles.
This is the main entry point for running the integration process.
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Optional, Dict

# Import our SOLID modules
try:
    # Try relative import first (when used as package)
    from . import data_loaders
    from . import data_validators
    from . import data_transformers
    from . import database_inserters
except ImportError:
    # Fall back to absolute import (when run directly)
    from scripts.database_integration import data_loaders
    from scripts.database_integration import data_validators
    from scripts.database_integration import data_transformers
    from scripts.database_integration import database_inserters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegrationRunner:
    """
    Main orchestrator for database integration process.

    Coordinates data loading, validation, transformation, and insertion
    following the SOLID principle of Dependency Inversion.
    """

    def __init__(self, validation_base_dir: Optional[str] = None,
                 db_path: str = "data/cp2b_maps.db",
                 dry_run: bool = False):
        """
        Initialize integration runner.

        Args:
            validation_base_dir: Base directory for validated data files
            db_path: Path to SQLite database
            dry_run: If True, validate data but don't modify database
        """
        self.validation_base_dir = validation_base_dir or data_loaders.get_validation_base_dir()
        self.db_path = db_path
        self.dry_run = dry_run
        self.report = {
            'start_time': datetime.now().isoformat(),
            'dry_run': dry_run,
            'steps': {}
        }

        logger.info(f"Initialized IntegrationRunner (dry_run={dry_run})")
        logger.info(f"Validation data: {self.validation_base_dir}")
        logger.info(f"Database: {self.db_path}")

    def discover_files(self) -> Dict:
        """
        Discover all validation data files.

        Returns:
            Dict: File paths for scenarios, factors, etc.
        """
        logger.info("=" * 60)
        logger.info("STEP 1: Discovering validation data files")
        logger.info("=" * 60)

        files = data_loaders.discover_validation_files(self.validation_base_dir)

        self.report['steps']['discovery'] = {
            'success': True,
            'files_found': files
        }

        return files

    def validate_data(self, files: Dict) -> Dict:
        """
        Validate all data files.

        Args:
            files: Dictionary of file paths

        Returns:
            Dict: Validation reports for each file
        """
        logger.info("=" * 60)
        logger.info("STEP 2: Validating data")
        logger.info("=" * 60)

        validation_reports = {}

        # Validate scenarios
        if files.get('scenarios'):
            logger.info("Loading and validating scenario data...")
            df_scenarios = data_loaders.load_scenario_data(files['scenarios'])
            report = data_validators.generate_validation_report(df_scenarios, 'scenarios')
            validation_reports['scenarios'] = report

            if report['overall_valid']:
                logger.info("  Scenario validation: PASSED")
            else:
                logger.warning("  Scenario validation: FAILED")

        # Validate availability factors
        if files.get('factors'):
            logger.info("Loading and validating availability factors...")
            df_factors = data_loaders.load_availability_factors(files['factors'])
            report = data_validators.generate_validation_report(df_factors, 'factors')
            validation_reports['factors'] = report

            if report['overall_valid']:
                logger.info("  Factors validation: PASSED")
            else:
                logger.warning("  Factors validation: FAILED")

        self.report['steps']['validation'] = {
            'success': all(r.get('overall_valid', False) for r in validation_reports.values()),
            'reports': validation_reports
        }

        return validation_reports

    def check_municipality_codes(self, files: Dict) -> Dict:
        """
        Check municipality code matches between validated data and database.

        Args:
            files: Dictionary of file paths

        Returns:
            Dict: Municipality code validation report
        """
        logger.info("=" * 60)
        logger.info("STEP 3: Checking municipality code matches")
        logger.info("=" * 60)

        # Load scenario data for municipality codes
        df_scenarios = data_loaders.load_scenario_data(files['scenarios'])

        # Load existing database municipality codes
        engine = database_inserters.get_database_engine(self.db_path)
        import pandas as pd
        df_db_mun = pd.read_sql("SELECT DISTINCT codigo_municipio FROM municipalities", engine)
        db_codes = df_db_mun['codigo_municipio'].tolist()

        # Validate
        is_valid, report = data_validators.validate_municipality_codes(df_scenarios, db_codes)

        logger.info(f"Municipality match rate: {report.get('match_rate', 0):.1f}%")
        logger.info(f"Matched: {report.get('matched_count', 0)}/{report.get('total_count', 0)}")

        if report.get('unmatched_codes'):
            logger.warning(f"Unmatched codes: {report['unmatched_codes'][:5]}...")

        self.report['steps']['municipality_check'] = {
            'success': is_valid,
            'report': report
        }

        return report

    def transform_data(self, files: Dict) -> Dict:
        """
        Transform validated data to database schema.

        Args:
            files: Dictionary of file paths

        Returns:
            Dict: Transformed DataFrames
        """
        logger.info("=" * 60)
        logger.info("STEP 4: Transforming data to database schema")
        logger.info("=" * 60)

        transformed = {}

        # Transform scenarios
        if files.get('scenarios'):
            logger.info("Transforming scenario data...")
            df_scenarios = data_loaders.load_scenario_data(files['scenarios'])
            df_transformed = data_transformers.transform_scenario_to_municipalities(df_scenarios)
            transformed['scenarios'] = df_transformed
            logger.info(f"  Transformed {len(df_transformed)} municipalities")

        # Transform factors
        if files.get('factors'):
            logger.info("Transforming availability factors...")
            df_factors = data_loaders.load_availability_factors(files['factors'])
            df_transformed = data_transformers.transform_factors_to_residues(df_factors)
            transformed['factors'] = df_transformed
            logger.info(f"  Transformed {len(df_transformed)} residues")

            # Split by sector
            sector_dfs = data_transformers.split_by_sector(df_transformed)
            transformed['sectors'] = sector_dfs

        self.report['steps']['transformation'] = {
            'success': True,
            'scenarios_count': len(transformed.get('scenarios', [])),
            'factors_count': len(transformed.get('factors', [])),
            'sectors': {k: len(v) for k, v in transformed.get('sectors', {}).items()}
        }

        return transformed

    def integrate_scenarios(self, df_scenarios) -> Dict:
        """
        Integrate scenario data into municipalities table.

        Args:
            df_scenarios: Transformed scenario DataFrame

        Returns:
            Dict: Integration result report
        """
        logger.info("=" * 60)
        logger.info("STEP 5: Integrating scenario data")
        logger.info("=" * 60)

        if self.dry_run:
            logger.info("DRY RUN: Skipping actual database update")
            return {
                'success': True,
                'dry_run': True,
                'would_update': len(df_scenarios)
            }

        engine = database_inserters.get_database_engine(self.db_path)
        result = database_inserters.update_municipalities_with_scenarios(
            engine, df_scenarios, backup=True
        )

        self.report['steps']['scenario_integration'] = result

        return result

    def generate_report(self) -> Dict:
        """
        Generate final integration report.

        Returns:
            Dict: Complete integration report
        """
        logger.info("=" * 60)
        logger.info("GENERATING FINAL REPORT")
        logger.info("=" * 60)

        self.report['end_time'] = datetime.now().isoformat()

        # Summary
        all_successful = all(
            step.get('success', False) for step in self.report['steps'].values()
        )

        self.report['summary'] = {
            'overall_success': all_successful,
            'total_steps': len(self.report['steps']),
            'successful_steps': sum(1 for s in self.report['steps'].values() if s.get('success', False))
        }

        logger.info(f"Integration {'SUCCESSFUL' if all_successful else 'FAILED'}")
        logger.info(f"Steps completed: {self.report['summary']['successful_steps']}/{self.report['summary']['total_steps']}")

        return self.report

    def run(self, step: str = 'all') -> Dict:
        """
        Run the complete integration pipeline or specific step.

        Args:
            step: Which step to run ('all', 'validate', 'scenarios', 'factors')

        Returns:
            Dict: Integration report
        """
        logger.info("=" * 60)
        logger.info(f"STARTING INTEGRATION PIPELINE (step={step})")
        logger.info("=" * 60)

        try:
            # Step 1: Discover files
            files = self.discover_files()

            if not files.get('scenarios') or not files.get('factors'):
                logger.error("Missing essential data files!")
                self.report['summary'] = {'overall_success': False, 'error': 'Missing files'}
                return self.report

            # Step 2: Validate
            if step in ['all', 'validate']:
                validation_reports = self.validate_data(files)

                if not all(r.get('overall_valid', False) for r in validation_reports.values()):
                    logger.error("Validation failed! Cannot proceed.")
                    if not self.dry_run:
                        return self.report

            # Step 3: Check municipality codes
            if step in ['all', 'validate', 'scenarios']:
                mun_report = self.check_municipality_codes(files)

                if not mun_report.get('is_valid', False):
                    logger.warning("Municipality code validation failed - review unmatched codes")

            # Step 4: Transform
            if step in ['all', 'scenarios', 'factors']:
                transformed = self.transform_data(files)

            # Step 5: Integrate scenarios
            if step in ['all', 'scenarios']:
                if 'scenarios' in transformed:
                    self.integrate_scenarios(transformed['scenarios'])

            # Step 6: Integrate factors (placeholder for now)
            if step in ['all', 'factors']:
                logger.info("Factors integration: Not yet implemented")

            # Generate final report
            return self.generate_report()

        except Exception as e:
            logger.error(f"Integration pipeline failed: {e}", exc_info=True)
            self.report['error'] = str(e)
            self.report['summary'] = {'overall_success': False}
            return self.report

    def save_report(self, output_path: str) -> None:
        """
        Save integration report to JSON file.

        Args:
            output_path: Path to save report
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        logger.info(f"Report saved to: {output_path}")


def main():
    """
    CLI entry point for integration runner.
    """
    parser = argparse.ArgumentParser(description='PanoramaCP2B Database Integration')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate data without modifying database')
    parser.add_argument('--step', choices=['all', 'validate', 'scenarios', 'factors'],
                        default='all', help='Which step to run')
    parser.add_argument('--validation-dir', type=str,
                        help='Base directory for validation data')
    parser.add_argument('--db-path', type=str, default='data/cp2b_maps.db',
                        help='Path to database file')
    parser.add_argument('--report-output', type=str,
                        help='Path to save integration report JSON')

    args = parser.parse_args()

    # Run integration
    runner = IntegrationRunner(
        validation_base_dir=args.validation_dir,
        db_path=args.db_path,
        dry_run=args.dry_run
    )

    report = runner.run(step=args.step)

    # Save report if requested
    if args.report_output:
        runner.save_report(args.report_output)

    # Exit with appropriate code
    success = report.get('summary', {}).get('overall_success', False)
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
