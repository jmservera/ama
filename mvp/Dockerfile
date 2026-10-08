FROM python:3.12-slim
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
WORKDIR /app
COPY properwarm_mvp ./properwarm_mvp
COPY web ./web
COPY data/properwarm.json ./data/properwarm.json
RUN mkdir -p /app/state && chown 10001 /app/state
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8088 PW_BIND=0.0.0.0 PW_DATA=/app/data/properwarm.json PW_STATE=/app/state
EXPOSE 8088
CMD ["python", "-m", "properwarm_mvp.server"]
