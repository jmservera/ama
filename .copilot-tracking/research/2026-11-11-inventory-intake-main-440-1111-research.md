---
title: Inventory and staff intake current-main checkpoint research (Refs 440, 131, 132, 1362)
ms.date: 2026-11-11
task_id: 440-inventory-intake-main-1111
---

## Disposition and scope

Research executed 2026-11-11T00:11Z to 00:15Z (actual clock), before any test run, plan or documentary edit. The witness `launch` and `research-open` markers were recorded together at 00:15:33Z after this record existed, so they do not attest the earlier reading time. Planning Readiness: Ready. Disposition: executed (new investigation of merged sources; no earlier research reused as proof).

Scope is a bounded early integrated documentary checkpoint on pinned `origin/main` after three merges: PR 1421 (checker issue 1362), PR 1422 (household inventory, issue 131) and PR 1425 (staff-mediated intake, issue 132). It also covers the independently identified need to verify that household holds still guard ordinary independent QA after the new staff intake. It is not new issue or scope discovery, a feature correction, a source repair or a full gate. Owner context (memory) is context, not evidence.

## Identities (verified, not assumed)

| Item | Value |
| --- | --- |
| Worktree and branch | `issue-440-inventory-intake-main-1111`, `docs/demo-inventory-intake-checkpoint-440`, clean at start |
| Pinned main and HEAD at start | `0509ddcef14d9c2046791b283fad65229f536202`, tree `69a4812252456e6b854f09ab0560468c89f22e9c` |
| Fresh `git fetch origin main` (2026-11-11T00:13Z) | `0509ddcef14d9c2046791b283fad65229f536202`, equal to the pin; merge base equals the pin |
| Trees at the pin | `src` `f47636fa76bcf295276c419f178d8d7855f862b9`, `src/core` `06418f54614c1fa2063d3b28c51498bc2eb9ceca`, `src/api` `ccb6944509692f43f80065128321e9d386bb944d`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` |
| PR 1421 | MERGED 2026-11-10T23:50:46Z, merge `6f5e5007a84ab719013b94d592d5416c7949b453`, head `355cbb0558d9f22824ad9f1c57c8116439033ce0`, closes 1362 (CLOSED) |
| PR 1422 | MERGED 2026-11-10T23:52:41Z, merge `83c28132ceb7c8609569c4c4fe9f1f9bca1ded58`, head `500a868ecda23e84bcf1d326817fb1626b7d3ac0`, Refs 131 only |
| PR 1425 | MERGED 2026-11-11T00:09:22Z, merge `0509ddcef14d9c2046791b283fad65229f536202`, head `204bc6adb2a1b5d429c634e8ed1b9a49f820553a`, Refs 132 only |
| Hosted checks at the pin | Capstone Rubric Scorer on `0509ddcef` was `in_progress` when read; the commit's check runs read 3 success and 1 incomplete. No Source projects CI result for the main head is claimed |
| Issue states (read live) | 440 OPEN `status:partially-delivered`; 131 OPEN `status:partially-delivered` and `status:not-started`; 132 OPEN `status:not-started`; 1362 CLOSED. No criterion is ticked or closed here |
| Excluded | Unmerged PR 1423 Capacity CSV and handoff parent (OPEN), 1426 served-transfer report (OPEN), worker issue 144 (OPEN), and the branch 1360 regression, which is not a main acceptance and is not reported as a main defect |

## Source blobs at the pin

| Path | Blob |
| --- | --- |
| `src/api/checks/atlas_tensions_browser_check.py` | `b1facccfa2c8396a3c798654a4e0544168659a40` |
| `src/api/tests/test_atlas_tensions_checker.py` | `63fd2327751bddce263b3973309975dc720ca882` |
| `src/core/src/zava_forward/core/resident_decisions.py` | `ba5d1c13e5a368013cc5fb4b6466d9d1a11e76b4` |
| `src/core/tests/test_resident_decisions.py` | `21fb8384be3299ecce0c865ea8446176cd1f22ec` |
| `src/api/tests/test_resident_api.py` | `425a13720574332aede2624911e8f24500613c31` |
| `src/core/src/zava_forward/core/staff_intake.py` | `3de31ca27b08ec4de0aa37affd54a2cd9a39ee53` |
| `src/api/tests/test_staff_intake_api.py` | `358e34b303277c74383b9e7c1fabf75d32271370` |
| `src/api/tests/test_staff_intake_browser.py` | `16f7d4edc5c5df298124ae395ac7121d9ae1750d` |
| `src/core/src/zava_forward/core/quality.py` | `23f97a33b98f5ede4a8d8c51a7131514e7b834c4` |

## Decision documents (read at the pin)

| Document | Status and identity |
| --- | --- |
| BRD Agentic Retrofit Programme 0.21.0 | `draft`, ms.date 2026-10-24, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; `business_goal_smart_status: fail`. Draft is not approval |
| PRD Zava Forward Retrofit Programme Workbench 0.21.0 | `in-review`, `exercise_status` author-complete-unsigned-pending-review-and-owner-acceptance, ms.date 2026-10-25, blob `c788b917bafaede215f326f0efc71e071a687f1c`. Not owner accepted |
| ADR 0007 Contractor Job Pack and Evidence Intake Delivery | Proposed 2026-11-04, not accepted, blob `abb21088a9bb9771234a305b8052c3bcdd181b33`. It says it does not close issue 132 criterion 6 |
| ADR 0003 and ADR 0006 | Accepted; blobs `d60645397b20fb70ac3d1dc47c7a6c8671201306` and `956da1a3b804c803041fe2e8a312bd9f400273ae`. Context only |

Requirement qualification (must not be conflated): BRD FR-015 (BR-061, AC-021) is the tenure and lease-interest decision route, with the unverified-tenure rule and communal-works hold (RULE-023); BRD AC-021 says agreement from one household is never applied to another and no automated capability interprets a lease. PRD FR-015 is hazard source, referral and retrofit-hold evidence (AC-018, AC-038) and is not tenure. BRD FR-016 and FR-017 are exception stops and handoff contents (AC-022, AC-023). PRD FR-016 is the versioned provider-package record (AC-019, AC-039) and PRD FR-017 is the independent per-measure quality-disposition record (AC-020, AC-042). Issue 132 cites PRD FR-016 and FR-017 as source references, so the staff-mediated intake maps to them only partly: it records worker-confirmed checklist evidence as a quality submission with a distinct receipt acknowledgement, and it does not own readiness, returns, chronology or provider submission authority.

## What the three merges changed (read from the merge diffs)

* 1421: only `atlas_tensions_browser_check.py` (+49/-7) and `test_atlas_tensions_checker.py` (+82). The checker matches the exact Current design version value and rejects hidden or transparent label or value. Checker-only, no product defect (issue 1362 text).
* 1422: `resident_decisions.py` (+209), Core and API READMEs, `test_resident_decisions.py` (+512), `test_resident_api.py` (+50). Caller-declared household inventory (`tenure_inventory_record`, read `tenure_inventory_view`) with a closed schema, digest per linked report, Unknown valid, malformed history never extended, and a stored revision missing the `households` key is malformed while explicit null stays Unknown.
* 1425: new `staff_intake.py` (480 lines), `staff-intake.js`, server routes `field-intake` GET and `field-capture`, `field-correct`, `field-acknowledge` POST, a one-line `quality.py` change (`_touched()` before a SQL quality operation), two test edits and `test_staff_intake_api.py` (484) and `test_staff_intake_browser.py` (137).

## Static trace of the QA guard (read, not yet observed)

* `resident_gate(c, bindings)` returns `[*_inventory_refusal(c), TENURE_HOLD]` whenever `_inventory_managed(c)`. The exact predicate (`resident_decisions.py:249`) is: the key `tenure_household_inventories` is present, or `tenure_review_required` is truthy, or `tenure_reports` is a non-empty list, or `tenure_reports` is present and not a list. An empty `tenure_reports` list or a false `tenure_review_required` alone does not opt in, so cases without those fields keep legacy behaviour (a stated limit of 1422).
* `accept_quality` and `hand_over_quality` (for accepted work) call `require_resident_clear(c, [binding])`, which raises `GateError` for any non-empty `resident_gate`; `handover_blockers` appends the same gate. `return_quality` does not call it. So for an inventory-managed case the shared gate refuses QA acceptance and handover whatever the scope binding. `reinspect_quality` passes through `accept_quality`.
* `staff_intake.capture` binds the work order's current resident scope revision as `context_revision`; `_res_scope_record` refuses a new scope on an inventory-managed case. Nothing in `staff_intake.py` references the inventory or `TENURE_HOLD`; acknowledgement leaves the quality state `Submitted`.

## Test selector map (existing tests only)

| Selector | Exercises | Does not exercise |
| --- | --- | --- |
| Core `tests.test_resident_decisions` `-k inventory` (JSON class, `SqlResidentDecisions` on SQLite, `MssqlResidentControls` skipped without opt-in) | inventory integrity, Unknown, stale link, malformed history, identity and route reasons, hold never released by refreshed data, committed-acknowledgement and race truthfulness, private projection | staff intake, `accept_quality` on an inventory-managed case |
| Core `test_resident_acceptance_never_clears_technical_or_hazard_gates`, `test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release` | shared resident and quality gates, QA accept and handover on non-inventory cases | inventory-managed case |
| API `tests.test_resident_api` `-k inventory` | HTTP opt-in, refusal-only, role hiding of the inventory | staff intake |
| API `tests.test_staff_intake_api` (JSON class; MSSQL class skipped without `ZF_STAFF_INTAKE_MSSQL=1`) | capture, correction, acknowledgement separate from acceptance, self-review denial, contractor denial, scope-binding refusal, retry replay, injected failure, independent QA positive control (`test_recorder_is_denied_and_independent_qa_accepts` on the non-inventory case ZF-3) | an inventory-managed case; no test mentions inventory |
| API `tests.test_role_endpoint_inventory` | role endpoint inventory including the new routes | household data content |
| API `tests.test_atlas_tensions_checker` (opt-in Chromium `ZF_BROWSER_TESTS=1`) | checker 1362 helper and real-DOM negatives | product behaviour |
| API `tests.test_staff_intake_browser` | screen axe capture; needs `ZF_STAFF_INTAKE_BROWSER=1` and pinned `ZF_AXE_PATH` (axe-core 4.10.3), neither available and not installed here | combined journey |

A scan of every `src/*/tests/test_*.py` function body for inventory setup together with `accept_quality`, `submit_quality`, field capture or `staff_intake` found no match, and for QA accept or handover together with tenure or inventory words found none. So no existing selector exercises the combined journey (household inventory-managed case, staff capture, independent QA). The inventory-managed refusal control for ordinary QA is therefore covered only through the shared function `resident_gate` (Core) plus the static trace, and the positive control only on a non-inventory-managed case. Creating a regression test is out of scope (owner brief) and none is created.

## Environment and constraints

* `~/.zava-forward` did not exist at start; `ZF_DATA`, `.env` and credentials are unset or unused. The primary checkout editable installs of `zava-forward-*` were observed in earlier records to shadow a worktree, so a fresh private venv with editable installs of this worktree is required; no `PYTHONPATH` source workaround.
* Heavy lock `/tmp/ama-rpi-heavy.lock` was held by another process (pid 75438) at 00:13Z; browser runs need one non-blocking `flock -n`, never queued or killed. Chromium 1248 is cached.
* Host: 15.9 GiB memory, 7.8 GiB available at 00:13Z.

## Findings that constrain the plan

* No new defect is yet evidenced. Any reproduced gap must first be compared with owners 131, 132 and 440.
* The combined journey is untested at selector level; the checkpoint must state this as an exact gap, classify the QA guard as implemented but unverified at the combined level, and not paper over it with the Core gate tests.
* BRD, PRD and ADR 0007 statuses stay draft, in-review and proposed; nothing is approved by this record.
* Residual boundaries: Legal interpretation of tenure, Home Ownership data owner, actual household roster, QA, resident consent and production identity remain human boundaries.
