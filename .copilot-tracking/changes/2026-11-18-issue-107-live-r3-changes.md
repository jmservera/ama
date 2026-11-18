# Changes: issue #107 third pass (docs/evidence only, Tier FOCUSED)

Planned: add docs/reference/research/issue-107-live-r3-assistants-evidence-2026-11-18.md, evidence under .copilot-tracking/evidence/2026-11-18/issue-107-live-r3/, README index and log entries. No src change. No Azure resource created.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover mismatches, revocation, restart; old images/restarts cannot restore revocation or replenish allowances | Partly proven, stays unticked | Actual SQL Server 2022 race, revocation and restart tests (r2, unchanged head); live same-image restart kept stored SUS-1; old-image path SQLite proxy only because ACR is private |
| Matching approved exercise record permits bounded proposals only; delivered-build real AI, SQL, Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists (OQ-017 holders unappointed); denial side re-proven live; approved side not fabricated |

## Completed

* Added docs/reference/research/issue-107-live-r3-assistants-evidence-2026-11-18.md; README index row and log entry; evidence in .copilot-tracking/evidence/2026-11-18/issue-107-live-r3/ (live_probe.py, live_probe_read.json).
* Validation (FOCUSED, docs only): relative links in the note resolve; git diff reviewed; no src change so mypy, ruff and unit tests not applicable; rpi-checks --all not run; heavy lock untouched.
* Witness: first implement-start was refused (`missing persisted artifact evidence: changes`) because the state changes pointer was null; fixed the state pointer and retried (seq 5 ok). Refusal retained.
* No Azure resource created; nothing to delete. Credentials never printed.
