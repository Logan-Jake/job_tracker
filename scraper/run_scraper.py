from scrapers.adzuna_api import fetch_jobs, save_raw

# this page runs the api fetches and or scrapers

data = fetch_jobs()
path = save_raw(data)
print(f"Saved {len(data.get('results', []))} jobs to {path}")