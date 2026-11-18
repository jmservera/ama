---
title: Issue 121 live changes
ms.date: 2026-11-18
---

Docs-only. No src, SQL, infrastructure or deployment change. Tier FOCUSED. No Azure resource was created or changed, so nothing needs deleting.

## Files

* `docs/reference/research/issue-121-live-data-protection-evidence-2026-11-18.md` (new)
* `docs/reference/research/issue-121-live-data-protection-register-2026-11-18.png` (new, screenshot of live register)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (appended entry)
* `.copilot-tracking/` research, plan, details, critique, changes, review, state and `evidence/2026-11-18/issue-121-live/`

## Per-criterion result (full basis in the research note)

| Criterion | Status |
| --- | --- |
| No resident personal data to a model until transfer position approved (DH-006) | Proven for the demo by construction and offline gate; live denial unproven |
| Map staff/tenant/review separately from fixtures and future residents | Proven offline; live partly (deployed register older) |
| Cover inputs through retained copies | Proven offline; live partly |
| Every task declares purpose, fields, prohibited content, necessity | Proven offline; live partly |
| DPO/Legal and owners approve purpose, transfer, retention, erasure and so on | Deferred (#1906) |
| Upload/store permission does not approve sending to AI | Proven offline; live unproven |
| Synthetic residents do not remove staff scope; UK hosting is not UK inference | Proven |
| Retention, erasure, audit, restore explicit and owned | Partly proven; ownership deferred (#1906 to #1908) |

## Validation

* core: `PYTHONPATH=src:tests python3 -m unittest test_data_protection test_ai_provider_payload_spy test_ai_input_bounds -q`: 52 tests OK.
* api: `test_document_controls`: 18 tests OK.
* mypy and ruff not applicable (no Python or src change). Link and diff review done. `rpi-checks.py --all` not run.
* Witness: `implement-start` was refused once (changes path missing from state), then recorded OK after the state pointed to the changes file.
* Correction pass: duplicate evidence screenshot removed (docs copy kept), subscription id redacted, log blank line fixed, evidence limits added.
