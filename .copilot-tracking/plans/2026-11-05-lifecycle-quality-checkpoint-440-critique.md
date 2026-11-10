---
title: Plan critique for the lifecycle quality-gate checkpoint (Refs #440 #82 #81)
description: Single critique of the tenth stabilization checkpoint plan, phase details and research
ms.date: 2026-11-05
ms.topic: reference
---

## Metadata

* Task ID: 440-lifecycle-quality-checkpoint
* Critique date: 2026-11-05
* Plan: .copilot-tracking/plans/2026-11-05-lifecycle-quality-checkpoint-440-plan.md
* Phase details: .copilot-tracking/details/2026-11-05-lifecycle-quality-checkpoint-440-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context: documentation-only tenth checkpoint in docs/architecture/cutover-evidence-pack.md, one README index paragraph, one appended log entry; three separate pins; 183-test light observation; no approvals or heavy gates.
* Evidence considered: the plan, details and research files, git objects for origin/feat/controlled-lifecycle-integration-81, origin/main and HEAD, the BRD and PRD on the parent, src/core/tests, /tmp/l440cd271/out/run.log, and the existing pack, README and log tails.
* Assessment boundary: claims were checked against git and the log. The supplied 10161 receipt, hosted checks, issue states and the receipt.json hash were not independently reproduced.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Pins (research) | Covered | Verified: cd271cfa tree 6bc66942 equals 10161ecb tree; 1faadaa3 tree 678085a2; main bb3a3b03; HEAD..origin/main is 0; commit cd271cfa is 2026-11-05T23:01:09Z, consistent with the 23:01:10Z merge time. |
| Source diff (research) | Covered | main..cd271cfa is 28 files, +682/-10, as stated. |
| P01-T01 identities | Partial | BRD blob 34d88395 (draft 0.21.0) and PRD blob c788b917 (in-review 0.21.0) verified; ADR blobs d6064539 and 956da1a3 verified at docs/adrs/ paths; docs diff main..parent is empty. |
| P01-T02 traceability | Partial | PRD FR-008 and AC-010, AC-011, AC-067, AC-144 verified; BRD FR-008 is a different requirement (verified). PRD acceptance rows read "Not run"; see PC-003. |
| P01-T03 evidence | Partial | run.log ends "Ran 183 tests in 80.183s / OK (skipped=1)" and sha256 matches; see PC-001 and PC-002. |
| P01-T04 recommendation | Covered | No approval, closure or tick; consistent with the constraints. |
| P02 and P03 | Covered | The ninth anchor exists at line 3594 and the README ninth paragraph at line 403; zero-removal and ASCII checks are planned. |
| P04 | Partial | See PC-004 and PC-005. |

## Verdict

* Verdict: Revise
* Rationale: The pins, source diff, document blobs and log result verify. Two evidence-wording gaps could make the record overclaim or misattribute (SQL boundary, skip attribution). Both are direct planner corrections and none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: "No SQL claim at the parent" conflicts with the observed run

* Related IDs: P01-T02, P01-T03, research "Evidence classification candidates", plan constraints
* Evidence: src/core/tests/test_quality_procurement.py (SqlStore at lines 74 and 637, class with sql = True) and src/core/tests/test_hazard_referral.py:310-312 (skipTest when self.sql). The run.log tracebacks show src/core/src/zava_forward/core/sqlstore.py executing.
* Concern: The 183-test run exercised SqlStore-backed test variants, which are SQLite-backed local SQL. The plan lists "SQL store behaviour at parent" as implemented-unverified and says no SQL claim. The classification is therefore too coarse. The run is local observed for SqlStore variants in three modules. SQL Server or Azure SQL, and the full 291-test SQL gate, are the unverified part.
* Impact: A reader could conclude the SQL path was never exercised, or the reverse and read the light run as the SQL gate.
* Smallest useful change: Split the row into (a) local observed: SqlStore-backed variants in the three modules at the cd271cfa export, and (b) implemented-unverified or blocked: SQL Server or the full SQL suite at the parent, with tree equality to 10161 not counting as a run.
* Action owner: planning parent
* Exact resolving evidence: The details P01-T02 and P01-T03 and the research classification state the SqlStore (SQLite) versus SQL Server boundary, matched to the plan non-goal wording.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Skip attribution is inconsistent between research and details

* Related IDs: P01-T03, research "Light observation"
* Evidence: Research says the skip reason is unattributed unless the log shows it. Details assert it is the JSON-only separate-file audit ordering test in test_hazard_referral.py. run.log is non-verbose and shows only a single "s" in the dot line, with no test name.
* Concern: The attribution comes from reading source (the only skipTest that matches in the three modules is at test_hazard_referral.py:312), not from the log, and the other two modules have no skipTest at all.
* Impact: Presenting a source-inferred reason as log-observed overstates the evidence.
* Smallest useful change: Word it as "inferred from source: the only skipTest in the three modules is test_hazard_referral.py:312; the non-verbose log shows one skip without a name". Optionally rerun with -v only if a new light observation is wanted; that is not required.
* Action owner: planning parent
* Exact resolving evidence: Details P01-T03 and the record use the inferred wording, and the research no longer contradicts the details.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Traceability must not imply acceptance criteria passed

* Related IDs: P01-T02, Functional Requirements
* Evidence: docs/prds/zava-forward-retrofit-programme-demonstrator.md lines 2106, 2107, 2163 and 2219 mark AC-010, AC-011, AC-067 and AC-144 as "Not run". AC-067 is the sensor-analysis criterion and AC-144 is the ApplicationAdmin criterion; both reach FR-008 only partly or incidentally.
* Concern: Mapping FR-008 to four ACs next to a green 183-test run invites reading that the ACs are verified. The code change touches only the quality gate, not AC-067 or AC-144 behaviour.
* Impact: Possible overclaim of requirement coverage.
* Smallest useful change: Add to P01-T02 that the PRD ledger status stays "Not run", that the observation is a unit-level indication only for the quality gate, and that AC-067 and AC-144 are cited only as the FR-008 link, not as evidenced.
* Action owner: planning parent
* Exact resolving evidence: The details name the ledger status and which ACs the quality change actually touches (AC-010 and AC-011 at most).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Critique disposition and ordering disclosure are not yet recorded

* Related IDs: Critique Disposition, P04
* Evidence: The plan says "Pending". The research notes the 183-test run was done during research, before the plan, details and critique.
* Concern: The plan calls the order prospective, but a run preceded the plan. The research discloses this, while the plan and details do not carry it into the record.
* Impact: Minor process-honesty risk in the published record.
* Smallest useful change: Record this critique's disposition (the findings accepted and applied) in the plan, and have the pack's "Actual commands and limits" state that the light run predated the plan as read-only research.
* Action owner: planning parent
* Exact resolving evidence: The plan Critique Disposition lists PC-001 to PC-005 as applied, and the pack text includes the ordering sentence.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: External evidence is not durable and there is no pre-publication freshness check

* Related IDs: P01-T03, P03, P04
* Evidence: The run log, export and venv live under /tmp/l440cd271 and /tmp/ama-main-440-ui-cache-wave3-venv. The plan has no step to re-confirm that origin/main, the lifecycle parent and 1faadaa3 are unchanged before commit. Currently HEAD..origin/main is 0 and the pins match.
* Concern: Hash-only references to /tmp artifacts cannot be re-read later. The pins may drift before publication.
* Impact: Weak auditability and possible stale pins.
* Smallest useful change: Add to P03 a re-fetch and rev-parse of the three pins immediately before commit, and state in the record that the log is external and identified by sha256 only, with the command and environment recorded. Optionally copy the 8 KB log into the tracking evidence if retention policy allows.
* Action owner: planning parent
* Exact resolving evidence: P03 lists the pin re-check, and the record states the external-artifact limit.
* Decision route: direct planner correction

## Strengths and Residual Risk

* The three pins are kept separate, the cd271 and 10161 trees are shown equal, and the BRD and PRD FR-008 are correctly qualified by document.
* Scope is tight (three files, append-only), with explicit non-goals and no heavy gates.
* Residual risk: the supplied receipt, hosted checks and issue states are taken as supplied and must stay labelled that way.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* The supplied child 10161 receipt, the receipt.json contents, hosted checks and live issue states were not re-verified. The run.log was read and not re-run.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply PC-001 to PC-005 directly in the plan, details and research wording, then proceed to the pack, index and log edits without another critique.
* User response required: no
