<!-- markdownlint-disable-file -->
# Research: issue #81 parent re-alignment onto post-#1245 main (2026-11-07)

Task `81-realign-r2`. Research disposition `executed`. Planning Readiness `Ready` for local alignment preparation only. Predecessor records (preserved, unmodified): [2026-11-06 research](../2026-11-06/issue-81-alignment-research.md), [plan](../../plans/2026-11-06/issue-81-alignment-plan.md), [critique](../../plans/2026-11-06/issue-81-alignment-critique.md), [review](../../reviews/2026-11-06/issue-81-alignment-review.md).

## Observed state (read-only, before any change)

| Item | Value |
| --- | --- |
| Branch / PR | `feat/controlled-lifecycle-integration-81`; existing PR #1240 targets `main`, OPEN, head `c5edb320ad10d3d73bb985bfb82b2d0bee94381a`, GitHub reports CLEAN/MERGEABLE against the old base |
| Frozen head / tree | `c5edb320ad10d3d73bb985bfb82b2d0bee94381a` / `4f2a712c483112e1c6c5faf231591c1b24fac234`; ignored-inclusive status empty |
| Prior base | `56eec736906774ef56d8c9a66ed7f3f9c1e520c6` |
| Fetched `origin/main` | `312fa3dcc4866deadf51336f840954852f0ec061` (#1245), three commits ahead of the prior base: `0209b46bf` (#1241 checklist list export, issue #80), `add72cc90` (rubric score 77/100), `312fa3dcc` (#1245 chat demo disclaimer, Refs #891) |
| Dry run `git merge-tree --write-tree HEAD origin/main` | clean, tree `c1d9790b87eb6907d043762d61e20822bbbaa204`; no conflict predicted |
| Post-merge Capstone Rubric Scorer run `42361331168` | `in_progress` on `312fa3dcc` (created 2026-11-07T09:49:19Z); may add a score-only main commit, so main must be fetched again after it completes |

## Main delta relevant to the parent

* `src/core` changes in main: `projection.py` (adds `checklists.csv` to `STAFF_GET`), `quality.py` (adds `from typing import Any` and a new `checklist_rows()` helper), `tests/test_list_export.py`. All additive from #1241.
* Parent also changes `quality.py` (#1226 fail-closed evidence gates). The dry run is clean, so edits are in disjoint hunks. Intent check still required after rebase: `checklist_rows()` reads `CHECKLISTS` only and does not touch gate, evidence or persistence paths, so it neither weakens nor depends on the fail-closed behavior.
* Other main changes are `src/api` (disclaimer visibility, browser checks, schema download UI, tests), `docs/reference/log.md`, a chat-demo storage approval doc, `.github/rubric/scores/latest.json` and tracking records. None overlap parent paths other than `quality.py`.
* #1245 is the "merged891" disclaimer/browser/UI/log entry set to preserve.

## Superseded evidence (preserved, not deleted)

The 2026-11-06 FULL receipt `/mnt/ama-gates/g81-r15-1106/receipt.json` (scope `full`, status `passed`, head `c5edb320a`, base `56eec7369`, CLI exit 0) is a genuine receipt for the old base only. It is invalid for the new main and is not a basis for any new claim. It stays on disk unmodified. The checkpoint in `docs/architecture/cutover-evidence-pack.md` also remains as written for the old base; a dated addendum, not an edit, records the re-alignment.

## Boundaries carried forward

Three merged child contributions (#1226, #1228, #1229) and their original RPI evidence; child #86 / PR #1243 targets this topic and is not touched; native #79 ranking stack is separate; no FULL/heavy gate, scanner, image, SQL service, push, PR or issue change. Human, resident, legal and independent approvals are not established and the four issue #81 criteria stay unticked.

## Selected approach

1. Wait boundedly for rubric run `42361331168`; fetch `origin/main` again, re-pin, inspect any new delta.
2. Preserve exact backup ref of the frozen head, commit prospective records, then local rebase onto the final main (conflict-free predicted; genuine conflicts resolved preserving both intents; unclear conflicts stop).
3. Prove ancestry and child preservation, run focused regressions and static checks in an isolated scratch environment, add a dated checkpoint addendum, author Review, freeze clean.
