---
title: Changes, issue 128 run 3
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-128-live3-equity-evidence-2026-11-18.md`, index row and log entry in `docs/reference/`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-128-live3/`.
* No `src/` change. Tier FOCUSED (docs-only); `rpi-checks.py --all` not run. No Azure resource created.

Divergence: the research note and live probes were written before the `implement-start` witness call because the probe was part of Research evidence gathering; the note content was finalised after plan-done.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Accessibility testing includes keyboard and screen reader (ticked, deferred #1907) | Unproven for demo; axe 0 violations on four desktop pages is engineering proof only |
| Missing data and incomplete appointments get human review (ticked) | Not re-audited |
| Direct user research protocol agreed | Unproven: agreement record has no named person or date; needs named humans |
| Usability measures aggregate only | Proven at source level (26 core tests OK, no API source match); live absence unproven (openapi 404) |
| Eight RAI cohort criteria (ticked) | Not re-audited |

## Validation

* `python3 -m unittest test_usability_programme test_journey_register` (src/core): 26 tests OK.
* Playwright 1366x900 axe and resident wait probes: see evidence folder.
* mypy, ruff and API tests not applicable (no source change). Hosted CI not observed (nothing pushed).

## Witness note

The first `implement-start` and `implement-done` calls were refused (seq 4, 5: "missing persisted artifact evidence: changes") because the state file did not yet list the changes path; `review-done` (seq 6) therefore carries a missing-predecessor qualification. The state was corrected and both calls were retried afterwards, out of order. Logs are unedited.
