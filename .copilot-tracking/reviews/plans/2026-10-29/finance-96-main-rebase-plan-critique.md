<!-- markdownlint-disable-file -->
# RPI Plan Critique: finance-96-main-rebase

## Metadata

* Task ID: finance-96-main-rebase
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-96-main-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/finance-96-main-rebase-phase-details.md
* Critique execution status: Complete
* Assessment count: one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: locally fetch/rebase existing draft PR #510,
  docs/finance-96, onto origin/main; preserve both conflict intents,
  append-only/index entries, main's rubric/scenario manifest and original
  adverse finance evidence; source under src/ and tests outside packages.
* Validation requirements: the designated shared venv with local source/test
  precedence and import provenance; full owning-project Ruff check/format,
  applicable mypy and relevant unittest modules; no test removals or new test
  files, with at most two methods only for necessary integration coverage.
  Full API discovery requires the specified successful nonblocking lock probe
  and retaining the heavy lock throughout execution.
* Operational requirements: no Azure activity, push or remote mutation;
  Conventional Commit, Refs only and requested Copilot trailer. Original
  finance RV-001/002 remain open and outside feature-fix scope.
* Primary evidence: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-29/finance-96-main-rebase-research.md.
* Bounded supporting evidence: research pointers C1-C6, including
  src/README.md, .github/workflows/src-ci.yml,
  src/core/pyproject.toml, src/core/tests/test_scenario_manifest.py,
  .copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md and
  .copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md.
  Read src/api/pyproject.toml to assess the stated API type-check boundary.
* Repository context: original/addendum, reference index and memory; memory
  was treated as context, not evidence. Read-only Git inspection confirmed
  docs/finance-96 and the seven original finance tracking paths in the
  supplied pre-rebase range.
* Decisions and dependencies: preserve commits e114bc45 and 373ab192;
  fetched base recorded as 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
  Conflict resolution precedes combined-source validation; reconciliation
  precedes the single independent implementation Review and local commit.
* Boundary: assess planning credibility, not implementation correctness,
  successful replay, actual validation results, fresh hosted status, financial
  approval or publication readiness. No rebase, tests or delegation performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01; research Q1 | Covered | Research records successful fetch, branch/PR relationship and two commits; details distinguish rebase ours/theirs, require stage inspection and prohibit global side selection. |
| P01-T01; additive documentation | Covered | Both index/log additions must survive; stage only resolved files and do not stash/delete unrelated work. Existing untracked task artifacts are acknowledged. |
| P01-T02; research Q2, C4/C6 | Covered | Range-diff and net diff assess endpoint dispatch, private projection and combined typing overrides rather than merely removing conflict markers. |
| P01-T02; main-owned protected files | Covered | Main rubric and scenario manifest must remain identical, including a final equality check; ancestor verification binds the replay to the fetched base. |
| P01-T02; historical evidence | Covered | Hash/compare seven original artifacts against 373ab192. Read-only range inspection confirms seven original tracking files, including original state, critique and Review. |
| P02-T01; Ruff/mypy | Covered | Full dot-scope Ruff check/format and configuration-driven mypy run from both affected owning projects, core and API; not changed-file-only validation. |
| P02-T01; shared-venv provenance | Covered | Explicit local core/API/agents source and test paths precede foreign editables; runtime module-file assertions require this worktree. Core mypy uses local src/tests; API configuration also points at local core source/tests. |
| Test Ownership and Coverage Lock | Covered | Existing core/API test ownership, zero removals/new test files, maximum two necessary regression methods and no generated tests are explicit. |
| P02-T01; focused regressions | Covered | Named core/API selectors cover review/staging, finance/grants, provenance/rescans, route inventory and dependency rules; canonical scenario-manifest test checks pinned combined sources. |
| P02-T01; heavy lock | Covered | Full API discovery is optional; successful prescribed probe is required if selected and the lock must remain held throughout. Focused testing is the default. |
| P02-T02; evidence and independent Review | Covered | Commands/results/skips/limits are recorded; implementation finishes before the single independent Review; original adverse outcomes remain unchanged. |
| P02-T02; local-only commit | Covered | Conventional subject, Refs #96, Copilot trailer, privacy-safe author/committer, clean final state and unchanged remote ref are required. No push or Azure operations are authorized. |
| Acceptance and Follow-Up Items; research Q3 | Covered | Local checks, full publication gate, exact-head assessment, hosted CI and external rubric budget remain distinct; no fresh hosted success or whole-issue acceptance is asserted. |
| Scope; original RV-001/002 | Covered | Both inherited findings and missing Finance/Board decisions remain open, not new integration-fix tasks or implied approval. |

## Verdict

* Verdict: Pass
* Rationale: the plan is credible for the caller's bounded local integration.
  Its replay checks protect both intents and historical evidence, validation
  uses the affected projects' complete lint/type scopes and selected existing
  regressions, and the shared-venv and heavy-lock hazards have explicit
  controls. No substantive plan correction is required on the supplied
  evidence.
* Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low.

## Findings

None. No actionable PC-xxx findings identified within the supplied criterion
boundary. No discoverable substantive findings are withheld for another pass.

## Strengths and Residual Risk

* Protected-file equality and canonical manifest validation are separate
  obligations. If the combined source fails the manifest check, the executor
  must preserve failure evidence rather than relax hashes/tests or silently
  replace the main-owned manifest.
* Original RV-001/002 remain open under explicit caller scope. Passing
  integration regressions cannot overturn the original Not accepted outcome
  or demonstrate missing Finance/Board authority.
* A recorded prerequisite failure or skipped optional integration test is
  transparent evidence, not a passed check. The plan's blocker-recording
  alternative must not be reported as successful validation.
* Shared-venv provenance assertions and selected unittest results remain
  implementation obligations, not facts established by this critique.
  Preserve project configurations and ordinary provenance evidence; missing
  dependencies do not authorize unrelated shared-environment mutation.
* The supplied no-push boundary leaves publication gates and fresh hosted
  checks outstanding. This critique grants neither publication nor merge
  approval. Before committing, follow the standing authenticated-account
  identity procedure rather than treating a recorded email as authentication.
* Main may advance. The plan correctly requires reporting the actual reviewed
  base rather than claiming currency against an unobserved later main.

## Questions or Blocking Evidence Gaps

None for this planning assessment. Concrete conflicts or validation failures
must be investigated during implementation without expanding into the original
finance feature defects.

## Limitations

* No fetch, rebase, test, lint, type check, venv access, Azure operation, commit,
  push or remote-state change was performed.
* Hosted PR/check facts and shared-venv state are attributed to the supplied
  research, not freshly verified here.
* Read-only Git inspection establishes the current branch/untracked task
  context and historical file inventory only; it does not prove a future
  candidate preserves those bytes or passes validation.
* Only this critique artifact was written. Plan, phase details, research,
  source and session-state records were not edited.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent / integration executor.
* Smallest next action: record the single Pass disposition and proceed with
  P01-T01 under the caller's local-only scope, then retain actual validation
  evidence and the single independent post-implementation Review.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/finance-96-main-rebase-plan.md](.copilot-tracking/plans/2026-10-29/finance-96-main-rebase-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/finance-96-main-rebase-phase-details.md](.copilot-tracking/details/2026-10-29/finance-96-main-rebase-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/finance-96-main-rebase-research.md](.copilot-tracking/research/2026-10-29/finance-96-main-rebase-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-29/finance-96-main-rebase-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/finance-96-main-rebase-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent may finalize the plan disposition and continue to
implementation within the existing authorization. No additional critique or
user response is required. This critique task stops here without running
implementation, validation or publication.
