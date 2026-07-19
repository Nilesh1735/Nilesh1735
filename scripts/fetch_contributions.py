import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

USERNAME = "Nilesh1735"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "contributions.json")

def fetch_contributions():
    print(f"Fetching contributions for {USERNAME}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    days = []
    for rect in soup.find_all("rect"):
        date = rect.get("data-date")
        count = rect.get("data-count")
        level = rect.get("data-level")
        if date and count is not None:
            days.append({"date": date, "count": int(count), "level": int(level) if level else 0})

    days.sort(key=lambda x: x["date"])
    total = sum(day["count"] for day in days)

    data = {"username": USERNAME, "total": total, "days": days}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {total} contributions.")

if __name__ == "__main__":
    fetch_contributions()