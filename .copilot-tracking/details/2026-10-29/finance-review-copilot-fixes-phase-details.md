<!-- markdownlint-disable-file -->
# RPI Phase Details: Finance review Copilot fixes

## Metadata

* Task ID: finance-review-copilot-fixes-510
* Task slug: finance-review-copilot-fixes
* Plan: .copilot-tracking/plans/2026-10-29/finance-review-copilot-fixes-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Required-input diagnostics | Complete | P01-T01 |
| P02 | Per-draft unavailability | Complete | P02-T01, P02-T02 |
| P03 | Validation and local commit | Checks/Review complete; commit/gate pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Required-input diagnostics

<!-- rpi:task id=P01-T01 -->
### P01-T01: Blank and typed confirmation regressions

* Context: _valid is type-only; changing it to reject blanks would misleadingly
  produce Wrong schema value type. Instead omit stripped-empty strings from
  confirmed after valid type checking.
* Targets: form_review.py and existing FormReview class.
* Boundaries: preserve correction acceptance, evidence, raw value and history;
  do not trim stored strings or use generic truthiness.
* Coverage: required string and required_when string with "" and whitespace;
  inspect review report, diagnose report and reopened saved diagnostics.
  Blank controlling string yields conditional Unknown. Zero and false remain
  confirmed, satisfy requirements and trigger exact typed conditional branches.
* Completion: failing-before/passing-after test evidence plus full focused tests.
* Dependencies/unresolved items: none.

<!-- rpi:phase id=P02 -->
## P02: Per-draft unavailability

<!-- rpi:task id=P02-T01 -->
### P02-T01: Opaque unavailable entries and two-draft regression

* Context: _visible checks retained sources including history and diagnostics;
  catching outside _report prevents partial reports from leaking.
* Target: view loop, after actor and case authorization; catch only
  DocumentUnavailable and construct the fixed three-key result.
* Regression: two drafts share case/schema but retain different sources; first
  draft contains history and a recorded diagnosis. Remove source bytes, remove
  document metadata, or set scan pending/infected; exact opaque first entry and
  unchanged full sibling survive reopened reads. Restore evidence and show
  history/snapshots readable again. Assert no saves/scans/writes during view.
* Existing retained-source/snapshot tests: change read expectations only;
  review/diagnose keep raising DocumentUnavailable and state/audit stay intact.
* Keep real DocumentStoreError propagating and existing exact-source read tests.
* Dependencies/unresolved items: none.

<!-- rpi:task id=P02-T02 -->
### P02-T02: HTTP contract and documentation

* Update old one-draft HTTP quarantine test to 200/per-entry Unavailable.
* Add HTTP two-draft test if core coverage alone does not demonstrate GET 200
  with a readable sibling; maximum four new methods across both test files.
* Update core/API READMEs for required blanks and opaque entries versus POST 403.
* No web assets, new route or broader source-document change.

<!-- rpi:phase id=P03 -->
## P03: Validate and preserve local candidate

<!-- rpi:task id=P03-T01 -->
### P03-T01: Requested checks and independent Review

* Dependencies: P01/P02.
* Run from src/core with the external venv on PATH:
  `PYTHONPATH=src:tests:../agents/src:../agents/tests python -m unittest discover -s tests -p 'test_form_review*'`;
  `ruff check .`; `ruff format --check .`; `mypy`.
* Also run form staging and targeted HTTP tests with documented fixture paths.
* Before Review reconcile plan markers/details, changes, commands and blockers.
* Fresh independent reviewer assesses just this task's diff and evidence,
  writes original outcome once, and routes findings instead of re-review.
* Completion: .copilot-tracking/reviews/logs/2026-10-29/finance-review-copilot-fixes-review.md
  records Complete / Residual work, no code defects and RV-001 Low gate
  readiness. Original outcome is preserved; no second Review.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local commit and full-gate attempt

* Dependencies: P03-T01 and original Review preserved.
* Resolve authenticated GitHub id/login for local privacy-safe author/committer
  email; use required Co-authored-by trailer. No amend, push or merge.
* Check actual heavy-lock ownership, fetch origin main, run full gate only
  with nonqueued admission. New external receipt directory; no Azure commands.
* If prerequisites are absent or lock busy, record exact blocker and do not
  fabricate a passed gate. Never interrupt foreign ownership.
* Required human/hosted approvals remain unmet and outside local acceptance.
* Current gate eligibility observation: git status --short --ignored shows
  existing ignored caches/bytecode and editable-install metadata. clean_identity
  refuses ignored inputs. Preserve unknown/pre-existing scratch rather than
  deleting it under this task; local focused results remain valid, full gate
  remains blocked until a clean authorized candidate is available.
