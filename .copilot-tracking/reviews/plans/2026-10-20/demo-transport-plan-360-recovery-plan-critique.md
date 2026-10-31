<!-- markdownlint-disable-file -->
# RPI Plan Critique: Authenticated roster transport design and tenant checklist (#360), recovery cycle

## Metadata

* Task ID: demo-transport-plan-360-recovery
* Critique date: 2026-10-20
* Plan: .copilot-tracking/plans/2026-10-20/demo-transport-plan-360-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only design (no execution) of an authenticated roster result transport plus tenant checklist after a process defect. No cloud, tenant, secret or private-data action. Parser not relaxed. Failed-attempt evidence preserved. No edits to budget/benefits (#126), cohort, Finance form or map domains. Old draft artifacts get an appended dated clarification only. No speculative success claims; whole #360 c, d and e unproved; cost and execution approval is a later precondition. Test ownership: no tests added, exact removals none, maximum additions two threat-table rows, one disclosure paragraph each in runbook and evidence pack, one new log entry, appended clarifications. Validation: git diff scope, ASCII check, link review, full local rpi-checks gate.
* Research and evidence considered: .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md; infra/README.md section "Authenticated Roster Result Transport Design"; infra/scripts/staff_azure.py (result_prefix, read_result, aad, encode_result, decode_result, wait loop); infra/scripts/staff-azure-worker.py (relay write guard); /tmp/ama-wave-20261020-2113-common.md.
* Decisions, dependencies, and acceptance criteria considered: plan Functional/Non-Functional Requirements, Acceptance Criteria, P01 to P03, DN1 to DN5, later cost/execution precondition.
* Assessment boundary: credibility of the plan as a bounded corrective edit set. Cited Microsoft Learn facts (W1 to W6) were not re-fetched; code facts were re-read from the repository. No live behavior, tag lag or Activity Log content is concluded.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Authentication wording (FR1, P01-T01) | Partial | Trust-assumption paragraph already says AEAD proves key possession only; plan adds "sharpening" without a bounded edit form (PC-002). |
| Threat rows Merge overwrite, Activity Log (FR2, P01-T01) | Partial | Rows planned but content constraints not pinned (PC-004). |
| Execution ID binding (FR3) | Covered | Already in the controller-held list; C9 consistent. No edit needed. |
| Process disclosure (FR4, P01-T02) | Partial | Wording target ambiguous; omits what stays unverified (PC-008). |
| Research contradiction on shared parser (Prior Knowledge Gate) | Missing | No plan task corrects the runbook "structured tag records" claim (PC-001). |
| Change budget and test ownership | Missing | Not stated in plan or details (PC-002, PC-003). |
| Records (P02) | Partial | Index edit and JSON "additive key" conflict with exact removals none (PC-002, PC-006). |
| Gate (P03) | Partial | Procedure and commit set under-specified (PC-005). |
| Protected domains, no execution, DN1 to DN5, whole #360 c/d/e unproved | Covered | Scope and Non-Goals, Unresolved items. |

## Verdict

* Verdict: Revise
* Rationale: The approach is credible and in scope, but the plan does not yet encode the caller's exact change budget, leaves one runbook overclaim that its own research contradicts uncorrected, and under-specifies the gate. All findings are planner-owned corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Runbook overclaim "structured tag records, not a byte stream" is contradicted by research and uncorrected

* Related IDs: research C4, Q4, Prior Knowledge Gate; P01-T01
* Evidence: infra/README.md Requirements table (Fail-closed parsing) and options table (T1 "structured records"); infra/scripts/staff_azure.py read_result wraps each tag as a console-style Log line and calls decode_result, which silently skips any record not starting with ZFSTAFF: and does not validate tag names beyond the run prefix.
* Concern: The research notes the draft claim is only partly right, yet no task schedules the correction. The design asserts a distinct, fail-closed structured path while code shares the console parser and silently ignores non-frame values under the run prefix. That conflicts with the design's own "no unknown field is silently dropped" rule.
* Impact: Reviewers may approve T1 believing the parser failure mode differs from the failed console path.
* Smallest useful change: Fold one additive corrective sentence into the single permitted runbook disclosure paragraph (no edit or removal of existing cells): tag frames are re-fed to the shared console-line decoder, non-frame values under the run prefix are currently skipped rather than refused, and the strict grammar in S2 is the planned fix; cite C4.
* Action owner: planning parent
* Exact resolving evidence: plan P01-T02 expected result and details name this sentence; implementation diff shows it inside the one disclosure paragraph; no existing README lines removed.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Plan lacks the exact change budget and implies edits or removals the caller forbids

* Related IDs: FR1, P01-T01, P02-T01, Acceptance Criteria
* Evidence: plan P01-T01 "Sharpen authentication claim... qualified wording"; details P01-T01 "requirements table" edit; P02-T01 "except index sentence if edited"; caller: exact removals none, maximum additions two threat rows, one disclosure paragraph in runbook and evidence pack, one log entry, appended clarifications.
* Concern: "Sharpen" or "qualify" existing cells is a replacement (a removal). FR1 is already met by the Trust assumption paragraph, so the edit is unnecessary. The index edit is likewise unbounded.
* Impact: Diff would exceed the stated budget and break the removals-none validation.
* Smallest useful change: Add a Change Budget to plan and details: removals none; additions exactly two threat rows, one paragraph in each of infra/README.md and docs/architecture/cutover-evidence-pack.md, one log entry, appended clarification blocks. Restate FR1 as satisfied by the existing paragraph, with any extra qualification inside the disclosure paragraph. Make any docs/reference/README.md change purely additive (a new pointer line, no sentence rewrite) or drop it if the existing pointer suffices.
* Action owner: planning parent
* Exact resolving evidence: plan and details contain the budget; the later diff shows zero removed lines in README, evidence pack, log and index, and only the budgeted additions.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Test ownership and no-test rationale not recorded

* Related IDs: P03, Non-Goals
* Evidence: plan Non-Goals "Source changes, tests"; caller test ownership statement.
* Concern: No explicit statement of tests added (none), removed (none) or who owns the future AAD v2, grammar and snapshot tests (S1 to S3, C11 gaps).
* Impact: A deliberate docs-only omission cannot be told from a gap.
* Smallest useful change: Add a Test Ownership line: no tests added or removed; infra/tests/test_staff_azure.py unchanged; future tests owned by the later S1 to S3 implementation.
* Action owner: planning parent
* Exact resolving evidence: line present in plan and details; diff shows no test files.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Threat row content is not constrained against overclaiming

* Related IDs: FR2, P01-T01, W2, W3, C8
* Evidence: infra/scripts/staff-azure-worker.py refuses overlap with existing names before a Merge PATCH; research W3 "whether tag values are recorded not established"; the existing first threat row already lists collide and "Activity Log evidence".
* Concern: A Merge-overwrite row can wrongly imply the worker overwrites (it refuses) or that Activity Log shows who changed tag values.
* Impact: Speculative claim about exposure and attribution.
* Smallest useful change: Specify both rows. (1) Another tag-write principal using Merge or Replace can overwrite an owned frame name; the worker guard does not constrain it; effect is AEAD refusal and denial of service, not forgery. (2) Whether Activity Log records tag values is unverified (only 90-day retention established); exposure and attribution effect unknown; control is DN1 review plus a read-only check before any run. Each row cites its URL and retrieval date 2026-10-20 and avoids "detected" or "proves".
* Action owner: planning parent
* Exact resolving evidence: details list both rows' wording and sources; implemented rows match and contain no success claim.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Gate and validation procedure under-specified

* Related IDs: P03, P03-T01, Acceptance Criteria
* Evidence: details P03 "commit, gate, receipt"; caller contract and AMA instructions (fetch main, record reviewed SHA, external receipt, no amend, no nested flock, noreply email and trailer, original artifacts committed before the gate).
* Concern: No commit set (README, evidence pack, index, log, old-artifact clarifications, recovery research/plan/details/critique/changes/review), no exact gate and verify commands, external output directory, or note that any later commit invalidates the receipt. Validation lacks an explicit allowlist diff and whole-section ASCII/link check. Review is a dependency of P03-T01 but not its own task.
* Impact: Risk of a stale receipt or an unnoticed protected-domain edit.
* Smallest useful change: In P03-T01 list the commit set, `git fetch origin main` and recorded base SHA, the gate command with `--all --base <sha> --out <new external dir>`, the `--verify-receipt` command, no post-gate commit, and a path allowlist plus denylist (budget/benefits, cohort, Finance form, map) diff check, ASCII check of changed sections and the README heading anchor check.
* Action owner: planning parent
* Exact resolving evidence: details P03-T01 contain these items; the changes record later shows receipt path, hash and verification output.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: "Byte-for-byte except append" is unachievable for the state JSON

* Related IDs: P02-T01, Acceptance Criteria
* Evidence: details P02-T01 "old state JSON (additive key)"; plan acceptance "Old artifacts preserved byte-for-byte except an appended dated clarification".
* Concern: Adding a JSON key changes the previous last line (comma), a removed line that breaks removals-none. The state file also wrongly says completed.
* Impact: The diff check would fail or the exception would be unrecorded.
* Smallest useful change: Choose and record one: declare the single trailing-comma line as the only permitted modified line, or leave the JSON untouched and record the clarification in the other appended artifacts plus a dated sidecar note. Prefer the sidecar if the coordinator disallows any modified line.
* Action owner: planning parent (state the choice in the changes record)
* Exact resolving evidence: plan acceptance states the exception or sidecar; diff stat matches.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: "Other prefixes ignored but counted" describes unimplemented behavior

* Related IDs: C2, existing threat row "Stale frames from another run"
* Evidence: infra/scripts/staff_azure.py read_result filters by prefix and counts nothing outside it.
* Concern: The control reads as current behavior; it is only proposed.
* Impact: Minor overstatement.
* Smallest useful change: Cover it in the same disclosure paragraph as PC-001 ("counted" is a proposed control). No row edit.
* Action owner: planning parent
* Exact resolving evidence: sentence present in the disclosure paragraph.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Disclosure wording target is ambiguous and omits what remains unverified

* Related IDs: FR4, P01-T02, research Process Disclosure
* Evidence: plan FR4 "superseded by the recovery cycle for verification"; details P01-T02; research says the draft "critique" and "review" were subagent calls, not RPI outcomes.
* Concern: "Superseded" can be read as the draft design being replaced or accepted. The paragraph should say the draft was authored before skill activation, its critique/review are not RPI outcomes, the recovery cycle re-read code evidence only (no live check, no independent review yet), and DN1 to DN5 and whole #360 c, d, e stay open.
* Impact: Risk of implied acceptance or a speculative success claim.
* Smallest useful change: Specify the paragraph content in a dated, non-backdated form for both the runbook and evidence pack, pointing to the recovery research, plan and critique paths.
* Action owner: planning parent
* Exact resolving evidence: details P01-T02 contain the required points; implemented paragraphs contain them and no acceptance wording.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: Plan status fields not yet reconciled with the critique

* Related IDs: plan Critique Disposition, Planning status, Handoff
* Evidence: disposition row "pending / open"; status "ready".
* Concern: Dispositions for PC-001 to PC-008 must be recorded before handoff.
* Impact: Handoff readiness is not auditable.
* Smallest useful change: Fill the disposition table with each PC and its response; keep Ready only after the corrections.
* Action owner: planning parent
* Exact resolving evidence: disposition table lists PC-001 to PC-009 with responses.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Scope is tight, execution and protected domains are excluded, and DN1 to DN5 and whole #360 c, d, e remain open.
* The re-read of staff_azure.py and the worker agrees with research C2, C4, C5, C8 and C9.
* Residual risk accepted by design: live tag lag, Activity Log tag-value content, pricing and real position count remain unverified; cost/execution approval is a later precondition.

## Questions or Blocking Evidence Gaps

* None blocking. No user decision is required.

## Limitations

* Learn pages W1 to W6, research arithmetic (247-character frame, 43-character name) and test locations C11 were not re-verified here.
* The critique cannot judge the later diff.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-002, which constrains how it can be fixed)
* Action owner: planning parent
* Smallest next action: revise plan and details directly for PC-001 to PC-009 (change budget, corrective sentence inside the one disclosure paragraph, pinned threat rows, P03 gate commands), record dispositions, then finalize without another critique.
* User response required: no
