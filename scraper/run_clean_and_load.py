from pipeline.clean import clean_latest
from pipeline.load import insert_adzuna_jobs


def clean_and_load_adzuna(raw_path):
    df = clean_latest(raw_path)
    records = list(df.itertuples(index=False, name=None))
    insert_adzuna_jobs(records)
    print(f"Inserted {len(records)} jobs")
