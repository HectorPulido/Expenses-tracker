# Debian "slim" is multi-arch and all of our dependencies ship prebuilt wheels
# for both amd64 and arm64, so the image builds with no compilation step and no
# platform-specific build tools. This is what makes it work on Apple Silicon
# (arm64) and on x86 servers alike. (The old Alpine image forced compiling
# psycopg2/wordcloud from source, which broke on ARM.)
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
