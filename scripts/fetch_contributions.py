import requests
from bs4 import BeautifulSoup
import json
import os
import re

USERNAME = "Nilesh1735"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "contributions.json")

def fetch_contributions():
    print(f"Fetching contributions for {USERNAME}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching data: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Use Regex to find the exact number anywhere in the HTML text
    total = 0
    text = soup.get_text()
    match = re.search(r'([\d,]+)\s+contributions', text)
    if match:
        total = int(match.group(1).replace(',', ''))
            
    print(f"Total contributions found: {total}")
    
    days = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level")
        
        if date:
            level_val = int(level) if level is not None else 0
            days.append({
                "date": date,
                "count": 0, # We don't need the exact day count, just the level for colors
                "level": level_val
            })

    print(f"Found {len(days)} days of contribution data.")
    
    if not days:
        print("No day data found.")
        return

    data = {
        "username": USERNAME,
        "total": total,
        "days": days
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved {total} contributions to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_contributions()