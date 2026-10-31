<!-- markdownlint-disable-file -->
---
title: Resident survey authorized main refresh before publication
description: Preserved gate failures and newly advanced main integration
ms.date: 2026-10-31
---

## Scope and Direction

Continuing task 571 publication under the owner's explicit latest-origin/main
merge authorization, same branch. Original and both child Research/critique/
Review artifacts remain immutable. This is upstream-input reconciliation before
the final gate, not another source correction or repeated Review.

## Actual Adverse Attempts

Correction1 full gate for `10401c5a` ran with base `a75bbdff` and failed static/
browser as recorded by correction2. Failed receipt preserved externally:
`/tmp/ama-571-correction1-full-gate/receipt.json`, SHA-256
`e6b5f56a9f65cd7d354e4bb905ece04f0d46f48fa0547e4e3d3b1496bd929685`.
Full log SHA-256 `49d5342cb6bc1f2453a044b926b12d9430a21bf9fd47b9a2c226ab708b952d08`.

Correction2 committed `e07e32730ad0f012927c94e53684c88fcd96dcc3` then attempted
full gate at base `a75bbdff`. First admission waited 1800s and timed out, exit1,
before checks. One automatic admission retry used a fresh output directory;
it rejected advanced current-main identity before validation, exit1:
`Reviewed base differs from current origin/main; reconcile before validation`.
No successful receipt or check execution for either attempt is claimed.
Original logs remain unchanged:

| Output | SHA-256 |
| --- | --- |
| `/tmp/ama-571-correction2-full-gate.log` | `a61e364435be7c6fffd44ae8f8a2a7359d918b0b5754b4b3f1bb6bf7f802039b` |
| `/tmp/ama-571-correction2-full-gate-retry.log` | `9596f596ca22ec160ac4914f536113df3b8c022f71678a3c8743a5083b2b3865` |

## Current-Main Integration

Fresh fetch returns `e64c6e6c9da407682de59b926944424f94f50671`, merged #600
for #572 exact chat-panel success evidence. Authorized merge auto-resolved
without conflicts; main rubric side retained, both log histories preserved.
No local workflow or WORKFLOW_HASHES change. Runner matches current main exactly;
its new strict exact-test validation is preserved, not rolled back.
Our source diff against current main is still only resident regression/guide,
iteration-bound formatted employee harness, local synthetic tooling capture and
related gate guide note. Main adds two tooling tests, not this correction.
No merge change to either resident/employee browser source.

## Fresh Reconciliation Validation

Complete verbose tooling discovery with task-owned pip Python:
39 tests pass; unchanged merged static parser gives tests39/executed39/skips[].
Exact isolated root Ruff check/format passes for runner/tooling; strict mypy
passes both. Log `/tmp/ama-571-main-refresh-tooling.log`, SHA-256
`cdaf4f03fa5f8864576efdf7caeb8de5fe2f615eb297fe98f7cabfd41a7ebfc4`.
No synthetic skip transcript leaks, no real skip acceptance change.
Both earlier full local browsers and API/Ruff evidence remain source-matching;
new complete gate must execute final merged inputs.

## Publication Handoff

Commit authorized merge and this original dated reconciliation evidence with
privacy-safe identity/trailer. Create new clean exact-HEAD candidate and execute
full --all with native shared-lock timeout1800, one admission retry.
Fetch main and verify immediately before approving independent exact-head
assessment and nonforce push/main PR. Any stale/missing/adverse evidence blocks
publication. No final passing receipt yet; authoritative final receipt/status
remain external/PR to avoid post-gate self-invalidation.
Closing issue language remains conditional on all three reviewed criteria and
final eligibility. Direct human/AT/live approval and hosted/owner gates remain
separate, no source correction or repeated Review follows this refresh.
