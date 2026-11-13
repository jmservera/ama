---
title: Issue 440 post-1504 checkpoint plan research (0630)
description: Bounded research for a prospective checkpoint plan to run only after PR 1504 merges, Refs #440
ms.date: 2026-11-13
ms.topic: reference
---

Task `issue-440-post1504-plan-0630`, parent task `issue-440-stabilization`. Refs #440. Disposition: executed, bounded read-only research (five-minute budget, tracking only). Planning Readiness: Ready for a prospective plan; Not Ready for any checkpoint execution, which cannot start before PR 1504 merges.

## Prior dispositions read first

* Ledger `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/demo-run-ledger.md` (1,084,053 bytes) read by targeted search only (`440`, `1504`, `post1504`, `checkpoint-plan`), not end to end. Result: no match under those search terms for an earlier post-1504 plan or disposition (absence under the searched terms only, not proof of none), so this lane is treated as not a repeat. Its last entries record 74 and 1504 as separate lanes and the holds named in the brief (184, 891, 531, 144, 146, 96, 153, 189, AI bdec); none of those lanes is reopened here.
* Reused same-pin finding: [post-1500 plan](../../plans/2026-11-13/issue-440-post1500-0240-plan.md) (commit `6f2918011`, annex docs-only, merged-main provenance checkpoint) is the existing 440 protocol for a docs-only post-merge checkpoint. Its structure is reused; its pin (`ad1a17229`) and its evidence classes are not re-derived.

## Identities (read-only, verified 2026-11-13)

| Item | Value |
| --- | --- |
| Worktree and branch | `demo-home-checkpoint-plan-0630`, `research/demo-home-checkpoint-plan-0630`, clean at start |
| Frozen parent | `b9d7db29bd7f55474f075b29a7d890df4cab3b92` on `feat/demo-home-parent-0555`, equal to the head of open PR 1504 |
| Tree at parent | `5626e500605d82775ddbf5abf548da3a844bcdf3` |
| Main baseline | `origin/main` `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626` (fresh fetch equals the pin); 1504 is not merged (`mergeCommit` null) |
| PR 1504 state | OPEN, mergeable, no review decision. Read hosted checks were SUCCESS for pre_activation, src-changes, activation, src-no-working-data, rubric_prepare, image-paths, agent, src-namespace, detection and mssql; the full rollup was not read, so completeness is UNKNOWN. A skipped or absent workflow is not a success |
| Issue 440 | OPEN. Criteria 1 to 6 ticked, the last two (triage of findings, genuine RPI artifacts in the PR) unticked; this lane ticks nothing |

## Affected #74 source (three files, blobs at the frozen parent)

| Path | Blob |
| --- | --- |
| `src/api/README.md` | `1b9fb02d3c0942c81c74fbeceebd9bde60f9c3dc` |
| `src/api/checks/home_case_browser_check.py` | `57db4756f858016c48ae19aa2c43c8e5241e3459` |
| `src/api/src/zava_forward/api/web/app.js` | `2fdf48045002460698f5c730b3f6aa83d0ed3572` |

The delta over main is these three files plus 24 tracking files (607 insertions, 3 deletions). The source records each shared building record's recorded `case_ids` and `package_ids` as read-only display (listed, Unknown or None). Optional G5 is read-only display and is not literal #74 criterion 2 acceptance.

## Document blobs and status (at the frozen parent, unchanged by 1504)

| Document | Blob | Status in file |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` | `34d88395de86` | draft, version 0.21.0, ms.date 2026-10-24 |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | `c788b917bafa` | in-review, version 0.21.0, ms.date 2026-10-25 |
| ADR 0001 `d42fa5c4615f` | as listed | `## Status` Proposed, non-production demonstrator design |
| ADR 0002 `cbe21530043f` | as listed | Proposed overall; a later owner acceptance for staff identity (2026-10-24) is scoped, not whole-ADR approval |
| ADR 0003 `d60645397b20` | as listed | Accepted with amendment by the owner, 2026-10-15, reconciled 2026-10-18 |
| ADR 0004 `9406c2e747ce` | as listed | Accepted as written by the owner, 2026-10-15 (staged option C) |
| ADR 0005 `4d610335a5a1` | as listed | Accepted for synthetic development only, 2026-10-16; operational use proposed |
| ADR 0006 `956da1a3b804` | as listed | Accepted by the owner, 2026-10-15 |
| ADR 0007 `541e0f72dd2c` | as listed | Proposed as a whole; owner direction for the synthetic demonstrator only |

Status is document-qualified, not approval. Nothing here is owner or legal sign-off.

## Per literal acceptance criterion of #440 (disposition for this lane)

| Criterion | Evidence read | Disposition |
| --- | --- | --- |
| 1 Trigger (after feature wave, record issues, PRs, main SHA, document versions) | Issue body read; prior checkpoints under `.copilot-tracking/changes/*-440-*` and post-1500 plan | A post-1504 trigger exists only after merge. Planned, not executed. Covered issues and main SHA are UNKNOWN until merge |
| 2 Reconcile requirement IDs and ADR decisions with code, tests, journeys | Blobs above; 74 source pack and independent assessments in the PR | Plan only. Source implemented, focused local results recorded in the PR; main acceptance not established |
| 3 Local-first ladder | Post-1500 plan P4 and issue text | Reused as the ladder in the plan; no test run in this lane |
| 4 Azure only for listed residuals | Issue text | No Azure call. Azure criteria stay unknown human or cloud residuals; they do not block local planning |
| 5 Boundaries, consent, AI failure and manual paths | 74 display adds no rule, approval or eligibility change (research 0555) | Plan carries the exclusion list |
| 6 Execute the first checkpoint | Ticked on the issue by earlier work | Not reopened |
| 7 Triage confirmed findings into issues | Unticked | Not done here: no new issues authorised |
| 8 Genuine RPI artifacts in the PR | Unticked | This lane contributes plan artifacts only; PR 1504 is not this lane's PR |

## Existing gaps (carried, not rediscovered)

* PR 1504: axe SKIPPED, valid base-red unverified, hosted CI incomplete or unread, human accessibility, WCAG conformance and owner confirmation of the G5 display absent. Source-focused local results: six API tests exit 0, one bounded browser run 24 PASS markers 0 FAIL (markers, not 24 independent tests).
* Held and out of scope: 184 candidate `e904` (partly new format FAIL, SQL unrun), c71 helper (null false pass, H4 unavailable), 891, 531 (criteria 1 to 6 delivered, live only), 144 E1 to E5 and 189 C5 exhausted, 146 paused, 96 saved copy C1 to C3 with older whole history unknown and no 153 budget laundering, AI bdec four modules exit 0, no OS network-denial proof, core preflight grep only.

## Candidate independent initial local increment

None. Evidence found no initial local engineering increment required by these criteria: the only code in the delta is already implemented and locally verified at source scope; its open items are human, cloud or hosted (axe, CI, accessibility, owner). The unrun items are unverified, not missing code. The prospective deliverable is a docs-only annex plan for after merge, which is the exact-slice disposition.

## Not read (explicit)

The whole ledger, the full PR 1504 rollup, the 440 history older than the post-1500 pack, the cutover evidence pack body and the regulatory snapshots were not read within the budget. Memory is context, not evidence.
