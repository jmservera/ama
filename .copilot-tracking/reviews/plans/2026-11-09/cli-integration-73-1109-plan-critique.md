<!-- markdownlint-disable-file -->
# RPI Plan Critique: parent73 CLI component integration with current main

## Metadata

* Task ID: issue-73-cli-integration-1109
* Critique date: 2026-11-09
* Plan: .copilot-tracking/plans/2026-11-09/cli-integration-73-1109-plan.md
* Phase details: .copilot-tracking/details/2026-11-09/cli-integration-73-1109-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: partial parent #73 CLI component integration only; child #135 (PR1334) is merged into parent a4317567f806d9585db716d6ae5ad4af6bed5366, not main 3bc20719803a77490c704f985559720e23aa169d; ordinary merge of main after Plan/Implement activation; no rebase/force/reset/amend; no Core/API/shared hook/register/navigation/roles edits; #80/#84/#122 not waived; no new feature or refactor; fresh-venv verification; noreply identity and trailer on every commit; no GitHub or push writes.
* Research and evidence considered: .copilot-tracking/research/2026-11-09/cli-integration-73-1109-research.md; coordinator report demo-next-ready-96-122-report.md (static evidence); read-only git checks (origin/main resolves to 3bc20719..., HEAD a4317567..., local noreply email set, 71 test functions under src/importer/tests, importer pyproject mypy/ruff config, main-side file list since the merge base).
* Decisions, dependencies, and acceptance criteria considered: plan AC1 to AC5, FR1 to FR3, NFR1 and NFR2, P01 to P04 tasks, dependency interpretation in research.
* Assessment boundary: static plan credibility only. No merge, install or test was run, so predicted conflict-freeness (research C6) and test outcomes are not confirmed here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Ordinary merge, no rewrite (FR1, P02-T01) | Covered | `--no-ff origin/main`, ancestry AC1. Message and trailer mechanics unspecified (PC-004). |
| No Core/API/hook edits (AC5, P02-T03) | Partial | Check is path-based against "main's" and loose on hooks and workflows (PC-005). |
| Dependencies not waived | Covered | Plan and research keep #80/#84/#122 retained. |
| Fresh venv, no PYTHONPATH (P01-T02) | Partial | Location in /tmp, network install not reconciled (PC-001, PC-002). |
| Importer tests, mypy, Ruff (P03-T01, T02) | Partial | Exact commands and the Core test invocation are not specified (PC-003). |
| Synthetic CLI scenarios (AC4, P03-T03) | Partial | Mechanisms, expected exits and oracles are missing (PC-006). |
| Clean tree precondition (P01-T01) | Missing | Plan, details and research are untracked now (PC-007). |
| Research C2 delta characterisation | Partial | Omits tracking files and rubric file in the main delta (PC-008). |
| Handoff and state (P04) | Partial | Handoff path ambiguous (PC-009). |

## Verdict

* Verdict: Revise
* Rationale: The scope, merge approach and dependency stance are credible and compliant with the requirements. Several verification and precondition details would cause a wrong or unverifiable result at Implement (untracked tree vs clean-tree check, /tmp usage and network install, undefined scenario oracles). All fixes are direct planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Scenario verification lacks concrete mechanisms and oracles

* Related IDs: AC4, FR3, P03-T03
* Evidence: .copilot-tracking/details/2026-11-09/cli-integration-73-1109-phase-details.md P03-T03; coordinator report section "Selected handoff and validation" item 3.
* Concern: P03-T03 lists scenario names but not how to produce them or what to assert. "Hashless identity", "unreadable file" and "DB write failure" have no stated construction (for example how a hashless refusal arises when the importer snapshots the file, or how a write failure differs from an unopenable path). No expected exit code, row content, or dedupe reason per scenario. "Same bytes under two names first reason kept" does not say which reason differs. The viewer hash check names no files hashed (DB plus WAL/journal sidecars, source files).
* Impact: A script written ad hoc at Implement may pass vacuously, and AC4 cannot be independently reviewed.
* Smallest useful change: Add a scenario table in P03-T03: setup, command, expected exit (1 for recorded refusal, 2 for DB open/write error), expected persisted row or absence, and for hash stability the exact file set including sidecars, hashed before and after. Derive constructions from src/importer/src/zava_forward/importer/exceptions.py and tests/test_import_exceptions.py.
* Action owner: planning_parent
* Exact resolving evidence: updated P03-T03 table covering every AC4 bullet with setup, command, expected exit and assertion; script run later reports each with raw exit codes.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Venv and scratch script placed in /tmp

* Related IDs: P01-T02, P03-T03, NFR2
* Evidence: phase details P01-T02 (`/tmp/zf73-venv`) and P03-T03 ("script in /tmp").
* Concern: The execution environment prohibits writing to /tmp or temp directories; the plan hard-codes it for the venv, the scenario script and implicitly the temp SQLite DB and synthetic files.
* Impact: Implement either violates the environment rule or deviates from the plan without record.
* Smallest useful change: Name an untracked, non-committed location outside the git index but not in /tmp, for example the session files directory or an ignored path under the worktree, and confirm it stays out of commits and of any "clean tree" check (verify with `git check-ignore` or `git status`).
* Action owner: planning_parent
* Exact resolving evidence: plan lists a non-/tmp venv, script and data path; P04 `git status --short` shows them absent.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Verification commands and tool-pin handling are underspecified

* Related IDs: AC2, AC3, P01-T02, P03-T01, P03-T02, C7
* Evidence: phase details P01-T02, P03-T01, P03-T02; src/importer/pyproject.toml (dev ruff==0.17.1, mypy==2.4.0, mypy files src and tests, Core follow_imports skip); research C7.
* Concern: (a) Core exception tests live in src/core/tests (test_exception_feeds.py, test_exception_queue.py) but no command, working directory or discovery pattern is given; without PYTHONPATH the Core tests may need the installed worktree Core. (b) Mypy and Ruff commands are not written (run from src/importer, config path, which paths for Ruff). (c) Installing `[blob]` extras and pinned tools requires a package index (network), which sits against "no network"; the plan does not say that package installation from the index is the only permitted network use, nor what to do if offline. (d) Local tool versions differ from pins (C7); the plan chooses pins but does not state that a mismatch is a failure. (e) AC2 "71" has no pass criterion beyond count, e.g. 71 run, 0 skipped.
* Impact: The "exact importer-project mypy" and test evidence could be non-reproducible or silently use the primary checkout.
* Smallest useful change: Write exact commands, cwd and pass criteria; record `pip freeze`-level versions of ruff, mypy and the two zava dists with resolved paths; state package-index installation as the sole network use and an offline blocker rule.
* Action owner: planning_parent
* Exact resolving evidence: details list literal commands for importer tests, Core exception tests, mypy, ruff format --check and ruff check with expected outcome (71 ran, 0 skipped, 0 errors), and an interpreter/path/version proof step.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Merge commit identity, trailer and ref freshness mechanics unspecified

* Related IDs: NFR1, FR1, P02-T01
* Evidence: phase details P02-T01; git check: origin/main is 3bc20719..., local user.email is the noreply address.
* Concern: `git merge --no-ff origin/main` alone opens an editor or default message without the Co-authored-by trailer. The plan does not state the `-m` message or that author and committer are both the noreply identity (user.name unchecked), nor that origin/main is used as a local ref without a fetch (fetch is network and a remote read; none is authorised). It also does not require a pre-merge re-check that origin/main still equals the pin.
* Impact: A trailer-less or editor-blocked merge commit violates NFR1; a stale or silently moved ref breaks the pin.
* Smallest useful change: Specify `git merge --no-ff -m "<Conventional Commit message>" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" 3bc20719803a77490c704f985559720e23aa169d` (by SHA, no fetch), verify committer name/email, and post-verify with `git log -1 --format=%an,%ae,%cn,%ce,%B`.
* Action owner: planning_parent
* Exact resolving evidence: details contain the literal command and a post-commit identity and trailer check for the merge and the P04 tracking commit.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: AC5 and P02-T03 diff checks are too weak for the no-shared-edit constraint

* Related IDs: AC1, AC5, P02-T03, P03-T04
* Evidence: plan AC5; phase details P02-T03 and P03-T04; git check: main-side delta since merge base includes .github/rubric, docs, api, core, agents.
* Concern: AC5 says no Core/API/hook/register/navigation/roles file "beyond what main brought" without a mechanism. The decisive test is that HEAD versus origin/main differs only in the parent's own delta (importer plus tracking), and HEAD versus parent differs only in main's delta. P03-T04 "no model/network/replay calls" by grep is undefined (patterns not stated). The register `NOT_CONNECTED` assertion is a grep and not a run of register tests, although Core exception register tests exist.
* Impact: A mistaken conflict resolution touching Core or API could pass the stated checks.
* Smallest useful change: Add `git diff --name-only 3bc20719...HEAD` must list only src/importer and .copilot-tracking paths matching the parent's C1 set (plus the new tracking files), and `git diff --name-only a4317567...HEAD` must equal main's delta; state concrete grep patterns; optionally run existing Core exception register tests (read-only).
* Action owner: planning_parent
* Exact resolving evidence: details list both diff commands with expected path sets and the grep patterns.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Clean-tree precondition contradicts the current worktree and the commit order

* Related IDs: P01-T01, AC1, P04-T01
* Evidence: `git status --short` shows the plan, details and research files untracked; phase details P01-T01 ("clean tree").
* Concern: The three RPI artifacts are untracked, so the P01 clean-tree check fails as written. Merge with untracked files is safe only when main does not add the same paths (no collision found by name, but not asserted). The plan does not say whether these artifacts are committed before the merge (the merge then has a tracking commit before it, so parent HEAD no longer equals a4317567 and AC1/P02-T03 "HEAD a4317567" statements change) or left untracked until P04.
* Impact: Implement would either stop on its own precondition or alter the merge baseline unannounced; the empty-diff check for src/importer against a4317567 stays valid either way but the base statements must be exact.
* Smallest useful change: Define the precondition as "no tracked modifications; only the three named untracked RPI artifacts", merge first, commit tracking in P04 only, and assert no path collisions via `git ls-tree` of main for those paths before merging.
* Action owner: planning_parent
* Exact resolving evidence: P01-T01 states the allowed untracked set and a collision check; P04 shows the commit order.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Research understates the main delta

* Related IDs: C2, C6
* Evidence: research C2 ("Touches api, core, agents, docs") versus git check: main delta since merge base includes 143 .copilot-tracking files and .github/rubric/scores/latest.json (39 non-tracking files: 21 api, 13 core, 2 docs/reference, 1 docs/architecture, 1 agents, 1 rubric).
* Concern: Tracking and rubric files are not listed; the "disjoint paths" argument still holds, but the plan's AC5 claim and handoff should not repeat the incomplete description. Rubric file is a workflow input, so the impact classification (focused tier) should note it is brought by main, not edited.
* Impact: Minor inaccuracy in evidence that the handoff will quote.
* Smallest useful change: Correct C2 and the plan summary, and state the validation tier classification and basis (focused tier; no workflow, dependency, Dockerfile or infra edit by this branch).
* Action owner: planning_parent
* Exact resolving evidence: research/plan text lists tracking and rubric paths and a recorded tier classification.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: Handoff path and post-merge contingency are ambiguous

* Related IDs: P04-T01, P02-T02
* Evidence: plan "Handoff file: coordinator files/handoff-73-cli-integration-1109.md"; details P04-T01.
* Concern: The relative path does not name which session-state directory; a failed test after merge has no rule (do nothing without a red repro, or stop) beyond "only after a red repro"; and the merge commit is not reverted by reset, so a bad merge's remedy (a new corrective commit, or stop) is not stated.
* Impact: Handoff could be written to the wrong place; a red verification has no defined outcome.
* Smallest useful change: Use the absolute handoff path and add: red result outside the importer compat scope means stop and report without history rewrite.
* Action owner: planning_parent
* Exact resolving evidence: absolute path in P04-T01 and a stop rule in P03.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Scope boundaries, dependency non-waiver, no-rewrite and no-write constraints are explicit and consistent with the requirements and the coordinator report.
* Trial merge evidence (C6) and byte-identical Core exception contracts (C3) give a credible low conflict risk; this remains a prediction until executed.
* Residual risk: the 71 count and predicted clean merge are unverified here; hosted CI, independent exact-head review and human approvals are outside this plan and stay required before publication.

## Questions or Blocking Evidence Gaps

* None. No user decision is required; every finding is resolvable by the planner from supplied evidence.

## Limitations

* Read-only static review plus a few git/grep checks; nothing was merged, installed or executed.
* Coordinator report is static evidence and not merge approval; it was not re-verified beyond the pins and local config.
* Whether the three untracked artifacts collide with main paths was inferred by name only.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: direct revision of phase details P03-T03 (scenario table with constructions, exit codes and hash file set), then PC-002 to PC-008 in the same pass, then finalize without another critique.
* User response required: no
