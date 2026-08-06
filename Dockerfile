FROM python:3.13-slim

WORKDIR /job_tracker

COPY pyproject.toml /job_tracker/

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir . \
  && curl -fsSLo /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/download/v0.2.48/supercronic-linux-amd64 \
    && chmod +x /usr/local/bin/supercronic


COPY alembic.ini /job_tracker/
COPY crontab /job_tracker/
COPY db/ /job_tracker/db/
COPY scraper/ /job_tracker/scraper/

ENV PYTHONPATH=/job_tracker:/job_tracker/scraper \
    PYTHONUNBUFFERED=1

RUN useradd --create-home appuser && chown -R appuser /job_tracker
USER appuser

WORKDIR /job_tracker/scraper

CMD ["supercronic", "/job_tracker/crontab"]

# TODO: multi-stage build - move curl+supercronic download to a builder stage,
# COPY --from=builder the static binary into final image to drop curl+apt dependencies to save space.