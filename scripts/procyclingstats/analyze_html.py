#!/usr/bin/env python3
"""
Script to analyze the HTML structure of rider pages.

Usage:
    python scripts/procyclingstats/analyze_html.py
"""

import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def analyze_html(filepath: str, rider_name: str):
    """
    Analyze the HTML structure of a rider page.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Check for common elements
        logger.info(f"\n=== Analyzing {rider_name} ===")
        
        # Check for the main rider info table
        rider_table = soup.find("table", {"class": "profile"})
        if rider_table:
            logger.info(f"✓ Found profile table for {rider_name}")
        else:
            logger.info(f"✗ No profile table found for {rider_name}")
        
        # Check for the results table
        results_table = soup.find("table", {"class": "results"})
        if results_table:
            logger.info(f"✓ Found results table for {rider_name}")
        else:
            logger.info(f"✗ No results table found for {rider_name}")
        
        # Check for the teams history
        teams_history = soup.find("div", {"class": "teams"})
        if teams_history:
            logger.info(f"✓ Found teams history for {rider_name}")
        else:
            logger.info(f"✗ No teams history found for {rider_name}")
        
        # Check for the rider name
        rider_name_element = soup.find("h1", {"class": "name"})
        if rider_name_element:
            logger.info(f"✓ Found rider name: {rider_name_element.text.strip()}")
        else:
            logger.info(f"✗ No rider name found for {rider_name}")
        
        # Check for the rider nationality
        nationality_element = soup.find("span", {"class": "nationality"})
        if nationality_element:
            logger.info(f"✓ Found nationality: {nationality_element.text.strip()}")
        else:
            logger.info(f"✗ No nationality found for {rider_name}")
        
        # Check for the rider birthdate
        birthdate_element = soup.find("span", {"class": "birthdate"})
        if birthdate_element:
            logger.info(f"✓ Found birthdate: {birthdate_element.text.strip()}")
        else:
            logger.info(f"✗ No birthdate found for {rider_name}")
        
    except Exception as exc:
        logger.error(f"Failed to analyze {rider_name}: {exc}")


def main():
    """
    Main function to analyze HTML files.
    """
    # Analyze both rider pages
    analyze_html("data/procyclingstats/zukowsky.html", "Nickolas Zukowsky")
    analyze_html("data/procyclingstats/hirschi.html", "Marc Hirschi")


if __name__ == "__main__":
    main()
