<!-- markdownlint-disable-file -->

# Task Research: issue-114-loadcheck-evidence

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher | RPI parent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md |

## Research Brief

* Research target: verify missing-observation and worker-failure false positives in the existing loadcheck harness at f91353169756dc41ebbcca944bdd3f44f7c04b89.
* Purpose and audience: trustworthy bounded offline evidence for issue #114 AC2; coordinator and PR reviewer.
* Scope: loadcheck, coupled core tests, component guides and configured checks.
* Non-goals: completing AC2 or issue #114, Azure measurement/cost, annual ledger verification, restore/deletion, deployment, IAM, billable AI, private inputs, web or concurrent #153 work.
* Criteria: invalid workload rejected before store initialization; absent required measurements and real worker failures cannot pass; good runs and existing latency limits remain intact.
* Requested outputs: evidence-backed recommendation preparing Plan.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1 false positives; Q2 minimal safe correction; Q3 deterministic offline validation and boundaries |
| Codebase scope | src/core plus directly relevant component guides/workflows |
| External scope | GitHub issue metadata only; no web research needed |
| Initial internal candidates | loadcheck.py, queue benchmark tests, core README/pyproject, workflow checks |
| Initial external candidates | None |
| Research posture | focused |
| Provenance | Bounded caller scope and named concrete source gaps |
| Explicit limits | One critique, one original Review; at most two post-Review source corrections |
| Completion basis | Covered scope and material claims; counter-evidence examined |
| Source edits allowed | No |
| Evidence root | .copilot-tracking/ |
| Excluded sources | Private datasets, .env, support, inherited Azure configuration in tests |

## Extension Registry and Provenance

| Kind | Candidate | Authority and disposition |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md, applyTo ** | Selected: repository safety, branch, evidence and component commands |
| Skill | rpi-research | Selected: ordered three-wave research and evidence IDs |
| Skill | Web/design/security skills | Skipped: no UI edits or security-audit request |
| Specialist | hve-core-all:rpi-researcher | Skipped: one tightly coupled source trace, handled inline |

## User Participation and Research Decisions

Explicit full-loop authorization and precise boundaries suffice; no intake question required.
Initial clean worktree and branch/base verified; no existing branch PR. Issue dependency is None; #113 is hierarchy, not ordering.

## Scope and Success Criteria

Verify all caller claims rather than trust supplied descriptions. Preserve list/detail/write workload,
limits 1/1/2 seconds and the passing all-observed path. Test failure accounting without exposing error
messages. Make no Azure or operational acceptance claim.

## Task Research Requests

Q1: Can empty evidence pass? Q2: Which failures escape accounting and which must remain distinct?
Q3: What validation is configured, and how can good/bad paths be deterministic and isolated?

## Direction Controls

Caller narrows source footprint to loadcheck.py and focused test_loadcheck.py; no new documentation
page, KB churn, mvp code, cloud action, issue checkbox/board writes, integration/rebase or merge.

## Research Questions

| ID | Type | Priority | Status |
| --- | --- | --- | --- |
| Q1 | depth | High | Answered, C1-C4 |
| Q2 | depth | High | Answered, C2/C5/C7 |
| Q3 | straightforward | High | Answered, C6/C8 |

## Prior Knowledge Gate

Original/addendum, KB index/memory and repository instructions read. Supplied failure claims are
starting hypotheses. No task-specific prior evidence reused as proof.

## Research Cycle Log

### Cycle 1

Focused posture, inline execution; no independent research lane warranted.

#### Wave 1: Wider

Read core README, pyproject, source CI, factory, PRD NFR-002 and both source ADRs.
The three existing workload classes are a subset of full PRD acceptance; preserve that boundary.
Reflection: no store/schema change needed. Source CI configures unittest, Ruff lint/format and mypy.

#### Wave 2: Deeper

Verified empty pct, no-sample within predicate, wall-clock loop and selection outside try.
Executed constructed Mock-store probes: seconds 0/-1, sessions 0 and expired workers all produce
errors=0, n=0, p95=0.0, within=True in every class and a passing exit predicate.
The actual initial interpreter failed with ModuleNotFoundError for zava_forward; installed
src/core[dev] using pip into the task-local session virtualenv, not global/shared environment.
Reflection: validate inputs before initialization, use monotonic deadlines and explicit absent
percentiles. Start failures and pre-request worker failures need separate sanitized categories;
successful observations must stay intact when a different worker fails.

#### Wave 3: Contrarian

Examined test_queue_benchmark.py: generated 60,000-case queue write/cold/repeat tests assert
bounded evaluations, not loadcheck evidence/CLI semantics. Its structural acceptance does not
repair this harness. Existing factory inherits explicit store choices; do not change that public
behavior, but clear environment entirely in all CLI tests and mock factory calls.
Reflection: reject broad store/runtime refactoring and blanket per-class failure. A worker error
must make the overall CLI nonpassing while accurately measured successful classes can stay within.
Keep p95 semantics rather than change max latency into a new acceptance threshold. Workers finish
an already-started list/detail/write cycle even when the deadline passes; preserve that behavior.

#### Parent Synthesis and Disposition

Accepted C1-C8: minimal two-file correction and offline tests. Rejected queue-benchmark-only changes
as wrong boundary; deferred full Azure load/cost and all other issue acceptance.
No additional cycle needed: in-scope claims verified, adjacent counter-evidence does not weaken
the correction; additional sources would not change the bounded recommendation.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Empty percentile returns 0.0; required classes have no observation guard | src/core/src/zava_forward/core/synthetic/loadcheck.py:36-72 | High, direct read |
| C2 | Case selection precedes request exception handler; wall-clock deadline shared | src/core/src/zava_forward/core/synthetic/loadcheck.py:41-65 | High, direct read |
| C3 | CLI accepts arbitrary integer duration, creates store before run | src/core/src/zava_forward/core/synthetic/loadcheck.py:75-99 | High, direct read |
| C4 | Original false greens reproduced for 0/-1 seconds, 0 sessions and expired workers | src/core/src/zava_forward/core/synthetic/loadcheck.py:36-72; task-local command 2026-10-18 | High, constructed offline probe |
| C5 | Store factory honors supplied env, otherwise ambient config; no harness lifecycle/schema fix needed | src/core/src/zava_forward/core/factory.py:9-25 | High |
| C6 | Queue benchmark covers a different predicate | src/core/tests/test_queue_benchmark.py:17-76 | High |
| C7 | Full PRD workload includes additional duration/classes/scale gates | docs/prds/zava-forward-retrofit-programme-demonstrator.md, Exercise acceptance contract, NFR-002 | High |
| C8 | Configured validation: unittest, Ruff, mypy; loadcheck migration exemptions remain | .github/workflows/src-ci.yml:77-95; src/core/pyproject.toml:20-75; src/core/README.md:135-145 | High |

## Findings Mapped to Questions and Evidence

Q1 answered by C1/C3/C4. Q2 answered by C2/C5/C7. Q3 answered by C6/C8.
All are local source/test facts, not Azure measurement or performance improvement.

## Alternatives and Decision State

Select input guards (ValueError for direct APIs, argparse error for CLI), explicit missing p95=None
and within=False, monotonic deadline, narrowly placed worker-boundary accounting with sanitized
exception type only, and deterministic tests of CLI plus real thread workers.
Reject treating missing observations as zero or inventing sample quotas/extra configuration.
No new generic abstraction or documentation page needed; existing core guide still accurately
describes the command and its local-only evidence boundary.

## Open Questions, Risks and Residual Uncertainty

No real Azure load/cost or operational acceptance can be established here.

## Planning Readiness

Ready. Research disposition: executed. Self-check: brief, all three ordered waves, code evidence,
counter-evidence, recommendation and non-goals recorded. No material unresolved planning blocker.
Continuation: authorized RPI parent advances to Plan; this research phase did not edit source.
