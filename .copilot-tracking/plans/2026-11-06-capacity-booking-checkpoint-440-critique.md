---
title: Capacity booking checkpoint plan critique (Refs #440 #82 #81)
description: Single critique of the eleventh checkpoint plan, details and research, verified against git and the light-run log
ms.date: 2026-11-06
ms.topic: reference
---

## Metadata

* Task ID: 440-capacity-booking-checkpoint
* Critique date: 2026-11-06
* Plan: .copilot-tracking/plans/2026-11-06-capacity-booking-checkpoint-440-plan.md
* Phase details: .copilot-tracking/details/2026-11-06-capacity-booking-checkpoint-440-details.md
* Research: .copilot-tracking/research/2026-11-06-capacity-booking-checkpoint-440-research.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task: documentation-only eleventh checkpoint in docs/architecture/cutover-evidence-pack.md, plus README index paragraph and appended log entry, for lifecycle parent af891a5cc, governance a97bea15 and main bb3a3b03 as separate pins.
* Verified directly: git pins and trees; origin/feat/controlled-lifecycle-integration-81 diffs against cd271cfa5, d4d33c7ec and origin/main; source of gates.py, procurement.py and appointments.py; PRD, BRD and ADR blobs; PRD FR-008, FR-016, FR-017 and AC rows; existing pack headings; /tmp/l440af891/out/run.log and its sha256; PR 1229 merge state via gh.
* Not verified: supplied receipt and SQL log contents (/tmp/g82-cap-r3-1106), hosted checks, issue bodies, approval states, the import-proof transcript.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Pins (P01-T01) | Covered | af891a5cc, tree cb8a3d46; main bb3a3b03; a97bea15 and HEAD tree 7995337f all match. PR 1229 mergedAt 2026-11-06T03:10:17Z, merge commit af891a5cc. #1226 (cd271cfa5) and #1228 (d4d33c7ec) are ancestors. |
| Document blobs | Covered | BRD 34d88395, ADR 0003 d6064539, ADR 0006 956da1a3 match parent and main. PRD c788b917 is docs/prds/zava-forward-retrofit-programme-demonstrator.md (v0.21.0); see PC-005. |
| Traceability (P01-T02) | Covered | FR-008 gates, FR-016 provider package and capacity record, FR-017 quality; AC-010 and AC-011 map to FR-008, AC-067 and AC-144 not re-read. CapacityGateError, Fail (False), Unknown (None) mapping and sole-failure rethrow match source. |
| Light run (P01-T03) | Covered with gaps | Log sha256 matches 3fd61476...; Ran 193 tests in 65.877s, OK (skipped=1). One skipTest in scope, in test_hazard_referral.py line 313. See PC-002, PC-003. |
| Overclaims (no SQL, no approval, no closure) | Partial | Stated in the plan, but borrowed approval and SQL results need explicit wording; see PC-001, PC-004. |
| Ordinal and append-only | Covered | Ninth heading at line 3594 and tenth at line 3734 exist; no eleventh yet. Plan requires zero removals. |
| Critique Disposition | Missing | Pending placeholder; must be filled after this critique. |

## Verdict

* Verdict: Revise
* Rationale: The pins, source semantics, blobs and run log are accurate and the plan is sound in structure. Five planner-correctable wording and provenance gaps would let the checkpoint overstate evidence or misattribute the diff. None needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Coordinator-supplied FULL, SQL and approval results at 272146 must not read as parent evidence

* Related IDs: P01-T03, plan Non-Goals, research Evidence classification candidates
* Evidence: git rev-parse 272146^{tree} equals af891a5cc tree cb8a3d463b0f1d31d1a5de0d1e1a2e68de7ebc8e; the receipt and SQL logs were hash-matched only, never read.
* Concern: The 17-group FULL, SQL 296 total, hosted 10 checks and "published and local functional approval with 0 findings" belong to commit 272146f4e. Same tree is a reason, not a run at af891a5cc, and "approval" can be mistaken for governance approval.
* Impact: Breaks the no-SQL-at-parent and no-approval boundaries.
* Smallest useful change: Add a detail that each such row names its commit (272146f4e), is classed "supplied, not reproduced", states tree equality once as non-run, and calls the review outcome a code-review result, not an approval or acceptance.
* Action owner: planning parent
* Exact resolving evidence: P01-T03 row text in the details file and, later, the pack table showing these labels.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: PR 1229 diff statistics are misattributed

* Related IDs: research "Source read", P01-T01
* Evidence: git diff --shortstat cd271cfa5 af891a5cc gives 23 files, +519/-16 (this spans #1228 and #1229); git diff d4d33c7ec af891a5cc gives 17 files, +447/-15. Only 5 files, +152/-16, are under src; the rest are .copilot-tracking records.
* Concern: Research states "git diff of #1229, 23 files, +519/-16".
* Impact: A wrong figure in an evidence pack that is meant to be reconstructible.
* Smallest useful change: Quote 17 files, +447/-15 for #1229 alone (d4d33c7ec..af891a5cc), or label 23 files, +519/-16 as "#1228 plus #1229 over #1226". State that 5 of the files are source and tests, and that the parent over main is 48 files, +1200/-25 (verified).
* Action owner: planning parent
* Exact resolving evidence: Pack text figures equal the two git --shortstat commands above.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Light-run evidence is transient and the skip and import proof are not in the log

* Related IDs: P01-T03
* Evidence: run.log (5374 bytes) lacks verbose output and import proof; it lives in /tmp. skipTest at src/core/tests/test_hazard_referral.py:313 is the only skip in the three modules (grep count 1).
* Concern: The skip attribution and import provenance rest on session claims, and the log is the only durable pointer.
* Impact: A later reader cannot re-derive these.
* Smallest useful change: In P01-T03 classify them "local observed, session-only; skip attributed by source reading", record the sha256 as the only durable pointer, and note that /tmp may be cleaned. Do not copy log content.
* Action owner: planning parent
* Exact resolving evidence: Pack row classification wording; no raw log copy.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The 13 expected nonzero probes and the false zero-nonzero assertion need exact qualified wording

* Related IDs: P01-T03, plan Bounded semantics
* Evidence: Research cites a native assertion that was false and an #82 comment; neither was read here.
* Concern: Repeating "13 expected nonzero probes individually read" as the checkpoint's own finding would assert an unverified reading.
* Impact: Converts a coordinator claim into an observation.
* Smallest useful change: Attribute it to the #82 comment as supplied, not reproduced, state that this checkpoint did not read the receipt, and do not quote the false assertion.
* Action owner: planning parent
* Exact resolving evidence: Pack evidence row classed supplied/unverified.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Two PRD files exist; blob and path must be named

* Related IDs: P01-T01, P01-T02
* Evidence: docs/prds/ holds proper-warm-retrofit-programme-demonstrator.md (blob f7f9b767, v0.13.0, in-review, historical) and zava-forward-retrofit-programme-demonstrator.md (blob c788b917, v0.21.0). CAPACITY_RULE.source cites the zava-forward path. The BRD FR-008 is a different requirement (material change invalidates approvals).
* Concern: Details say only "PRD" and the PRD blob without a path, and FR numbering is shared across both files.
* Impact: Wrong FR source if a reader opens the legacy file.
* Smallest useful change: Give the path with each blob and note the legacy file is not the governing one. Draft and in-review are not approval.
* Action owner: planning parent
* Exact resolving evidence: Pack identities table lists both path and blob.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Close the critique disposition and anchor convention before implementation

* Related IDs: plan Critique Disposition, Functional Requirements
* Evidence: Plan says "Pending". The tenth heading uses a preceding explicit anchor line with a slug.
* Concern: The disposition is unrecorded and the eleventh anchor is not specified, so an implementer may vary the pattern.
* Impact: Weak audit trail and possible broken anchor.
* Smallest useful change: Record dispositions PC-001 to PC-005 as accepted or rejected, and state the anchor will follow the tenth pattern (a id line before the heading, slug of the heading).
* Action owner: planning parent
* Exact resolving evidence: Updated plan disposition section committed before any pack edit; the validation step greps the anchor once.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Pins, trees, merge time, blobs and test counts reproduce exactly; semantics for Fail, Unknown, sole-failure rethrow and capacity-last match source.
* No source, API or store schema changed in #1229, supporting "Pass is internal only".
* Residual risk accepted by design: SQL Server, browser and the full gate at af891a5cc are unrun.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static read and git only; the supplied receipt, SQL log, issue states and import proof were not independently checked.
* AC-067 and AC-144 mappings were not re-read.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Revise the details and plan (PC-001 to PC-006) directly and finalize without another critique.
* User response required: no
