---
title: Changes, issue 360 live criterion d third measurement
ms.date: 2026-11-18
---

Refs #360. Tier FOCUSED: documentation and evidence only; no `src/` change, so no mypy, ruff or unit tests apply. No `rpi-checks.py` run.

## Changes

* Added: `.copilot-tracking/evidence/2026-11-18/issue-360-live-r3/` (Azure CLI JSON, anonymous curl output, `signin_proof_r3.py`, run 1 and 2 outputs, chat status, two screenshots (the signed-in workbench screenshot showed personal names and is not retained)).
* Edited: `docs/reference/research/direct-ingress-live-demo-2026-11-18.md` (third-measurement section), `docs/reference/log.md` (one entry).
* Edited: the session state file at the brief's fixed path. Its earlier committed content (task slug `issue-360-live`) is preserved in Git history.
* Azure: read-only, plus app-level writes of two throwaway chat threads, both deleted (200). No resource created or deleted, so nothing to clean up in Azure.

## Per-criterion table

| Criterion | Ticked on #360 | Proven or unproven | Basis |
| --- | --- | --- | --- |
| a | Yes | Proven live | External environment, own subnet, NSG 443 and private backing services reconfirmed |
| b | Yes | Not re-tested | Offline tests |
| c | No | Unproven; owner decision needed | No owner approval of the migration plan on record; replacement already exists |
| d, direct HTTPS welcome and health 200 | No | Proven | `anonymous-curl.txt` |
| d, anonymous protected API denied | No | Partly proven | 401 for non-browser and forged requests; browser-mode requests get 302 |
| d, real browser sign-in | No | Proven for the test account | Entra redirect and return, title, `/api/me` |
| d, role enforcement | No | Partly proven | One staff role; `/api/sensors` 403; forged headers ignored; second role unavailable |
| d, SQL persistence | No | Partly proven | `ZF_STORE=mssql`; 443 cases in two logins; thread readable from a second session; no restart drill |
| d, AI calls | No | Not reproduced today; earlier proof stands | Both runs `workflow-only`, `activation-not-approved`; 08:36 UTC run returned a model answer (1230 tokens) |
| e | No | Unproven; owner decision needed | No Front Door resource exists, but authorisation and order after d are not recorded |
| f | Yes | Not re-tested | Documentation |

Criterion d therefore stays unticked.
