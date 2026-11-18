<!-- markdownlint-disable-file -->
# RPI Changes: PR #1745 Cycle-2 Rebase of Issue #1288 onto `origin/feat/demo-164-chat-grounding-provenance-0900`

## Metadata

* Task ID: quality-1288-sensor-ai-2142-c2
* Related plan: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`
* All remaining active-plan markers: None
* Status basis: Rebased `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` (`4df840df3`), resolved `_sensor(r: Reply)` in `src/core/src/zava_forward/core/chat_case_answers.py`, added two focused `DomainAnswerTests` seam methods in `src/core/tests/test_chat_case_answers.py`, passed all targeted `-p` test suites and bare `mypy`/`ruff` static checks across `src/core`, `src/agents`, and `src/api`, and reconciled pre-review artifacts.

## Execution Summary

Rebased `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf` -> `4df840df3`) directly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238f78e37e31baaed87f5d1eb81943cf14`), resolving the sole merge conflict in `src/core/src/zava_forward/core/chat_case_answers.py` (`_sensor(r: Reply)`). Under `if not cite:`, `_sensor(r)` checks `conflict = r.fact("sensor.conflict")` first and returns early with the Issue #1288 conflict refusal before `r.fact("sensor.detail")` can emit `"No retained sensor reading is shown for this case."` or add a `case-record` citation; when `not conflict`, it preserves upstream `#157`/`#164` (`2b1d40db0`) behavior by emitting `detail` when present and delegating to `return _damp(r)`. Added two strict-typed (`-> None`) seam test methods in `DomainAnswerTests` (`src/core/tests/test_chat_case_answers.py`), verified static and `-p` test checks across `src/core`, `src/agents`, and `src/api`, and prepared the local pre-review commit without pushing.

## Completed Work

### Rebased `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and Resolved `_sensor(r: Reply)`

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/chat_panel.py` (clean auto-merge), `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json`
* What changed and why: Configured local privacy-safe git identity (`jmservera <8036360+jmservera@users.noreply.github.com>`) via `gh api user`, rebased `a2a39b2cf` onto `5f50fc238` (`4df840df3`), and resolved `_sensor(r: Reply)` in `chat_case_answers.py` so `sensor.conflict` preempts `sensor.detail` + `_damp(r)` on reading clashes while non-conflict `not cite` delegates to `sensor.detail` + `_damp(r)` and clean `cite` retains `sensor.source`.
* Completion evidence: `git merge-base origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` equals `5f50fc238f78e37e31baaed87f5d1eb81943cf14`; rebased commit `4df840df3` preserves all 19 files from `a2a39b2cf`.
* Validation: Passed (`src/core` `mypy`, `ruff check .`, and `ruff format --check .` passed immediately after rebase).

### Added `DomainAnswerTests` Seam Coverage and Verified `-p` Test Suites

* Related phase or task: `P02`, `P02-T01`
* Files: `src/core/tests/test_chat_case_answers.py`
* What changed and why: Added `test_sensor_conflict_preempts_damp_fallback_while_missing_reading_delegates_to_damp` and `test_sensor_rules_answer_preserves_skill_lens_and_citation_kinds` (`-> None`) to `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` (`1` test file modified, `0` removals, `2` methods added), verifying `answer()`, `ChatPanel._rules_answer(..., skill="funding-evidence")`, and `ChatPanel._source_kind(...)` across conflict, non-conflict `_damp(r)` fallback, and clean `sensor.source` regimes.
* Completion evidence: All targeted `-p` suites and static checks exited `0` across `src/core`, `src/agents`, and `src/api`.
* Validation: Passed (`12` tests in `test_chat_case_answers.py`, `60` in `test_chat_panel.py`, `4` in `test_sensor_view_conflicts.py`, `6` in `test_regulatory_chat_case_domain_grounding.py`, `14` in `test_quality_sensor_grounding.py`, `19` in `test_quality_sensors_correlation.py`, `191` (`94` skipped) in `test_quality_sensors.py`, `11` in `test_sensor_staleness_ui_badge.py`, `29` in `test_content_standard.py`, plus `mypy` and `ruff` in `src/core` and `src/api`).

## Implementation-Time Plan and Detail Updates

### Aligned Non-General Skill Lens Identifier and Citation Kind Expectations in `P02-T01`

* Affected plan area or markers: `P02-T01` in `.copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md`
* What changed: Updated the example non-general skill identifier in `P02-T01` from `"resident-communications"` to `"funding-evidence"` (an actual `assistants.REGISTRY` key whose `categories` omit `"hazards"` and `"sensor"`) and recorded `ChatPanel._source_kind` outputs (`"decision-rule"` for `hazards.*`, `sensor.conflict`, `sensor.source`; `"case-record"` for `sensor.detail`, `sensor.0.state`, `sensor.latest.citation`; `"workflow-rule"` for `workflow/domain-boundary`).
* Why: `"funding-evidence"` is a real registered non-general skill lens in `REGISTRY` that proves `skill_sources` `common` (`"sensor"`) and `RULES_SOURCE_ROOTS["sensor"] = ("hazards",)` preserve citations on the merged seam.
* Triggering evidence: `src/core/src/zava_forward/core/chat_panel.py` (`skill_sources`, `ChatPanel._source_kind`) and `src/core/tests/test_chat_panel.py`.
* User answer or decision: None needed (immediately relevant current-state update preserving approved intent).
* Reconciliation performed: Updated `P02-T01` in `c2-phase-details.md` and `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py`.
* Planning and critique state: Not needed; preserves `PC-002` disposition.

## Validation Record

* Validation tier classification (`owner decision D4 / issue #1294`): `focused` (targeted rebase conflict resolution in `chat_case_answers.py` + `1` unit test file; zero changes to workflows, gate tools, Dockerfiles, dependency manifests, SQL schemas, or Bicep/deployment assets). Hosted CI is unobserved locally because pushing is prohibited by caller instructions (`Do NOT push`).

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | `Success: no issues found in 328 source files`; `All checks passed!`; `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_domain_questions.py' -q` | `src/core` (caller-listed selector) | Skipped (`0` matching files at `5f50fc238`) | Exits `5` (`NO TESTS RAN`) on Python 3.12 because domain tests on `5f50fc238` live in `test_chat_case_answers.py` and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (both run below) |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_case_answers.py' -q` | `src/core` (`DomainAnswerTests` + `CitationBoundTests` + `UnblockTests`) | Passed | `Ran 12 tests in 0.004s OK` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_chat_panel.py' -q` | `src/core` (`HybridAttributionTests` + `ChatPanel` rules) | Passed | `Ran 60 tests in 14.549s OK` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_sensor_view_conflicts.py' -q` | `src/core` (`#1288` conflict detection) | Passed | `Ran 4 tests in 0.515s OK` |
| `PYTHONPATH=../core/src:src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat_case_domain_grounding.py' -q` | `src/agents` (`#157`/`#164` case-domain grounding) | Passed | `Ran 6 tests in 0.002s OK` |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | `Success: no issues found in 280 source files`; `All checks passed!`; `196 files already formatted` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensor_grounding.py' -q` | `src/api` (`#1288` sensor grounding & conflict refusal) | Passed | `Ran 14 tests in 13.687s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensors_correlation.py' -q` | `src/api` (`#1288` UI-to-snapshot correlation) | Passed | `Ran 19 tests in 21.608s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_quality_sensors.py' -q` | `src/api` (`#1288` end-to-end sensor workflow) | Passed | `Ran 191 tests in 140.560s OK (skipped=94)` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_sensor_staleness_ui_badge.py' -q` | `src/api` (`#1288` conflict vs offline badge precedence) | Passed | `Ran 11 tests in 0.001s OK` |
| `PYTHONPATH=... python3 -m unittest discover -s tests -p 'test_content_standard.py' -q` | `src/api` (plain-language lexical & sentence checks) | Passed | `Ran 29 tests in 0.238s OK` |
| Hosted GitHub Actions CI (`PR #1745`) | `feat/quality-1288-sensor-ai-2142` | Unavailable (unobserved) | Caller explicitly forbade pushing (`Do NOT push`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01` checked and marked `completed`).
* Completed-work evidence and handoff prose: Current across `c2-plan.md`, `c2-phase-details.md`, and `c2-changes.md`.
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active-plan markers, `2` carried-forward follow-ups).
* Review readiness: Ready for single-pass `rpi-review`.

## Blockers

* None.

## Remaining Work

* None.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md, `## Follow-Up Items`
* Adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` (`RV-001`, carried forward from parent Cycle 1).
* Add seeded conflicting-reading browser state in `src/api/checks/quality_sensors_browser_check.py` (`RV-002`, carried forward from parent Cycle 1).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`; remaining: none
* Validation coverage: Focused tier complete (`mypy` + `ruff` in `src/core` and `src/api` + `-p` unit/integration suites across `src/core`, `src/agents`, and `src/api`); hosted CI unobserved (unpushed per caller directive)
* Blockers: None
* Current plan and detail updates: Updated non-general skill key example in `P02-T01` to registered `"funding-evidence"` and exact `_source_kind` values
* Planning and critique state: Ready (`PC-001` and `PC-002` resolved)
* Follow-up items: `RV-001` and `RV-002` carried forward from parent Cycle 1
* Review readiness or no-handoff reason: Ready for `Review` (`rpi-review`)
* Continuation owner: Confirmed automatic RPI Agent parent
