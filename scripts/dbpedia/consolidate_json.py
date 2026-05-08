#!/usr/bin/env python3
"""
Script to consolidate all DBpedia cyclist JSON files into a single file.

Usage:
    python scripts/dbpedia/consolidate_json.py

Output:
    - Saves consolidated data to `data/dbpedia/dbpedia_cyclists_all.json`
"""

import json
import os
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def consolidate_json() -> None:
    """
    Consolidate all JSON files in data/dbpedia/ into a single file.
    """
    # Ensure data directory exists
    data_dir = "data/dbpedia"
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} does not exist.")
        return
    
    # Collect all JSON files
    json_files = [f for f in os.listdir(data_dir) if f.startswith("dbpedia_cyclists_") and f.endswith(".json")]
    logger.info(f"Found {len(json_files)} JSON files to consolidate.")
    
    # Read and merge all JSON files
    all_records: List[Dict] = []
    for json_file in json_files:
        filepath = os.path.join(data_dir, json_file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                records = json.load(f)
                all_records.extend(records)
            logger.info(f"Loaded {len(records)} records from {json_file}")
        except Exception as exc:
            logger.error(f"Failed to read {json_file}: {exc}")
    
    # Save consolidated data
    output_file = os.path.join(data_dir, "dbpedia_cyclists_all.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Consolidated {len(all_records)} records into {output_file}")


if __name__ == "__main__":
    consolidate_json()
