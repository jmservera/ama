---
title: Issue 202 release preparation evidence (2026-11-22)
ms.date: 2026-11-22
---
Scope: demo release preparation for issue #202 (synthetic, desktop only, resource group `ama`, no estate change). Read-only commands only; no secret read or printed.

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Tag: `git rev-parse v0.21.0` returns `0096b113...` (annotated); `git log -1 v0.21.0` is commit `65a514ed`, 2026-10-27; `git ls-tree -r v0.21.0` lists one `mvp/` file. `README.md:45` and `docs/reference/log.md` record the tag.
* Folders: `ls mvp prototype` fails for both; `git ls-files | grep -c -E '^(mvp|prototype)/'` returns 0.
* Workflows: `.github/workflows/mvp-ci.yml` and `mvp-validation.yml` exist, are `workflow_dispatch` only, named `Source CI` and `Source validation`, and run `src/*`. `src-ci.yml` is the pull request gate and its path filter still lists both files.
* Protection: `gh api repos/jmservera/ama/rulesets` shows `main` disabled and `mainprotect` active; `mainprotect` has `required_status_checks` with an empty list; classic protection returns 404. No required check names the old workflows.
* Live revisions: `az containerapp revision list` shows `ca-cutover-test-demo-api--0000053` and `ca-resident-demo--0000025` active, Healthy, 100 percent; `/healthz` returned 200 on both.
* Commit range for the notes: 1388 first-parent commits `v0.21.0..6fd6e3f8`; see [the release notes](./issue-202-release-notes-demo-2026-11-22.md) and [the checklist](./issue-202-release-checklist-2026-11-22.md).

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Parity matrix, owner agrees | Ticked in issue | Not re-proven |
| `prototype/` removed, no tracked file | Proven | 0 tracked files, directory absent |
| Archive tag created, named `v<BRD version>`, recorded in log and README | Proven locally | Tag, README and log entries read; push not performed |
| Rubric registry PR merged first | Ticked in issue | Not re-proven |
| Old workflows removed or replaced, protection updated | Unproven | Replaced in content but files remain; removal needs the FULL tier and an external receipt; protection lists no required checks and was not changed |
| No tracked file under `mvp/` | Proven | 0 tracked files |

## Not proven for the demo

Deleting the two workflow files changes pinned-hash gate tooling, so it is outside the focused tier and was not attempted. Publishing a release is an open owner decision.
