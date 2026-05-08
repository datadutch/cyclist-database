#!/usr/bin/env python3
"""
Script to inspect the HTML structure of rider pages.

Usage:
    python scripts/procyclingstats/inspect_html.py
"""

import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def inspect_html(filepath: str, rider_name: str):
    """
    Inspect the HTML structure of a rider page.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        
        soup = BeautifulSoup(html, "html.parser")
        
        logger.info(f"\n=== Inspecting {rider_name} ===")
        
        # Print the title
        title = soup.find("title")
        if title:
            logger.info(f"Title: {title.text.strip()}")
        
        # Print all tables
        tables = soup.find_all("table")
        logger.info(f"Found {len(tables)} tables")
        for i, table in enumerate(tables, 1):
            logger.info(f"\nTable {i}:")
            logger.info(f"  Classes: {table.get('class', [])}")
            logger.info(f"  Rows: {len(table.find_all('tr'))}")
        
        # Print all divs
        divs = soup.find_all("div")
        logger.info(f"\nFound {len(divs)} divs")
        for i, div in enumerate(divs, 1):
            if div.get("class"):
                logger.info(f"  Div {i} Classes: {div.get('class', [])}")
        
        # Print all h1 elements
        h1_elements = soup.find_all("h1")
        logger.info(f"\nFound {len(h1_elements)} h1 elements")
        for h1 in h1_elements:
            logger.info(f"  h1: {h1.text.strip()}")
        
        # Print all span elements
        span_elements = soup.find_all("span")
        logger.info(f"\nFound {len(span_elements)} span elements")
        for span in span_elements:
            if span.get("class"):
                logger.info(f"  span Classes: {span.get('class', [])}, Text: {span.text.strip()}")
        
    except Exception as exc:
        logger.error(f"Failed to inspect {rider_name}: {exc}")


def main():
    """
    Main function to inspect HTML files.
    """
    # Inspect both rider pages
    inspect_html("data/procyclingstats/zukowsky.html", "Nickolas Zukowsky")
    inspect_html("data/procyclingstats/hirschi.html", "Marc Hirschi")


if __name__ == "__main__":
    main()
