#!/usr/bin/env python3
"""
Script to deduplicate cyclist entries in dbpedia_cyclists.json
Keeps the first occurrence of each unique cyclist URI.
"""

import json
from collections import OrderedDict

# Read the input file
input_file = 'data/dbpedia/dbpedia_cyclists.json'
output_file = 'data/dbpedia/dbpedia_cyclists.json'

print(f"Reading {input_file}...")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Original count: {len(data)} entries")

# Deduplicate using OrderedDict to preserve order
seen = set()
deduplicated = []
for entry in data:
    cyclist_uri = entry.get('cyclist')
    if cyclist_uri and cyclist_uri not in seen:
        seen.add(cyclist_uri)
        deduplicated.append(entry)
    elif not cyclist_uri:
        # Keep entries without cyclist URI (though this shouldn't happen)
        deduplicated.append(entry)

print(f"Deduplicated count: {len(deduplicated)} entries")
print(f"Removed {len(data) - len(deduplicated)} duplicates")

# Write back to file
print(f"Writing to {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(deduplicated, f, indent=2, ensure_ascii=False)

print("Done!")