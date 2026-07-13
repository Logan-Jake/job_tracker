import psycopg2
from db.config import load_config


def insert_adzuna_jobs(job_data):

    sql = ("INSERT INTO adzuna_jobs(id, title, description, company_name, "
            "salary_min, salary_max, salary_is_predicted, contract_type, "
            "contract_time, category_label, latitude, longitude, "
            "location_display, location_area, redirect_url, adref, created) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            "ON CONFLICT (id) DO UPDATE SET last_seen_at = now()")
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, job_data)

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

