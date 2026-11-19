---
title: Issue 185 live r5 changes
ms.date: 2026-11-18
---

Refs #185. Tier FOCUSED, docs only. Classification basis: no `src`, workflow, dependency or infrastructure file changed; live Azure use was read-only.

## Files

* `docs/reference/research/issue-185-live-r5-reverification-2026-11-18.md` (new)
* `docs/reference/README.md` (index sentence), `docs/reference/log.md` (entry)

## Per-criterion table

| Criterion | Proven or unproven for the demo | Evidence |
| --- | --- | --- |
| Credentials are issued and stored without appearing in source or logs | Issuance and no-leak proven; durable storage unproven (Key Vault excluded by the owner) | Retained logs 0 key matches; repository scan clean except scrubber fixtures; 12 api and 24 core tests OK |
| Teardown removes all simulated identities | Proven | Runs 1 to 3 delete 204 and empty read-back; hub-wide count 0 at 17:04 UTC; no 185 job or role assignment left |

## Validation

* `unittest test_iot_credential_hygiene` in `src/api`: 12 OK. `unittest test_device_provision test_live_provisioning` in `src/core`: 24 OK.
* mypy, ruff and the web checks do not apply: no Python or web file changed. `rpi-checks.py --all` not run, by instruction.
* No Azure resource was created, so there is nothing to delete.
