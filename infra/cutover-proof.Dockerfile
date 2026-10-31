ARG API_IMAGE
FROM ${API_IMAGE}
COPY --chown=10001:10001 scripts/private-cutover-proof.py /app/private-cutover-proof.py
COPY --chown=10001:10001 scripts/initialize-workbench-staff.py scripts/staff_roster.py scripts/staff_azure.py scripts/staff_blob.py scripts/staff-azure-worker.py /app/scripts/
COPY --chown=10001:10001 entra/app-registration.json /app/entra/app-registration.json
ENTRYPOINT ["python", "/app/private-cutover-proof.py"]
