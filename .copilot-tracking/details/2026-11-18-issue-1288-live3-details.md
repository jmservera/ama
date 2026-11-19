# Details: issue 1288 live run 3

* Phase 1: `live_probe.py` signs in with Playwright (credentials read at run time, never printed), calls GET-only endpoints, screenshots `#sensors`. It must not POST `/api/assistants/quality-evidence/invoke` (run 2 wrote an unintended denial proposal).
* Phase 2: `az containerapp revision/job list`, `az eventhubs eventhub list`, app env names AI_DEPLOYMENT and AI_MODEL_VERSION only. Create nothing; nothing to delete.
* Phase 3: from `src/api`, unittest of the correlation, c7, e1, e2, simulation-lane and grounding modules with the guide's PYTHONPATH; SQL Server classes skip without `ZF_TEST_MSSQL=1` (SQL run 2 evidence reused, source unchanged since #2005).
* Phase 4: do not tick criteria; do not fabricate a release record or run a simulator (no authority, OQ-017).
