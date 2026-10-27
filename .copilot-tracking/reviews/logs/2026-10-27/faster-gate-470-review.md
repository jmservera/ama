---
title: Issue 470 independent post-implementation RPI Review
description: One bounded evidence-based review of the faster local gate implementation
ms.date: 2026-10-27
---

## Scope and Evidence

* Task: #470 / faster-gate-470; review date 2026-10-27.
* Assessment count: this is the one independent post-implementation RPI Review, not a critique or a repeated correction assessment.
* Committed implementation: da2969b894b1457c6648bc807312d9f414608c01.
* Reviewed main: 2fbb42f0ed80b84429fc7962eda1e04e3265e15e. The local origin/main ref still resolved to this SHA during review.
* Source boundary: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md and .github/agents/ama-backlog-delivery-coordinator.agent.md. All four were read completely; a diff against the implementation commit confirmed no later worktree changes in these files.
* Compared artifacts: .copilot-tracking/research/2026-10-27/faster-gate-470-research.md; .copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md; .copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md; .copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md; .copilot-tracking/changes/2026-10-27/faster-gate-470-changes.md; .copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-static.md.
* Read-only task evidence: /mnt/ama-rpi-gates/issue470-fast-da2969b8/receipt.json, its receipt.sha256 and receipt-listed files, and /mnt/ama-rpi-gates/issue470-fast-measurement.json.
* Repository context: original case study, addendum purpose/status, knowledge-base index and owner memory were read. They introduce no application, legal or Azure work into this tooling review.
* No source, plan, critique, details, changes, state or behavior-simulation artifact was corrected. No agent, full gate, Azure operation, commit, push or dependency installation was performed.

## Opening Review State

* Interpreted review goal: independently assess issue #470 implementation, once, against approved direction and evidence, without implementing corrections.
* Review scope: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md and .github/agents/ama-backlog-delivery-coordinator.agent.md at da2969b894b1457c6648bc807312d9f414608c01 versus origin/main 2fbb42f0.
* Evidence readiness: supplied research, plan, critique, details, changes and static agent assessment located; later worktree changes are evidence/state only. Existing unrelated evidence changes will not be modified.
* Acceptance basis: supplied task artifacts, fail-closed changed selection, bounded concurrency, immutable resume lineage, exact command/full receipt preservation and policy consistency.
* First comparison boundary: reconcile current artifacts, then inspect complete four-file source boundary and focused validation.
* Active read-only boundaries: only this review record may be written; no agents, full gate, Azure, commits, pushes or source/artifact corrections. External supplied measurement evidence is read only.
* Initial blockers: no initial review blocker. Independent behavior simulation and publication/final-head refresh are outside observed validation; owner prohibits full benchmark, which remains residual work.

## Execution Status

* Execution status: Complete.
* The supplied bounded review, artifact reconciliation, complete source comparison and read-only focused probes are complete. This does not mean implementation acceptance or P02 publication is complete.
* Outcome is separately recorded below as Not accepted because material implementation defects remain.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01: selection, scope, dependency closure | P01 completed; schema 4, NUL-delimited paths, full fallback | Partial conformance | Scope and general mapping implemented; direct SQL manifest dependency omitted, RV-001. |
| P01-T02: concurrency and resume | P01 completed; thread-local state, resource locks, immutable parents | Partial conformance | Core machinery exists; extra-api shared-state and nested-cgroup gaps, RV-002/RV-003. Resume design is substantively implemented. |
| P01-T03: tests and policy/docs | 27 focused cases, 13 new methods, source/policy updates | Reconciled with defects | Budget respected and prior mutation tests preserved. Coverage misses the three reproduced cases. |
| P02-T01: unit/focused checks and measured changed tier | Validation and P02 measured partial execution | Reconciled | Current checked marker is supported by supplied results and inspected measurement; it is not full-matrix performance or final-head acceptance. |
| P02-T02: Review, final evidence commit, exact-head refresh, PR | Remaining work | Open, accurately unchecked | This Review supplies the original assessment only. Behavior gate, final exact-head validation, independent assessment and publication remain with the parent. |
| Follow-Up Items | Unmeasured full performance and deferred cache/image reuse | Reconciled | Distinct residual work, not active implementation or completed acceptance. |

## Completed Work Assessment

| Scope | Files | Assessment and evidence |
| --- | --- | --- |
| Exact command/full receipt preservation | tools/rpi-checks.py | Independently constructed representative full receipts and compared trusted required_checks output with the original module loaded directly from git show 2fbb42f0:tools/rpi-checks.py. All 184 no-extra command contracts matched exactly, including argv, cwd, environment, timeout, suite/integration flags and probe/readiness attempts. This is stronger preservation evidence than fixtures generated solely from the new oracle, but is not a full execution. |
| Scope-aware verifier | tools/rpi-checks.py:379-420,813-921,2010-2123 | Recomputes paths/groups/scope, binds clean HEAD/tree/base/matrix/helper and tools, validates successful-group command order despite interleaving, and conditionally requires selected environments/browser/scanner/images/workflow evidence. Default verification rejects partial scope before live probes. Full changed fallback is genuinely full only when it equals the full trusted group list. Schema 3 is not promoted. No partial-as-full acceptance defect found. |
| Mapping and setup | tools/rpi-checks.py:323-404,1845-1903 | NUL-delimited no-rename Git diff includes old/deleted and new paths; empty changes still select static; unknown paths select the full matrix. Project consumers and namespace/API bootstrap are explicit. Source reader setup is serialized before scheduled suites. RV-001 prevents an unqualified dependency-closure claim. |
| Threaded state, dependency failures and resources | tools/rpi-checks.py:996-1243,1752-1843 | Thread-local group/process/last-entry, locked log reservation, isolated group caches and trusted dispatch preserve group state. Failed prerequisites block descendants; installers run before snapshot readers; namespace mutation chains precede images; SQL/images share a Docker lock. RV-002 identifies an omitted shared-venv consumer. |
| Cancellation and cleanup | tools/rpi-checks.py:1099-1197,1718-1750,1810-1843 | Cancellation event prevents later command starts, launched children check cancellation, tracked process groups receive TERM then bounded KILL escalation, and the executor context joins workers before run cleanup. Owned-container checks and dirty-snapshot refusal remain. This is structural inspection plus supplied/mock test coverage, not an observed multi-live-child signal exercise. No independent cancellation defect is asserted. |
| CPU/memory admission | tools/rpi-checks.py:422-452,2197-2220 | Jobs are positive, admission is inside the fixed host lock, and the nominal two-CPU/four-GiB-plus-headroom formula is conservative for the files it reads. Root-only cgroup lookup fails to establish effective capacity, RV-003. |
| Resume and receipt lineage | tools/rpi-checks.py:1845-2007,2010-2107,2172-2191 | Requires a new external directory, failed eligible parent, matching exact clean source/base/tool identity and recomputed selection. Parent hash and recursively verified successful-group evidence/environments/live images remain authoritative; depth is bounded. Successful selected groups are inherited, excluded from current trusted execution, and coverage is the union. Fresh setup groups recreate only necessary environments; failed/incomplete parent commands do not become successful coverage. Files/reports use the new attempt directory and new owned image tags. |
| No arbitrary argv replay | tools/rpi-checks.py:466-810,1752-1783,2010-2107 | Receipt argv is compared as inert data; no execution path dispatches it. Runtime uses fixed methods and validated tracked unittest selectors. Parent successes are checked in their original directories, not executed through receipt-adjacent Python. No replay or cross-commit reuse defect found. |
| Policy and documentation | src/README.md; .github/agents/ama-backlog-delivery-coordinator.agent.md | Full-risk categories take precedence; focused checks do not replace required checks or hosted CI. Parent/child stacks, main-bound runner base versus parent-bound child diff, exact-head refresh and image retention are consistently stated. Static agent report matches the committed delta and appropriately disclaims behavioral acceptance. No additional policy-source defect found within this delta. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and readiness | Assessment |
| --- | --- | --- | --- |
| P01 selection/verifier contracts | PC-001/PC-002 required concrete mappings and conditional evidence | Current plan, details and changes describe schema 4, focused tooling bootstrap and dependency closure; source reflects that direction | Compatible planner-owned refinement, no new owner decision. RV-001 exposes an incomplete edge, not authorization for broader scope. |
| P01 resume contract | PC-003 replaced in-place retry with immutable parent/new attempt and fresh setup | Plan, details, changes and README agree on unchanged identity, parent verification and no successful-suite rerun | Justified safety-preserving design update; current source implements it. |
| P01 scheduler/admission | PC-004/PC-005 specified setup/readers, shared resources and deterministic capacity formula | Plan/details/source agree on intended resource rules | Direction reconciled; implementation incomplete in RV-002/RV-003. |
| P02-T01 marker and validation prose | Later worktree evidence records broader tests and actual changed-tier measurement | Diff from da2969b8 changes the marker to complete and replaces pending prose with qualified results; no four-file source change | Evidence-only descriptive update preserves owner intent. Fresh planning/critique is not required for recording an authorized measured result. |
| P02-T02 and handoff | Review and behavior gate still pending in supplied changes; final evidence commit invalidates previous head | P02-T02 remains unchecked; this Review does not silently rewrite that state | Parent must reconcile the completed Review and routed defects later, preserving this original outcome. |

## Critique and Material Revision Assessment

* PC-001 through PC-006 have explicit dispositions in the current plan; the critique's original Revise verdict and six findings remain intact.
* PC-001 is partially resolved in implementation: concrete mapping/bootstrap exists, but RV-001 shows missing actual dependency closure.
* PC-002 is substantively resolved: conditional trusted commands, environment/result/image requirements and default full verification are present. The observed measured partial receipt has no fabricated SQL/image/browser evidence.
* PC-003 is substantively resolved in architecture and ordinary namespace/static fixture coverage: immutable failed parent, new attempt, successful-group verification, trusted fresh setup and bounded lineage are implemented. The broader adverse-case coverage requested by the critique is not all present; see test-quality limits below.
* PC-004 is partially resolved: staged installers, namespace/API chains and Docker exclusion are implemented; RV-002 shows extras were not included in the shared-API ownership contract.
* PC-005 is partially resolved: explicit capacity formula is implemented, but RV-003 demonstrates an invalid mounted-root-equals-effective-cgroup assumption.
* PC-006 is supported by the actual recorded preselection and four-group measurement. No full fallback was executed, and the benchmark restriction remains unchanged.
* No unaccepted significant design divergence or unjustified expansion was found. The documented revisions are compatible direct critique dispositions; the three defects fit the existing accepted direction and route to implementation, not a new planning decision or another Review.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Like-for-like parallel full benchmark | Explicit owner prohibition; the supplied 23-26 minute history is not a new after-full result | Parent retains the open issue criterion; owner may authorize a separate future measurement | RV-004, distinct follow-up, not a defect or a request to execute it now. |
| Shared pip cache and image reuse | Deliberately deferred to preserve freshness and avoid unrelated optimization | Maintainer may propose separately bounded future work | Remains optional distinct follow-up; no active task or acceptance claim added. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Changed selection omits the real SQL consumer of its driver manifest

* Related scope: P01-T01, P01-T03; PC-001 dependency closure.
* Evidence: tools/rpi-checks.py:335-376 maps src/api/requirements.txt to project-api, image-api and logo-0600 plus common setup/static, but not mssql. The trusted mssql matrix at tools/rpi-checks.py:668-675 directly installs that exact requirements file before SQL_DRIVER, and Runner.sql does the same at tools/rpi-checks.py:1548-1560. A read-only probe confirmed both the omitted group and the SQL command's manifest dependency.
* Impact: A SQL-driver dependency or hash update can receive a verified changed-tier receipt without executing its actual SQL driver/connectivity/contracts. Filename matching for store/schema/sql/assistants is not transitive input closure.
* Destination: rpi-implement.
* Smallest useful next action: Add explicit direct/transitive dependency-manifest edges, including this SQL dependency, and regression expectations that assert required consumers rather than preserve the omission. Reconcile the mapping documentation to the already accepted dependency-closure requirement.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Additional API suites can overlap mutations of their shared environment

* Related scope: P01-T02, P01-T03; PC-004 shared-state exclusion.
* Evidence: tools/rpi-checks.py:323-332 gives extra-api selectors only project-api as a prerequisite. tools/rpi-checks.py:1791-1806 chains project-api/browser/mssql but excludes extra-api consumers. Runner.browser writes the API environment's startup .pth file at tools/rpi-checks.py:1513-1517; Runner.sql installs into that same environment at tools/rpi-checks.py:1551-1553. A barrier-based, read-only scheduler probe with project-api already complete and jobs=2 observed browser and extra-api:test_fixture.Case.test_method active together.
* Impact: An explicitly requested suite may run while its interpreter/startup files or SQL dependencies are being changed. That invalidates the claimed independence and permits nondeterministic test evidence; the Docker lock does not protect extra-api.
* Destination: rpi-implement.
* Smallest useful next action: Include every shared-API consumer, including extra selectors, in dependency/resource admission. Add deterministic overlap-denial tests for browser/SQL writers versus extra-api readers, including resumed setup.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Worker admission ignores the process's actual nested cgroup limits

* Related scope: P01-T02, P01-T03; PC-005 CPU/memory admission.
* Evidence: tools/rpi-checks.py:422-452 reads only /sys/fs/cgroup/cpu.max and memory.max/current at the mounted root, without resolving /proc/self/cgroup or walking applicable ancestors. In a read-only mocked cgroup-v2 hierarchy, root was unlimited with 16 affinity CPUs and ample host memory, while the current /limited group had two CPUs and only four GiB available. worker_limit(8) returned 8 rather than blocking for the required one-GiB headroom. It never read the process membership or nested files. This host also reports non-root process membership, although no actual host overcommit is claimed.
* Impact: On ordinary non-cgroup-namespaced systemd/service hierarchies, parallel work can exceed the controlling CPU/memory limits despite apparently successful conservative admission and the host-wide lock. A tighter ancestor can likewise be missed. The fixed lock serializes gates, not resource capacity.
* Destination: rpi-implement.
* Smallest useful next action: Resolve the effective process cgroup/mount and limiting ancestors, conservatively intersect CPU and available-memory constraints, and fail closed for unsupported/unresolvable capacity. Add nested and ancestor-limited tests, not only mounted-root fixtures.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Full before/after performance acceptance remains residual, not completed

* Related scope: P02-T01 and plan Follow-Up Items.
* Evidence: current plan, details and changes expressly prohibit a full benchmark. The supplied measurement is a 62.668-second changed tooling tier, with 28 commands and two effective workers, versus a historical 17-run full baseline of 23-26 minutes and representative 1547-second command sum.
* Impact: This is not a like-for-like full improvement result and cannot complete the issue's full-before/after performance criterion or justify issue closure.
* Destination: distinct follow-up, not rpi-implement or active plan scope.
* Smallest useful next action: Parent leaves the criterion open, uses Refs #470 only in the PR and records full parallel timing as unmeasured. Any future full benchmark needs separate owner authorization.

## Defects

* RV-001, RV-002 and RV-003 are implementation defects. Their smallest compatible corrections and regression tests belong to a later rpi-implement invocation.
* The original plan's completed P01 markers describe execution, not defect-free acceptance. Review does not edit those markers or erase original outcomes.

## Test Quality Assessment

* The 13 added test methods are within the plan's maximum 18; all 27 focused methods remain. Existing rejection tests still remove each trusted full command and mutate selectors, suite counts/logs, scan/browser/workflow outputs, tool/environment identities and dirty inputs.
* New tests meaningfully exercise rename/deletion and unusual NUL-separated paths, explicit partial opt-in, interleaved commands with within-group order, true barrier-based independent overlap, unique logs/thread-local groups, dependent failure propagation and Docker exclusion.
* The mapping fixture at tools/test_rpi_checks.py:688-756 explicitly expects no SQL for src/api/requirements.txt; it therefore codifies RV-001 instead of detecting it.
* The shared-environment scheduler test at tools/test_rpi_checks.py:1073-1096 covers only the named namespace/API chains; no extra-api reader is included. RV-002 passes the current suite.
* The resource test at tools/test_rpi_checks.py:912-942 assumes root-mounted limits. It covers finite/unlimited roots, fractional CPU insufficiency, memory insufficiency and nonpositive jobs, but not nested membership, tighter ancestors, mount resolution or absent/malformed-limit variants. RV-003 passes these fixtures.
* Resume fixtures at tools/test_rpi_checks.py:964-1071 demonstrate namespace/static successful-group reuse, unchanged parent bytes, final parent-hash binding and rejection of parent tampering/tool/environment/head drift. They do not independently exercise repeated failed lineage, live-image invalidation, successful API followed by failed browser/SQL mutation, or namespace followed by failed infra/migration mutation. Generic full-verifier mutation coverage is useful but not equivalent to executing those resume transitions.
* Cancellation tests establish mock interruption cleanup and the cancellation flag; the threaded scheduler test raises KeyboardInterrupt before a real child is active. Actual concurrent child termination/join-before-cleanup is not freshly observed. No full matrix or prohibited benchmark is requested to improve these focused fixtures.
* Many successful receipt fixtures are generated by required_checks itself, so a weakened oracle can escape them. The review's independent comparison to all 184 original no-extra contracts mitigates that uncertainty for this candidate; it is not a newly added persistent regression test.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent routes SQL manifest closure and regression expectations | Implementation omits a direct input consumer under the accepted mapping requirement. |
| RV-002 | rpi-implement | Parent routes shared-API extras scheduling and deterministic exclusion tests | Shared environment mutation can overlap a selected test reader. |
| RV-003 | rpi-implement | Parent routes effective cgroup/ancestor admission and focused tests | Existing admission can substantially overcommit actual capacity. |
| RV-004 | Distinct future follow-up | Parent retains open criterion; owner decides any later full benchmark | Explicitly deferred performance evidence, not a source defect. |

Later implementation of routed defects does not require this Review to run again. Preserve this complete original finding set and route outcomes separately.

## Residual Work

* RV-004 remains outside active scope; after-full timing is Not run, intentionally, and the PR must use Refs #470 only.
* Shared pip cache and image reuse remain deferred, with freshness requirements unchanged.
* Independent agent-policy behavior simulation is in progress elsewhere. Its logs were not read or awaited; this Review assesses source/static evidence only and does not declare that gate passed.
* Publication, hosted CI, owner merge and final exact-head independent assessment are distinct later gates. No local/static result satisfies them.

## Blockers and Remaining Work

* Acceptance blockers: RV-001 through RV-003. No unresolved owner design choice prevents routing their compatible fixes.
* P02-T02 remains active with the parent: disposition the preserved Review, finish the independent behavior gate, commit the final source/evidence candidate, fetch current main, run the authorized fresh partial tier only after confirming selection is partial, and verify the external receipt against the final exact HEAD/base before independent exact-head assessment and push.
* The supplied da2969b8 measurement cannot authorize publication of a later evidence-only commit. A later source correction likewise invalidates that head-bound evidence. If trusted changed selection becomes full, stop rather than execute the owner-prohibited full gate.
* No behavior-simulation conclusion, final-head receipt, push, PR or hosted-check result is claimed here.

## Validation Evidence

| Command or assessment | Scope | Status | Evidence and limit |
| --- | --- | --- | --- |
| git status --short; git branch --show-current; git diff --exit-code da2969b8 -- four source files; git rev-parse origin/main | Source identity and worktree boundary | Passed, observed | Topic feat/faster-gate-470; existing later changes are evidence/state only; scoped source unchanged; main still 2fbb42f0. |
| Read-only Python heredoc loading current runner and git show 2fbb42f0:tools/rpi-checks.py; assert before == after for required_checks | Full trusted command preservation | Passed, observed | All 184 no-extra contracts identical; no full runner, setup, subprocess test suite or Docker execution. sys.dont_write_bytecode=True and PYTHONDONTWRITEBYTECODE=1. |
| Read-only Python barrier probe of Runner.schedule with browser/mssql/extra-api | Shared-API resource ownership | Failed intended invariant, observed | Browser and extra-api overlapped with two workers, RV-002. In-memory runner and mocked dispatch created no files/children. |
| Read-only changed_groups and trusted mssql required_checks assertions | Direct SQL manifest closure | Failed intended invariant, observed | API requirements selected images/project but omitted its real SQL consumer, RV-001. |
| Read-only worker_limit probe with mocked process membership and nested limits | Effective CPU/memory admission | Failed intended invariant, observed | Eight workers admitted although current nested group could not fit one reservation plus headroom, RV-003. No actual heavy work was started. |
| Read-only digest of receipt/sidecar and each receipt-listed file; verify_commands and verify_results on external supplied receipt | Measured partial evidence | Passed, observed bounded checks | All 29 receipt-listed file hashes and 28 exact commands/results matched; matrix hash matched committed runner. This did not invoke full validate_receipt, clean/live/tool/environment validation or establish current-head publication readiness. |
| cd tools && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q test_rpi_checks | Focused gate suite | Passed, supplied | 27 tests reported. Not rerun by this Review; no test scratch or cache was created. |
| cd tools && PYTHONDONTWRITEBYTECODE=1 external-python -m unittest -q | Tools discovery | Passed, supplied | 123 cases after external installation of missing application distributions and pytest. Unittest discovery is not claimed to run pytest-style function tests. |
| Pinned Ruff 0.17.1 lint/format and mypy 2.4.0 strict | Runner and gate tests | Passed, supplied | Recorded in changes and supported by measured tooling command logs; no fresh linter installation or rerun here. |
| --changed --jobs 3 on clean da2969b8 checkout, base 2fbb42f0 | Real four-group tooling tier | Passed, supplied run; evidence inspected | 62.668 seconds, exit 0, effective jobs=2, preflight/namespace/static/tooling; receipt explicitly partial and runner verification recorded. Not a real concurrency benchmark: namespace setup and static/tooling ordering largely serialize this tier. |
| Fresh complete receipt verification in this checkout | Final publication identity | Not run | Evidence/state changes make the checkout dirty; final evidence commit and refreshed partial run/verification belong to the parent. |
| Independent agent behavior simulation | Policy runtime behavior | Unavailable to this Review | Separate worker in progress; deliberately neither awaited nor read. Static report is not behavior acceptance. |
| Full matrix / after-full benchmark / Azure | Heavy or cloud validation | Skipped | Explicit owner prohibition. Historical full timing remains supplied context, not independently remeasured or like-for-like after evidence. |

## Outcome

* Outcome: Not accepted.
* Rationale: The four-file implementation is substantial and preserves full command identity, scope separation and trusted immutable resume direction, but three reproduced functional defects invalidate an unqualified fail-closed/dependency/resource-safety acceptance claim.
* Severity summary: Critical 0; High 3; Medium 0; Low 1. RV-004 is non-blocking residual work; RV-001 through RV-003 are blocking defects.
* Review execution is Complete for the supplied boundary. Policy behavior simulation and publication/final-head evidence are explicitly outside observed validation, not silently passed and not reasons to rerun this Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent routes RV-001/RV-002/RV-003 and focused regression coverage; preserve this original assessment. |
| Decision gap or invalid assumption needing a changed direction | None | Correct resource/input assumptions within the already accepted direction; no new owner choice or rpi-plan invocation is required by this Review. |
| Material evidence gap needing new research | None | Unobserved simulation/publication checks already have an assigned later gate; no rpi-research phase is invented. |
| Non-blocking residual work | Distinct future follow-up | RV-004: owner-authorized full benchmark only later; maintain open criterion and Refs #470. Optional cache/image reuse stays deferred. |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: complete bounded source/artifact comparison, unchanged 184-command full contract, inspected partial measurement and evidence hashes, three read-only reproductions; supplied unit/lint/type results distinguished from fresh observation.
* Blockers: three implementation defects; separate behavior gate and final-head/publication evidence remain pending with the parent.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/faster-gate-470-research.md](.copilot-tracking/research/2026-10-27/faster-gate-470-research.md) | Research boundary |
| [.copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md](.copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md) | Current plan |
| [.copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md](.copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md) | Original critique |
| [.copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md](.copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md) | Current contracts |
| [.copilot-tracking/changes/2026-10-27/faster-gate-470-changes.md](.copilot-tracking/changes/2026-10-27/faster-gate-470-changes.md) | Execution evidence |
| [.copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-static.md](.copilot-tracking/reviews/2026-10-27/faster-gate-470-agent-static.md) | Static policy assessment |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Reviewed runner |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Reviewed tests |
| [src/README.md](src/README.md) | Reviewed gate documentation |
| [.github/agents/ama-backlog-delivery-coordinator.agent.md](.github/agents/ama-backlog-delivery-coordinator.agent.md) | Reviewed coordinator policy |
| [.copilot-tracking/reviews/logs/2026-10-27/faster-gate-470-review.md](.copilot-tracking/reviews/logs/2026-10-27/faster-gate-470-review.md) | This one Review |

## Next Steps

Return this complete finding set to the active parent for later rpi-implement routing of RV-001 through RV-003, without a correction-review loop. Keep RV-004 as separate owner-controlled follow-up. The parent owns behavior-gate completion, final candidate/evidence reconciliation, a new authorized partial gate and immediate final-head receipt verification before any permitted push. This review task stops here; no user action is required to complete the review.
