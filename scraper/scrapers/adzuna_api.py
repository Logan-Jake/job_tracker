import requests
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
#  https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={YOUR_APP_ID}&app_key={YOUR_APP_KEY}


def fetch_jobs(keyword="data engineer", page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": keyword,
        "results_per_page": 1,
        "content-type": "application/json",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def save_raw(response, source="adzuna"):
    out_dir = Path("data/raw") / source
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(response, f, indent=2)
    return out_path


if __name__ == "__main__":
    all_jobs = []              # accumulator list
    page = 1
    max_pages = 1

    while page <= max_pages:   # note: <= so you include page 5, and : at end
        data = fetch_jobs(page=page)
        results = data.get("results", [])
        if not results:        # stop early if API returns nothing
            break
        all_jobs.extend(results)  # .extend merges lists, .append would nest them
        print(f"Page {page}: got {len(results)} jobs")
        page += 1              # don't forget to increment!

    # 3. Save everything once
    path = save_raw({"results": all_jobs})
    print(f"Saved {len(all_jobs)} total jobs to {path}")