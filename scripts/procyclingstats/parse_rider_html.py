#!/usr/bin/env python3
"""
Script to manually parse rider HTML files and extract rider data.
"""

import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def parse_rider_html(filepath: str) -> dict:
    """
    Parse rider HTML file and extract rider data.
    
    Args:
        filepath: Path to the HTML file.
    
    Returns:
        Dictionary containing rider data.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract rider name
        title = soup.find("title")
        rider_name = title.text.strip() if title else "Unknown"
        
        # Extract rider info
        rider_data = {
            "name": rider_name,
            "team": "",
            "date_of_birth": "",
            "nationality": "",
            "height": "",
            "place_of_birth": "",
            "specialties": {},
            "social_media": {},
            "top_results": [],
            "teams": [],
            "program": [],
            "key_statistics": {},
        }
        
        # Extract team
        subtitle = soup.find("div", class_="subtitle")
        if subtitle:
            h2 = subtitle.find("h2")
            rider_data["team"] = h2.text.strip() if h2 else ""
        
        # Extract date of birth
        dob_li = None
        for li in soup.find_all("li"):
            if "Date of birth" in li.get_text():
                dob_li = li
                break
        if dob_li:
            dob_text = dob_li.get_text(separator=" ", strip=True)
            # Extract the date part (e.g., "3rd June 1998")
            dob_parts = dob_text.replace("Date of birth:", "").strip().split()
            if len(dob_parts) >= 3:
                rider_data["date_of_birth"] = " ".join(dob_parts[:3])
        
        # Extract nationality
        nationality_li = None
        for li in soup.find_all("li"):
            if "Nationality" in li.get_text():
                nationality_li = li
                break
        if nationality_li:
            nationality_text = nationality_li.get_text(separator=" ", strip=True).replace("Nationality:", "").strip()
            rider_data["nationality"] = nationality_text
        
        # Extract height
        height_li = None
        for li in soup.find_all("li"):
            if "Height" in li.get_text():
                height_li = li
                break
        if height_li:
            height_text = height_li.get_text(separator=" ", strip=True)
            # Extract only the height part (e.g., "1.88 m")
            if "Height:" in height_text:
                height_value = height_text.split("Height:")[-1].strip().split()[0]
                rider_data["height"] = height_value
        
        # Extract place of birth
        pob_li = None
        for li in soup.find_all("li"):
            if "Place of birth" in li.get_text():
                pob_li = li
                break
        if pob_li:
            pob_text = pob_li.get_text(separator=" ", strip=True).replace("Place of birth:", "").strip()
            rider_data["place_of_birth"] = pob_text
        
        # Extract specialties
        specialties_div = soup.find("div", string=lambda text: text and "Specialties" in text if text else False)
        if specialties_div:
            specialties_ul = specialties_div.find_next("ul", class_="pps")
            if specialties_ul:
                specialties = {}
                for li in specialties_ul.find_all("li"):
                    xtitle = li.find("div", class_="xtitle")
                    xvalue = li.find("div", class_="xvalue")
                    if xtitle and xvalue:
                        specialty_name = xtitle.get_text(strip=True)
                        specialty_value = xvalue.get_text(strip=True)
                        specialties[specialty_name] = specialty_value
                rider_data["specialties"] = specialties
        
        # Extract social media
        social_media_div = soup.find("div", class_="mt5")
        if social_media_div:
            social_media_ul = social_media_div.find("ul", class_="list horizontal")
            if social_media_ul:
                social_media = {}
                for li in social_media_ul.find_all("li"):
                    a_tag = li.find("a")
                    if a_tag and a_tag.get("href"):
                        platform = a_tag.get_text(strip=True).upper()
                        url = a_tag.get("href")
                        social_media[platform] = url
                rider_data["social_media"] = social_media
        
        # Extract top results
        top_results_div = None
        for div in soup.find_all("div"):
            if "Top results" in div.get_text():
                top_results_div = div
                break
        if top_results_div:
            top_results_ul = top_results_div.find_next("ul", class_="topresults")
            if top_results_ul:
                top_results = []
                for li in top_results_ul.find_all("li"):
                    nrs = li.find("div", class_="nrs")
                    races = li.find("div", class_="races")
                    if nrs and races:
                        result = nrs.get_text(strip=True)
                        race = races.get_text(strip=True)
                        top_results.append({"result": result, "race": race})
                rider_data["top_results"] = top_results
        
        # Extract teams
        teams_div = None
        for div in soup.find_all("div"):
            if "Teams" in div.get_text():
                teams_div = div
                break
        if teams_div:
            teams_ul = teams_div.find_next("ul", class_="rdr-teams2")
            if teams_ul:
                teams = []
                for li in teams_ul.find_all("li"):
                    season = li.find("div", class_="season")
                    name = li.find("div", class_="name")
                    if season and name:
                        teams.append({"season": season.get_text(strip=True), "name": name.get_text(strip=True)})
                rider_data["teams"] = teams
        
        # Extract program
        program_div = None
        for div in soup.find_all("div"):
            if "Program" in div.get_text():
                program_div = div
                break
        if program_div:
            program_ul = program_div.find_next("ul", class_="list dashed flex")
            if program_ul:
                program = []
                for li in program_ul.find_all("li"):
                    bold = li.find("div", class_="bold")
                    ellipsis = li.find("div", class_="ellipsis")
                    if bold and ellipsis:
                        date = bold.get_text(strip=True)
                        race = ellipsis.get_text(strip=True)
                        program.append({"date": date, "race": race})
                rider_data["program"] = program
        
        # Extract key statistics
        key_statistics_div = None
        for div in soup.find_all("div"):
            if "Key statistics" in div.get_text():
                key_statistics_div = div
                break
        if key_statistics_div:
            key_statistics_ul = key_statistics_div.find_next("ul", class_="rider-kpi")
            if key_statistics_ul:
                key_statistics = {}
                for li in key_statistics_ul.find_all("li"):
                    kpi = li.find("div", class_="kpi")
                    title = li.find("div", class_="title")
                    if kpi and title:
                        key_statistics[title.get_text(strip=True)] = kpi.get_text(strip=True)
                rider_data["key_statistics"] = key_statistics
        
        return rider_data
    except Exception as exc:
        logger.error(f"Failed to parse {filepath}: {exc}")
        return {}


def main():
    """
    Main function to parse rider HTML files.
    """
    html_files = [
        "data/procyclingstats/zukowsky.html",
        "data/procyclingstats/hirschi.html",
    ]
    
    for filepath in html_files:
        rider_data = parse_rider_html(filepath)
        if rider_data:
            rider_name = rider_data.get("name", "unknown")
            output_file = f"data/procyclingstats/{rider_name.replace(' ', '_')}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(rider_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved rider data to {output_file}")


if __name__ == "__main__":
    main()
