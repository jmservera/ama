---
title: Issue 217 plan - live-data readiness gate
ms.date: 2026-11-01
---

## Phases

* [x] 1. Add `readiness_report(env)` and criteria matrix to `regulatory_privacy.py` (no new package).
* [x] 2. Add unit tests in `src/core/tests/test_regulatory_privacy.py`: default refuses; SYNTH refs refuse; all real refs permit only the gate not approval; no content/secret echo of unknown env keys.
* [x] 3. Update `src/core/README.md` note and run ruff check, ruff format --check, mypy, unit tests.
* [x] 4. Commit, push, PR with `Refs #217` and unmet criteria.

## Critique (single pass)

Verdict: proceed. Risk: a reference present is not approval. Disposition: report keeps `dpo_reviewed` false and labels the gate "references recorded, human approval not verified". Risk: scope creep to API. Disposition: deferred to follow-up.
