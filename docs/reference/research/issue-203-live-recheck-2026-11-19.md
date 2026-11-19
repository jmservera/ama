---
title: Issue 203 post-cleanup verification, third live run
description: Per-criterion proven and unproven results for the two unticked issue 203 criteria, with retained raw output
ms.date: 2026-11-19
---

Refs #203. Synthetic demo, desktop only, resource group `ama`, no production change. Archive tag: `v0.21.0`. Raw output is in `issue-203-live-recheck-2026-11-19/`. This supersedes the 20-violation result of [the second run](issue-203-refs-verify-live-2026-11-18.md); that record is preserved unchanged.

## Result

| # | Unticked criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Search for `mvp/` and `prototype/` returns only intentional references naming the archive tag; `zavaforward_mvp` only in dated records | Proven at head `3e5371eb0` (equal to `origin/main`): `python3 tools/check-legacy-references.py` reports 0 reference violations, exit 0; `python3 -m unittest tools.test_check_legacy_references` passes 8 tests | `legacy-check.txt`, `heads.txt` |
| 5 | Deployed app and CI green from `src/` | Partly proven. Proven: both apps `Succeeded`, active revisions `Healthy` at 100 percent traffic, `/healthz` 200 on both. Unproven: the running digest was built from `src/`; a push-triggered CI result on `main` | `az-api.json`, `az-resident.json`, `az-revisions*.json`, `healthz.txt`, `gh-src-ci.json`, `gh-src-deploy.json` |

## Detail

Criterion 1. The checker accepts historical mentions only where the archive tag sits nearby, and treats the old package names as allowed in dated records and regression guards. The 20 violations of the previous run no longer occur on `main`. Remaining hits in `README.md` and `src/README.md` name `v0.21.0`.

Criterion 5. Revisions: `ca-cutover-test-demo-api--0000033` and `ca-resident-demo--0000014`, both `Healthy`. The first `/healthz` call to `ca-resident-demo` returned 000 inside a 30 second cap (cold start); the retry returned 200. The first attempt is retained in the log. Source projects CI is green on the five latest pull-request runs (heads in `gh-src-ci.json`), but the workflow runs only on pull requests and dispatch, and `src-deploy.yml` has no runs (`[]`), so neither a `main` push run nor a `src/`-built digest can be shown. The registry has public access disabled, so image labels cannot be read, and changing that is a production change outside the owner decision.

Informational: `--all-links` reports 3585 unresolved links in 14699 documents, mostly append-only history; the ticked changed-document link criterion is unaffected.

## Unmet

Criterion 5 remains unticked: digest provenance and a `main` CI run need a deploy workflow run or a registry change, both out of demo scope.
