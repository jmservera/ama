---
title: Issue 96 saved Held export freshness check research
description: Prospective research for the first served consumer of the existing saved-export freshness comparison
ms.date: 2026-11-12
---

## Identities and scope

* Worktree `issue-96-form-readiness-2236`, branch `research/demo-96-readiness-2236`, clean head and base `eac1206c6ca08bd551e3d0d2384bb87a1f05c24f` (tree `ff26901294f2678afc877d68457cbb1db2ef49e4`), equal to `origin/main` at fetch. No open pull request exists.
* Task id and slug `issue-96-saved-export-check-2236`. Refs #96 only; no closing claim. Owner demo-UX tier: targeted checks only, no blanket full or `--changed` gate, no push, PR, merge, new issue or criterion tick.
* Read in full for this task: issue #96 body and all 19 comments, the coordinator refill log, `form_export.py`, `form_review.py` (report, view, freshness), `forms.py` outline, `server.py` form routes, held-download tests and the role endpoint inventory test. Case study original and addendum, the knowledge-base index and memory were opened for project context; this is a synthetic-demo engineering slice that adds no regulatory claim.

## Comparison with delivered work (no duplication)

* Core stale logic is delivered and unchanged here: #888/#1083 (manifest stale and changed fields), #1093 (`export_freshness`), #1345 (history, dependency evidence) and #1482 (issue-change staleness, Refs #98). Tests: `test_form_export` 11, `test_form_dependencies` 10, all OK at this head.
* #98 slice (1482) changed core freshness only. The #82 funding and #153 denial/chat-copy slices touch other modules. No overlap with `server.py` form routes.
* #1369 (merged) serves only `GET .../held-export`. `grep` shows `export_freshness` and `proposal_freshness` have no caller outside core tests: a saved Held copy cannot be checked through any served interface. That is the distinct missing local behavior.

## Separation of the remaining criteria

* C1 approved schema: needs named Finance/template approval; not local. Untouched. No template or rule is invented.
* C5 reviewed export: no reviewed state may exist without approved template and rules; the Held export stays the only state. Untouched.
* C6 dependent-only stale: core marking is delivered; what is missing locally is a served way to see which fields of a saved copy are stale and which are unaffected. This slice supplies it read-only. It does not tick C6; approved-rule calculations and reviewed-pack staleness remain unproven.
* Not a whole-issue blocker: the human criteria C1/C5 do not prevent this engineering slice.

## Source findings

* `export_freshness(store, user, case_id, saved)` is read-only under `store.lock`, re-checks `forms._actor`, returns status Current, Stale, Invalid or Unavailable with `stale_fields`, `unaffected_fields`, `reasons`, `action`, `reviewed: False`. Invalid covers edited, incomplete or legacy history-less copies (owner decision 2026-11-05: Invalid and regenerate).
* It takes `draft_id` from the saved copy; a route draft id must therefore be compared with it, otherwise the path would claim a different draft than the one checked.
* `_forms` already maps `PermissionError` 403, `KeyError` 404, `ValueError` 400, `ConflictError` 409, store failures 502/503 safely. POST `form-review` is already role-projected through `projection.allowed(u, "post", "POST")`; the new path would be a read-only POST whose only inputs are the saved copy.
* Guard parity: the saved copy exists only when the Held download is enabled (`held_download_enabled`: synthetic-demo-only, demo profile, not trusted-proxy). The check uses the same guard and answers 404 otherwise. Operator attestation, not provenance proof.
* `test_role_endpoint_inventory` requires explicit inventory entries and a source-string assertion for new routes.
* Response holds no field values, only identifiers, statuses and reasons, so it discloses less than the existing `form-review` GET.
* Web: API-only change; no HTML, CSS or JS edited, so web-design skills and guideline retrieval are not needed. No UI claim is made.

## Baseline (owned external venv `venv-96-refill-2236`, pip `--no-deps` editable installs, no source-package PYTHONPATH)

* `ZF_DATA` pointed at an owned empty temp folder; no private dataset read.
* Core: `test_form_export` 11 OK, `test_form_dependencies` 10 OK. API: `test_form_held_download_api` 6 OK, `test_form_staging_api` 14 OK, `test_role_endpoint_inventory` 24 OK. The repository-documented `PYTHONPATH=../core/tests:../agents/tests` was used only for sibling test helpers.

## Planning readiness

Ready. Research disposition `executed`. No STOP.
