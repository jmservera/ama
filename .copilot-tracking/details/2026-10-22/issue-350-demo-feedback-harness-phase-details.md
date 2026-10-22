<!-- markdownlint-disable-file -->
# RPI Phase Details: Offline demo-feedback acceptance harness (Refs #350)

## Metadata

* Task ID: issue-350-demo-feedback-harness
* Task slug: issue-350-demo-feedback-harness
* Related plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-harness-research.md

## Phase Index

| Phase ID | Name                  | Status | Detail sections        |
|----------|-----------------------|--------|------------------------|
| P01      | Implement the checker | ready  | P01, P01-T01, P01-T02  |
| P02      | Focused tests         | ready  | P02, P02-T01           |
| P03      | Validate and publish  | ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Implement the checker

### Context

No existing check consumes supplied deployed evidence (C1-C4). Runtime schemas are importable (C5-C12).

### Intent

A standalone, deterministic, offline script reporting four states per check.

### Boundaries

* Included: `tools/check-demo-feedback.py`.
* Excluded: any change to src, infra, gate, workflows, KB files; network, subprocess, env credentials.

### Likely Targets

* tools/check-demo-feedback.py: new file, hyphenated like existing `tools/rpi-checks.py`.

### Dependencies

* Installed zava_forward core and api packages.

### Validation Expectations

* Ruff clean (version recorded); P02 tests pass including the AST handler check.

### Completion Evidence

* Changes record lists the file and focused test output.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: Evidence loading, report model and CLI

#### Context

Overall rule: any `fail` gives `fail`; else any `blocked` gives `blocked`; all `not-run` gives `not-run`; otherwise (including all required checks `pass` with `spend_bound` and `admin_account` `not-run`, and any fixture origin) `blocked`. Overall `pass` is unreachable in this slice by design; reports state `acceptance: not-accepted`, a `gaps` list and a `self_declared` list. Runtime packages are imported lazily only when evidence is supplied; an import failure is a whole-run `blocked` naming the import.

#### Intent

Loader and CLI with bounded input and specific exceptions.

#### Boundaries

* Included: file size cap 1 MiB, regular file only, UTF-8 JSON object, `schema_version == 1`, `origin` in the two allowed values, `--format`.
* Excluded: directory scans, URLs, env lookups, stdin.

#### Likely Targets

* tools/check-demo-feedback.py: loader, `Check` result helper, overall computation, `main`.

#### Dependencies

* None

#### Validation Expectations

* Missing, oversized, malformed, wrong-type input produce a `blocked` overall with a reason and exit 2, never a traceback.

#### Completion Evidence

* Tests for each loader failure.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Check implementations

#### Context

Imports: `zava_forward.core.projection` (`STAFF_ROLES`, `CONTRACTOR`, `me_payload`, `NOTE_HELD`), `zava_forward.api.workbench.navigation`, `zava_forward.core.taskqueues.contract`, `zava_forward.core.ranking.CURRENT`, `zava_forward.core.store.Store.REC_LABEL` (class constant; read via attribute, no instance). An ImportError for these is reported as `blocked` for the whole run with the import name, not swallowed into success.

Evidence slots (runtime response bodies verbatim; harness-owned markers are listed as self-declared): `image.reference`; `me.status/body`; `programme.status/body` (the `/api/cases?view=all` page); `case_write.{synthetic, case_id, outcome, channel, before, write, after, restart_between_write_and_read, audit_before, audit_after}`; `ai.status/body` where body is the bare `POST /api/ai/priority` record (not the `GET` `{recommendation}` wrapper).

#### Intent

Each check implements its plan rules, with denial statuses (3xx, 401, 403) producing `fail` and non-200 other statuses `fail`.

#### Boundaries

* Included: the five check ids plus `spend_bound`, `admin_account` (always `not-run`).
* Excluded: inventing fields not in runtime responses; computing spend.

#### Likely Targets

* tools/check-demo-feedback.py

#### Dependencies

* P01-T01

#### Validation Expectations

* Covered by P02-T01.

#### Completion Evidence

* Per-check test names in the changes record.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Focused tests

### Context

Fixtures must come from runtime builders so schema drift fails the tests.

### Intent

Cover pass, fail, blocked, not-run for each check; the fixture cap; loader errors; denial-not-success; 60,000 vs 980; template/workflow-only vs real; held outcome; no restart marker; determinism; no-evidence invocation touches nothing.

### Boundaries

* Included: `tools/test_check_demo_feedback.py` using unittest and `importlib` to load the hyphenated script.
* Excluded: network, subprocess, real stores, AI calls.

### Likely Targets

* tools/test_check_demo_feedback.py: new.

### Dependencies

* P01

### Validation Expectations

* `python -m unittest tools.test_check_demo_feedback` equivalent run from repo root in the venv.

### Completion Evidence

* Test counts and output in the changes record.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Unittest module with synthetic fixtures

#### Context

Test ownership locked: additions limited to this one module; no removals; semantic coverage (state rules) plus a small number of regression cases (loader bounds). Fixture users are synthetic dicts with `example.test` emails.

#### Intent

Deterministic tests.

#### Boundaries

* Included: all states; excluded: gate integration.

#### Likely Targets

* tools/test_check_demo_feedback.py

#### Dependencies

* P01-T02

#### Validation Expectations

* All tests pass; Ruff clean.

#### Completion Evidence

* Unittest output.

#### Unresolved Items

* None

<!-- rpi:phase id=P03 -->
## P03: Validate and publish

### Context

The gate cannot discover the new test module; `--extra-test` accepts only tracked project selectors (C15), so the module is run directly and the unchanged gate is run on the committed candidate.

### Intent

Evidence-bound publication as a draft PR.

### Boundaries

* Included: focused tests, Ruff, review, commit, `git fetch`, full gate with `--lock-timeout` long and a new external `--out`, receipt verification, push, `gh pr create --draft` with `Refs #350`.
* Excluded: merge, protection changes, closing keywords.

### Likely Targets

* Git history and PR only.

### Dependencies

* P01, P02, Review evidence committed first.

### Validation Expectations

* Receipt verifies against current origin/main immediately before push.

### Completion Evidence

* Exact head, receipt path and SHA-256 recorded in the PR body.

### Unresolved Items

* None

<!-- rpi:task id=P03-T01 -->
### P03-T01: Validation, gate and draft PR

#### Context

Pip, installed packages, no `PYTHONPATH=mvp`, no uv; do not alter gate environments or images.

#### Intent

Publish only with a verified receipt.

#### Boundaries

* Included: as in P03.
* Excluded: a gate failure is investigated, never bypassed.

#### Likely Targets

* none

#### Dependencies

* Review committed

#### Validation Expectations

* Gate passes or the blocker is reported.

#### Completion Evidence

* Receipt verify output.

#### Unresolved Items

* None
