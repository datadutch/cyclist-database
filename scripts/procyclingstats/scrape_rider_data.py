#!/usr/bin/env python3
"""
Script to scrape rider data from ProCyclingStats and save as JSON files.

Usage:
    python scripts/scrape_rider_data.py

Output:
    - Saves rider profiles to `data/riders.json`
    - Saves startlist data to `data/startlists.json`
"""

import json
import os
import time
import logging
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Progress bar setup
class ProgressBar:
    def __init__(self, total: int, prefix: str = "", suffix: str = "", length: int = 50):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.progress = 0
        self.start_time = time.time()

    def update(self, increment: int = 1):
        self.progress += increment
        percent = self.progress / self.total
        filled_length = int(self.length * percent)
        bar = "█" * filled_length + "-" * (self.length - filled_length)
        elapsed = time.time() - self.start_time
        rate = self.progress / elapsed if elapsed > 0 else 0
        eta = (self.total - self.progress) / rate if rate > 0 else 0
        print(f"\r{self.prefix} |{bar}| {self.progress}/{self.total} [{elapsed:.1f}s<{eta:.1f}s, {rate:.2f} riders/s] {self.suffix}", end="\r")
        if self.progress == self.total:
            print()

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Import the scraping functions
try:
    from procyclingstats import Ranking, Rider, RaceStartlist
except ImportError:
    logger.error("procyclingstats library not found. Install it with: pip install procyclingstats")
    exit(1)

# For Cloudflare-protected sites, we need cloudscraper
try:
    import cloudscraper
    _scraper = cloudscraper.create_scraper()
    _USE_CLOUDSCRAPER = True
except ImportError:
    import requests
    _scraper = requests
    _USE_CLOUDSCRAPER = False

RANKING_BASE = (
    "rankings.php?s=&nation=&age=&zage=&page=smallerorequal"
    "&team=&offset={offset}&teamlevel=&filter=Filter"
)

SLEEP_BETWEEN_REQUESTS = 1.0  # seconds


def get_all_rider_urls() -> List[str]:
    """
    Paginate through the UCI individual ranking and collect all rider URLs.
    """
    rider_urls: List[str] = []
    offset = 0

    while True:
        url = RANKING_BASE.format(offset=offset)
        logger.info(f"Scraping ranking at offset {offset}: {url}")
        try:
            page_ranking = Ranking(url)
            riders = page_ranking.individual_ranking("rider_url")
        except Exception as exc:
            logger.warning(f"Failed at offset {offset}: {exc}")
            break

        if not riders:
            logger.info(f"No riders returned at offset {offset} — done.")
            break

        new = [r["rider_url"] for r in riders if r.get("rider_url") and r["rider_url"] not in rider_urls]
        if not new:
            logger.info(f"No new riders at offset {offset} — done.")
            break

        rider_urls.extend(new)
        logger.info(f"  +{len(new)} riders (total: {len(rider_urls)})")
        offset += 100
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    logger.info(f"Collected {len(rider_urls)} unique rider URLs.")
    return rider_urls


def get_rider_profile(rider_url: str) -> Optional[Dict]:
    """
    Fetch full profile for a single rider.
    Returns a flat dict with profile fields, or None if scraping fails.
    """
    try:
        rider = Rider(rider_url)
        data = rider.parse()

        # Extract current (most recent) team from teams_history (handle missing data)
        team_name = None
        team_url = None
        history = data.get("teams_history") or []
        if history and len(history) > 0:
            current = history[0]  # most recent entry is first
            team_name = current.get("team_name")
            team_url = current.get("team_url")

        # Handle missing or empty fields
        name = data.get("name") or "Unknown"
        nationality = data.get("nationality") or None
        birthdate = data.get("birthdate") or None
        height = data.get("height") or None
        weight = data.get("weight") or None

        return {
            "rider_url": rider_url,
            "name": name,
            "nickname": None,  # Nickname field added, can be populated manually
            "nationality": nationality,
            "birthdate": birthdate,
            "height": height,
            "weight": weight,
            "team_name": team_name,
            "team_url": team_url,
        }
    except Exception as exc:
        logger.warning(f"Failed to scrape rider {rider_url}: {exc}")
        return None


def get_race_startlist(startlist_url: str) -> List[Dict]:
    """
    Fetch and parse the startlist from a ProCyclingStats startlist URL.
    
    Args:
        startlist_url: Full URL to the PCS startlist page
                    (e.g., "https://www.procyclingstats.com/race/giro-ditalia/2026/startlist")
    
    Returns:
        List of rider dicts with keys: rider_url, rider_name, team_name
        Returns empty list on failure.
    """
    try:
        logger.info(f"Fetching startlist from {startlist_url}")
        
        # Use cloudscraper to bypass Cloudflare
        response = _scraper.get(startlist_url, timeout=30)
        response.raise_for_status()
        
        # Parse the startlist
        startlist = RaceStartlist(startlist_url, html=response.text, update_html=False)
        riders = startlist.startlist("rider_url", "rider_name", "team_name")
        
        # Format the results
        result = []
        for rider in riders:
            result.append({
                "rider_url": rider.get("rider_url"),
                "rider_name": rider.get("rider_name"),
                "team_name": rider.get("team_name") or "",
            })
        
        logger.info(f"Found {len(result)} riders in startlist")
        return result
        
    except Exception as exc:
        logger.error(f"Failed to fetch startlist from {startlist_url}: {exc}")
        return []


def save_to_json(data: List[Dict], filename: str, chunk_size: Optional[int] = None) -> None:
    """
    Save data to a JSON file in the data directory.
    If chunk_size is provided, data is saved in chunks.
    """
    filepath = os.path.join("data", filename)
    if chunk_size:
        # Save in chunks
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            chunk_filename = f"{os.path.splitext(filename)[0]}_{i//chunk_size}.json"
            chunk_filepath = os.path.join("data", chunk_filename)
            with open(chunk_filepath, "w", encoding="utf-8") as f:
                json.dump(chunk, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved chunk {i//chunk_size} with {len(chunk)} records to {chunk_filepath}")
    else:
        # Save all data at once
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(data)} records to {filepath}")


def main():
    """
    Main function to scrape and save rider data.
    """
    logger.info("Starting rider data scraping...")
    
    # Step 1: Scrape rider URLs
    rider_urls = get_all_rider_urls()
    if not rider_urls:
        logger.error("No rider URLs collected. Exiting.")
        return
    
    # Step 2: Scrape rider profiles with progress bar
    riders: List[Dict] = []
    progress_bar = ProgressBar(len(rider_urls), prefix="Scraping riders:", suffix="Complete")
    
    for i, url in enumerate(rider_urls, 1):
        profile = get_rider_profile(url)
        if profile:
            riders.append(profile)
        progress_bar.update()
        time.sleep(SLEEP_BETWEEN_REQUESTS)
        
        # Save results to JSON after every 25 riders
        if i % 25 == 0 or i == len(rider_urls):
            chunk_index = i // 25
            save_to_json(riders, f"riders_{chunk_index}.json", chunk_size=100)
            logger.info(f"Saved intermediate results to riders_{chunk_index}.json")
    
    # Step 3: Save rider profiles in chunks of 100
    save_to_json(riders, "riders.json", chunk_size=100)
    
    # Step 4: Example startlist scraping (optional)
    # Uncomment and modify the URL below to scrape a specific race startlist
    # startlist_url = "https://www.procyclingstats.com/race/giro-ditalia/2026/startlist"
    # startlist = get_race_startlist(startlist_url)
    # save_to_json(startlist, "startlists.json")
    
    logger.info("Scraping completed successfully!")


if __name__ == "__main__":
    main()
