#!/usr/bin/env python3
"""
Script to query DBpedia for cyclist data using SPARQL.

Usage:
    python scripts/dbpedia/scrape_dbpedia.py

Output:
    - Saves cyclist data to `data/dbpedia_cyclists.json`
"""

import json
import os
import time
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# SPARQL endpoint for DBpedia
SPARQL_ENDPOINT = "https://dbpedia.org/sparql"
SLEEP_BETWEEN_QUERIES = 1.0  # seconds


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
    # Use source-specific subfolder
    source_folder = os.path.join("data", "dbpedia")
    os.makedirs(source_folder, exist_ok=True)
    
    filepath = os.path.join(source_folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")


def main():
    """
    Main function to query DBpedia for cyclist data.
    """
    logger.info("Starting DBpedia scraping...")
    
    # Example SPARQL query to fetch cyclists
    sparql_query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?cyclist ?name ?birthDate ?team ?nationality WHERE {
      ?cyclist a dbo:Cyclist ;
               rdfs:label ?name ;
               dbo:birthDate ?birthDate .
      OPTIONAL { ?cyclist dbo:team ?team . }
      OPTIONAL { ?cyclist dbo:nationality ?nationality . }
      FILTER(LANG(?name) = "en")
    }
    LIMIT 100
    """
    
    # Step 1: Query DBpedia
    results = query_dbpedia(sparql_query)
    if not results:
        logger.error("No results collected. Exiting.")
        return
    
    # Step 2: Save results
    save_to_json(results, "dbpedia_cyclists.json")
    
    logger.info("Scraping completed successfully!")


if __name__ == "__main__":
    main()
