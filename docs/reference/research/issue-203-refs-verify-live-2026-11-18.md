---
title: Post-cleanup references and live health, second live run (issue 203)
description: Per-criterion observed and unproven results for the two unticked issue 203 criteria, with retained raw output, on the synthetic demo
ms.date: 2026-11-18
---

Refs #203. Synthetic demo only, desktop only, resource group `ama`. Archive tag for retired `mvp/` and `prototype/` paths: `v0.21.0`. Owner decisions of 2026-11-18 apply (no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed). Only read commands ran against Azure; nothing was created, so nothing needed deleting. No credential was read or printed. Raw output is retained in [issue-203-refs-verify-live-2026-11-18/](issue-203-refs-verify-live-2026-11-18/). Working head `a39ae2339`; `origin/main` at read time `79fed518e`. This supersedes the non-retained observations in [issue-203-live-references-evidence-2026-11-18.md](issue-203-live-references-evidence-2026-11-18.md).

## Result

| # | Unticked criterion | Before this change | After this change |
| --- | --- | --- | --- |
| 1 | Search for `mvp/` and `prototype/` returns only intentional references naming the archive tag; old package name only in dated records | Failing: 20 violations (`legacy-check-before.txt`) | Still failing: 20 violations; no checker change in this branch (see follow-up) |
| 5 | Deployed app and CI green from `src/` | Partly proven | Partly proven; see below |

Criterion 5 detail:

* Proven (raw output retained): `ca-cutover-test-demo-api` provisioning `Succeeded`, revision `ca-cutover-test-demo-api--0000031` `Healthy`, traffic 100, image digest `sha256:5368f4e4...`; `ca-resident-demo` revision `ca-resident-demo--0000012` `Succeeded`; `/healthz` returns 200 on both (`az-*.json`, `healthz.txt`). `Source projects CI` is `success` on all eight latest runs, all pull requests (`gh-src-ci.json`).
* Unproven: that the running digest was built from `src/` (`src-deploy.yml` has no runs, `gh-src-deploy.json` is `[]`; the registry has public access disabled so labels cannot be read) and a push-triggered CI result on `main` (source CI is pull request and dispatch only; the `main` runs are rubric scoring and skipped what-if runs, `gh-main-runs.json`). Neither can be proven for the demo without a deploy run, which is a production-affecting action not authorised here.

## Needed full-tier follow-up

The 20 violations need a change to `tools/check-legacy-references.py`: add the three regression-test files to `GUARD_FILES` and add an exact-path exemption list for the three dated notes. That alters gate semantics, so it takes the full validation tier (complete local gate and an external receipt) and is not made here. Raise it as a separate full-tier issue.

## Criterion 1 findings

20 violations from `tools/check-legacy-references.py` at the working head (`legacy-check-before.txt`): 11 in three regression-test files under `tools/` that must name the old strings and were never added to the guard list, and 9 in three dated research notes (#198, #200, #203 evidence) that quote retired paths or the package name as history. No violation in any live document, `src/` file or workflow. The 4,000-line raw `git grep` count is dominated by generated cut-over inventories that the checker already exempts.

Informational: `--all-links` reports 3,585 unresolved links across 13,465 tracked documents (`links-all.txt`), mostly in append-only history. The changed-document link criterion (ticked) passes with 0 violations.
