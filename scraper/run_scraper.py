from scrapers.adzuna_api import fetch_jobs, save_raw

# this page runs the api fetches and or scrapers


def fetch_adzuna():
    data = fetch_jobs(keyword="data engineer", num_jobs_to_fetch=5000)
    path = save_raw(data)
    print(f"Saved {len(data.get('results', []))} jobs to {path}")


if __name__ == "__main__":
    fetch_adzuna()
