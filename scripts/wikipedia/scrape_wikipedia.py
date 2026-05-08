#!/usr/bin/env python3
"""
Script to scrape Wikipedia for cyclist details.

Usage:
    python scripts/wikipedia/scrape_wikipedia.py --name "Alejandro Valverde"

Output:
    - Saves cyclist details to `data/wikipedia/cyclist_details.json`
"""

import json
import os
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs("data/wikipedia", exist_ok=True)


def scrape_wikipedia(cyclist_name: str) -> dict:
    """
    Scrape Wikipedia for cyclist details.
    
    Args:
        cyclist_name: Name of the cyclist to scrape.
    
    Returns:
        Dictionary containing cyclist details.
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Search for the cyclist's Wikipedia page
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={cyclist_name.replace(' ', '+')}"
        headers = {
            "User-Agent": "CyclistDatabase/1.0 (https://github.com/datadutch/cyclist-database)",
        }
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()
        search_results = response.json()
        
        if not search_results[1]:
            logger.error(f"No Wikipedia page found for {cyclist_name}")
            return {}
        
        # Get the first search result (most relevant)
        page_title = search_results[1][0]
        page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        logger.info(f"Fetching Wikipedia page: {page_url}")
        
        # Fetch the Wikipedia page
        response = requests.get(page_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract details from the infobox
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            logger.error("No infobox found on the Wikipedia page.")
            return {}
        
        # Extract years active from professional teams section
        years_active = ""
        for row in infobox.find_all("tr"):
            th = row.find("th")
            if th:
                th_text = th.text.strip().lower()
                # Print all th texts for debugging
                if "team" in th_text or "professional" in th_text or "career" in th_text:
                    logger.info(f"Found relevant th text: {th_text}")
                if "professional teams" in th_text:
                    logger.info(f"Matched professional teams: {th_text}")
                    # The "professional teams" row is a header, so we need to look at the next rows
                    # Extract years from the rows following the "professional teams" header
                    import re
                    year_ranges = []
                    for next_row in row.find_next_siblings("tr"):
                        # Check if the next row is part of the professional teams section
                        td = next_row.find("td")
                        if td:
                            td_text = td.get_text(separator=" ", strip=True)
                            logger.info(f"Next row td text: {td_text}")  # Print for debugging
                            
                            # Extract text from all links in the td
                            link_texts = [link.text.strip() for link in td.find_all("a")]
                            logger.info(f"Link texts: {link_texts}")  # Print for debugging
                            
                            # Use regex to find year ranges in the td text (including text before team names)
                            found_ranges = re.findall(r"\d{4}–\d{4}", td_text)
                            logger.info(f"Found year ranges in td text: {found_ranges}")  # Print for debugging
                            
                            # Also check for single years (e.g., "2023")
                            single_years = re.findall(r"\b\d{4}\b", td_text)
                            logger.info(f"Found single years in td text: {single_years}")  # Print for debugging
                            
                            if found_ranges:
                                year_ranges.extend(found_ranges)
                                logger.info(f"Found year ranges in row: {found_ranges}")
                        else:
                            # Stop if we reach a header row
                            logger.info("Reached header row, stopping.")
                            break
                    if year_ranges:
                        # Convert year ranges to integers for comparison
                        years = []
                        for year_range in year_ranges:
                            start, end = map(int, year_range.split("–"))
                            years.extend([start, end])
                        if years:
                            years_active = f"{min(years)}–{max(years)}"
                            logger.info(f"Found years active: {years_active}")
                    break
        
        # Extract other common details
        birth_date = ""
        birth_place = ""
        height = ""
        weight = ""
        team = ""
        
        for row in infobox.find_all("tr"):
            th = row.find("th")
            if th:
                th_text = th.text.strip().lower()
                td = row.find("td")
                if td:
                    if "born" in th_text:
                        birth_date = td.text.strip()
                    elif "birth place" in th_text:
                        birth_place = td.text.strip()
                    elif "height" in th_text:
                        height = td.text.strip()
                    elif "weight" in th_text:
                        weight = td.text.strip()
                    elif "team" in th_text:
                        team = td.text.strip()
        
        # Compile all extracted details
        details = {
            "name": cyclist_name,
            "wikipedia_url": page_url,
            "years_active": years_active,
            "birth_date": birth_date,
            "birth_place": birth_place,
            "height": height,
            "weight": weight,
            "team": team,
        }
        
        logger.info(f"Extracted details: {details}")
        return details
        
    except Exception as exc:
        logger.error(f"Failed to scrape Wikipedia: {exc}")
        return {}


def save_to_json(data: dict, filename: str) -> None:
    """
    Save data to a JSON file in the data directory.
    """
    filepath = os.path.join("data/wikipedia", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved data to {filepath}")


def main():
    """
    Main function to scrape Wikipedia for cyclist details.
    """
    parser = argparse.ArgumentParser(
        description="Scrape Wikipedia for cyclist details.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the cyclist to scrape",
    )
    args = parser.parse_args()
    
    logger.info(f"Scraping Wikipedia for {args.name}...")
    details = scrape_wikipedia(args.name)
    
    if details:
        save_to_json(details, "cyclist_details.json")
    else:
        logger.error("No details collected.")


if __name__ == "__main__":
    main()
