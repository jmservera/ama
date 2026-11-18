<!-- markdownlint-disable-file -->
# RPI Phase Details: PR #1797 c2 Cross-PR Continuity SQL Gate Fix (Refs #81)

## Metadata

* Task ID: safety-81-exercise-gates-c2
* Task slug: safety-81-exercise-gates
* Related plan: .copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/safety-81-exercise-gates-research.md, src/core/src/zava_forward/core/assistants.py

## Phase Index

| Phase ID | Name                                                            | Status   | Detail sections |
|----------|-----------------------------------------------------------------|----------|-----------------|
| P01      | Continuity SQL Gate Stamp in `Assistants.challenge()`           | Complete | P01, P01-T01    |
| P02      | Focused Cross-Package Validation and Local Git Identity Check   | Complete | P02, P02-T01    |

<!-- rpi:phase id=P01 -->
## P01: Continuity SQL Gate Stamp in `Assistants.challenge()`

### Context

Research (`C1`, `C2`, `C3`, `C5`) verified that PR `#1787` (`#122`) added `assistant_tasks_gate_update` to `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS`, requiring `NEW.reviewed_revision = NEW.revision` and `NEW.review_gate_version = continuity_gate_state.gate_version` whenever `(OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)` or `NEW.state = 'accepted'`. PR `#1796` (`#220`) added `Assistants.challenge()` using pre-`#122` DML (`SET body=?,state=?,revision=revision+1`), causing `sqlite3.IntegrityError: continuity SQL gate mismatch` when rebasing `#81` (`PR #1797`) onto `feat/demo-164-chat-grounding-provenance-0900`.

### Intent

Update `Assistants.challenge()` in `src/core/src/zava_forward/core/assistants.py` to supply `review_gate_version=?` (`continuity.GATE_VERSION`) and `reviewed_revision=revision+1` alongside `revision=revision+1`, matching `Assistants.review()` (`assistants.py:3638-3641`).

### Boundaries

* Included: Single DML `UPDATE assistant_tasks` statement in `Assistants.challenge()` (`src/core/src/zava_forward/core/assistants.py:4064-4067`), formatted to `src/core/pyproject.toml` `line-length = 100`.
* Excluded: Modifying `SQLITE_ATTEMPT_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `Assistants._row()`, `Assistants.review()`, or any `#81` safety/consent gate module.

### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`: Surgically update `Assistants.challenge()` `db.execute(...)` statement (`<= 100` columns; do not invoke `ruff format` directly on `assistants.py` because `src/core/pyproject.toml` excludes it under `[tool.ruff.format] exclude` per `PC-001`; verify via directory-scoped `python3 -m ruff check . && python3 -m ruff format --check .`).

### Dependencies

* None.

### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_challenge_no_retaliation_220.py tests/test_restart_gate_sql_fences.py -v` in `src/core` passes.

### Completion Evidence

* Updated `src/core/src/zava_forward/core/assistants.py` passing `ruff check .`, `ruff format --check .`, `mypy`, and `#220`/`#122` unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update `Assistants.challenge()` `UPDATE assistant_tasks` in `src/core/src/zava_forward/core/assistants.py`

#### Context

In `Assistants.challenge()` (`assistants.py:4064-4067`), `db.execute("UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?", (canonical(stored), state, tid, revision))` omits `review_gate_version` and `reviewed_revision=revision+1`. Research (`C4`) confirmed neither column is selected by `_row()` or used by Python review logic.

#### Intent

Stamp `review_gate_version=continuity.GATE_VERSION` and `reviewed_revision=revision+1` in `Assistants.challenge()` while keeping line length `<= 100` (`src/core/pyproject.toml`).

#### Boundaries

* Included: `Assistants.challenge()` `UPDATE assistant_tasks` SQL string and parameter tuple in `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Adding new tests (existing `test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py` directly exercise all 5 `challenge` sub-actions: `open`, `update`, `escalate`, `resolve`, `reopen`).

#### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`

#### Dependencies

* None.

#### Validation Expectations

* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`.

#### Completion Evidence

* Clean diff in `src/core/src/zava_forward/core/assistants.py` formatted to `line-length = 100`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Cross-Package Validation and Local Git Identity Check

### Context

Research (`C8`) identified that the actual `#81` test module in `src/core/tests/` is `test_safety_consent_exercise_scenarios_81.py` (whereas caller shorthand wrote `test_safety_consent_exercise_gates_81.py` and `test_safety_consent_exercise_gates_81_api.py`). Running the real `#220`, `#122`, `#81`, and content-standard suites across `src/core` and `src/api` plus `ruff`, `mypy`, and `tools/rename-zava-tests.py` verifies `10/10` CI parity.

### Intent

Execute full Focused-tier validation across `src/core`, `src/api`, and repository root, and confirm local noreply git author/committer configuration ahead of post-Review commit closeout.

### Boundaries

* Included:
  * `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_challenge_no_retaliation_220.py tests/test_restart_gate_sql_fences.py tests/test_safety_consent_exercise_scenarios_81.py -v`
  * `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_challenge_no_retaliation_api_220.py tests/test_continuity_restart_gate.py tests/test_content_standard.py -v`
  * `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`
  * `cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy`
  * `python3 tools/rename-zava-tests.py`
  * Confirm `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`) and `git config --local user.name` (`Juan Manuel Servera`).
* Excluded: Pushing to `origin`.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run Focused `src/core`, `src/api`, and migration validation suites and verify local git identity

#### Context

Matches `.github/workflows/src-ci.yml` `src-core` and `src-api` lint, type-check, and unit-test commands locally.

#### Intent

Prove zero errors or regressions across `#220`, `#122`, and `#81` in both `src/core` and `src/api` and verify local git author configuration.

#### Boundaries

* Included: Validation commands listed under `P02` Boundaries and local git config check.
* Excluded: Remote git operations.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md`

#### Dependencies

* `P01-T01`

#### Validation Expectations

* All five command groups exit `0` with non-zero test counts and zero lint/format/type findings.

#### Completion Evidence

* Recorded command outputs and counts in `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md`.

#### Unresolved Items

* None.
