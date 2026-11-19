# Changes, issue 185 r4 (Refs #185)

Files: docs/reference/research/issue-185-live-r4-audit-2026-11-18.md (new), docs/reference/README.md (index), docs/reference/log.md (entry). No src change; FOCUSED tier (docs-only plus read-only live checks; no SQL/security/infra/deployment change).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Approach decided with credential owner | Proven (ticked) | owner decision 2026-11-18; live_provisioning.py |
| One device identity per home and stock home ID | Proven (ticked) | tests 55 OK; run 3 one_device_per_home true |
| Credentials issued/stored without appearing in source or logs | Issuance and no-leak proven (demo); durable storage unproven (Key Vault excluded) | runs 1-3, repo scan clean, hygiene tests 12 OK |
| Teardown removes all simulated identities | Proven (demo hub) | delete 204 and read-back empty; show-stats 0/0/0 at 16:11Z |

Production-only, unproven: durable store and rotation, X.509, scale to N, MQTT, repository SAS command, independent review/CI.

## Validation

* core tests with iothub extra (temp venv): 55 OK + 24 OK; api hygiene: 12 OK; without SDK 34 failures/16 errors SDK_MISSING (adverse, kept).
* az iot hub show-stats, hub show, role list, job list: read-only.
* mypy/ruff not applicable (no Python changed).
