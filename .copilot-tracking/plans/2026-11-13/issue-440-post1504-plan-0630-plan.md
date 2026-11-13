---
title: Issue 440 post-1504 checkpoint plan (0630)
description: Prospective, candidate-qualified plan for a docs-only checkpoint after PR 1504 merges, Refs #440
ms.date: 2026-11-13
ms.topic: reference
---

## Status

Draft, prospective, local-only, not approved. This is a plan for a checkpoint that may run only after PR 1504 merges. It is not a checkpoint, not main acceptance and not cutover evidence. Research: [research](../../research/2026-11-13/issue-440-post1504-plan-0630-research.md). Critique: [critique](./issue-440-post1504-plan-0630-critique.md). Protocol reused: [post-1500 plan](./issue-440-post1500-0240-plan.md).

## Objective

After 1504 merges, record one smallest merged-main checkpoint as an appended annex in `docs/architecture/cutover-evidence-pack.md`, with a state record, reconciling the home-case display source with document-qualified requirements and ADR status. Distinguish four classes: main (baseline `15bfee2d7`, not containing 1504), the qualified parent (frozen `b9d7db29b`, G5 read-only display, candidate evidence only), hosted observations on the merged head, and human, Azure or cloud residuals.

## Trigger and resume pin

* Trigger: PR 1504 shows MERGED. Until then nothing in this plan executes and no current cutover pack edit is made.
* Resume pin: fetch `origin/main`; record the actual merge commit, resulting main SHA and tree. The pins in this plan (`15bfee2d7`, `b9d7db29b`, tree `5626e500`) become historical inputs, not the checkpoint pin. If 1504 merges by squash or rebase, blobs may differ; re-read the three source blobs at the merged head and report any difference. If main also gained other merges, list covered issues and PRs from `git log` of the new main only.

## Affected source (blobs at the frozen parent)

`src/api/README.md` `1b9fb02d3`, `src/api/checks/home_case_browser_check.py` `57db4756f`, `src/api/src/zava_forward/api/web/app.js` `2fdf48045`. BRD `34d88395d` (draft, 0.21.0), PRD `c788b917b` (in-review, 0.21.0), ADRs 0001 to 0007 blobs listed in the research. Status is document-qualified, not approval.

## Original RPI to preserve (byte-unchanged, cited)

The 74 independent assessments `c3aecd946`, `4b8689031` and the retained-validation records, the 74 review and the parent 0555 research, plan, critique, changes and review, including adverse and qualified outcomes. No rewrite, reset or relabelling.

## Exclusions

184 candidate `e904`; c71 helper; 74b9 optional G5 as criterion 2 acceptance; 891; 531 live; 144, 189, 146, 96, 153 (no budget laundering), AI bdec diagnostics as acceptance; B1 1473, 1288, 1331 and v2 continuity or capacity policy rediscovery; routing campaign; new issues, issue or board edits, ticks, push or PR in this lane.

## Reconciliation map to fill at checkpoint time (all UNKNOWN until merge)

| Item | Code and test source | Journey and boundary | Status class |
| --- | --- | --- | --- |
| #74 criterion 2 (compound) | G5 display in `app.js`, checker markers; not criterion 2 acceptance | Read-only display; no eligibility, approval, filter or rule change | implemented, unverified on main; criterion open |
| Requirement IDs in the BRD and PRD touching the home case view | UNKNOWN: to be read at the merged head, not asserted from titles | Resident consent, human approval and manual path boundaries unchanged by the delta (research 0555) | each ID classed local observed, implemented but unverified, deferred, blocked or unknown |
| ADR decisions | ADR 0003, 0004, 0006 accepted scopes; 0001, 0002, 0007 proposed | AI failure and manual path: no AI change in the delta | document-qualified, not approval |

## Targeted ladder (after merge, smallest first)

1. Re-pin and `git diff --check`; read-only blob comparison of the three source files and the pack.
2. Focused local checks by the later admission only if the merged source differs from the frozen parent: node syntax check of `app.js`, Ruff check and format on the checker, six existing API tests, the one bounded browser run (the harness is local-only and was run once at source). Any check run is stated as its own observation; none refreshes earlier counts.
   Evidence equivalence is judged on all named inputs, not the three blobs alone: also the API tests, core and agents dependencies the checker imports, workflows and manifests changed by intervening merges. If equivalence cannot be established, mark inherited results UNKNOWN and rerun only the affected focused check. If the annex edits the cutover pack, run `test_live_doc_links` from `src/core` once and report it separately from the source observations.
3. Hosted CI read for the exact merged head, with absent, path-filtered or skipped workflows stated as not success (axe skip is not a pass).
4. No SQL, Docker, Azure, provider, model, private data or full gate. Tier: focused documentation tier; classification and basis recorded; a mixed or unresolved impact takes the full tier.

## Unknown human and Azure criteria (stay UNKNOWN, not blocked local engineering)

Owner confirmation of the G5 display and label, human accessibility test, WCAG conformance, axe outcome, valid base-red, any Azure-only residual, owner decision on #440 triage and deliberate deferrals. No Azure call is authorised.

## Existing gaps carried

Listed in the research. Triage criterion and PR-artifacts criterion of #440 stay unticked.

## Increment and dependency decision

No independent initial local engineering increment is required by these criteria (source already implemented and locally verified at its scope; remaining items are human, cloud or hosted). Exact-slice disposition: docs-only annex, after merge only. Dependencies: PR 1504 merged (owner decision, exact-head independent assessment, human approvals, hosted CI); fresh `origin/main`; clean topic branch from merged main. Shared-file overlap: the annex edits the cutover pack and `docs/reference/log.md`, which held candidates (203 pack-reading link test, 184) also read or touch; propose one at a time, never concurrently. Authority: explicit root admission of the Implement stage by name; no authority to approve a pivot, deferral or relaxation.

## Phases

* P1 Re-pin (after merge).
* P2 Draft the annex: trigger and identities, four classes, document status table, hosted observations with qualifications, preserved adverse items, backlog and holds, CONTINUE proposal not a decision.
* P3 Hygiene: append a log entry; change the index only if the pack row's description changes.
* P4 Focused checks above.
* P5 One independent Review, then exact-head assessment by root, owner merge decision. Review findings become later work; no repeat Review.

## Resume condition

Resume at P1 only when PR 1504 reads MERGED and root names the Implement stage. If 1504 is closed unmerged or retargeted, this plan is void for the pin and needs a new research.
