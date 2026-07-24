FROM python:3.13-slim

WORKDIR /job_tracker

COPY pyproject.toml /job_tracker/

RUN pip install --no-cache-dir .

COPY db/ /job_tracker/db/
COPY scraper/ /job_tracker/scraper/

ENV PYTHONPATH=/job_tracker:/job_tracker/scraper \
    PYTHONUNBUFFERED=1

RUN useradd --create-home appuser && chown -R appuser /job_tracker
USER appuser

WORKDIR /job_tracker/scraper

CMD ["python", "--version"]