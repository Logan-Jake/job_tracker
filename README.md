# UK Data Engineering Job Market Tracker

A self-hosted data pipeline that tracks the UK data engineering job market over time — listing volume, in-demand skills, and salary trends — by collecting job postings daily, normalizing the data, and storing it in PostgreSQL for analysis.

Runs entirely in Docker on a home server, with secure remote access via Cloudflare Tunnel (no exposed ports, no port forwarding).

## Why this project

Job postings are noisy, inconsistent, and ephemeral — salaries are written a dozen different ways, listings disappear without notice, and "data engineer" means something different at every company. This project turns that mess into structured, queryable, historical data, answering questions like:

- Is demand for data engineering roles rising or falling in the UK?
- Which tools and skills show up most often in job descriptions, and how does that shift over time?
- What's the real salary range for these roles, by seniority and region?
- How long do listings typically stay open?

It's a small end-to-end data engineering system: ingestion, transformation, storage, and scheduling, deployed the way a real service would be.

## How it works

```
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   scraper     │   │  postgres     │   │  cloudflared  │
│ (fetch +      │──▶│  (storage)    │──▶│  (remote      │
│  clean +      │   │               │   │   access)     │
│  load)        │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
       │
   scheduled internally (supercronic), no host cron required
```

1. **Collect** — Pulls UK data engineering listings from job board APIs (Adzuna, Reed) on a daily schedule
2. **Clean** — Parses messy salary text into normalized annual GBP figures, maps locations to UK regions, infers seniority from job titles, and extracts mentioned skills (Python, SQL, Spark, Airflow, dbt, AWS, etc.) from descriptions
3. **Store** — Loads structured records into PostgreSQL, deduplicating against previous runs and tracking which listings are still active
4. **Track** — A daily snapshot table captures listing counts and salary stats over time, enabling trend analysis without re-scanning the full dataset

Everything runs as Docker containers on a `docker-compose` network. A Cloudflare Tunnel gives remote access to the server without opening any inbound ports on the home network.

## Tech stack

| Layer | Tools                                 |
|---|---------------------------------------|
| Language | Python 3.13                           |
| Data collection | Adzuna API, Reed API, `requests`      |
| Validation | Pydantic                              |
| Database | PostgreSQL 16                         |
| DB access / migrations | SQLAlchemy, Alembic                   |
| Scheduling | supercronic (in-container cron)       |
| Containerization | Docker, Docker Compose                |
| Remote access | Cloudflare Tunnel + Cloudflare Access |
| Dashboard | Gafana                                |

## What's in the database

- **`jobs`** — every listing seen, with normalised salary, region, seniority, and active/inactive status tracked across runs
- **`skills`** / **`job_skills`** — many-to-many mapping of jobs to detected skills, for frequency analysis
- **`daily_snapshot`** — daily rollups of listing counts and salary stats, for fast time-series queries
- **`scrape_runs`** — audit log of every collection run (records found, inserted, errors)

## Example questions this enables

```sql
-- Most in-demand skills this month
SELECT s.name, COUNT(*) 
FROM job_skills js
JOIN skills s ON s.id = js.skill_id
JOIN jobs j ON j.id = js.job_id
WHERE j.posted_date >= date_trunc('month', current_date)
GROUP BY s.name
ORDER BY COUNT(*) DESC;

-- Median salary trend by month
SELECT date_trunc('month', snapshot_date) AS month,
       AVG(median_salary_min) AS avg_median_min
FROM daily_snapshot
GROUP BY month
ORDER BY month;
```

## Running it

```bash
git clone https://github.com/yourusername/jobpipeline.git
cd jobpipeline
cp .env.example .env   # add your Adzuna/Reed API keys and DB credentials
docker compose up -d
```

This starts PostgreSQL, the scraper/scheduler, and the Cloudflare Tunnel. The scraper runs on its internal schedule (configurable in `scraper/crontab`); check progress with:

```bash
docker compose logs -f scraper
```

## Project structure

```
jobpipeline/
├── docker-compose.yml
├── scraper/
│   ├── Dockerfile
│   ├── crontab
│   ├── scrapers/          # one module per job source
│   ├── pipeline/          # cleaning, salary parsing, skill extraction
│   ├── run_scraper.py
│   ├── run_clean_and_load.py
│   └── build_daily_snapshot.py
├── db/
│   ├── init/               # schema
│   └── migrations/         # alembic
└── README.md
```

## Design notes

- **Why Docker:** the whole stack (app + database + tunnel) is reproducible with one command, with no host dependencies beyond Docker itself
- **Why Cloudflare Tunnel over port forwarding:** no inbound ports opened on the home network; all connections are outbound from the server, with identity-based access control on top
- **Why normalize salary at ingest time, not query time:** source data is wildly inconsistent (hourly/daily/annual, ranges, missing values) — resolving that once during cleaning keeps every downstream query simple
- **Why track `is_active` instead of just inserting rows:** treating "still listed" as a tracked state (rather than re-scraping from scratch) is what makes duration/longevity analysis possible

## Roadmap

- [ ] Grafana dashboard for listings, salary, and skill trends
- [ ] Additional job sources beyond Adzuna/Reed
- [ ] Time-to-fill analysis (days between first seen and delisted)
- [ ] Salary-by-skill correlation analysis

## License

MIT