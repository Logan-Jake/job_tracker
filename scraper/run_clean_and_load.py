from pipeline.clean import clean_latest
from pipeline.load import insert_adzuna_jobs


def clean_and_load_adzuna():
    df = clean_latest()
    records = list(df.itertuples(index=False, name=None))
    insert_adzuna_jobs(records)
    print(f"Inserted {len(records)} jobs")


if __name__ == "__main__":
    clean_and_load_adzuna()
