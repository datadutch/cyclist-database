#!/usr/bin/env python3
"""
Script to compare the HTML structure of two rider pages.

Usage:
    python scripts/procyclingstats/compare_riders.py
"""

import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# For Cloudflare-protected sites, we need cloudscraper
try:
    import cloudscraper
    _scraper = cloudscraper.create_scraper()
    _USE_CLOUDSCRAPER = True
except ImportError:
    import requests
    _scraper = requests
    _USE_CLOUDSCRAPER = False


def fetch_rider_page(rider_url: str) -> Optional[str]:
    """
    Fetch the HTML content of a rider page.
    """
    try:
        logger.info(f"Fetching rider page: {rider_url}")
        response = _scraper.get(rider_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as exc:
        logger.error(f"Failed to fetch rider page {rider_url}: {exc}")
        return None


def compare_riders():
    """
    Compare the HTML structure of two rider pages.
    """
    # Rider URLs to compare
    zukowsky_url = "https://www.procyclingstats.com/rider/nickolas-zukowsky"
    hirschi_url = "https://www.procyclingstats.com/rider/marc-hirschi"
    
    # Fetch the HTML for both riders
    zukowsky_html = fetch_rider_page(zukowsky_url)
    hirschi_html = fetch_rider_page(hirschi_url)
    
    # Compare the HTML
    if zukowsky_html and hirschi_html:
        logger.info("Both rider pages fetched successfully.")
        logger.info(f"Zukowsky HTML length: {len(zukowsky_html)}")
        logger.info(f"Hirschi HTML length: {len(hirschi_html)}")
        
        # Save HTML to files for inspection
        with open("data/procyclingstats/zukowsky.html", "w", encoding="utf-8") as f:
            f.write(zukowsky_html)
        with open("data/procyclingstats/hirschi.html", "w", encoding="utf-8") as f:
            f.write(hirschi_html)
        
        logger.info("HTML files saved to data/procyclingstats/ for inspection.")
    else:
        logger.error("Failed to fetch one or both rider pages.")


if __name__ == "__main__":
    compare_riders()
