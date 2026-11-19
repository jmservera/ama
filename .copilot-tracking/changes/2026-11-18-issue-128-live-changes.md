---
title: Issue 128 live demo changes
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/issue-128-live-equity-evidence-2026-11-18.md` (per-criterion note).
* Added driver and redacted evidence under `.copilot-tracking/evidence/2026-11-18/issue-128-live/`.
* Updated `docs/reference/README.md` index and appended `docs/reference/log.md`.
* No `src/` change, no Azure resource created or changed, nothing to delete. Tier FOCUSED (docs and evidence only); `rpi-checks.py --all` not run.

## Per-criterion table

| # | Criterion | Status for the demo |
| --- | --- | --- |
| 1 | Keyboard and screen reader testing (ticked, deferred to production, #1907) | Not re-opened; person-run AT stays unproven. Desktop axe 0 violations on four surfaces |
| 2 | Missing data and incomplete appointments get human review (ticked) | Unchanged; 59 core tests pass (rerun) |
| 3 | Direct user research protocol agreed | Unproven: draft only, agreement record has no named person or date |
| 4 | Usability measures aggregate only | Proven at source level (core tests: small-cell masking, forbidden fields, unagreed audit-use blocked); no research store found in API source; deployed route inventory unavailable (OpenAPI 404) |
