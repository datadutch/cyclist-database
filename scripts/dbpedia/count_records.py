#!/usr/bin/env python3
"""
Script to count the total number of cyclist records in DBpedia.

Usage:
    python scripts/dbpedia/count_records.py

Output:
    - Saves the count to `data/dbpedia/record_count.txt`
"""

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def count_dbpedia_records() -> int:
    """
    Query DBpedia to count the total number of cyclist records.
    
    Returns:
        Total number of cyclist records.
    """
    try:
        import requests
        
        # SPARQL query to count cyclists
        sparql_query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT (COUNT(?cyclist) AS ?count) WHERE {
          ?cyclist a dbo:Cyclist ;
                   rdfs:label ?name .
          FILTER(LANG(?name) = "en")
        }
        """
        
        logger.info("Querying DBpedia to count cyclist records...")
        response = requests.get(
            "https://dbpedia.org/sparql",
            params={"query": sparql_query, "format": "json"},
            headers={
                "Accept": "application/sparql-results+json",
                "User-Agent": "CyclistDatabase/1.0 (https://github.com/datadutch/cyclist-database)",
            },
            timeout=30,
        )
        response.raise_for_status()
        
        data = response.json()
        count = int(data.get("results", {}).get("bindings", [{}])[0].get("count", {}).get("value", 0))
        
        logger.info(f"Found {count} cyclist records in DBpedia.")
        return count
        
    except Exception as exc:
        logger.error(f"Failed to count DBpedia records: {exc}")
        return 0


def save_count(count: int) -> None:
    """
    Save the record count to a file.
    """
    with open("data/dbpedia/record_count.txt", "w", encoding="utf-8") as f:
        f.write(str(count))
    logger.info(f"Saved record count to data/dbpedia/record_count.txt")


def main():
    """
    Main function to count DBpedia records.
    """
    count = count_dbpedia_records()
    if count > 0:
        save_count(count)
    else:
        logger.error("No records counted.")


if __name__ == "__main__":
    main()
