from run_scraper import fetch_adzuna
from run_clean_and_load import clean_and_load_adzuna

KEYWORDS = [
    "Data Engineer",
    "Data Scientist",
    "Data Analyst",
    "SQL Developer"
]


def run_adzuna_etl():
    for keyword in KEYWORDS:
        print(f"--- Running ETL for: {keyword} ---")
        path = fetch_adzuna(keyword, num_jobs_to_fetch=6000)  # min 1 page / 50 jobs
        clean_and_load_adzuna(path)


if __name__ == "__main__":
    run_adzuna_etl()
