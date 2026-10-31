---
title: RPI Plan Critique - Live Azure verification
description: One final-candidate assessment of execution safety, evidence sufficiency and publication feasibility
ms.date: 2026-10-31
ms.topic: reference
---

## Metadata

* Task ID: 3a44be57-db3a-46d1-b9e4-fe82bd7c74e7
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md
* Research: .copilot-tracking/research/2026-10-31/live-azure-verification-research.md
* Critique execution status: Complete
* Execution count: One final-candidate critique; no prior or follow-up critique executed here.

## Inputs and Criterion Boundary

* Caller requirements: bounded LIVE verification of the two owner-named Azure apps; credential reads inside automation only; at most two sign-ins per account across this task; pip-only installation; no Azure configuration, replica, job or deployment changes. Check employee chat, first-load tabbed layout/assets, resident dock/resize, capacity #523/#524, identity #570 and metering #432. Publish sanitized evidence and conservative issue updates, deduplicate bugs, and require the complete local gate before a normal push/main-targeted Refs PR.
* Supplied candidate inputs: the exact plan, phase details and research paths above, including C1-C5, W1-W2, the three phases/tasks, acceptance criteria, dependency boundaries and Test Ownership Lock.
* Relevant source evidence: src/README.md local-rpi-gate; tools/rpi-checks.py clean_identity, heavy_lock and main; src/api/README.md AI consumption report and employee acceptance sections; src/api/checks/employee_acceptance_check.py; src/api/checks/capacity_browser_check.py MANAGER_ROUTES; src/api/checks/resident_demo_browser_check.py fixture boundary; docs/architecture/cutover-evidence-pack.md historical employee-origin evidence.
* Repository context read: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory was context, not evidence.
* Target issue bodies were read through read-only `gh issue view` on 2026-10-31: #523, #524, #570 and #432 in jmservera/ama. Across their 23 criteria, nine are currently checked and fourteen unchecked. #523/#524 each have one unchecked live-record criterion; #570 has three unchecked criteria; #432 has nine.
* Decisions assessed: use the maintained employee adapter after independent immutable identity admission; reject resident fixture mains as live drivers; retain financial/operational approval gates; no product fixes; preserve original critique/Review and historical adverse evidence.
* Ownership lock assessed: no existing test edits/removals; at most one dated live driver and one sanitized JSON addition; canonical evidence/index/log and RPI artifacts; no screenshot/HAR/session/identity-claim output. The findings below do not authorize more test files or source changes.
* Assessment boundary: plan credibility, execution safety, proof strength and publication feasibility only. This critique neither establishes live outcomes nor redesigns the product. Credential files, authentication, Azure writes, source edits and agent spawning were excluded.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Full RPI loop; P01-P03 | Partial | Research/candidate/changes/original Review/critique ownership is explicit; final publication has a known incompatible gate path, PC-001. |
| Credential secrecy and two-attempt task-wide maximum; P01-T01 | Partial | Internal parsing, pre-submit increment and capture exclusions are credible; interruption/restart accounting is unspecified, PC-002. |
| Two named live apps and independent identity; C3, P01-T01 | Partial | Strict independent tid/oid admission and zero sign-ins when unavailable are correct; both execution origins are not pinned, PC-003. |
| No Azure changes; resident fixture exclusion; C4, P01-T01 | Covered | Resident SQL fixture mains are explicitly excluded; no booking, consent, configuration or scaling operations are planned. |
| Employee chat/map/case; C3, #570 | Covered | Actual verify_employee uses fresh admission at action boundaries and correlated map rendering. Early-stage failure legitimately leaves later stages blocked. Source regression evidence and live acceptance remain distinct. |
| First-load tabbed layout/assets; #524, P01-T01 | Partial | Fresh contexts and no cache-busting are good; initial-response attribution and layout pass predicates are not defined, PC-004. |
| Capacity UI/API; C5, #523, P01-T01 | Partial | Routes and safe reads exist; rendered/API agreement and empty/error classification need a bounded observation contract, PC-004. |
| Resident dock/resize; P01-T01 | Partial | UI-only operation is appropriate; viewports, geometric invariants and measurable control outcomes need specification, PC-004. |
| Metering; W2, #432, P01-T01/P02-T01 | Partial | No billing/quality/batch authority is inferred; specify the safe report projection, availability/Unknown interpretation and time boundary, PC-004. |
| Evidence pack/index/append-only log; P02-T01 | Covered | Canonical targets and preservation of historical verdicts are explicit. |
| Issue ticks, closures and nonduplicate bugs; P02-T01 | Covered | Re-fetch/exact-text editing and readback are appropriate. Checking #523/#524's literal recorded-or-pending criterion must never imply successful live acceptance. |
| Test ownership, semantic versus regression coverage | Partial | One driver/result and unchanged full suites are appropriate; semantic live assertions need PC-004, and full-suite execution remains blocked by PC-001. |
| Exact-HEAD gate, receipt, independent assessment, Refs PR; C1, P03-T01 | Partial | Sequence and no-bypass policy are sound in principle; this runtime cannot execute the supplied runner contract, PC-001. |

## Verdict

* Verdict: Revise
* Severity summary: Two High and two Medium actionable findings; zero Critical or Low findings.
* Rationale: bounded observation remains credible after direct safety/evidence corrections. However, publication is already blocked by a proven gate/runtime conflict, not merely an unmeasured missing tool. The plan must distinguish executable observation work from unavailable publication and must prevent a restart from resetting the sign-in budget.
* Publication status: Blocked under the current runtime constraints. This is separate from the Complete critique execution status and Revise plan verdict.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The required full gate has no permitted execution path in this runtime

* Related IDs: C1, Q3, P03-T01, final-gate acceptance criterion, Test Ownership Lock validation.
* Evidence: tools/rpi-checks.py:64 fixes HEAVY_LOCK_PATH to `/tmp/ama-rpi-heavy.lock`; heavy_lock at tools/rpi-checks.py:2337-2370 opens that path with O_CREAT/O_RDWR. main at tools/rpi-checks.py:2399-2407 requires a new output directory outside the repository root. clean_identity at tools/rpi-checks.py:168-175 also refuses untracked and ignored scratch. The current execution instructions forbid all `/tmp`/temporary-directory file operations and require created files to remain relative to the working directory inside the project. The plan/details instead schedule an external venv and external full receipt, with only missing prerequisites described as blockers.
* Concern: changing `--out` or TMPDIR does not change the fixed heavy-lock path. An inherited lock descriptor still checks the same forbidden path and is not a bypass. An in-repository output is rejected by the runner. Source/tool changes are outside this candidate's no-source-change scope and would invalidate existing gate identity.
* Impact: the mandated complete gate cannot run as planned here; commit/push/PR completion cannot truthfully be promised. Trying the command to discover a known forbidden path would itself breach execution safety.
* Smallest useful change: mark P03 publication blocked now; explicitly prohibit invoking the gate in this runtime. Separate safe documentation/observation completion from blocked push/PR. Replace the external-venv assumption with reuse of an available environment or an explicitly permitted setup, and record any unavailable dependency as a blocker. Preserve the full gate requirement without fallback, protection changes or runner patches.
* Action owner: Planning parent; an authorized compatible execution environment is the publication dependency owner.
* Exact resolving evidence: revised plan/details identify the incompatible fixed lock and external-output contracts, mark publication blocked, and state that no push/PR occurs without a fresh full passing receipt and independent exact-head assessment. Actual publication becomes eligible only in an environment that legitimately permits the unchanged runner's paths and required tools; its receipt must then bind the clean committed candidate and current origin/main and be verified immediately before publication.
* Decision route: Direct planner correction to disclose and enforce the blocker. No user decision or exception to current prohibitions is required to record it. Moving execution or broadening source scope is not implicitly authorized.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The sign-in counter can reset after interruption or driver restart

* Related IDs: two-sign-ins/account requirement, P01-T01, non-functional task-wide accounting, one-driver/one-JSON lock.
* Evidence: the plan requires a maximum across all scripts; P01-T01 increments a counter before clicking and records attempt counters only in the completion JSON. Neither artifact defines recovery from a timeout, crash, partial run or repeat command.
* Concern: an in-memory counter protects one process, not the full task. A restart after a submitted login but before completion can consume a third attempt while still reporting an apparently valid per-process count.
* Impact: retries during scale-from-zero or automation debugging could violate the explicit authorization budget; lost attempt evidence cannot be repaired by guessing zero.
* Smallest useful change: designate the one permitted live driver as the sole credential-submitting executor. Use the already permitted sanitized result JSON as a durable checkpoint before any credential submission, with task/account-slot labels and counts only. Refuse concurrent live executions and fail closed on missing/corrupt/uncertain state after execution has begun. Unchanged command reruns must resume the consumed budget, not initialize a fresh one; health retries remain separate.
* Action owner: Planning parent for the contract; implementing parent for its enforcement.
* Exact resolving evidence: revised P01-T01 specifies initial state, pre-submission durable increments, restart/concurrency refusal and no reset across scripts. Driver inspection and credential-free validation demonstrate that two recorded submissions prevent another and that uncertain restart state prevents submission. This validation must not consume live sign-ins or add product test files; the sanitized final JSON preserves consumed counts and interrupted/blocked reason codes.
* Decision route: Direct planner correction; current user direction already fixes the maximum. No new sign-in budget or user response is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The two authorized application origins are not pinned in the candidate

* Related IDs: two-app requirement, research external scope, C3, P01-T01.
* Evidence: the plan/details/research refer to supplied or named Azure URLs but contain no explicit two-origin table. src/api/checks/employee_acceptance_check.py:22 pins the employee APP to `https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io`; allowed_page at lines 57-83 permits only that deployed origin or loopback. Historical cutover evidence also names other APIs, so an arbitrary historical URL is not proof of the owner-named resident target.
* Concern: the resident target and the association of each credential slot with its authorized app remain implicit. A guessed origin can test the wrong release or submit credentials outside the intended boundary; a different employee origin will be refused by the maintained adapter.
* Impact: results could be misattributed to the wrong app, and the authorized account/origin boundary is not reproducible from the committed candidate.
* Smallest useful change: recover the two exact origins from the parent's original owner request and pin them with account-slot and expected app type. Specify allowed authentication redirects separately from app/API/asset targets. Confirm the employee origin matches the maintained adapter; otherwise record that adapter-origin incompatibility as blocked, not a reason to weaken or edit it.
* Action owner: Planning parent with the original intake context.
* Exact resolving evidence: plan/details contain both exact public origins and provenance to the original request; driver constants and result labels match them. App API and public-asset reads are origin-restricted, while credentials are submitted only to the recognized intended login flow. If the original resident origin cannot be recovered, its authenticated checks are explicitly blocked before credential reads/submission.
* Decision route: Direct planner correction to restore supplied scope; no redesign or inferred new target. User response is not required for parent recovery of already supplied directions.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Supplemental live checks lack resolving semantic observation contracts

* Related IDs: P01-T01, C5, #523/#524/#432, first-load tabbed layout, resident dock/resize, semantic coverage and validation lock.
* Evidence: P01-T01 specifies asset hashes/byte counts, capacity API/render checks, resident no-content geometry and report field-presence projections, but no explicit measured invariants, viewport set, asset-response attribution or report projection/window. C5 supplies capacity routes and selectors, not a live agreement predicate. src/api/README.md:11-35 documents a manager-only report where HTTP 200 can mean unavailable consumption and Unknown costs.
* Concern: the existing employee adapter has strong actual assertions, but the supplemental checks could devolve into HTTP success, element existence or geometry collection without testing the requested behavior. Fetching assets again after navigation can hash a later successful response rather than the bytes implicated in the initial load. Presence of report fields cannot establish metering joins, financial reconciliation or functional availability.
* Impact: a successful command could still leave the core requested surfaces untested, or blur failed first-load delivery with later recovery and unavailable report data with working metering.
* Smallest useful change: add a compact observation matrix inside the existing phase details, not extra drivers/tests. For each surface, define the action, expected invariant, sanitized projection and pass/fail/blocked rule:
  * First load: attach relevant response/error observers before initial navigation; distinguish initial workspace delivery and automatic recovery from any later manual reload. Attribute hash/bytes/status to the actual response used; explicitly cover `/vendor/leaflet.js` and required workspace assets. Compare against the recorded local source pin without treating hash mismatch alone as an application defect.
  * Tabbed layout: specify the expected initial visible/selected panel and offered tab-switch outcomes using native control state and visible panel behavior, without modifying data.
  * Capacity: compare read-only `/api/packages` and `/api/workorders` projections with the visible list/count or a consistent empty state; classify an alert/retry state separately. If checking other manager pages for the known failure class, list the bounded routes; preserve their historical test verdicts.
  * Resident: name the offered open/close/dock/resize controls, selected narrow/wide viewports and measured invariants such as containment, overflow and meaningful size/position change. Unsupported controls or missing authenticated access are explicit blocked/failed observations, not implicit passes.
  * Metering: specify an explicit UTC report range/as-of, an allowlisted consumption-only projection, and separate available/incomplete/held/Unknown outcomes. A read/schema observation proves no dispatch limit, billing join, quality floor or authorized batch criterion by itself.
* Action owner: Planning parent for the matrix; implementing parent for the single supplemental driver.
* Exact resolving evidence: revised details define these bounded assertions and safe result fields. The one driver's actual dated execution records each invariant and initial-versus-recovery/report-availability distinction, including failures and blocked actions. Documentation and issue comments map only those observed facts to exact criteria; the complete unchanged regression gate remains separate and subject to PC-001.
* Decision route: Direct planner correction within the requested verification scope and locked additions. No product redesign or user response is required.

## Strengths and Residual Risk

* Independent tid/oid expectation provenance and zero employee attempts when unresolved are correct. Neither display email, roster binding nor `/api/me` may supply the expected identity.
* verify_employee already guards chat, map and case actions; using it rather than a weaker replacement is a substantive strength. Its advisory chat can legitimately return workflow-only output, which must remain distinguishable from actual AI labeling.
* The supplied resident fixture mains create/drop local SQL databases and are correctly excluded from live execution.
* Fresh contexts, internal-only credential parsing, capture exclusions and fixed sanitized observations substantially reduce privacy exposure. Browser/subprocess exception text must remain excluded even on failures.
* Health warming may remove the observable cold-start condition. This limitation is explicitly accepted in the candidate, as are the inability to establish historical-cache recovery and whole #432 economics from a chat or report read.
* #523/#524's literal live-record criteria allow truthful pending records; checking those rows does not upgrade a failed/blocked observation to passing acceptance. Issue closure still requires every criterion to be proven under its actual wording.
* #570's source mismatch cause/regression criteria can be assessed from exact source and executed regression evidence independently of its live chat/map/case criterion. A historical identity failure must not be retroactively reclassified.
* No additional findings are withheld for a later pass. Cosmetics, template preferences and unrequested accessibility/product redesign were not graded.

## Questions or Blocking Evidence Gaps

* No new user choice is needed for the four direct corrections.
* Missing independent directory attestation remains an explicit runtime blocker for employee actions, not a critique-requested identity bypass.
* The parent's original two-origin intake must resolve PC-003; a historical resident/API URL is insufficient substitution.
* Publication remains blocked by PC-001 even if every live observation succeeds. No source changes, gate fallback or permission exception is inferred.

## Limitations

* No credential file was read, no sign-in attempted, no app/API health or live UI checked, and no Azure write performed.
* No driver was implemented, dependencies installed, local gate run, issue edited/commented/closed, or push/PR performed.
* Review used supplied evidence pointers and their directly relevant contracts; no open-ended external research was performed.
* Issue bodies are read-only snapshots from the critique date and must be re-fetched immediately before later mutations.
* Only this critique artifact was written; existing untracked candidate artifacts and topic branch docs/live-verification-2026-10-31 were left intact.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: mark current-runtime publication blocked and reconcile the four direct corrections in the existing plan/details before any live implementation. Do not rerun critique.
* User response required: No for planner-owned corrections. A compatible authorized publication environment remains a dependency, not an invitation to override prohibitions.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md](.copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md) | Exact final candidate assessed |
| [.copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md](.copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md) | Existing task contracts requiring direct corrections |
| [.copilot-tracking/research/2026-10-31/live-azure-verification-research.md](.copilot-tracking/research/2026-10-31/live-azure-verification-research.md) | Supplied research and evidence boundary |
| [.copilot-tracking/reviews/plans/2026-10-31/live-azure-verification-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/live-azure-verification-plan-critique.md) | Complete original critique; preserve unchanged |

## Next Steps

The active planning parent should disposition PC-001 through PC-004 directly,
finalize the corrected candidate without another critique, and proceed only with
the safe eligible observation work. Keep publication blocked until the unchanged
complete gate and independent exact-head assessment are legitimately available.
No user action or peer-stage invocation is required by this critique.
