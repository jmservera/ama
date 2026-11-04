ARG API_IMAGE
FROM ${API_IMAGE}
COPY --chown=10001:10001 scripts/resident_sensor_seed.py scripts/resident_showcase_sql.py /app/scripts/
COPY --chown=10001:10001 sql/resident-showcase.sql /app/sql/resident-showcase.sql
ENTRYPOINT ["python", "/app/scripts/resident_sensor_seed.py"]
