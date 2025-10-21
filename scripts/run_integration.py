"""
Standalone Integration Runner Script

Entry point for running the database integration pipeline.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.database_integration import integration_runner

if __name__ == '__main__':
    integration_runner.main()
