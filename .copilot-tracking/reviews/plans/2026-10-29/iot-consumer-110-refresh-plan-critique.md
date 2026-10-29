---
title: IoT consumer 110 refresh final-candidate plan critique
description: One bounded critique of the PR 508 refresh candidate
ms.date: 2026-10-29
---

## Metadata

* Task ID: pr-508-refresh-2026-10-29
* Task slug: iot-consumer-110-refresh
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-consumer-110-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-consumer-110-refresh-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique; no implementation or independent implementation Review performed.

## Inputs and Criterion Boundary

* Caller requirements: refresh draft PR #508 on feat/iot-consumer-110 through fetch/rebase, preserve both sides, main-owned rubric/scenario contract, src-only application code and externally owned tests, bounded validation, preserved original evidence, read-only official pricing confined to PR notes, local Conventional Commit with Copilot trailer, and no push or Azure resource operations.
* Primary inputs: the supplied plan, phase details and .copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md, including C1-C7/W1-W2.
* Bounded supporting evidence: src/README.md local RPI gate, .github/workflows/src-ci.yml, src/core/pyproject.toml, src/api/pyproject.toml and sensor/IoT test filenames. Required project orientation documents were read; they do not establish technical acceptance.
* Decisions and dependencies: main owns .github/rubric/* and scenario-manifest.json except necessary digest refresh; no test removals or weakened assertions/exemptions; at most two demonstrated integration regressions; full API only under held nonblocking heavy admission; coordinator alone publishes and obtains hosted results.
* Inspection found feat/iot-consumer-110 with only newly untracked task-evidence directories. This critique does not move, stage or commit that work.
* Boundary: assess plan credibility, not integrated source correctness, live IoT acceptance, current remote state, actual prices or successful tool execution. No external research, fetch, rebase, tests, remote writes or resource operations were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01; research Q1 | Partial | Intent-aware conflict approach is sound, but fresh fetch/base capture is not executable in the task and rebase identity setup is delayed; PC-003/PC-005. |
| P01-T02; C3-C5 | Covered | Main model/noise semantics, dynamic version, allowlisted digest refresh and manifest/inventory tests are explicit. |
| Test ownership and change budget | Covered | Owning src/<project>/tests, zero removals, bounded justified additions and no assertion/exemption weakening. |
| P02-T01; C6 | Partial | Appropriate test families and lint/type scope, but environment constraint and exact invocations remain unresolved; PC-002/PC-004. |
| Original 2026-10-27 evidence | Covered | Preserve historical outcomes and appended records; no authority to replace adverse evidence or delete history. |
| P03-T01/P03-T02; C7 | Partial | Original Review-before-commit is preserved, but separate post-gate exact-head assessment is absent; PC-001. |
| Hosted CI and rubric; W1 | Covered | Historical missing verdict/403 is not attributed to source tests; no permission changes or current-head green claim. |
| Read-only pricing; W2 | Covered within plan boundary | Official dated regional estimate reserved for coordinator PR notes with exclusions; price calculation itself is not validated here. |
| No Azure operations; no push | Covered | Explicit constraints, deferred live criteria and coordinator publication ownership. |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 2 High, 3 Medium, 0 Low.
* Rationale: The scoped integration strategy is credible, but the publication handoff omits a required independent exact-head control, and validation depends on paths forbidden in this execution environment. Three bounded procedural corrections also prevent stale-base, irreproducible-test and identity errors. These are planner-owned corrections, not grounds for a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Separate original Review from post-gate exact-head assessment

* Related IDs: P03-T01, P03-T02; C7; acceptance criteria for one independent Review and publication handoff.
* Evidence: The plan places the one Review before the implementation/evidence commit. Phase details end with coordinator fetch/receipt verification but no independent exact-head assessment. src/README.md:150-159 requires fresh receipt verification immediately before independent exact-head review and push.
* Concern: The original Review cannot also attest to a later committed HEAD and its subsequently generated receipt. Treating every finding as later work does not distinguish an adverse implementation Review from a publishable candidate.
* Impact: A locally committed candidate could be handed off as publication-ready without the required independent assessment, or with unresolved Review findings implicitly accepted.
* Smallest useful change: Keep exactly one original post-implementation Review, commit it unchanged with the candidate, then gate. Assign the coordinator a separate independent exact-head assessment after fresh-base receipt verification and before any authorized push. Explicitly prohibit publication on adverse original Review, missing/failed gate or missing exact-head assessment. Do not equate this later control with repeating or rewriting the original Review.
* Action owner: Planning parent for the handoff contract; coordinator for later exact-head assessment.
* Exact resolving evidence: P03 and acceptance criteria explicitly distinguish original Review, committed candidate SHA, external full receipt, freshly fetched base SHA, verification and independent exact-head assessment. Handoff identifies these as pending/blocking unless actually satisfied and states that subsequent commit/base/tool/input changes invalidate the receipt.
* Decision route: Direct planner correction; existing repository instructions resolve the control. No user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Requested temporary paths conflict with execution restrictions

* Related IDs: P02-T01, P03-T02; environment and heavy-lock dependencies.
* Evidence: Plan and details prescribe /tmp/mv and /tmp/ama-rpi-heavy.lock. The supplied runtime instructions prohibit all file operations under /tmp, /var/tmp or temporary directories and require created files to be project-relative. src/README.md:109-119 additionally requires external gate output and the shared temporary-path lock.
* Concern: The plan presents these prerequisites as usable without reconciling the stricter execution constraints. Opening the lock or installing dependencies there is a prohibited file operation. Silently substituting a project-local lock would not coordinate with the existing shared gate.
* Impact: Literal execution violates runtime restrictions; a substituted lock can permit concurrent heavy workloads; a relocated receipt inside the candidate can fail clean-input/external-output requirements.
* Smallest useful change: Mark the requested environment/shared-lock/full-gate path combination as an explicit execution blocker under this runtime. Permit a project-relative non-temporary environment for eligible focused checks only if it can meet the installation contract, recording the deviation rather than claiming the requested /tmp/mv checks ran. Do not relocate the shared lock or bypass runner restrictions. Assign the coordinator the blocked checks/gate in a compliant execution context.
* Action owner: Planning parent; coordinator owns provisioning a compatible execution context and any deferred checks.
* Exact resolving evidence: Plan/details contain a constraint-aware command/output policy, named blocked checks and coordinator handoff, with no prohibited path writes, lock substitution, full-suite run without admission or fabricated receipt. Any future full-gate success must come from an environment satisfying both path policy and the authoritative runner contract.
* Decision route: Direct planner correction to execution status and handoff. User permission cannot override the runtime prohibition; no request to weaken safeguards is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Make fresh fetch and actual base capture an explicit integration step

* Related IDs: P01-T01; research Q1; caller fetch/rebase requirement.
* Evidence: Research records fetched main b0364e4b. Details assume the four commits replay onto that value; P01-T01 only executes git rebase origin/main.
* Concern: Research-time freshness is not an execution-time fetch. A moved remote base would leave the implementation targeting a stale ref while the ancestry assertion still succeeds.
* Impact: The candidate may satisfy a local ancestor test but not the requested current-main integration or receipt base contract.
* Smallest useful change: Begin P01-T01 with git fetch origin main, record the full resolved origin/main SHA and topic HEAD, then rebase that fetched base. Treat b0364e4b as historical research evidence only. If new upstream changes materially alter scope, stop and record the divergence rather than silently expanding the plan.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Revised P01-T01 specifies the fetch/base-capture sequence and changes artifact records actual before/after SHAs, rebase result and ancestry against the captured base; final publication freshness remains separately coordinator-owned.
* Decision route: Direct planner correction; the caller already requires fetch/rebase. No user response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Pin executable focused selectors and installed-distribution checks

* Related IDs: P02-T01; C4-C6; test ownership/change budget.
* Evidence: Details name sensor/backfill/privacy families and bare colon-separated paths but do not give complete unittest invocations or identify whether paths are PYTHONPATH versus MYPYPATH. They say to use installed distributions, while the concrete setup only describes installing missing SDKs. The CI installs editable owning distributions before unittest, Ruff and mypy.
* Concern: Two implementers can run different coverage or accidentally substitute direct source imports for required installed packages. A blocked full API run makes unambiguous focused coverage especially important.
* Impact: An apparently green result may omit historical backfill, stock/fault/privacy or main manifest regressions, or fail to exercise the installed package contract.
* Smallest useful change: Add complete per-directory, environment-aware lint/format/mypy and unittest commands with exact module selectors. Explicitly include test_sensor_stream, test_sensor_consumer, test_sensor_faults, test_sensor_stock, test_sensor_privacy, test_sensor_backfill, test_historical_backfill, test_scenario_manifest and test_needs_inventory for core, and test_iot_stream/test_sensor_ingestion for API. Identify each path variable and verify installed core/agents/API distributions before relying on sibling fixture paths. Preserve existing pins and only restore/install dependencies after an observed missing prerequisite or manifest change.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: P02 details provide copyable commands, working directories, environment/path roles and expected selectors; changes record actual selected modules, exit status, failures/reruns, installed-package provenance and skips. No new tests, exemptions or private datasets are needed to resolve this planning gap.
* Decision route: Direct planner correction. No user response required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Configure privacy-safe committer identity before rebase

* Related IDs: P01-T01, P03-T02; authenticated noreply identity requirement.
* Evidence: P01-T01 replays four commits and preserves their authors; authenticated gh api user and repository-local identity setup occur only at P03-T02.
* Concern: Rebase creates new commits with a current committer identity before the planned privacy-safe configuration. Configuring identity only for the final evidence commit does not correct those replayed committers.
* Impact: The local candidate can contain new private-email committer metadata or fail future email-privacy publication checks, leaving an unauthorized rewrite as the apparent remedy.
* Smallest useful change: Resolve the authenticated account and configure repository-local noreply identity before rebase, checking that effective committer identity is not overridden. Retain the historical authors as explicitly directed; use authenticated privacy-safe author and committer for the newly authored implementation/evidence commit and include the required Copilot trailer.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: P01 has the identity prerequisite before any history replay; changes record successful identity validation without exposing private email, and final inspection confirms authenticated noreply committer metadata on replayed commits plus correct author/committer/trailer on the new commit.
* Decision route: Direct planner correction; preserve historical authors and do not amend existing commits to resolve this critique. No user response required.

## Strengths and Residual Risk

* Conflict resolution inspects base/main/topic intent rather than choosing an entire side indiscriminately. Main rubric bytes and scenario contract remain authoritative; only necessary allowlisted source digests may change.
* Main generator/noise semantics and dynamic version are protected without freezing historical replay bytes.
* Test ownership, zero removals, bounded additions and no weakened assertions/exemptions are explicit. If more tests are demonstrably necessary, record a budget/scope blocker rather than hiding additions.
* Historical evidence, unresolved live criteria and rubric failures remain distinguishable from new local evidence. No approval, hosted verdict or live IoT acceptance is inferred.
* No UI changes are planned; any necessary web edits must first activate the repository's applicable skill/review requirements.
* Lock availability at research time is not admission for a future suite. Missing admission or tooling must remain an honest blocker.

## Questions or Blocking Evidence Gaps

* No unresolved user product or conflict-ownership decision is needed for these corrections.
* A compliant execution context for the requested environment/shared lock/external receipt is not established by the inputs. Treat it as blocked, not a basis for a skip token or cloud fallback.
* Actual rebase conflicts, present prices and final local/hosted results remain future execution evidence, not critique conclusions.

## Limitations

* This is the single complete assessment of the supplied candidate boundary. Referenced supporting files were inspected only to resolve its validation/publication contracts; no open-ended audit was performed.
* No implementation validation was attempted. Complete describes critique execution, not implementation acceptance.
* Plan, phase details, research, historical records and source remain unchanged. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P03's original-Review versus exact-head-assessment contract, then incorporate PC-002 through PC-005 directly into the same plan/details update.
* User response required: No. Return to the active parent for direct disposition and finalization without another critique; implementation may proceed only within the corrected executable boundary.

| [.copilot-tracking/plans/2026-10-29/iot-consumer-110-refresh-plan.md](.copilot-tracking/plans/2026-10-29/iot-consumer-110-refresh-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-29/iot-consumer-110-refresh-phase-details.md](.copilot-tracking/details/2026-10-29/iot-consumer-110-refresh-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md](.copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md) | Supplied evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/iot-consumer-110-refresh-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/iot-consumer-110-refresh-plan-critique.md) | Complete critique; Revise |

## Next Steps

The active planning parent should disposition all five findings directly and finalize without another critique. No user action is required. Stop this critique here; do not implement, publish or operate resources.
