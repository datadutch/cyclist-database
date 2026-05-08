#!/usr/bin/env python3
"""
Script to query DBpedia for cyclist data using SPARQL.

Usage:
    python scripts/dbpedia/scrape_dbpedia.py

Output:
    - Saves cyclist data to `data/dbpedia/dbpedia_cyclists.json`
"""

import json
import os
import time
import logging
import argparse
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs("data/dbpedia", exist_ok=True)

# SPARQL endpoint for DBpedia
SPARQL_ENDPOINT = "https://dbpedia.org/sparql"
SLEEP_BETWEEN_QUERIES = 5.0  # Increased delay to reduce server load

# Pagination settings
BATCH_SIZE = 20  # Reduced batch size to avoid server overload
OFFSET_FILE = "data/dbpedia/offset.txt"
MAX_RECORDS = 6000


def get_offset() -> int:
    """
    Get the last fetched offset from the offset file.
    Returns 0 if the file does not exist.
    """
    try:
        if os.path.exists(OFFSET_FILE):
            with open(OFFSET_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        return 0
    except Exception as exc:
        logger.error(f"Failed to read offset file: {exc}")
        return 0


def save_offset(offset: int) -> None:
    """
    Save the current offset to the offset file.
    """
    try:
        with open(OFFSET_FILE, "w", encoding="utf-8") as f:
            f.write(str(offset))
        logger.info(f"Saved offset: {offset}")
    except Exception as exc:
        logger.error(f"Failed to save offset file: {exc}")


def query_dbpedia(sparql_query: str) -> List[Dict]:
    """
    Query DBpedia using SPARQL and return the results.
    
    Args:
        sparql_query: SPARQL query string.
    
    Returns:
        List of dictionaries representing the query results.
    """
    try:
        import requests
        headers = {
            "Accept": "application/sparql-results+json",
            "User-Agent": "CyclistDatabase/1.0 (https://github.com/datadutch/cyclist-database)",
        }
        
        logger.info("Querying DBpedia SPARQL endpoint...")
        response = requests.get(
            SPARQL_ENDPOINT,
            params={"query": sparql_query, "format": "json"},
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for binding in data.get("results", {}).get("bindings", []):
            result = {}
            for key, value in binding.items():
                result[key] = value.get("value", "")
            results.append(result)
        
        logger.info(f"Found {len(results)} results")
        return results
        
    except Exception as exc:
        logger.error(f"Failed to query DBpedia: {exc}")
        return []


def save_to_json(data: List[Dict], filename: str) -> None:
    """
    Save data to a JSON file in the data directory.
    """
    filepath = os.path.join("data/dbpedia", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Query DBpedia for cyclist data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Number of records to fetch from the current offset",
        default=None,
    )
    return parser.parse_args()


def main():
    """
    Main function to query DBpedia for cyclist data.
    """
    args = parse_args()
    logger.info("Starting DBpedia scraping...")
    
    # Get the last fetched offset
    offset = get_offset()
    logger.info(f"Starting from offset: {offset}")
    
    # Determine the target offset
    target_offset = offset + args.limit if args.limit else MAX_RECORDS
    logger.info(f"Target offset: {target_offset}")
    
    # Fetch batches until target_offset is reached or no more results
    total_fetched = 0
    while offset < target_offset and total_fetched < args.limit:
        # Check if we've reached the target offset
        if offset >= target_offset:
            logger.info(f"Target offset ({target_offset}) reached. Exiting.")
            break
        
        # SPARQL query with pagination (simplified to reduce server load)
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?cyclist ?name ?birthDate WHERE {{
          ?cyclist a dbo:Cyclist ;
                   rdfs:label ?name ;
                   dbo:birthDate ?birthDate .
          FILTER(LANG(?name) = "en")
        }}
        ORDER BY ?name
        LIMIT {BATCH_SIZE}
        OFFSET {offset}
        """
        
        # Step 1: Query DBpedia
        results = query_dbpedia(sparql_query)
        if not results:
            logger.error("No results collected. Exiting.")
            break
        
        # Step 2: Save results
        chunk_index = offset // BATCH_SIZE
        save_to_json(results, f"dbpedia_cyclists_{chunk_index}.json")
        
        # Step 3: Update the offset and total fetched
        new_offset = offset + len(results)
        total_fetched += len(results)
        save_offset(new_offset)
        
        logger.info(f"Saved chunk {chunk_index} with {len(results)} records. Total fetched: {total_fetched}/{args.limit}. Next offset: {new_offset}")
        
        # Step 4: Break if fewer records than batch size (end of results)
        if len(results) < BATCH_SIZE:
            logger.info("Fewer records than batch size. Likely end of results.")
            break
        
        # Step 5: Prepare for next batch
        offset = new_offset
        time.sleep(SLEEP_BETWEEN_QUERIES)
    
    logger.info(f"Scraping completed! Total fetched: {total_fetched} records.")


if __name__ == "__main__":
    main()
