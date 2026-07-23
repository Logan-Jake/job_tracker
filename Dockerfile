FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install --no-cache-dir

COPY db/ /app/
COPY scraper/ /app/

ENV PYTHONPATH=???

CMD ["python", "--version"]