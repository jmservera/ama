---
title: Issue 138 live changes record
ms.date: 2026-11-18
---

## Changes

* Added docs/reference/research/issue-138-live-cicd-oidc-evidence-2026-11-18.md.
* Updated docs/reference/README.md (index) and docs/reference/log.md (append-only entry).
* No source, workflow, permission, infrastructure or GitHub/Azure setting change. Process note: the note, index and log were written before this changes file existed; they are documentation, not source, so the implement-start witness records a later start than the first write.
* Azure use: read-only what-if, show and list; anonymous HTTP probes. No resource created, so nothing to delete; the temporary parameter file was removed.

## Validation (focused, documentation-only)

* `python3 -m unittest discover -s infra/tests -p test_pipeline.py -q`: 32 tests OK (run during research; pipeline.py unchanged).
* Link and diff review: see review record. `rpi-checks.py --all` not run, per brief.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| OIDC federated credentials scoped per environment | Unproven (no variables, environments or readable federated credentials; needs repository-admin and Entra work) |
| what-if on PRs changing infra/ with result attached | Partly proven (live what-if succeeded; PR job never ran, variable unset, no runner) |
| Per-environment approval, same templates and parameter set | Unproven (gate refuses live; no protected environment; deploy never ran) |
| Versioned image built, pushed and referenced | Unproven (demo app digest-pinned, no workflow run produced it; registry private) |
| Post-deployment checks automatic and failing on unhealthy or unauthenticated success | Partly proven (smoke passes live, fails on negative control; automatic run unobserved) |
| No secret in logs or repository | Partly proven (pattern scan of tree and one CI log clean; not exhaustive) |

All six remain unticked; Refs #138 only, no closing keyword.
