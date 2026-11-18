---
title: Issue 203 changes
---
Tier: FOCUSED (docs and evidence only). The proposed `tools/check-legacy-references.py` change alters gate semantics and is not made here; it is recorded as a needed full-tier follow-up. Refs #203.

Changes:
* docs/reference/research/issue-203-refs-verify-live-2026-11-18.md plus raw output folder (new evidence), README row and log entry.

Validation:
* python3 tools/check-legacy-references.py at this head: see the note; before-run output retained in legacy-check-before.txt (20 violations).
* No tool, src, SQL, infra or deployment change.

Per-criterion table (unticked criteria):

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Only intentional historical refs to retired paths and package | Not met: 20 violations; full-tier checker follow-up needed | legacy-check-before.txt |
| 5a | Deployed app healthy | Proven (raw output retained) | az-*.json, healthz.txt |
| 5b | CI green from src/ | Proven for pull requests (8/8 success); unproven for push to main | gh-src-ci.json |
| 5c | Running digest built from src/ | Unproven for the demo | no src-deploy run; registry private |

Ticked criteria were not re-proven. No Azure resource created.
