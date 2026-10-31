<!-- markdownlint-disable-file -->
# Review: Chromium pathname admission

## Scope and Evidence

* Task ID: 608
* Task slug: gate-chromium-path-608
* Review date: 2026-10-31
* Scope: Full P01-P02 task, focused tooling tier.
* Assessed boundary: pathname admission, CLI/resume/Runner, owned output,
  cleanup, source/receipt identity, regression coverage and documentation.
* Plan: .copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md
* Details: .copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chromium-path-608-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/gate-chromium-path-608-changes.md
* Research: .copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md
* Reviewed base: 87bf629c630314f5be086697e322e1b0ec22277d (fetched origin/main).

## Opening Review State

* Goal: independently assess correctness of admitted/rejected paths and preserved boundaries.
* Evidence readiness: full artifact set reconciled; all plan markers checked,
  six new tests and 54-test pass, isolated Ruff pass.
* Acceptance basis: user request, #608 criteria 1-2, plan, PC-001 disposition.
* First boundary: exact source diff and independently assessed resume probe ordering.
* Read-only boundary: no source/plan/changes edits; only this canonical Review record.
* Initial blockers: None for focused Review; actual full browser/SQL remains residual.

## Execution Status

* Execution status: Complete.
* Exactly one independent read-only correctness lens executed.
* Independent lens verdict: Approve within focused scope; no significant functional defects.
* Lens also passed independent in-memory boundary/Unicode/constructor/resume
  ordering checks, isolated Ruff and diff checks. It did not rerun fixture suite.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Shared admit_browser_output; main, Runner and validate_receipt wiring | Reconciled; filesystem byte limit correct, rejected paths stop before tools/writes/lock |
| P01-T02 | Six methods, no removals; local gate documentation | Reconciled; boundary, Unicode, alias, real resume and preserved-contract coverage |
| P02-T01 | 54-test pass after formatting, isolated Ruff pass | Reconciled; full gate deliberately not run |
| Follow-Up Items | Actual browser/SQL criterion 3 outside focused tier | Open distinct follow-up, not active implementation defect |

## Completed Work Assessment

Formula is 107 -45 -4 =58 output bytes. Tests bind a real 107-byte socket,
reject 108 bytes, and prove 58/59 output boundary. Browser-only selection
condition preserves browser-free long outputs. Main resolves aliases and
retains new/external output checks. Runner backstop precedes owned writes.
Long all/changed/resume cases assert no tool/lock/Runner/verify call and no new
output or receipt. No scanner, workflow, cleanup, environment or receipt schema
change is present; WORKFLOW_HASHES are unchanged.

## Implementation-Time Plan and Detail Update Assessment

Validation command refinement from global Ruff defaults to the existing
Runner.lint isolated selector is justified local judgment, not a scope change.
The initial failure remains recorded rather than overwritten. All declared
markers, phase status, changes, handoff, blockers and follow-ups reconcile.

## Critique and Material Revision Assessment

Original critique execution Complete / verdict Revise remains immutable.
PC-001's direct disposition is implemented: validate_receipt checks new output
after integrity/schema/recomputed selection/source validation, before tool
probes and recursive provenance verification. Admitted paths continue unchanged
validation; default None preserves standalone verification. Regression cases
use the real fixture validation path, verify tools are reached on admission,
and reject source/integrity tampering. No repeat critique or premature work.

## Plan Follow-Up Assessment

| Follow-up | Why outside scope | Owner / action | Route |
| --- | --- | --- | --- |
| Actual full browser and SQL groups, zero skips | Caller selected focused tooling, excludes heavy lock/full gate | CI/full-run owner retains actual full evidence on supported short external path | Distinct verification follow-up for #608 criterion 3 |

## Findings

No implementation defects or unresolved decision gaps found in the complete
focused boundary. Severity counts: Critical 0, High 0, Medium 0, Low 0.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Actual full browser/SQL execution evidence remains outstanding

* Scope: issue #608 criterion 3; not an active P01-P02 defect.
* Evidence: changes Validation Record explicitly excludes heavy/full gate;
  focused fixture checks do not launch Chromium or SQL.
* Impact: all issue criteria cannot yet be claimed proven.
* Destination: distinct follow-up, CI/full-run owner.
* Next action: execute real full browser/SQL groups without skips on supported
  short external output, retain authoritative evidence; use Refs #608 meanwhile.

## Defects

None. Focused correctness is conformant, but full issue acceptance is not claimed.

## Routed Findings

| Finding | Destination | Owner / action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct full-run verification follow-up | CI/full-run owner | Residual evidence outside focused tier, not implementation defect |

No return to Implement or second Review is part of this task.

## Validation Evidence

| Command / check | Status | Summary |
| --- | --- | --- |
| python3 -m unittest tools.test_rpi_checks | Passed | 54 tests; repeated after formatting, exit 0 |
| python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py | Passed | Existing tooling selector |
| python3 -m ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py | Passed | Both files formatted |
| git diff --check | Passed | No whitespace errors |
| Initial global-config Ruff check | Failed; corrected selector | 16 pre-existing diagnostics recorded; no unrelated fixes |
| Independent read-only in-memory regression lens | Passed | Socket budget, Unicode, constructor and resume/default validation ordering |
| Heavy local full/browser/SQL gate | Not run | Explicit focused tier; no full or partial receipt created |
| Human/hosted approval | Not performed | CI/owner gates remain required |

## Blockers and Remaining Work

No active P01-P02 work or implementation blocker. Full issue acceptance is
blocked on RV-001 and hosted/owner gates; publication may proceed under explicit
focused-tier user authorization with Refs #608, not a closing keyword.

## Outcome

* Outcome: Residual work.
* Rationale: focused implementation conforms, independently approved with no
  defects; actual full browser/SQL evidence remains outstanding (RV-001).

## Closeout Routing Record

| Finding class | Destination | Owner / action |
| --- | --- | --- |
| Implementation defect | None | None |
| Decision gap | None | None |
| Material design research gap | None | None |
| Non-blocking task residual | Distinct full-run evidence follow-up | CI/full-run owner, RV-001 |

Review execution Complete; outcome Residual work. Automatic parent may commit,
push and open PR as explicitly requested; no merge, live gate or approval inferred.

## Later Hosted Fixture Finding and Correction (2026-10-31, PR #610)

The original one-pass independent Review and its outcome above are historical.
Copilot thread PRRT_kwDOUU8JX86yStiP later identified an uncovered environment:
Runner.static uses owned TMPDIR, inflating nested fixture paths. Its 61-byte
cancel-False output and 88-byte self.out at a 58-byte outer output invalidate
the earlier ordinary-TMPDIR coverage claim. The defect is in tooling fixtures,
not evidence that the production guard should be weakened.

User-selected P03 implements that hosted finding. Real pathname tests now own
short temporary roots independently of the outer TMPDIR. Mock-only constructors
use explicit browser-free selections; cancellation retains preflight execution
and owned child/container cleanup. Production admission is unchanged.

### Bounded correction assessment and evidence

Direct assessment of the changed test diff found no remaining defect within
this fixture correction. This is not a repeated independent Review or closure
of RV-001. One new regression runs ten affected methods under Runner-owned
TMPDIR at 18/58/100-byte outer outputs. The complete 55-test focused suite also
passed independently in each of those three ambient contexts, in fresh child
processes, after formatting. Existing isolated lint/format and diff checks pass.
Real 107/108-byte Unix socket and 58/59-byte output assertions remain intact.

* Correction execution: implementation and focused validation complete.
* Publication/thread resolution: pending commit and non-force push.
* Full browser/SQL, CI and human acceptance: not performed or inferred.
* Original Review: execution Complete / outcome Residual work, unchanged.
* Later hosted finding: source correction validated; publish then reply/resolve.
* Issue relationship: Refs #608 only; RV-001 remains outstanding.
