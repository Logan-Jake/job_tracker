import json
import requests
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2] #up 3 levels to the root
load_dotenv(ROOT / ".env")


def fetch_jobs(keyword="data engineer"):
    auth = {"app_id": os.getenv("ADZUNA_API_ID"), "app_key": os.getenv("ADZUNA_API_KEY")}
    base = "https://api.adzuna.com/v1/api"
    country = 'gb'
    page = 1
    max_pages = 2
    all_jobs = []
    while True:
        resp = requests.get(
            f"{base}/jobs/{country}/search/{page}",
            params={
                **auth,
                "what": keyword,
                "where": "uk",
                "results_per_page": 50,
                "sort_by": "date",        # date | salary | relevance | hybrid | default
                "salary_min": 50000,        # minimum salary
                "full_time": 1,
                #"part_time": 0,
                #"contract_time": 0,
                #"permanent_time": 0,
                "content-type": "application/json",
            },
            timeout=10,
        )
        resp.raise_for_status()
        response = resp.json()

        results = response["results"]  # break of there is no data
        if not results:
            break

        all_jobs.extend(results)  # add page results to list

        if len(all_jobs) >= response["count"]:  # break when there is no more data
            break

        if page >= max_pages:  # break when we reach the desired number of pages
            break

        page += 1
        time.sleep(0.5)

    # print statements for testing
    # print(f"Fetched {len(all_jobs)} of {response['count']}")

    # print(json.dumps(all_jobs, indent=2))

    # for job in all_jobs:
    #    print(f"ID: {job['id']}")
    return response


def save_raw(response, source="adzuna"):
    out_dir = Path("data/raw") / source
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(response, f, indent=4)
    return out_path


if __name__ == "__main__":
    data = fetch_jobs()
    path = save_raw(data)
    print(f"Saved {len(data.get('results', []))} jobs to {path}")
