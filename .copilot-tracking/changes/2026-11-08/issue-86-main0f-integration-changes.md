---
title: Issue 86 Main 0f05 integration changes
description: Changes record for the normal current-Main merge and its interrupted first LIGHT attempt
ms.date: 2026-11-08
---

Scope: issue #86 only, `Refs #86`, local only. Tier FULL. Executed the planned sequence A to D of `issue-86-full-admission-prep`; step E onward is NOT recorded here and is not pre-ticked.

## Integration

* Pre-merge state verified: child clean at `b56f97d6` (tree `795f0083`), `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638`, merge base `f548b65f`, parent ref `c5edb320` and PR #1243 (OPEN, base `feat/controlled-lifecycle-integration-81`, published head `6ff492ad`) as expected. Incoming delta (merge base to Main) was 42 paths (40 added, 2 modified): 39 new inert tracking files, `.github/rubric/scores/latest.json` (M), `src/api/tests/assistant_process_worker.py` (A) and `src/api/tests/test_assistant_release.py` (M). `git merge-tree` predicted no conflict.
* One normal `--no-ff` merge, commit `10410729fe64f9fc292e2da06c79c8867b652dcc`, tree `ed40a4005c3d16b9bc34e297cc360e7b71163bc1`, parents `b56f97d6` and `0f05e9aa`. Author and committer both `8036360+jmservera@users.noreply.github.com`, matching the fresh `gh api user` id 8036360, login jmservera.
* Explicit ancestry exit 0 for `0f05e9aa`, `c5edb320`, `e888a499`, `f548b65f`.
* Post-merge delta against the first parent is exactly the three permitted files plus tracking additions; the two API test blobs and the rubric blob equal Main's; the rubric parses as JSON; `docs/reference/log.md` has no diff; `src` production, tools and infra are unchanged. No conflicts, so no resolution was needed.

## Deviations and interruptions (preserved)

* The merge command ran in the same session whose later LIGHT command was interrupted. The coordinator had launched this session's shell launcher directly rather than inside tmux and stopped that bash process (1806); no terminal CLI exit marker was seen, so that CLI exit is unknown. The interrupted log `/tmp/rpi-86-main0f-full-1108.log` and scratch `/home/azureuser/.local/share/ama/gates/g86-main0f-light` are kept untouched and are not evidence of a pass.
* Process gap: the merge was made before the admission brief's identity re-resolution was re-recorded in this file; the identity was validated afterwards against `gh api user` (match).
* First LIGHT retry in new scratch `g86-main0f-light-r2` failed because I used a wrong module name and omitted `tests` from the path (exit 1, `rel.err`); the corrected run is `rel2`. Both retained.

## LIGHT results (scratch `/home/azureuser/.local/share/ama/gates/g86-main0f-light-r2`, whole git archive, non-editable venv)

| Check | Exit | Result |
| --- | --- | --- |
| pip install | 0 | no failure |
| import origin | 0 | `store` and `assistant_release` load from the scratch venv site-packages |
| `test_assistant_release` from `src/api` | 0 | 52 tests OK, 3 skipped (SQL opt-in, includes `MssqlUnleasedRevocation`; not SQL proof) |
| core `test_quality_procurement`, `test_gates`, `test_hazard_referral`, `test_resident_decisions` | 0 | 505 OK, 111 skipped (SQL/Azure opt-in) |
| mypy (core) | 0 | 269 files |
| ruff check and format `src tests` (api) | 0 | 117 files formatted |

API mypy was not run separately. LIGHT is not FULL; no SQL, browser or image check ran.

## Pending

FULL, receipt verification, independent assessment of the local `e888a499` delta, the published `c5edb320` delta and Main-versus-final for all inherited gates, procurement, quality, store and appointments hunks, hosted checks, human approvals and the #1238 policy.
