from run_scraper import fetch_adzuna
from run_clean_and_load import clean_and_load_adzuna


def run_adzuna_etl():
    fetch_adzuna()
    clean_and_load_adzuna()


if __name__ == "__main__":
    run_adzuna_etl()


