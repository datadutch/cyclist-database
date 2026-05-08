#!/usr/bin/env python3
"""
Entry point for the Cyclist Database application.

Usage:
    python main.py [--help] [--version] [--db-path DB_PATH]
"""

import argparse
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Version
__version__ = "0.1.0"


def main(db_path: Optional[str] = None):
    """
    Main function to run the Cyclist Database application.
    
    Args:
        db_path: Path to the database file. Defaults to "data/cyclists.db".
    """
    logger.info(f"Starting Cyclist Database v{__version__}")
    
    if db_path:
        logger.info(f"Using database at: {db_path}")
    else:
        db_path = "data/cyclists.db"
        logger.info(f"Using default database at: {db_path}")
    
    # Placeholder: Add your application logic here
    logger.info("Application logic to be implemented.")
    
    # Example: Initialize database, CLI, etc.
    # from database import init_db
    # from cli import run_cli
    # init_db(db_path)
    # run_cli()


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Cyclist Database Application",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Cyclist Database v{__version__}",
    )
    parser.add_argument(
        "--db-path",
        type=str,
        help="Path to the database file",
        default=None,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(db_path=args.db_path)
