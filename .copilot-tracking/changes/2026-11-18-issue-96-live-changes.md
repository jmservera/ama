---
title: Issue 96 live changes
ms.date: 2026-11-18
---

Tier: FOCUSED (documentation and evidence only; no `src/` change; `rpi-checks.py --all` not run).

Files: `docs/reference/research/issue-96-live-demo-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), evidence under `.copilot-tracking/evidence/2026-11-18/issue-96-live/`, and the RPI artifacts.

Prior evidence: the tracked state file and an earlier note (`issue-96-live-form-schema-approval-evidence-2026-11-18.md`) from a previous run exist; the state file was overwritten (history keeps it) and the earlier note was left unchanged.

Validation: `PYTHONPATH=src:tests python3 -m unittest tests.test_form_staging tests.test_form_review tests.test_form_dependencies tests.test_form_export tests.test_form_criteria_5_6` in `src/core`: 67 tests OK (`offline-core-tests.txt`). mypy and ruff not applicable (no Python source changed). Live probe: `probe.py`, `probe1.json`, `form-schemas-response.png`. Literal scan of this run's files for the account name and password: no match.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Each assisted form has an approved versioned schema | Unproven: zero schemas in the demo, no path sets Approved, approval is a human act |
| 2 | Candidate values carry raw value, source ID, document hash and locator | Not re-proven live (no batches); offline pass |
| 3 | Accept, correct or reject per field preserves prior values and reviewer | Not re-proven live (no drafts); offline pass |
| 4 | Validation reports field-specific unknown, conflict or fail | Not re-proven live; offline pass |
| 5 | A reviewed export never submits or implies eligibility | Live notice states no eligibility or submission; offline pass |
| 6 | Source, schema or rule change marks only dependents stale | Not re-proven live; offline pass |
