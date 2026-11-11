---
title: Staff intake 132 extension E1 review
ms.date: 2026-11-10
---

Extension E1 of five. Refs #132. Review executed once, directly by the author, against the diff from merge `173cd9ff7` and the working tree. It is not a substitute for the coordinator's independent reviewer.

## Boundary assessed

* The one-file test change in `src/api/tests/test_staff_intake_api.py` (`correction` return type, typed `view` result).
* The ordinary merge `173cd9ff7` of origin/main `6d4cd624`, three conflict resolutions (`projection.py`, `test_role_endpoint_inventory.py`, `src/core/README.md`).

## Outcome: conformant, no open findings

* The annotation change is type-only; no runtime behaviour, route, permission, consent or contract path changed.
* Project `mypy` (strict) exits 0 over 228 files; `ruff format --check` and `ruff check` pass.
* Merge resolutions keep both intents: main's `aftercare` and `held-export` additions plus the intake `field_intake` projection key and three intake POST routes; both README sections kept.
* The unit run (132 tests, OK) covers intake, role endpoint inventory and content standard on the merged tree.

## Process disclosure

* The `implement-done` marker (seq 5) was recorded after the standalone validator raised a KeyError because it lacked that event; the artifact set was validated afterwards with the equivalent `implement-start` requirement and passed. The marker is therefore weaker evidence than intended.

## Unobserved or carried limits

* 34 tests skipped: env-gated MSSQL class and JSON-store SQL-contract cases. Not re-run, so the earlier MSSQL pass is not current live acceptance.
* Browser and axe not re-run (no UI change); no WCAG or assistive-technology claim.
* Carried: legacy staff-code receipts, JSON store has no cross-process guard, `app.js` retry guard does not cover `staff-intake.js`, AC5 escalation gap. Synthetic approvals are not QA, legal, resident or live acceptance.

## Routed follow-ups

* None block this task. See the state record for ranked later work.
