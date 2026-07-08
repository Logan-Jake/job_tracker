from pipeline.clean import clean_latest
from pipeline.load import insert_adzuna_jobs


def main():
    df = clean_latest()
    records = list(df.itertuples(index=False, name=None))
    insert_adzuna_jobs(records)
    print(f"Inserted {len(records)} jobs")


if __name__ == "__main__":
    main()
