<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 PR #1774 CI Correction Cycle 1

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Related plan: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`–`P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: None
* Status basis: All phases (`P01`–`P03`) and tasks (`P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`) completed and passed focused-tier verification across `src/core`, `src/agents`, `src/api` regulatory suites, and `tools/rename-zava-tests.py`.

## Execution Summary

Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), verified PR `#1774`'s sole topic branch is `feat/ai-216-citation-eval-2142`, and rebased `feat/ai-216-citation-eval-2142` cleanly onto `36aeddae345426fdf8ee53565fef1540979de967` (`be8fa85cb`) with all `2026-11-15` `c1` tracking files preserved. Updated `RegulatoryChat.bundle()` (`src/core/src/zava_forward/core/regulatory_chat.py`) so `provision_ids` is attached strictly when `len(result["cards"]) > 1` and a card's base `source_id` maps to multiple provisions in `sources`, restoring exact 10-field `regulatory-chat-v1` card compatibility for single-card and distinct-source lookups while keeping `#216` multi-card shared-source disambiguation fail-closed. Exported `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, updated `src/core/README.md`, added `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` in `src/core/tests/test_regulatory_eval_gates_216.py`, added the `PC-002` `_TESTS_DIR` `sys.path` guard to `src/agents/tests/test_regulatory_citation_card_gates.py` and `src/agents/tests/test_regulatory_gates.py` so verbatim file-path `unittest` invocation passes without `:tests:` on `PYTHONPATH`, and verified all focused-tier checks exit `0`.

## Completed Work

### Rebase PR #1774 Branch Onto Target Parent

* Related phase or task: `P01`, `P01-T01`
* Files: Git branch `feat/ai-216-citation-eval-2142` (rebased commit `be8fa85cb` atop `36aeddae345426fdf8ee53565fef1540979de967`)
* What changed and why: Fetched `origin`, verified `origin/feat/demo-164-chat-grounding-provenance-0900` equals `36aeddae345426fdf8ee53565fef1540979de967` (incorporating `#1772`, `#1766`, and `#1773`), verified `git show-ref` and `gh pr view 1774` confirm `feat/ai-216-citation-eval-2142` is PR `#1774`'s exact head branch (no `feat/demo-216-citation-eval-2142` ref exists), and rebased cleanly with zero conflicts and all `2026-11-15` `c1` tracking files preserved.
* Completion evidence: `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exited `0`; `git log -n 5 --oneline` shows `be8fa85cb` directly atop `36aeddae3`.
* Validation: Passed (`git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD`).

### Gate Card provision_ids Emission and Export Deterministic Comparator Alias

* Related phase or task: `P02`, `P02-T01`
* Files: src/core/src/zava_forward/core/regulatory_chat.py, src/core/src/zava_forward/core/regulatory_eval_gates.py, src/core/README.md
* What changed and why: Updated `RegulatoryChat.bundle()` to record per-card provision lists during card collection and attach `card_entry["provision_ids"] = pids` after refusal clearing only when `len(result["cards"]) > 1` and `any(provs_per_source.get(pid.split("@v", 1)[0], 0) > 1 for pid in pids)`, matching `_active_cards_link_provisions` 1-for-1 while preserving the exact 10-key `regulatory-chat-v1` card envelope on single-card and distinct-source bundles. Bound module-level `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` in `regulatory_eval_gates.py` (which uses module-scope public exports without `__all__`) and updated `src/core/README.md` (`#216` section) to document both.
* Completion evidence: Diff inspection across `regulatory_chat.py`, `regulatory_eval_gates.py`, and `src/core/README.md`, plus passing `src/core` and `src/agents` test/lint/type checks.
* Validation: Passed (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents`).

### Add Focused Regression Coverage for 10-Key Card Envelope and Comparator Alias

* Related phase or task: `P02`, `P02-T02`
* Files: src/core/tests/test_regulatory_eval_gates_216.py
* What changed and why: Added `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` verifying (1) `compare_chat_against_deterministic_rule_cards is compare_chat_against_rule_cards` and returns `measured_value == True` / `ship_mode == "chat_with_cards"`, (2) single-card `RegulatoryChat.bundle()` and `ask()` return exact 10-key `regulatory-chat-v1` card dicts (`"provision_ids" not in card`) and pass `grade_chat_turn`, and (3) a 2-card distinct-source bundle (`synthetic` + `synthetic-second`) preserves the 10-key card envelope while projecting both deterministic rule cards cleanly (complementing `test_c11`'s 2-card shared multi-provision source `provision_ids` assertions).
* Completion evidence: `Ran 89 tests in 97.805s — OK` in `src/core`.
* Validation: Passed (`PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q`).

### Execute Verbatim Focused Validation across Core and Agents

* Related phase or task: `P03`, `P03-T01`
* Files: src/agents/tests/test_regulatory_citation_card_gates.py, src/agents/tests/test_regulatory_gates.py, .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md
* What changed and why: Executed the verbatim Step 5 `src/agents` command first; confirmed `PC-002`'s predicted `ModuleNotFoundError: No module named 'regulatory_gate_fixture'` when running file-path `unittest` without `:tests:` in `PYTHONPATH`; applied the repository-standard `_TESTS_DIR = str(Path(__file__).resolve().parent)` `sys.path` guard to `test_regulatory_citation_card_gates.py` and `test_regulatory_gates.py` (with zero changes to `src/agents/src/`, `regulatory_gate_fixture.py`, or `evals/regulatory_gates_results.json`); then re-ran and passed every focused-tier command in `src/core`, `src/agents` (both verbatim file-path selector and CI `discover`), `src/api` regulatory tests, and `tools/rename-zava-tests.py`.
* Completion evidence: Exit code `0` across all validation suites, including `test_recorded_60000_home_report_matches_exact_rerun` matching `src/agents/evals/regulatory_gates_results.json` unchanged.
* Validation: Passed (all checks recorded in `## Validation Record`).

## Implementation-Time Plan and Detail Updates

### Activate PC-002 Test Import-Path Fallback in Two Target Agents Test Modules

* Affected plan area or markers: `P03`, `P03-T01` (`phase-details.md` `Boundaries` and `Likely Targets`)
* What changed: Recorded `src/agents/tests/test_regulatory_citation_card_gates.py` and `src/agents/tests/test_regulatory_gates.py` as `P03` targets carrying the 3-line `_TESTS_DIR` `sys.path` guard already pre-authorized by critique disposition `PC-002` in `plan.md`.
* Why: Verbatim execution of `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q` imports `tests.test_regulatory_citation_card_gates` with cwd `src/agents` rather than `src/agents/tests` on `sys.path`, raising `ModuleNotFoundError: No module named 'regulatory_gate_fixture'` without `_TESTS_DIR` insertion.
* Triggering evidence: Initial verbatim Step 5 run in `src/agents` (`ModuleNotFoundError` at `test_regulatory_citation_card_gates.py:9` and `test_regulatory_gates.py:15`).
* User answer or decision: Confirmed caller requirement to pass verbatim Step 5 command; pre-authorized by `PC-002` in `plan.md`.
* Reconciliation performed: Reconciled `P03` `Boundaries` and `Likely Targets` in `.copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md` and `P03-T01` in `.copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md`; `src/agents/src/`, `regulatory_gate_fixture.py`, and `evals/regulatory_gates_results.json` remain completely untouched.
* Planning and critique state: Ready (`PC-002` satisfied within approved plan boundary; no planning reconsideration needed).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` | Branch ancestry (`P01-T01`) | Passed | Exit `0`; `feat/ai-216-citation-eval-2142` rebased cleanly atop `36aeddae3` with `2026-11-15` `c1` files preserved |
| `cd src/core && PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q && ruff check . && ruff format --check . && mypy` | `src/core` focused suite (`AC-2`) | Passed | `Ran 89 tests in 97.805s — OK`; `All checks passed!`; `291 files already formatted`; `Success: no issues found in 344 source files` |
| `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` | `src/agents` verbatim Step 5 suite (`AC-3`) | Passed | `Ran 27 tests in 52.437s — OK`; `All checks passed!`; `62 files already formatted`; `Success: no issues found in 66 source files` |
| `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` | `src/agents` CI-equivalent regulatory discovery (`AC-3`) | Passed | `Ran 40 tests in 40.773s — OK` |
| `cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` | `src/api` downstream regulatory regression check | Passed | `Ran 75 tests in 21.187s — OK` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression check | Passed | `Ran 25 tests in 0.489s — OK` |
| `tools/rpi-checks.py` | Full local gate | Skipped | Focused validation tier applies to bounded Python contract/test correction (`D4` / `#1294`) and caller explicitly excluded `tools/rpi-checks.py` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` all checked; `Phase Index` all `Complete`).
* Completed-work evidence and handoff prose: Current (`Handoff` points to `Review`).
* Validation, blockers, remaining work, and follow-up items: Current (zero blockers, zero remaining active tasks, human governance gates tracked in `## Follow-Up Items`).
* Review readiness: Ready for single-pass `rpi-review`.

## Blockers

* None.

## Remaining Work

* None (`P01`–`P03` complete; local git commit follows `rpi-review` artifact creation per `AC-4` / caller Step 6 so `git status --short` is clean).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md, `## Follow-Up Items`
* Human governance gates for `#216` (`OwnerGateAgreement` dual-capacity sign-off by Legal/DPO and Compliance/Building Safety owners, live non-synthetic staff paired trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification) remain outside executable offline-harness scope (`Refs #216`).

## Return-to-Caller State

* Implementation execution status: Complete (Full plan `P01`–`P03`)
* Declared scope and markers: Full plan (`P01`–`P03`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier passed across `src/core` (89 regulatory tests, `ruff`, `mypy`), `src/agents` (27 verbatim + 40 discovered regulatory tests, `ruff`, `mypy`), `src/api` (75 regulatory tests), and `tools/rename-zava-tests.py` (25 tests); `tools/rpi-checks.py` skipped per focused tier and caller direction
* Blockers: None
* Current plan and detail updates: Recorded `PC-002` `_TESTS_DIR` `sys.path` guard in `P03` details
* Planning and critique state: Ready (`PC-001`–`PC-004` incorporated and verified)
* Follow-up items: Human governance gates for `#216` (`Refs #216`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
