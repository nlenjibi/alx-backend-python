# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose Django port; map with `-p 8000:8000` when running the container
EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
