FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PORT=8080 \
    APP_INTERNAL_INGRESS=false \
    DATA_DIR=/var/lib/properwarm \
    SOURCE_DIR=/app/source-data

WORKDIR /app
COPY prototype/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY prototype/properwarm ./properwarm
COPY prototype/web ./web
COPY prototype/seed/container-source ./source-data
RUN useradd --create-home --uid 10001 appuser && mkdir -p /var/lib/properwarm && chown -R appuser:appuser /app /var/lib/properwarm

USER appuser
EXPOSE 8080
CMD ["python", "-m", "properwarm.server"]
