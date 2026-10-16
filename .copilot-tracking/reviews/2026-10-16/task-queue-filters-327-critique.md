---
title: Task queue filters 327 final-candidate plan critique
ms.date: 2026-10-16
---

## Metadata

* Task ID: #327
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/task-queue-filters-327-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/task-queue-filters-327-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research, plus relevant code in src/core/src/zava_forward/core/store.py, taskqueues.py, resident_decisions.py and sqlstore.py.
* Assessed meaningful correctness and performance gaps in a snapshot-scoped inverted ID index built once using canonical work_context, with warm candidates restricted before existing filtering and paging.
* The caller permits the indexed path and snapshot caching. Cold construction remains measured work, not an eliminated cost. Membership keys include store version, snapshot as_of, ranking policy and controls.today. Visibility and redaction remain request-specific.
* Considered all functional/non-functional requirements, acceptance criteria, P01-T01, P02-T01 and P02-T02. Verification depends on implementation; delivery depends on verification.
* Maximum eight additional test methods, no test removals. No implementation, test execution, agent dispatch, external research or prohibited data reads were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Canonical membership; P01-T01 | Covered | Store.work_context calls the existing evaluators. taskqueues.context constructs all six memberships independently of reason_ok; that flag controls narrative text rather than membership conditions. |
| Snapshot and policy invalidation; P01-T01 | Covered | The research specifies version/hash/approval/owner alongside store version, as_of and controls.today; phase details require snapshot/day and ranking definition/approval keys. Resident authority and retention checks use the current day, not only as_of. |
| Shared and cross-process changes; P01-T01, P02-T01 | Covered | SqlStore._SyncLock invokes _sync before the outer read; _sync refreshes changed cases and shared documents and advances Store.version. Planned shared/cross-process regressions address this boundary. |
| Visibility, guards and redaction; P01-T01, acceptance criteria | Covered | Invalid-queue and contractor guards precede index access; closed view retains its existing contract. Current objects, existing visibility filters and fresh output projection remain in use; cached values contain IDs only. |
| Paging, sorts, search, totals and CSV; acceptance criteria, P02-T01 | Covered | Existing page_cases ranking/sorting/cursor/output stages are retained. The planned cached-versus-uncached comparisons cover all queues and existing sorts, with paging/search/filter/CSV parity required by acceptance. |
| Warm performance and cold measurement; P01-T01, P02-T01 | Covered | Generated 60k before/after timing distinguishes cold construction from repeated reads. Context-call counts, including negative queues, detect repeated canonical scans independently of wall-clock noise. |
| SQL compatibility and scope | Covered | Queue reads already delegate to Store. The index needs no new dialect-specific SQL or ID parameter lists; ordinary SQL paging remains unchanged. |
| Test budget and mutation; P02-T01 | Covered | At most eight core test methods, no removals, existing API coverage reused; runtime replacement with original selection must make a new regression fail. Multiple scenarios can share parameterized/subtest methods. |
| Delivery; P02-T02 | Covered | Documentation, actual measurement figures, remaining limitations, review and PR steps are specified. Delivery execution is outside this critique. |

## Verdict

* Verdict: Pass
* Rationale: No actionable meaningful correctness or performance gap was established within the supplied boundary. The proposed index removes repeated non-output work_context evaluation without redefining membership, caching role-projected narratives or bypassing existing paging semantics. Its key and refresh strategy account for the identified membership dependencies.
* This is planning credibility, not evidence that the implementation already meets its correctness or 1500 ms targets.

## Findings

No actionable PC-xxx findings. No cosmetic or speculative concerns are promoted to required revisions.

## Strengths and Residual Risk

* Atomic publication on successful construction under the existing lock avoids exposing partially built membership.
* Request-time authority/visibility and narrative projection are retained rather than cached per viewer.
* Cold builds still evaluate all open cases, including cases outside a particular viewer's result set, and hold the Store lock. The caller explicitly accepts honest measurement of this cost; the plan makes no cold-latency elimination claim.
* An index is not an end-to-end constant-time page operation. Broad queues can still require filtering and sorting many candidates, and CSV still projects every matching output row. Existing page logic and measured warm latency remain the acceptance boundary.
* Day, policy and store-version changes may rebuild all six queues. Rebuild frequency and actual timings must be reported as measured implementation evidence, not assumed production performance.

## Questions or Blocking Evidence Gaps

* None requiring a user response or a plan revision within this boundary.

## Limitations

* No private datasets, environment files, properwarm.json or issue-cache files were read.
* No tests, benchmarks, Docker, Azure or uv commands were run. Generated-data timings, parity and mutation outcomes are future implementation evidence.
* No review of unrelated code or independent operational acceptance is implied. The supplied inputs, rather than issue history or external sources, define the requirements assessed here.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Finalize the candidate and proceed through its implementation gate, retaining the stated verification requirements and eight-method ceiling.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/task-queue-filters-327-plan.md](.copilot-tracking/plans/2026-10-16/task-queue-filters-327-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/task-queue-filters-327-phase-details.md](.copilot-tracking/details/2026-10-16/task-queue-filters-327-phase-details.md) | Assessed implementation and verification details |
| [.copilot-tracking/research/2026-10-16/task-queue-filters-327-research.md](.copilot-tracking/research/2026-10-16/task-queue-filters-327-research.md) | Supplied research and cache decision |
| [.copilot-tracking/reviews/2026-10-16/task-queue-filters-327-critique.md](.copilot-tracking/reviews/2026-10-16/task-queue-filters-327-critique.md) | Complete final-candidate critique |

## Next Steps

No user action is required. Return Pass to the planning parent for finalization and its next approved gate. This critique stops here without implementation or another critique pass.
