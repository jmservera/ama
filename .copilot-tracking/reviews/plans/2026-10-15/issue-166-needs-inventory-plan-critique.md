---
title: Issue 166 needs inventory final-candidate plan critique
description: Independent bounded assessment of scope, regression evidence and delivery controls
ms.date: 2026-10-15
---

## Metadata

* Task ID: issue-166
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md
* Research: .copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md
* Critique execution status: Complete
* Worktree: /home/azureuser/source/ama-wt/issue-166
* Branch verified: feat/src-needs-inventory-166
* Output: .copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md

## Inputs and Criterion Boundary

The caller authorizes full RPI delivery by the parent, not implementation by
this reviewer. This assessment covers the supplied candidate once, including
research C1-C8/W1-W3, both phases, all four tasks, acceptance criteria,
dependencies, human decisions and publication safeguards.

The supplied direction fixes the engineering scope: reuse #240's inventory
and gate; one new scenario integration JSON; at most eight added test methods
in src/core/tests/test_needs_inventory.py; no new runtime module; corrections
from public migrated sources only. No private data, prohibited configuration
paths, issue-cache writes, mvp code, uv, invented approvals or deployment.
Existing untracked planning inputs were left untouched.

Direct evidence inspected includes:

* docs/reference/research/retrofit-synthetic-data/needs-inventory.json
* docs/reference/research/retrofit-synthetic-data/provenance-register.json
* docs/reference/research/retrofit-synthetic-data/README.md
* src/core/tests/test_needs_inventory.py
* src/core/tests/test_synthetic_provenance.py
* src/core/tests/dataset.py
* src/core/pyproject.toml and src/api/pyproject.toml
* src/README.md and src/core/README.md
* Public migrated scale, sensor and chat fixture source evidence.
* docs/adrs/0006-src-layout-and-cutover.md and required project context.

No private dataset, private README, configuration secret or answer key was
opened. Linked issue/PR claims are assessed as supplied research evidence,
not independently refreshed remote state. This is plan credibility assessment,
not implementation, application acceptance or a second research exercise.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Full RPI and reuse of #240 | Covered | Research, bounded implementation, one implementation review and PR are explicit; no duplicate gate runtime. |
| C1-C8; P01-T01 metadata corrections | Covered | Existing public sources support qualified fixture/generator corrections, not private-register regeneration or live acceptance. |
| #103 linkage and acceptance honesty | Covered | Reciprocal inventory binding is an integration seed; full profiles, workflows, defaults and endpoint execution remain deferred. |
| Thirteen stable SN rows and governance | Covered | Preserve row identities, proposed owners, volume decisions and build-start citations; owner ratification remains unchecked. |
| P01-T02 mutation regressions | Covered | Actual canonical JSON plus independently mutated version/date, missing/duplicate IDs, reciprocal path and approval states are required, within the eight-method ceiling. |
| P01-T02 changed-file quality | Covered | Explicit checks outside migration exemptions are required; configured whole-project checks alone do not establish this. |
| P02-T01 no-private-data validation | Partial | PC-001: existing core discovery executes private-file readers. |
| P02-T01 worktree-only validation | Partial | PC-002: ordinary tempfile users need explicit scratch-root isolation. |
| P02-T01 acceptance and dependencies | Covered | Pip-only recovery after observed missing dependencies; five suites, lint/type checks, synthetic smoke and Docker limits recorded; real AI/SQL/Azure acceptance Not run. |
| P02-T02 publication | Partial | PC-003: recorded account does not replace required authenticated-account resolution. |
| Open human and historical dependencies | Covered | Owner ratification, volumes/scope, gap mapping and unavailable historical matrix stay open; Refs #166, not closure. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: The bounded engineering proposal and acceptance claims are
  credible. Validation and publication instructions need three concrete
  safeguards before automatic execution. These are direct planner
  corrections, not reasons to expand scope, invent owner decisions or run
  another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Full core discovery conflicts with the no-private-data boundary

* Related IDs: P02-T01; no-private-data requirement; local validation acceptance.
* Evidence: Phase details lines 66-73 require five suites and limit the smoke
  to constructed data. However,
  src/core/tests/test_synthetic_provenance.py:85-94 opens and iterates the
  private stock CSV, and :96-108 opens its README-private.txt. These reads are
  not guarded by an availability or opt-in check.
* Concern: Restricting the smoke fixture does not restrict suite behavior.
  Unfiltered discovery either reads prohibited private files when present or
  fails when absent. Discovering the prohibition only from a missing-file
  failure is not a safe access control.
* Impact: The planned validation can cross an explicit caller boundary, or
  produce misleading full-suite completion evidence.
* Smallest useful change: Specify a validation-only discovery/filtering
  invocation that excludes private-file-dependent cases before execution.
  Name at least these two cases, inspect the remaining selected test setup
  for equivalent reads, and record excluded cases and reasons as Not run.
  Run the public/constructed remainder of all five suites. Do not alter
  provenance tests, copy private data, or expand the locked code scope.
* Action owner: Planning parent for the invocation and acceptance wording;
  implementing parent for recorded execution evidence.
* Exact resolving evidence: P02-T01 names the two private-reader test IDs,
  pre-execution filtering and honest suite counts; changes/PR evidence shows
  their exclusion before execution, selected test counts and outcomes, and
  no private-file access. No claim of an unqualified full core-suite pass.
* Decision route: Directly applicable planner correction. No owner decision
  or additional private-data authorization is needed or implied.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Validation does not bind temporary-file APIs to the permitted worktree

* Related IDs: P02-T01; caller worktree-only restriction; runtime prohibition
  on /tmp and /var/tmp file operations.
* Evidence: Phase details lines 66-74 specify an environment under the
  worktree and named smoke cleanup but not the scratch root used by tests.
  src/core/tests/dataset.py:ImproveTests.setUp calls
  tempfile.TemporaryDirectory() without dir. The same pattern exists in
  src/core/tests/test_sensor_backfill.py and src/api/tests/test_mvp.py.
* Concern: A worktree-local virtual environment does not change Python's
  temporary-file directory. Without explicit controls, these existing tests
  can write to the operating-system temporary directory.
* Impact: Otherwise ordinary test execution can violate the execution
  boundary before useful verification completes.
* Smallest useful change: Define an ignored, named validation scratch root
  under this worktree, outside src. Set TMPDIR, TMP and TEMP to its absolute
  path before starting test interpreters, and give smoke data/state explicit
  worktree-local paths. Preflight tempfile.gettempdir() and the effective
  smoke paths. Track and clean only this run's owned paths/processes.
  Do not change existing application or test modules to accomplish this.
* Action owner: Planning parent for explicit environment controls;
  implementing parent for preflight and cleanup evidence.
* Exact resolving evidence: P02-T01 records the scratch directory and
  environment setup; command evidence demonstrates tempfile.gettempdir()
  resolves inside this worktree before suite execution, smoke uses only
  constructed local data, and no scratch outputs are staged.
* Decision route: Directly applicable planner correction. No user response.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Publication relies on a recorded account rather than resolving the authenticated identity

* Related IDs: P02-T02; repository commit-identity safeguard.
* Evidence: Phase details lines 81-83 direct use of account
  8036360/jmservera. The repository instructions supplied with the task
  require gh api user immediately before committing, constructing the
  privacy-safe address from returned id/login, and setting repository-local
  identity for author and committer. The plan's general reference to an
  authenticated email does not resolve this more specific instruction.
* Concern: The recorded identity is not evidence of the currently
  authenticated account. Following the details literally can misattribute
  delivery or conflict with privacy protection if authentication differs.
* Impact: Commit/push publication can fail or use the wrong identity despite
  otherwise successful engineering validation.
* Smallest useful change: Replace the hardcoded operative identity with
  authenticated-account resolution, repository-local email configuration,
  and author/committer verification. Keep the requested coauthor trailer.
  If the authenticated account conflicts with an explicitly required
  identity, report the publication blocker rather than substituting or
  rewriting existing history.
* Action owner: Planning parent for P02-T02 wording; publishing parent for
  the live check.
* Exact resolving evidence: Revised task requires gh api user and the
  returned-id/login-derived noreply address; publication evidence records
  successful resolution, repository-local configuration and matching
  resulting author/committer identity without disclosing private email.
* Decision route: Directly applicable planner correction. No current owner
  decision is needed; only an observed authentication conflict would create
  a later publication blocker.

## Strengths and Residual Risk

* The plan does not turn the missing #103 link into a claim that full #103,
  FR-035 or AC-043 is delivered. It expressly leaves issue #166 open.
* Actual mutation regressions are required, not just JSON parsing. The
  implementation review should require canonical data and independent
  mutated copies to exercise the same assertions/helper, with each named
  invalid condition rejected. This fits within eight added test methods
  using subtests and test-local helpers; no runtime validator is justified.
* Preserve the existing gate/open-items assertions when replacing the stale
  missing-sensor assertion. The stated exception is an assertion update,
  not permission to remove the structural regression coverage.
* Sensor provenance needs careful compatibility handling:
  src/core/tests/test_synthetic_provenance.py:43-46 still expects DS-SENSOR
  visibility not-generated. A generator's existence is not proof that a
  dataset has been materialized. Within the locked test scope, retain an
  explicitly explained unmaterialized-output state while correcting the
  generator and intended ZF_DATA output, unless actual permitted evidence
  justifies a different state. Do not silently relabel it public or claim
  a full-stock run. The plan already requires this distinction.
* Project ruff/mypy exemptions are real. Evidence must include commands
  that actually bypass them for the changed inventory test, not simply an
  additional invocation that inherits the same ignores. Existing untyped
  methods may need typing/formatting within that already permitted file.
* The supplied partial/missing-row owner gate is not waived. This
  documentation/test-metadata iteration is not authorization to start a
  data-consuming build epic or generate the deferred datasets.
* Accepted residuals remain owner ratification, volume/scope and proposed
  row-owner decisions, historical-matrix reconciliation, full #103 evidence
  and real AI/SQL/Azure acceptance. Neither automated engineering review
  nor passing CI supplies those decisions.

## Questions or Blocking Evidence Gaps

No new decision-critical owner question is required for these corrections.
Unavailable owner/historical evidence is already honestly excluded from
local completion. Remote lifecycle assertions remain attributed to supplied
research; publication must perform its normal live checks.

## Limitations

No implementation, suite, linter, type checker, application smoke or remote
mutation was run. This assessment establishes executable-plan gaps from
source, not observed test failures. No source or supplied RPI input was
edited. Only this requested critique artifact is written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add pre-execution exclusion of private-file readers
  and honest partial-suite reporting to P02-T01, then apply PC-002 and
  PC-003 in the same revision.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md](.copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md) | Candidate plan assessed. |
| [.copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md](.copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md) | Phase instructions requiring direct corrections. |
| [.copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md](.copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md) | Supplied bounded research and remote evidence claims. |
| [.copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md) | Complete independent finding set and verdict. |

## Next Steps

The active planning parent should disposition PC-001 through PC-003, revise
the two planning inputs directly, and finalize without another critique.
Continue the authorized RPI loop only after those safeguards are explicit.
No user action is required. This reviewer stops here without implementation
or another critique.
