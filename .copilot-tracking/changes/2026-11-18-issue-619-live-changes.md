---
title: Issue 619 live demo changes
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-619-live-at-consent-evidence-2026-11-18.md` (per-criterion note).
* Added drivers, redacted JSON and screenshots under `.copilot-tracking/evidence/2026-11-18/issue-619-live/`.
* Updated `docs/reference/README.md` index and appended `docs/reference/log.md`.
* No `src/` change, no Azure resource created or changed, nothing to delete. Tier FOCUSED (docs and evidence only); `rpi-checks.py --all` not run.

## Per-criterion table

| # | Criterion | Status for the demo |
| --- | --- | --- |
| 1 | Screen reader testing by a person | Unproven (production-only; no screen reader, person waived) |
| 2 | Keyboard testing by a person | Engineering proof only (employee chat, case tabs, blocker, resident chat); person record unproven |
| 3 | Zoom testing by a person | Partly proven (320 and 683 px viewport equivalents; chat input needs scroll at 320 by 256); person record and real zoom unproven |
| 4 | Consent proven with a real resident journey | Proven with the synthetic resident only; real journey unproven |
| 5 | #550 consent before data use | Proven for the demo (rules path; AI disabled live) |
| 6 | #552 Fluent 2 and WCAG baselines preserved | Partly proven (axe 0 violations on three surfaces); Fluent 2 not re-audited; O-1 open |

## Validation

* Markdown links in the new note checked present; evidence scanned for credential values (0 hits) and e-mail addresses (none).
* No unit tests, mypy or ruff applicable (no Python under `src/`; evidence scripts are not packaged).
* Hosted CI was not observed (no push by instruction).
