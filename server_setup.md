# Job Tracker Server Setup Guide

This document describes how to deploy the Job Tracker scraper and PostgreSQL database on an Ubuntu server.

## Prerequisites

- Ubuntu server with SSH access
- PostgreSQL installed and running
- Python 3.10+
- python3.14-venv
- Adzuna API credentials ([developer.adzuna.com](https://developer.adzuna.com))

## 1. Clone the Repository

```bash
ssh your-server
git clone https://github.com/Logan-Jake/job_tracker.git
cd job_tracker
```

## 2. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install psycopg2-binary requests pandas python-dotenv numpy
```

> **Note:** The `requirements.txt` in the repo has a UTF-16 encoding issue. Install dependencies manually as shown above, or re-save the file as UTF-8 and run `pip install -r requirements.txt`.

## 3. Create the Database and Table

Connect to PostgreSQL as the superuser and run the schema setup:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE job_tracker;
\c job_tracker

CREATE ROLE python_user WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    NOBYPASSRLS
    CONNECTION LIMIT -1
    PASSWORD 'your_secure_password';

GRANT pg_write_all_data, pg_read_all_data TO python_user;

CREATE TABLE adzuna_jobs (
    id                  BIGINT PRIMARY KEY,
    title               TEXT NOT NULL,
    description         TEXT,
    company_name        TEXT,
    salary_min          NUMERIC(10,2),
    salary_max          NUMERIC(10,2),
    salary_is_predicted BOOLEAN,
    contract_type       TEXT,
    contract_time       TEXT,
    category_label      TEXT,
    latitude            NUMERIC(9,6),
    longitude           NUMERIC(9,6),
    location_display    TEXT,
    location_area       TEXT,
    redirect_url        TEXT,
    adref               TEXT,
    is_active           BOOLEAN DEFAULT TRUE,
    created             TIMESTAMPTZ,
    last_seen_at        TIMESTAMPTZ DEFAULT now(),
    inserted_at         TIMESTAMPTZ DEFAULT now()
);

\q
```

## 4. Configure Database Connection

Create `db/database.ini` in the project root. This file is read by `db/config.py` at runtime.

```ini
[postgresql]
host=localhost
database=job_tracker
user=python_user
password=your_secure_password
```

> **Security:** Add `database.ini` to `.gitignore` to keep credentials out of version control.

## 5. Configure API Keys

Create a `.env` file in the project root:

```
ADZUNA_API_ID=your_app_id
ADZUNA_API_KEY=your_api_key
```

> **Security:** Add `.env` to `.gitignore`.

## 6. Run Manually to Verify

From the project root, activate the virtual environment and run both scripts in sequence:

```bash
source venv/bin/activate
cd scraper

# Step 1 — Fetch jobs from the Adzuna API and save raw JSON
python run_scraper.py

# Step 2 — Clean the data and load into PostgreSQL
python run_clean_and_load.py
```

Verify data was inserted:

```bash
sudo -u postgres psql -d job_tracker -c "SELECT count(*) FROM adzuna_jobs;"
```

## 7. Schedule with Cron

Add a cron job to run the scraper daily at 8:00 AM:

```bash
crontab -e
```

```
0 8 * * * cd /home/youruser/job_tracker/scraper && /home/youruser/job_tracker/venv/bin/python run_scraper.py && /home/youruser/job_tracker/venv/bin/python run_clean_and_load.py >> /home/youruser/job_tracker/cron.log 2>&1
```

Replace `/home/youruser/` with the actual path to the project.

To confirm the cron job is registered:

```bash
crontab -l
```

## Project Structure

```
job_tracker/
├── .env                        # API keys (not committed)
├── db/
│   ├── config.py               # Reads database.ini
│   ├── database.ini            # DB credentials (not committed)
│   ├── init/
│   └── migrations/
├── scraper/
│   ├── run_scraper.py          # Fetches jobs → saves raw JSON
│   ├── run_clean_and_load.py   # Cleans → inserts into PostgreSQL
│   ├── scrapers/
│   │   └── adzuna_api.py       # Adzuna API client
│   └── pipeline/
│       ├── clean.py            # Data cleaning/transformation
│       └── load.py             # PostgreSQL insert logic
└── data/
    └── raw/                    # Raw JSON files (created at runtime)
```