---
title: Issue 130 live changes
ms.date: 2026-11-18
---

Refs #130. Docs and evidence only; no `src/` change. Tier: FOCUSED (non-applicability: no src, SQL, infrastructure, deployment or web file changed, so mypy, ruff, accessibility and content-standard tests do not apply).

## Files

* `docs/reference/research/issue-130-live-nomination-route-evidence-2026-11-18.md` (new)
* `docs/reference/README.md` (index entry), `docs/reference/log.md` (appended entry)
* `.copilot-tracking/evidence/2026-11-18/issue-130-live/` (drivers, JSON, screenshots)
* RPI artifacts under `.copilot-tracking/` (research, critique, plan, details, changes, review, state)

Note on order: the live probes and the research note were produced during Research and before this record; no source was edited at any point.

## Per-criterion proven or unproven table

| Criterion | Status for the demo | Basis |
| --- | --- | --- |
| Representative participation and comprehension need authorized human evidence (UNTICKED) | Unproven, cannot be proven for the demo; stays unticked | Synthetic data, empty `representative_authorities`, person-run testing excluded; UI shows no representative option without confirmed authority |
| Original account, source and channel kept | Offline only | 19 core tests; live write refused (identity defect) |
| Acknowledged route and named owner | Read live, write offline | Permissions list a named staff owner; no live record created |
| Challenge or correction with competing evidence | Read live, write offline | Challenge panel renders; write blocked |
| Correction re-reviews only dependents | Offline only | Needs live write |
| Hazard concerns route to #85 | Read live | Route view and panel text; no live hazard referral |
| Non-response never lowers priority; unknown not none | Read live, partly | Panel guarantees; "Not recorded" shown; null hazard concern not defaulted |
| Tests cover wrong identity, limited authority, manual route | Offline only | 9 api tests pass |
| Nothing sent or approved automatically | Read live | "Nothing is sent here"; no write succeeded |

## Validation run

* `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_nomination_route tests.test_nomination_bootstrap -q`: 19 tests OK.
* `src/api`: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_nomination_api_routes tests.test_representative_expiry_api -q`: 9 tests OK.
* Literal scan of every evidence file for the three credential values: 0 hits.
* Hosted CI was not observed (no push by instruction). No Azure resource created or changed.

## Process note

The first `plan-done` witness call was refused ("missing persisted artifact evidence: plan, details, critique") because the state file had not yet been updated with those paths; a shell `cd` error caused the state update to fail. It was corrected and the second call returned ok.

The first `implement-start` call was also refused (changes path not yet in state); the retry returned ok with the qualification that the worktree was already dirty because the docs predate it.
