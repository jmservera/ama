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

## Second Main Advance After Complete Gate Execution

Full gate for `0631436fbf6ed2ee970f8aa954d33673e22173f3` / base `e64c6e6c`
admitted 2026-10-31T13:22:12.181442Z after queue starting 13:09:47.090191Z,
one worker. All seventeen required groups passed, including all five project
suites, static, infra, migration, actual browser, disposable SQL, four image
contracts/scans and logo-mode stress. 200 commands were recorded.
Full gate API: 1430 tests, 1109 executed/321 enumerated opt-in skips; the
additional asset browser skip occurs before the later required browser install.
Core: 1608 tests, 1402 executed/206 enumerated opt-in skips. Required dedicated
chat browser executed exactly one successful named test, zero skips; disposable
SQL 268 tests/267 executed/one explicitly JSON-only non-applicability.
No skip or axe incomplete was converted to executed acceptance.

At final sealing, main had advanced to `5198a1ff4bdf416249b64d5f4d832e88f3f7040b`
(merged #603 documentation-only resident gauge evidence). Current-main identity
rejected publication despite completed checks; receipt status failed, exit1.
It is historical complete execution, not a current verified publication receipt:
`/tmp/ama-571-final-full-gate/receipt.json`, SHA-256
`ff74040819a74ee6dba08b550f77951d4957eab3c5338ea35ff67cb0d6436954`;
log SHA-256 `4d837759c38821c4dbc2f13a7d3ed69782479e6155d493ac78c4b8ed4ab9aa06`.
Both remain unchanged. No resume across changed base/HEAD is allowed.

Latest main merged automatically under the same explicit authorization, retaining
main rubric/workflows/runner/log, and both knowledge-log histories. No merge
delta to browser harnesses, tooling capture or any runtime source. New main changes
only documentation/evidence; original and child Review outcomes remain unchanged.
Commit merge plus this dated original refresh evidence, then fresh complete gate
at the resulting clean exact HEAD/base, fresh verification and approving independent
exact-head assessment. No weakened identity, partial tier, force, cloud or premature
PR publication. Final authoritative receipt/status remain external/PR-bound.

## Third Main Advance and Equivalent Upstream Harness Repairs

Publication gate for `74f50fc9` / `5198a1ff` again passed all seventeen required
groups, then failed current-main identity at sealing (14:51:18.033722Z). Preserve
failed receipt `/tmp/ama-571-publication-full-gate/receipt.json`, SHA-256
`c99c2c95df3ff3fff3f26f8a58067eda89fb25557a5b72719bf32a47e828aa30`,
and log SHA-256 `30121008c30d46357b9bb9aedfec2ca413e620d9ff5064eb9284e847196a0d44`.
No stale receipt verification/approval, push or PR followed.

Fresh main `28fbe6b6111c5aae4fc2c4f55f8ffca2876ab589` contains merged #601/#604
employee checks/evidence and independently delivered equivalent mandatory
harness repairs. Main's case journey now equals our bound/formatted harness.
Resolve two overlaps by keeping main's gate guide and capture implementation/
outer-transcript regression; retain our stronger two-complete-occurrence capture
assertion in addition to main's existing inclusion assertion. Main-added tests
are preserved. Final tooling diff against main is one additive assertion only.
Main's added workflow command and matching runner WORKFLOW_HASHES are retained
unchanged; no locally recalculated hash or workflow change. Main score and both
knowledge-log histories remain intact. Resident seven-line regression and guide
remain additive-only and unaffected.

Fresh local validation after resolution: tooling 43 tests pass, unchanged static
parser tests43/executed43/skips[]; exact isolated Ruff/format and strict tooling
mypy pass. Tool log `/tmp/ama-571-third-refresh-tooling.log`, SHA-256
`e3a94fc5f0b53e4bb7976386f9b56c590ba02d53aae2bbbaa17044c07ef1a0d9`.
Requested API unit discovery: 1442 tests in 652.499s, OK (skipped=320);
API Ruff check passes and 66 files formatted. Log
`/tmp/ama-571-third-refresh-api.log`. Existing source-matching resident browser
evidence remains valid as historical focused execution; the new full gate must
execute all newly merged required employee/browser/SQL/image contracts.
Documented jobs3 preflight admits one worker; no capacity override/lock bypass.
Original and child Review outcomes remain immutable; final exact-head assessment
must compare equivalent merge resolutions and the final verified receipt.

Commit original refresh evidence and merge, then fresh full current-main gate,
fresh fetch/verification and approving exact-head assessment before publication.
No passing current receipt exists at this handoff; no partial/stale-base shortcut.

## Fourth Advance: Final Main Batch

Full gate for `24941741` / `28fbe6b6` passed all seventeen groups, including the
new three-test employee browser contract, then rejected current-main identity
at sealing after merged #602/#605. Preserve failed receipt
`/tmp/ama-571-current-publication-gate/receipt.json`, SHA-256
`71c355889ab9ab906f2891b515ac5eba9331269e3c1c77682177c545eec83ab2`,
and full log SHA-256
`2ed34158199f2eab72ee9f6694025273e07e37f9ab6ec0a9fcbf46a3911666d2`.
Again this is complete historical execution, not eligible current evidence.

Fresh main `7136be9778b17e495b1941e6eb93f50d32de8a2b` adds source-only AI
metering and capacity contracts. No open main PR was returned at this fetch.
Owner-authorized merge completed automatically without conflicts; main score,
workflow/runner/hash inputs and both log histories remain intact. Final source
diff remains only resident check7/guide5 and one capture assertion. No branch
AI/Azure/approval change is introduced by reconciliation.

Local complete tooling suite and unchanged static parser pass:
tests48/executed48/skips[]. Exact isolated runner/tooling Ruff/format and strict
mypy pass; normal API Ruff passes and 67 files formatted. Capacity preflight
still admits only one worker for documented jobs3. Refresh source-matching
resident browser on this runtime base, commit original reconciliation evidence,
then run complete fresh gate including final API/SQL/image contracts.
All prior original/child Review outcomes and adverse receipt identities remain
immutable; final assessment must bind the current verified HEAD/base/receipt.

Resident browser first admission timed out after 1800s (exit75, no execution,
empty original log). The single allowed retry passed complete resident flows
against merged `7136be97`: Chromium156.0.8078.4, pinned axe executed32scans,
zero violations/42 incompletes, no errors/external requests. Report
`/tmp/ama-571-last-resident-retry/report.json`, SHA-256
`9503e463bd668a7e554abf9e2e998b53724a62a180f21df5ee547d8cd27e9974`;
retry log SHA-256
`ee40fa95aa4a7fcbc9cdc83e338f0f6c9ef6887c3f91565f7e2b6d0f68eb992d`.
Tooling48 tests completed in14.027s; log SHA-256
`0008dbda8e08f0dfd4e82b58820075ab615de468689ea661b089f529dd39f485`.
Main advanced again during admission to `87bf629c630314f5be086697e322e1b0ec22277d`
(#606/#607 equivalent gate-baseline and employee progress evidence). Commit the
current authorized merge, reconcile that final advance preserving both histories,
then new complete receipt. Earlier complete executions remain immutable adverse
identity evidence; no premature publication or silent skip/approval follows.
