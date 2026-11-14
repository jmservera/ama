# Research: Issue #144 scale, probes, load and restart (local slices)

* Task: `issue-144-scale-probes-load-2315`; date 2026-11-13; branch `feat/demo-144-scale-probes-load-2315`; base `origin/main` `3033dc9c2`.
* Research disposition: executed (repository evidence only; no Azure access).
* Planning Readiness: Ready.

## Scope

Local slices of #144 criteria 2, 4 and 5. Frozen #79/#146 candidates touch `infra/main.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/modules/storage.bicep` and `infra/modules/containerapps.bicep`: this task reads them and edits none.

## Evidence read

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `infra/README.md` (hosting completeness table, ~line 1334), `src/api/README.md`, `gh issue view 144 --comments`.
* Audit 2026-10-31 and 2026-11-03 comments: C2, C4, C5 unmet; C6 ticked by #682. Hosted proof needs live Azure and the #138 pipeline, which this task does not claim.

## Findings

| Area | Existing state | Gap for this task |
| --- | --- | --- |
| Scale rules | `containerapps.bicep`: API http rule 50 concurrent, `minReplicas: apiMinReplicas`, max 4 (1 on the public simulation lane); agents azure-queue rule, 0 to 5 | Pinned only for the API and agents by two tests in `test_container_contract.py`; no single cross-workload invariant check (every container has limits, every app has bounded replicas, every ingress app has all three probes on the listening port) |
| Probes | API Startup, Readiness, Liveness on `/healthz` port 8088. Agents has no listener, so no hosted probe (documented) | `/healthz` behaviour (200 when store ready) not tied to the Bicep probe path by a test |
| Limits | API and agents 0.5 vCPU / 1 GiB; jobs 0.25 / 0.5 | No cross-check that `scale_load.API_LIMITS` equals Bicep |
| Revision rollback | `activeRevisionsMode: Single`; README documents revert PR plus `src-deploy.yml` redeploy; `pipeline.py` accepts only current-run digests | Rollback prose not tied to code by a test; no historical digest redeploy path exists (not invented) |
| Load test | `src/api/tests/scale_load.py` runs in-process; recorded `docs/architecture/scale-load-2026-11-01.json` (60,000 homes, 120 s, p95 over NFR-002) | Server shares the interpreter with the load client, so RSS and CPU are mixed. No separate-process run and no record of closed-loop concurrency |
| Restart | `test_restart_audit.py` reopens the SQLite store in-process after a graceful close | No real API process killed and restarted over HTTP; no check through `/api/audit-check` |
| Fixture | Declared 60,000 homes / 600,000 events (`scale_load.DECLARED`, issue #174); current fixture yields about 54,000 events | Unchanged; stays disclosed |

## Constraints and decisions

* Do not edit the four Bicep files; tests read them as text.
* Pip venv `/tmp/venv-144-2315`, no `uv`; remove at the end.
* Local loopback benchmark records concurrency, p50/p95, error rate, RSS, restart durability. No production or Azure scale claim; all figures are local measurements on one shared machine.
* SQLite is one process only; the single-replica claim is limited to one OS process killed with SIGKILL and restarted on the same SQL file.

## Follow-up candidates (for ranking)

1. Hosted load and rollback run in the #138 pipeline (needs authorisation).
2. API-side dedupe of repeated worker post-backs.
3. Dashboard recompute cost (p95 over NFR-002 at 60,000 homes).

## Planning Readiness

Ready: tests plus benchmark script plus documentation record.
