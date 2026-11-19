---
title: Issue 96 live changes, 2026-11-19
ms.date: 2026-11-19
---

No source change. Only these dated artifacts were added.

| Criterion | Status | Basis |
| --- | --- | --- |
| Each assisted form has an approved versioned schema | Unproven (needs a human) | Code never sets `Approved`; live demo holds zero schemas (2026-11-18 probe); approval is a named human decision |
| Candidate values carry raw value, source ID, document hash and locator | Ticked earlier; offline tests OK 2026-11-19 | `test_form_staging` |
| Accept, correct or reject per field preserves prior values and reviewer | Ticked earlier; offline tests OK | `test_form_review` |
| Validation reports field-specific unknown, conflict or fail | Ticked earlier; offline tests OK | `test_form_review` |
| A reviewed export never submits or implies eligibility | Ticked earlier; not re-run live | prior export tests |
| A source, schema or rule change marks only dependent items stale | Ticked earlier; offline tests OK | `test_form_dependencies` |

Validation: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_form_staging tests.test_form_review tests.test_form_dependencies -q` gave 50 tests OK. mypy, ruff and web checks not applicable (no source change). No Azure resource was created.
