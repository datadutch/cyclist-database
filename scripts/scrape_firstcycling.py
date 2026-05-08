#!/usr/bin/env python3
"""
Script to scrape race results from firstcycling.com.

Usage:
    python scripts/scrape_firstcycling.py

Output:
    - Saves race results to `data/firstcycling_results.json`
"""

import json
import os
import time
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Use cloudscraper to handle potential Cloudflare protection
try:
    import cloudscraper
    scraper = cloudscraper.create_scraper()
except ImportError:
    import requests
    scraper = requests

# Constants
BASE_URL = "https://firstcycling.com"
SLEEP_BETWEEN_REQUESTS = 2.0  # seconds


def fetch_race_results(race_url: str) -> List[Dict]:
    """
    Fetch and parse race results from a firstcycling.com race URL.
    
    Args:
        race_url: Full URL to the race results page.
    
    Returns:
        List of rider results with keys: position, rider_name, team, time.
        Returns empty list on failure.
    """
    try:
        logger.info(f"Fetching race results from {race_url}")
        response = scraper.get(race_url, timeout=30)
        response.raise_for_status()
        
        # Parse the HTML (placeholder: replace with actual parsing logic)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Example: Extract race results (adjust selectors based on actual HTML structure)
        results = []
        rows = soup.select("table.result tr")  # Update selector as needed
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 4:
                results.append({
                    "position": cols[0].text.strip(),
                    "rider_name": cols[1].text.strip(),
                    "team": cols[2].text.strip(),
                    "time": cols[3].text.strip(),
                })
        
        logger.info(f"Found {len(results)} results")
        return results
        
    except Exception as exc:
        logger.error(f"Failed to fetch race results from {race_url}: {exc}")
        return []


def save_to_json(data: List[Dict], filename: str) -> None:
    """
    Save data to a JSON file in the data directory.
    """
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")


def main():
    """
    Main function to scrape race results from firstcycling.com.
    """
    logger.info("Starting firstcycling.com scraping...")
    
    # Example race URL (replace with actual URL)
    race_url = "https://firstcycling.com/race.php?r=123&y=2026"  # Placeholder
    
    # Step 1: Fetch race results
    results = fetch_race_results(race_url)
    if not results:
        logger.error("No results collected. Exiting.")
        return
    
    # Step 2: Save results
    save_to_json(results, "firstcycling_results.json")
    
    logger.info("Scraping completed successfully!")


if __name__ == "__main__":
    main()
