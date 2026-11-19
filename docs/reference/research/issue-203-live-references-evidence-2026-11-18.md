---
title: Post-cleanup references and live health, live run 2026-11-18 (issue 203)
description: Per-criterion proven and unproven results for the two unticked issue 203 acceptance criteria, measured with the legacy-reference checker, CI history and read-only Azure CLI on the synthetic demo
ms.date: 2026-11-18
---

Refs #203. Scope: the synthetic demo only, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure is authorised (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed. Only read commands ran. Nothing was created in Azure, so nothing needed deleting. No credential was read or printed. Repository head: `76d89fee2`; `origin/main` at the time of the CI read: `2f00efd09`.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Repository-wide search for `mvp/` and `prototype/` returns only intentional historical references naming the archive tag; `zavaforward_mvp` only in dated historical records | Not proven; failing (observed; raw output not retained) | `tools/check-legacy-references.py` reports 11 violations in three regression-test files; no violation in any document |
| 5 | Deployed app and CI are green from `src/` | Partly proven (observed; raw output not retained); build provenance and main-branch CI unproven | Revision healthy and `src` CI green on recent pull requests; registry unreadable, no deploy workflow run, no push-triggered CI on `main` |

## Evidence limits

Every command result below was observed during the run and the raw output was not retained in the repository. Treat the exit codes, counts, revision state, HTTP statuses and run lists as observations that a reviewer can repeat, not as stored evidence.

The four ticked criteria (links, index and log, rubric comparison) were not re-proven here.

## 1. Stale `mvp/` and `prototype/` references

Commands at `76d89fee2` (observed; raw output not retained):

* `git grep -I -n -E '(^|[^A-Za-z0-9_-])(mvp|prototype)/' -- . ':!.copilot-tracking'` returns 1,974 lines. 1,338 are in the generated `docs/architecture/cutover-reference-inventory.tsv` and 171 in `docs/architecture/mvp-to-src-parity-matrix.md`; both are immutable cut-over records.
* `python3 tools/check-legacy-references.py` exits 1: `references: 11 violation(s); links: 0 violation(s) in 1 document(s)`.
* `python3 -m unittest tools.test_check_legacy_references`: Ran 7 tests, FAILED (1); the failing test is `test_repository_has_no_violations`, which asserts the same empty list.

Where the 11 violations are (all in `tools/`, none in `docs/`, `src/` or workflows):

| File | Violations | Kind |
| --- | --- | --- |
| `tools/test_epic_legacy_path_retirement.py` | 3 (lines 1, 25, 37) | retired path without archive tag `v0.21.0`; one retired package name outside dated records |
| `tools/test_epic_parity_matrix_old_paths.py` | 5 (lines 1, 38, 63, 69, 114) | retired path without archive tag |
| `tools/test_private_mvp_data_exclusion.py` | 3 (lines 1, 33, 40) | retired path without archive tag |

These files are regression guards that must name the old strings, like the entries already in `GUARD_FILES`, but they were added after that list (commits `0999ce7bf`, `e8a352584`) and were never added to it. Documents are clean under the checker's rules, so the criterion's documentation half holds; the criterion as written (a repository-wide search) fails until the guard list is updated. The fix is one list edit in `tools/check-legacy-references.py`. This run is docs and evidence only, so the edit was not made; it is the first follow-up. The same failure was recorded for #201 in [cutover-gate-live-2026-11-18.md](cutover-gate-live-2026-11-18.md).

Informational: `--all-links` reports 3,585 unresolved links across 13,092 tracked documents (for example historical `docs/reference/log.md` entries pointing at the removed `docs/capstone/pitch/` and `docs/capstone/deck/` paths). Those are outside this issue's changed-document link criterion, which the checker passes (0 violations), and earlier log entries must not be rewritten.

## 5. Deployed app and CI from `src/`

Deployed (read-only Azure CLI and unauthenticated requests, 2026-11-18; observed; raw output not retained):

* `ca-cutover-test-demo-api`: provisioning `Succeeded`, latest ready revision `ca-cutover-test-demo-api--0000031` (created 2026-11-17T19:42:06Z), health `Healthy`, 1 replica, traffic 100.
* Image `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`.
* `GET /healthz` returns 200 on the API and on `ca-resident-demo`; `GET /health` returns 401 (authenticated path, as designed).
* Signed-in Playwright proof of pages rendering from this revision is in [deployed-parity-live-2026-11-18.md](deployed-parity-live-2026-11-18.md); it was not repeated here.

CI (observed; raw output not retained):

* Workflow `Source projects CI` (`src-ci.yml`) triggers only on pull requests (path-filtered) and manual dispatch. The latest eight runs are all `success`, the newest on 2026-11-18T10:49:14Z for pull request branch `docs/usability-testing-programme-155`. No push-triggered run exists for `main`; the only non-skipped `main` runs are `Capstone Rubric Scorer` (latest success 2026-11-18T06:57:32Z, one cancelled run at 06:57:13Z by superseding push) and `Dependency Graph`.
* `Source image release and deployment` (`src-deploy.yml`) has no recorded runs, so the running digest cannot be tied to a build from `src/`. The registry has public network access disabled, so tags and labels cannot be read from here (same limit as #201).

Unproven: that the running digest was built from `src/`, and a green CI result on the current `main` head. A source-CI run is green only per pull request, which is by design.

## Follow-ups

1. Add the three regression-test files to `GUARD_FILES` in `tools/check-legacy-references.py` (or reword their mentions) so the checker and `test_repository_has_no_violations` pass; focused tier, `tools/` only.
2. Run `src-deploy.yml` or add a build-provenance label so the running digest links to a `src/` build.
