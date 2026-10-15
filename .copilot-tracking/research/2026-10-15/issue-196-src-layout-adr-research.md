<!-- markdownlint-disable-file -->
# Research: issue 196 src layout and cut-over ADR

Task: `issue-196-src-layout-adr`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Issues #195 to #203 (`gh issue view`): acceptance criteria for #196, owner decisions of 2026-10-14, child issues #197 to #203 and dependent epics.
* Owner decisions of 2026-10-15 (task brief): several isolated packages, namespace `zava_forward`, no `zavaforward_mvp`, new code only in `src/`, deploy on Azure only.
* `.github/rubric/artifacts.json`: `solution-code` already includes `src/**/*`; excludes only `mvp/data/**` and `mvp/web/vendor/**`; `infrastructure` lists the dead `prototype/deploy/**/*.bicep`.
* `docs/adrs/0001-azure-architecture.md`: four workloads (api, agents, orchestrator, import) with separate identities; agents has no database, blob or Key Vault access.
* `mvp/zavaforward_mvp/` import graph (relative imports, 42 files):
  * `store.py` imports almost all domain modules including `doc_controls`, `ai`; `sqlstore.py` imports `ai`, `doc_controls`, `documents`, `chatthreads`; `mssqlstore.py` imports `sqlstore`, `chatthreads`.
  * `assistants.py` imports `continuity`, `projection`, `quality`, `ranking`, `ai.FORBIDDEN`, `store.ConflictError`; `ai_registry.py` imports `assistants`; `ai_eval.py` imports `ai_tasks`, `store`.
  * `server.py` imports `assistants`, chat modules, `documents`, `lawstore`, `factory`, `timecapture`, `auth`, `profile`.
  * `digest_blob.py` imports `ledger`, `documents`; `token_store.py` is standalone; both are Container Apps jobs (`infra/modules/containerapps.bicep` lines 241 and 380).
  * Runtime data paths: `ranking.POLICY_DIR`, `lawstore.REGISTER`, `ai_eval.GOLDEN` use `__file__` parents.
* `mvp/Dockerfile`, `.github/workflows/mvp-ci.yml`: build context `mvp`, non-root, no-data and read-only checks.
* `.gitignore` ignores `/mvp/data/`; private data exists in the owner's main checkout only.
* Open PR #287 edits `assistants.py`.

## Findings that changed the design

* The domain core is cohesive and large; workloads are thin. Isolation value is identity, image and dependency (extras `sql`, `blob`), not code size.
* `doc_controls` and `ai` cannot sit in workload packages without a dependency cycle, so they stay in the core.
* `import` is a Python keyword, so the import workload package is `importer`.
* `src/**/*` covers tests, pyproject and Dockerfiles when each project holds them under `src/<project>/`; only excludes for vendor and data are needed.

## Alternatives considered

* Single package: rejected by owner decision 2026-10-15.
* `src/<name>/` flat packages with tests in repository-level `tests/`: rejected, breaks per-package isolation of tooling.
* Move `doc_controls` to importer: rejected, creates a core-to-workload import.

## Open items for the owner

Approval, soak period, temporary `api` to `agents` import until #144.
