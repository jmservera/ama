ARG API_IMAGE
FROM ${API_IMAGE}
COPY --chown=10001:10001 scripts/private-cutover-proof.py /app/private-cutover-proof.py
ENTRYPOINT ["python", "/app/private-cutover-proof.py"]
