---
title: Behavior report 010, coordinator idle recovery (issue 1204)
ms.date: 2026-11-06
---

* Targets: .github/agents/ama-backlog-delivery-coordinator.agent.md (agent, isolation), blob acefb44a4d254ede6d86413343127b763dec42cb, unchanged. HEAD at execution 769d620b8ff4aec520fffac1a43e50a45d3b4954, tree 593c7d9f8c1190d7278a9a170701391b24b28006 (planning commit made before any dispatch).
* Run type: full fresh, the one owner-approved final fixture-only round. Reuse eligibility: Not applicable. Reports 005 to 009 and sandboxes 001 to 008 were not reused, copied, regraded or modified.
* Profile: HIGH responsibility and rigor inference, not backend identity, not native Automatic.
* Model and host attribution (own events.jsonl, subagent.completed, no override, modelSelectionSource session_inheritance, model and firstDispatchedModel claude-sonnet-5.5; this differs from the explicit gpt-5.6-sol overrides of earlier runs):
  * design, general-purpose, toolu_01GtLRsrNQWQRNVmLLEQxTFB, 16:52:58Z, 357807 ms;
  * execution, hve-core-all:hve-artifact-tester, toolu_01JLBY45dv5SXsdmP7PqgdDm, 16:59:29Z, 337596 ms;
  * grading, general-purpose, toolu_01RgUrohEb3cJmt1jiULZiKi, 17:01:38Z, 98511 ms.
  This is host attribution, not backend attestation. The designer, executor and grader are separate subagents.
* Fidelity: simulation (read-only HVE Artifact Tester). Native Deferred.
* Execution status: Complete (11 scenarios, all sub-snapshots). Verdict: **Pass** (independent grader, simulation-grade): 0 Critical, 0 High, 0 Medium, 6 Low; 0 material target defects.
* Sandbox: .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-009 (retained). External verbatim returns at /mnt/ama-gates/restart-1106-1204/final-fixtures-r5/ (designer-return-raw.txt sha256 64b5f038a3902774e7fb88f0f37d781b22922b59089ec823afee5d3e07900e01; executor-return-raw.txt sha256 3a467ef077b0c619b218ff4ea11adacb8b643b4c5f50857ebd67ec8706ba8371; grader-return-raw.txt sha256 6e657cabd02b94eb8a81f6eded784727e3f4c61c511ae567fc298a68d1803fe3). The executor return was a host-saved pointer file copied unchanged; the grader return was extracted from the session event record.

## Summary

The three report 009 findings are resolved in the fixtures. Seven retained assignments including exited #334 gave one free slot and a literal successful launch (H-03B, H-03F); H-06 used canonical RPI paths and the positive batched, stacked publication was exercised with parent targets and Refs wording; the previously unsupplied facts were supplied and used. The stale brief negative case (H-08) was refused and a fresh brief with the parent target used. The executor invented no outcomes and reported missing facts as not supplied.

## Findings

| # | Category | Severity | Dimension | Summary |
|---|---|---|---|---|
| F1 | target ambiguity, advisory | Low | Liveness, retries | No quiet-worker hang threshold; no rule for when a transient route error stops being retry work. |
| F2 | target ambiguity, advisory | Low | Board, reporting | Board status for a child merged into a parent topic, and local assessment of a human-blocked frozen candidate, unspecified. |
| F3 | target ambiguity, advisory | Low | Schedules, pause | Whether an owner pause of delivery also stops cleanup, and whether a pause releases a slot, unspecified. |
| F4 | fixture defect | Low | Fixture | H-06 #502 stack command lacks PR_HEAD and stack-member; H-03E push-before-validation order; H-08 pin later than brief time; H-01 #210 body versus review result. |
| F5 | executor error | Low | Report fidelity | H-11 collapsed #911 to #917 into one row; #213 and #214 labelled unknown; hashes abbreviated in prose. |
| F6 | oracle note | Low | Oracle | #500 focused tier while the integrated parent includes full-tier #502 work; parent re-gate expected. |

No source correction is proposed or made; F1 to F3 are advisory and are for the coordinator to route.

## Adjudication and honest qualifications

* Lead agrees with the grader (sandbox test-review.md). Pass is simulation conformance only.
* Planning (research, plan, details, one critique, state) was committed as 769d620b before the sandbox and any dispatch. Earlier rounds consumed their cycles; this is the one extra owner-approved round.
* Live schedule state (delivery #4 every 5 minutes, maintenance #5 hourly, obsolete 1, 2, 3 stopped, criterion 4 ticked) is supplied coordinator operational evidence, not read or changed by this run; live prompts do not prove the source edits are deployed.
* Tool frontmatter was not inspected or graded. Raw verbatim traces contain original whitespace and Unicode; git diff --check is reported excluding those verbatim files and is not claimed as a whole clean diff.

## Fidelity and limitations

Simulation supports conformance claims only. All Git, GitHub, SQL, schedule, session, merge and cleanup actions were emulated from fixture facts. Native tool reliability, atomicity, locking and restore are untested; containment was by read-only tools and instruction. Executor file reads are self-reported. The harness-default model differs from earlier runs.

## Coverage

Criteria 1, 2, 3, 5 and the behavior part of 6 are covered in simulation, including the positive publication and stack path and the capacity rule. Criterion 4 is simulated only (H-04) and live state is supplied evidence. Closure batching is covered by H-01 only; H-11 supplies no closure queue. Criterion 6 PR-level artifacts and human review remain unmet here.

## Containment

Pre-run ignored-inclusive status 0 lines; post-run only the new sandbox untracked; target blob unchanged. No shell, Git, GitHub, cloud, schedule or cleanup action by the executor.

## Satisfied-and-skipped

None.

## Human review

* [ ] Human review of this behavior report is complete.
