---
title: "Original independent RPI Review: issue 108 evaluation runs"
description: "One original post-implementation review of the exact issue 108 delivery boundary."
ms.date: 2026-10-18
---

## Opening Review State

* Interpreted review goal: independently assess bounded repeated-priority-run evidence and accounting, preserving final-only quality and all-repetition safety gates without expanding evaluation policy.
* Review scope: complete 22-file base-to-candidate boundary, issue acceptance, research, plan/details, original adverse critique/disposition, source and consumer contracts, tests, README, raw evidence and current state.
* Evidence readiness: branch fix/evaluation-run-accounting-108 and candidate HEAD a39ebe9755d07df23730ee81256c0c792fc0ff51 confirmed; parent state JSON is the sole pre-existing uncommitted change. Artifact comparison has not begun.
* Acceptance basis: supplied issue 108 objective and repository requirements, reconciled against the committed task artifacts and raw validation.
* First comparison boundary: 69091f4149f2fd217fc33a8c965ebcb6d5064956 to a39ebe9755d07df23730ee81256c0c792fc0ff51, all changed files and necessary upstream contracts.
* Active read-only boundaries: only this review record may be durably written; no source, research, plan, details, changes, critique, state, commits, remotes, nested agents or second Review. Optional tests are offline, sanitized and confined to the named review scratch directory.
* Initial blockers: none identified; evidence completeness and outcome remain unassessed.

## Scope and Evidence

* Task: issue #108, bounded repeated-priority-run evidence/accounting delivery.
* Review date: 2026-10-18.
* Review count: exactly one original independent post-implementation RPI Review. This reviewer did not author the implementation, research, plan or critique. No nested reviewer or other agent was used.
* Exact base: 69091f4149f2fd217fc33a8c965ebcb6d5064956.
* Exact committed candidate and verified HEAD: a39ebe9755d07df23730ee81256c0c792fc0ff51.
* Branch: fix/evaluation-run-accounting-108.
* Complete comparison: all 22 base-to-candidate changed files, not just production changed lines. The artifact table below enumerates all 22, followed by additional relevant contracts. The production harness patch is 18 insertions/four deletions, a 22-line diff; the other source-tree changes are seven focused test methods, one API assertion block and 30 README lines.
* Acceptance basis: the supplied objective/constraints; current plan Functional Requirements and Acceptance Criteria; research C1-C7; PRD model-evaluation, RAI, real-inference and platform boundaries. No online issue, PR or branch state was fetched. Current remote issue text/lifecycle is not independently attested by this offline review.
* Necessary upstream trace: Store.ai_priority -> Ai.run -> Store._rec_view; Store.resolve_priority authority and recorded disposition; manager-only GET /api/ai/report pass-through; all retained focused/API negative controls; configured quality exclusions and CI commands.
* Current-state boundary: committed state still says Implement; the parent's sole pre-existing working-tree change changes active_phase to Review, supplies this record's path and pins the candidate in next_action. The state diff does not alter source or acceptance. That transition is consistent with this Review and is not a source mismatch.
* All source changes, research, plan, details, changes, original critique and raw evidence remained read-only. The only durable reviewer write is this file. Named review scratch was removed after each independent execution.

## Execution Status

* Execution status: Complete.
* Evidence: full supplied boundary compared; requirements, completion markers, disposition, logs and consumer contracts reconciled; independent focused/agents/API/quality checks and exact-base negative controls executed offline.
* This describes Review execution, not completion of the parent's entire P03 or whole-issue acceptance. P03-T02 deliberately includes this Review and later publication.

## Plan-to-Change Reconciliation

| Current scope | Changes-record evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01 / P01-T01 checked | Completed Work: Behavioral red baseline | Reconciled | Exactly seven new focused methods; original six retained. Raw red has 13 methods, two failures/six errors, including both mixed-order subtests. Independently reproduced against exact-base harness in memory. |
| P02 / P02-T01 checked | Completed Work: Canonical run evidence | Reconciled | Ordered returned metadata and both latencies drive accounting; final-quality selection and all existing gate code preserved. |
| P02-T02 checked | Direct contract and README | Reconciled | API implementation unchanged; one existing manager-only test gains reconciliation assertions. README documents correction, additive fields and exclusions. |
| P03-T01 checked | Validation Record and Pre-Review Reconciliation | Reconciled | Focused 13, agents 105, API 33 and configured agents checks independently corroborated. Failed explicit API formatting and inherited exclusions are not hidden. |
| P03 / P03-T02 unchecked | Execution Status, Blockers and Remaining Work | Reconciled | Correct before Review/publication. No unfinished implementation is inferred from this future gate. No future PR is falsely required as pre-Review evidence. |
| Plan Follow-Up Items | Changes Follow-Up Items | Reconciled | Coordinator exact-head judgment/integration authority and actual-evaluation prerequisites remain distinct, outside this source delivery. |

## Completed Work Assessment

| Requirement or marker | Concrete evidence | Impact and assessment |
| --- | --- | --- |
| Per-returned-run identity, P02-T01 | src/agents/src/zava_forward/agents/ai_eval.py:213-222 copies run ordinal, returned id/source/model/prompt, measured harness latency and returned latency from recs/latencies. Store._rec_view returns a distinct view and resolve_priority does not rewrite these identity fields. | No reconstruction from the final model, no fabricated model version, no ID loss across five outputs. Unknown model remains null in the record. Conformant. |
| Correct run denominators | ai_eval.py:298-337 flattens run_results; counts actual source equality, not successful provider dispatches or final-source scenarios. | Existing report reconciles 14 recommendations = eight AI-sourced + six template/fallback. Workflow comparator and text-task outputs are excluded. Conformant for the actual two-source Store/Ai contract. No requirement for a new arbitrary-source schema is inferred. |
| Distinct scenario denominators | priority_scenarios counts measured priority records; ai_scenarios/template_scenarios use any matching run per scenario. | Full fixture: ten priority scenarios, four AI-containing and six template-containing; mixed tests demonstrate overlapping membership (one scenario counted in both). Top-level eleven still includes text-task checks. Conformant. |
| Aggregate model/prompt evidence | ai_eval.py:336-337 takes known identities from every row; focused five-output wrapper mutates each returned identity and latency independently. Mixed tests put null on fallback, including when fallback is last. | Earlier known identities survive an unknown final model. Deployment labels on validation fallback remain evidence, not AI success or serving attestation. Conformant. |
| Both mixed orders and template-only | test_ai_eval.py:76-119 exercises valid/fallback and fallback/valid with real Store/Ai parsing; repeated template scenario has three null-model rows. | Each mixed order yields two runs, one AI and one template, one scenario and one reviewer action. Template-only is three template runs, no invented model. Conformant. |
| Existing five-output case | test_ai_eval.py:35-74 checks five distinct IDs, ordinals, exact returned metadata, both latency meanings, identity sets, five AI runs and one edit. | Detects the original five-to-one collapse without a new fixture or dataset. Conformant. |
| Real scripted review-action denominator and identity | ai_eval.py:180-197 performs the actual successful final resolve_priority call after authority/reason negative checks; :220-221 binds OWNER email and final ID. Store.resolve_priority verifies ownership and writes resolved_by/audit. | Ten actual successful scripted priority actions: eight accept, one edit, one reject, not 14 repetitions and not human participants. Refused probes, workflow comparator and separate text-task review are excluded. Conformant. |
| Final-only quality | ai_eval.py:139,209-215,300,311-322,340-344; summary.quality_scope; README Priority repetition accounting; final-only test compares repeated case with its final single output. | Legacy overlap/Spearman/recall and AI-final recall eligibility remain unchanged. Summary scope is explicit, not an all-run quality average. Conformant. |
| Critical/citation/invariant gates | Entire _run gate block inspected, not just diff; per-repetition checks at :143-165 remain unchanged. Ranking/state snapshots, approval/authority/refused-answer/audit/workflow checks remain unchanged. Early critical and citation negative controls still fail despite a later valid output; retained mutation/authority controls pass. | Critical/citation and returned-record invariants retain all-repetition scope. Ranking/state snapshots retain their existing block/final-review boundaries, not new per-call transient-state monitoring. No threshold or policy change. Conformant. |
| Consumer compatibility and claims | src/api/src/zava_forward/api/server.py:451-458 passes run_eval through; test_ai_tasks.py:254-273 checks authorization and returned totals; README :294-323 distinguishes sources, scenarios, quality and claim limits. | No API schema mapper, browser, core runtime, registry, golden data or policy changed. Existing summary reviewer counts/reasons, latency arrays and variation retained. Conformant. |
| Protected boundaries | Exact-base-to-candidate git diff --exit-code for docs, src/core, src/agents/evals and .github/workflows; source hashes match changes record. | No new quality framework/task/dataset, private input, actual inference or upstream control change. Conformant. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Trigger and decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| Non-Functional Requirements; details P03-T01 | Added explicit pre-created project-local TMPDIR, resolution verification and cleanup for subsequent isolated application commands. | PC-001 direct planner disposition; execution hardening, not a source/design decision. | Research baseline retained as historical default-temp execution; red log verifies subsequent task-local root. Plan, details, changes and current state agree. No material scope revision or new critique required. |
| P01/P02/P03-T01 completion markers | Changed to completed after red/green, source and local validation. | Actual raw evidence and minimal implementation. | Matches committed source/tests, recorded counts and independent runs. No premature P03 completion. |
| API formatter validation | Explicit file formatter failed because it bypasses legacy configured exclusion. Added assertion block formatted; configured force-exclude honestly skips the file. | Original api-quality failure, untouched-base failure and final API rerun. | Failure remains adverse evidence; no unrelated legacy reformat. Independent exact-indentation block check passes. This is a justified validation-recipe divergence, not a new quality policy or concealed pass. RV-001 records inherited coverage. |
| Current phase/state | Parent changes Implement to Review after source commit. | Candidate a39ebe9755d07df23730ee81256c0c792fc0ff51 and user-supplied review boundary. | Source still exactly candidate. Review/publication remains P03-T02, not an unfinished source task. |

No significant or divergent implementation decision altered confirmed user intent,
thresholds, scoring, task eligibility, datasets or acceptance. No user decision
was bypassed and no dependent source work resumed across an unresolved material
planning gap.

## Critique and Material Revision Assessment

* Exactly one original critique is present and retained. Its original execution is Complete, verdict Revise, finding PC-001 Medium.
* Independently verified original critique SHA-256: b6117e40523ce84c5c163d913263224abda62b8d40530e09fd6de4f5b33f1397.
* Direct disposition is explicit in plan Critique Disposition, details P03-T01 and changes Implementation-Time Plan and Detail Updates. Subsequent red evidence prints the exact resolved project-local TMPDIR.
* The critique's asserted universal external-temp prohibition is not established by its recorded caller/repository evidence. The planner documents that qualification without deleting the adverse finding or rewriting historical baseline execution. Useful explicit TMPDIR isolation is adopted. This review independently obeyed its own supplied stricter scratch constraint.
* Research and baseline hashes still match critique inputs: research 39905b6e9ee58611cedb9749d6e9a3ee8be2dff4b6adb9a0f182a06a29006bca; baseline c6937e4e8a973cd729bdb0f618300ae743584028ceb02f75074f4c22ab921a50.
* Changed plan/details fingerprints relative to the critique are explained by direct disposition and implementation-status reconciliation. There is no unreviewed material design change requiring another critique.
* No second critique, original Review, correction pass or closure pass was performed.

## Plan Follow-Up Assessment

| Existing follow-up | Why outside immediate source scope | Owner or next action | Assessment |
| --- | --- | --- | --- |
| Complete exact-final-head review and integration authority | This original Review assesses the pinned pre-publication source/artifact candidate, not an unknown future publication head. | Coordinator after parent publication; authorize any integration separately. | Correctly open. Not a source defect or demand that a PR already exist. |
| Actual-model, held-out, human and Finance evidence | Constructed accounting cannot establish labels/thresholds, human effectiveness, calibrated value, actual serving IDs/usage/version or cost. | Authorized future exercise owners: Product/Data, human reviewers and Finance, under finite authority. | Unmet and explicitly disclosed. No new active task, acceptance checkbox or finding demanding scope expansion. |
| Regional/version/quota, privacy/consent and real-platform gates | No cloud, actual inference, private records or operational activation authorized here. | Existing exercise/platform, Legal/DPO and accountable release owners. | CON-009/AC-057, privacy/consent and release prerequisites remain unmet. Offline passes are not substitutes. |

## Findings

This is the complete RV set for the supplied boundary. Severity totals:
Critical 0; High 0; Medium 0; Low 1. Newly introduced implementation defects: 0.
The Low entry records an inherited, explicitly disclosed checking residual,
not a failed source requirement or mandatory expansion of issue #108.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Configured quality passes retain inherited coverage exclusions

* Classification: non-blocking inherited validation residual, not an introduced implementation defect.
* Related scope: P03-T01; plan Non-Functional Requirements and Test Ownership.
* Evidence: src/agents/pyproject.toml exempts ai_eval.py and test_ai_eval.py from formatting and ignores their mypy errors, with inherited broad per-file lint ignores. src/api/pyproject.toml excludes test_ai_tasks.py from formatting. Raw quality.log passes 19 formatted files/23 mypy files; api-quality.log retains the explicit formatter failure. api-format-baseline.log and independent base/candidate controls both fail the same explicit file-format route. The actual new API block passes at its original indentation; force-exclude skips the legacy file and provides no file-format coverage.
* Impact: Green configured quality results are not strict whole-harness/test formatting or typing evidence. Treating them as such at publication would overstate assurance; inherited code-wide format/type debt remains. The changed accounting behavior is covered by independent executable tests and source review, and this limitation is already honestly disclosed.
* Destination: distinct existing migration-quality follow-up associated with #199/ADR 0006, not rpi-implement, rpi-plan or rpi-research for this bounded delivery.
* Owner and smallest useful next action: parent preserves the exclusion/failure caveat in publication; existing migration-quality owner may address exemptions in separately authorized work. No new issue/task was created and no broad reformat or stricter quality policy is required here.
* Acceptance effect: non-blocking. Do not relabel explicit failure as a formatter pass or configured skip as coverage.

## Defects and Routed Findings

* No newly introduced correctness, source-contract, approval-boundary, plan-decision or material research/evidence defect found.
* No later rpi-implement, rpi-plan or rpi-research invocation is required by this Review.

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 Low | Existing distinct migration-quality follow-up; parent disclosure now | Preserve limited-coverage caveat; any exemption removal needs separately authorized migration-quality work. | Inherited static-check residual, not an unimplemented accounting requirement. |

Later implementation, if separately authorized, does not require another original Review.

## Validation Evidence: Original Raw Delivery

All raw changed evidence files were inspected, including complete red tracebacks,
the API formatter failure and its base control. The JSON was parsed in full and
every priority record/row reconciled rather than inferred from summary counts.
Log paths below share prefix
.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-.

| Raw evidence | Status | Exact material result and limit |
| --- | --- | --- |
| baseline.log | Historical reproduction | Six original focused tests reported passed; initial missing-package/install narrative; five AI outputs reported as one, mixed orders zero versus one, full summary four rather than eight AI runs. This short historical log is not a complete installation transcript or verified task-local-temp execution. |
| red.log | Expected failure | 13 tests, two failures/six errors, exit 1. Missing run_results/quality_scope and (2,1) versus (2,2) counts; explicit env -i and resolved task-local TMPDIR retained. |
| focused.log | Passed | 13 tests in 0.393s, exit 0. |
| agents.log | Passed | 105 tests in 18.210s, exit 0. |
| api.log | Passed | 33 tests in 6.264s, exit 0. |
| quality.log | Passed with exclusions | Ruff pass; formatter 19 files; mypy 23 source files; exit 0. RV-001 applies. |
| api-quality.log | Failed honestly | Lint pass then explicit formatter exit 1, including legacy formatting and the then-unformatted assertion block. This is intermediate evidence, not the final source block. |
| api-format-baseline.log | Expected inherited failure | Exact untouched base piped to explicit formatter; BASELINE_EXIT_CODE=1. No formatter stdout is present in that original receipt. |
| api-final.log | Passed / skipped accurately | Lint pass; configured force-exclude skips formatting; 33 tests in 5.355s, exit 0 after new block formatting. No whole-file formatting pass claimed. |
| offline-report.json | Passed, scripted | Eleven results; ten priority scenarios; 14 priority rows = eight AI/six template; ten final-review bindings; all relevant records and identity/latency arrays reconcile. |
| console.log | Passed, scripted | Explicit priority run/scenario counts, not provider calls; claim and open-gate disclosures present. |
| reconciliation.log | Passed assertions | Exact denominators/sets/reviews; baseline quality unchanged; actual-model/human not evaluated, benefit not permitted; report hash retained. |

## Independent Command Evidence

No dependencies were installed or restored by this reviewer. All test/application
processes used the supplied installed venv, an empty inherited environment,
constructed fixtures/scripted adapters and this explicit recipe:

```bash
V=/home/azureuser/.copilot/session-state/c9d20e32-acb0-442b-b8a6-6ed95534cb8b/files/eval-venv
H=/home/azureuser/.copilot/session-state/c9d20e32-acb0-442b-b8a6-6ed95534cb8b/files
T=/home/azureuser/source/ama-wt/issue-108-runs/.copilot-tracking/.issue-108-review-tmp
env -i PATH="$V/bin:/usr/bin:/bin" HOME="$H" TMPDIR="$T" \
  PYTHONDONTWRITEBYTECODE=1 python -B ...
```

Each execution first created only the named scratch root, asserted
tempfile.gettempdir() equalled its absolute path, and removed that root on exit.
Python bytecode writes were disabled; Ruff used --no-cache and mypy's cache was
inside that scratch root. Imported ai_eval.__file__ was asserted to be the exact
candidate worktree path. No inherited endpoints, credentials or ZF_DATA entered
the application environment. Component test helper PYTHONPATH values were
absolute, with agents/tests before core/tests for agents discovery and
core/tests before agents/tests for the API selection.

| Independent command or comparison | Result | Observed evidence |
| --- | --- | --- |
| Root: python -B -m unittest discover -s src/agents/tests -p test_ai_eval.py -q | Passed | 13 tests in 0.397s, exit 0. |
| src/agents: python -B -m unittest discover -s tests -q, corrected fixture order | Passed | 105 tests in 17.543s, exit 0. |
| src/api: python -B -m unittest discover -s tests -p test_ai_tasks.py -q | Passed | 33 tests in 5.129s, exit 0; JSON/SQLite, loopback HTTP, manager restriction and retained negative controls. No service SQL. |
| src/agents: ruff check --no-cache . | Passed | All checks passed, exit 0, configured ignores apply. |
| src/agents: ruff format --no-cache --check . | Passed with exclusions | 19 files already formatted, exit 0. |
| src/agents: mypy --cache-dir "$T/mypy" | Passed with exclusions | No issues in 23 source files, exit 0. |
| src/api: ruff check --no-cache tests/test_ai_tasks.py | Passed | Exit 0 with existing per-file ignores. |
| src/api: ruff format --no-cache --check --force-exclude tests/test_ai_tasks.py | Skipped by configuration | Exit 0, no formatting coverage claimed. |
| In-memory ai_eval.run_eval(), plus complete committed JSON parse/assertions | Passed | Both eleven/ten/14/eight/six/ten; every row ordinal, ID uniqueness, both latency arrays, identity sets and final reviewer binding checked; final-quality, variation, reviewer reasons and evidence blocks match. Fresh IDs/latencies are intentionally not byte-equal. |
| Exact-base harness loaded from git show into an in-memory module; current AiEvalTests temporarily bound to it | Expected failure independently reproduced | 13 methods, two failures/six errors. Five missing run_results cases including both mixed subtests, missing quality_scope, and the two source-count mismatches. No source file was swapped or written. |
| src/api: exact-base and candidate whole-file content supplied to ruff format --no-cache --check --stdin-filename tests/test_ai_tasks.py - | Failed as expected | Both return 1; both stdout/stderr empty in these stdin checks. Matches inherited base failure; not a candidate-only formatting regression. |
| Same formatter, only new API block enclosed in a class/method at its actual eight-space indentation | Passed | Exit 0, no output. New block is formatted. |
| git diff --check BASE CANDIDATE | Passed | No whitespace errors across all 22 committed files. |
| git diff --exit-code BASE CANDIDATE -- docs src/core src/agents/evals .github/workflows | Passed | Protected contracts, datasets, KB and workflows byte-identical. |
| Source fingerprints, current source diff and scratch cleanup | Passed | Four source-tree hashes match changes record; golden unchanged; no working-tree source changes; named scratch absent. |

### Independent execution failures and corrections

The following reviewer command-construction failures are retained explicitly;
they are not disguised source failures or omitted adverse commands:

* First combined validation used core/tests before agents/tests for agents discovery. Focused 13 passed, then discovery exited 1 with ImportError: test_dependency_rule imported from core/tests instead of agents/tests. The batch stopped before API/quality/JSON. Using the documented component-specific order produced the 105/33 and quality passes above. No source correction was made.
* A supplemental exact-base-red/formatter script completed and asserted the expected 13/two/six red result, then its output summarizer raised IndexError by indexing the last line of empty formatter output. The next script recorded empty stdout/stderr and both actual formatter return codes correctly.
* That follow-on script de-indented the new block before checking it, changing formatter line-width context and producing an exit-1 assertion. A final control preserved the actual class/method indentation and passed. The de-indented fragment is not the candidate file; no candidate formatting failure is inferred from it.

All named scratch roots were removed even on these nonzero exits. No source,
evidence log or parent-state repair was attempted.

### Independent report observations

* Committed JSON latency: mean 2.111ms, maximum 3.11ms; fresh in-memory report: mean 1.326ms, maximum 1.86ms. These are constructed offline harness wall times, not provider-call performance or real model latency measurements.
* Both reports: overlap 0.9; Spearman 0.722; zero critical misses; 74/74 cited facts; recall differences 0.25 on two eligible final-AI scenarios; five-output variation three distinct orders, pairwise overlap 0.867 and Spearman 0.0.
* The scripted model label is capable, the returned prompt identity is 15ed5b165b2074a1, and the top-level prompt release label is 2026-10-09.1. These are distinct existing identity concepts, not serving-version attestation.
* Evidence still says actual-model and human effectiveness not evaluated, calibration not applicable, benefit not permitted, with all five open items retained.

## Fingerprints

| Evidence | Independently verified SHA-256 |
| --- | --- |
| Original critique | b6117e40523ce84c5c163d913263224abda62b8d40530e09fd6de4f5b33f1397 |
| Committed offline JSON | b89eaf3d50ecc43365d71a6e92f53cd8b9f9986d1698eb06103edec8f6258192 |
| Unchanged golden JSON | 45c5762bbece1ff5604ea51ee6408e82f0ae5576d17cae8a4c925991c1610d5b |
| ai_eval.py | 9101bef9f27c3a79d87d4eb2dcbb9683bd822a9ff00a00ed2c9b7d94e55b16e5 |
| test_ai_eval.py | 0f0c7935043152c623d70ee4fc52b93a9b108e0128de465e1bdc9d4fcf1b4cea |
| test_ai_tasks.py | e05240b1a4d61357def93a5b4d2eab7e62807128ae2e73612a2a7caed2a32c58 |
| Agents README | 7cd9c4482b83354428af56f6ac9bf66fd6e0b308730b47eb6bbc9c1374d81865 |

This original Review's own SHA-256 is returned separately after final write,
avoiding a self-referential file digest. Preserve this complete original record
and verdict, including the Low residual and failed-command disclosures.

## Residual Work, Blockers and Not-Run Boundaries

* Review blockers: none.
* Remaining parent active work: P03-T02 publication/handoff; source implementation is complete. Parent may reconcile its own state and delivery artifacts after this result, outside this reviewer's write boundary.
* RV-001 remains the existing migration-quality residual only.
* Coordinator exact-final-head review and any integration decision remain separate.
* Held-out/human/cohort/approved-threshold studies, actual serving usage/model version, quota/region/access, Finance/effort/cost, privacy/consent/processor approval, real AI/SQL/Azure CON-009/AC-057 and operational release are unmet and unrun here, not defects demanding expansion.
* Docker/image, actual inference, Azure/IAM/deployment and service SQL: N/A to this offline source-accounting patch, not passes or acceptance. Browser/accessibility checks: N/A, no web source changed. No external regulatory-currentness/legal approval is claimed.
* No live GitHub checks, PR publication, issue closure, checkbox, board, remote, commit, merge or integration operation was performed by this reviewer.

## Outcome

* Outcome: Conformant with justified divergence.
* Rationale: the complete candidate meets the bounded accounting/evidence acceptance criteria, preserves final-only quality and all existing failure/authority gates, and has meaningful red/green and direct consumer evidence. The only divergence is the justified handling of an explicit formatter check that also fails on untouched base: final added-block formatting passes and configured exclusion is accurately disclosed, not substituted for strict coverage.
* Scope of acceptance: this pinned offline engineering delivery only. No whole-issue completion, actual-model/human result, benefit claim, live authorization, source publication or future-head acceptance follows.
* Severity summary: no Critical/High/Medium findings; one Low non-blocking inherited checking residual. No source correction cycle requested.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement route required. |
| Significant decision gap or invalid assumption | None | No rpi-plan route required. |
| Material research/evidence gap | None within the accepted offline boundary | No rpi-research route required; live issue/remote state not independently fetched under the offline constraint. |
| Non-blocking residual | RV-001, existing migration-quality follow-up | Parent retains caveat; separate migration-quality owner handles exemptions only if authorized. |
| Already planned remaining work | P03-T02, then coordinator exact-head review | Parent publishes with original Review/hash intact; coordinator separately assesses complete exact final head. |

* Review execution: Complete.
* Outcome: Conformant with justified divergence.
* Validation: independent 13 focused, 105 agents, 33 API; configured Ruff/format/mypy pass with explicit exclusions; exact-base red and legacy formatter failures corroborated; JSON rows/claims reconciled.
* Blockers: none for this Review or bounded offline source delivery.

## Artifacts

The first 22 rows are the complete committed base-to-candidate file inventory.
Additional rows are necessary upstream/acceptance context and this sole review
output. Link text and targets are workspace-relative.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/changes/2026-10-18/issue-108-evaluation-runs-changes.md](.copilot-tracking/changes/2026-10-18/issue-108-evaluation-runs-changes.md) | Completion, limitations and validation reconciliation |
| [.copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md](.copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md) | Execution details and remaining publication gate |
| [.copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md](.copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md) | Requirements, acceptance, markers and direct disposition |
| [.copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md](.copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md) | Research C1-C7 and bounded alternatives |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-agents.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-agents.log) | Original 105-test receipt |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-final.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-final.log) | Final API tests/lint and honest formatter exclusion |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-format-baseline.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-format-baseline.log) | Untouched-base explicit formatter failure |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-quality.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api-quality.log) | Original full explicit formatter failure |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-api.log) | Initial 33-test API receipt |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log) | Historical original defect reproduction |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-console.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-console.log) | Console denominators and claim boundaries |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-focused.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-focused.log) | Green 13-test receipt |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-offline-report.json](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-offline-report.json) | Complete scripted report and every priority row |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-quality.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-quality.log) | Configured agents quality receipt |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-reconciliation.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-reconciliation.log) | Denominator/quality/claim assertions and report hash |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-red.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-red.log) | Complete pre-repair adverse tracebacks |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-108-evaluation-runs-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-108-evaluation-runs-plan-critique.md) | Immutable Revise / PC-001 Medium original critique |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue-108-evaluation-runs-state.json](.copilot-tracking/rpi-sessions/2026-10-18/issue-108-evaluation-runs-state.json) | Committed Implement state and parent-only Review transition |
| [src/agents/README.md](src/agents/README.md) | Narrow accounting and compatibility disclosure |
| [src/agents/src/zava_forward/agents/ai_eval.py](src/agents/src/zava_forward/agents/ai_eval.py) | Full priority harness and repaired report source |
| [src/agents/tests/test_ai_eval.py](src/agents/tests/test_ai_eval.py) | All 13 focused regressions and retained controls |
| [src/api/tests/test_ai_tasks.py](src/api/tests/test_ai_tasks.py) | API pass-through, authority and negative controls |
| [src/core/src/zava_forward/core/ai.py](src/core/src/zava_forward/core/ai.py) | Returned source/model/latency fallback semantics |
| [src/core/src/zava_forward/core/store.py](src/core/src/zava_forward/core/store.py) | Actual recommendation/view/review contract |
| [src/api/src/zava_forward/api/server.py](src/api/src/zava_forward/api/server.py) | Unchanged manager-only report pass-through |
| [src/agents/evals/ai_priority_golden.json](src/agents/evals/ai_priority_golden.json) | Unchanged constructed scenarios and digest |
| [src/agents/pyproject.toml](src/agents/pyproject.toml) | Configured checks and inherited exclusions |
| [src/api/pyproject.toml](src/api/pyproject.toml) | API inherited lint/formatter exclusions |
| [.github/workflows/src-ci.yml](.github/workflows/src-ci.yml) | Existing component test/quality commands |
| [src/README.md](src/README.md) | Migration and component boundaries |
| [docs/case_study_48_original.md](docs/case_study_48_original.md) | Original proposal and human/resident authority |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Current proposal/RAI acceptance distinctions |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base routing context |
| [docs/reference/memory.md](docs/reference/memory.md) | Owner context, not evidence |
| [docs/reference/research/sector/housing-association-primer.md](docs/reference/research/sector/housing-association-primer.md) | Customer context, not invented company facts |
| [docs/prds/zava-forward-retrofit-programme-demonstrator.md](docs/prds/zava-forward-retrofit-programme-demonstrator.md) | Evaluation, RAI and real-platform acceptance limits |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-review.md](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-review.md) | This one original independent Review |

## Next Steps

Return this original record, outcome and SHA-256 to the active parent. The parent
owns remaining P03-T02 publication and must preserve the original critique and
Review, including RV-001 and failed-check disclosures, without claiming whole
issue acceptance. No source correction or further RPI invocation is requested.
The coordinator separately owns the complete exact-final-head review after
publication and any integration authorization. No user action is required.
This reviewer stops after the one original Review.
