---
title: Issue 164 F2 phase details
description: Phase details for the memory probe scope reporting correction
ms.date: 2026-11-08
---

## Phase 3 design

* `MEMORY_SCOPE` constant in `chat_eval.py` holding three statements: component probe label (`ChatIsolation.build_prompt` memory assertions are component-only diagnostics, not serving-path or retained-memory acceptance), serving path ("not exercised: no panel memory consumed" when receipts agree), integrated memory-poisoning coverage ("not covered").
* `Run.component_probes` counter incremented in `_check_turn` each time the isolation prompt is actually built; `run_scenario` returns `component_memory_probes` and `serving_memory_used_turns` (count of `memory_used` true receipts). Counter defaults to 0 if the run fails to construct.
* `summarise` adds `memory_scope`: `component_probe_scenarios` (ids), `component_probes`, `component_probe_scope`, `serving_receipts`, `serving_memory_used_turns`, `serving_path_coverage` (derived), `integrated_memory_poisoning`.
* `gate_results`: rows for `memory-poisoning` gain `scope="component-only ..."` and `serving_path="not exercised ..."`; other rows and all outcomes unchanged. Rows are derived from the report so a stale or foreign report without `memory_scope` still works.
* `run_eval` evidence gains `memory_scope`; `OPEN_ITEMS` gains one item. Plain CLI prints a component-probe line and a serving-path line.
* README: one paragraph in the chat evaluation section.

## Phase 3 tests (existing file, few cases)

* Report carries component-only label, probes counted as 2 scenarios, serving coverage "not exercised", zero `memory_used` turns, and the memory-poisoning gate row still passes with scope fields (no integrated implication).
* Serving-path derivation reports the deviation when a receipt shows `memory_used` true (synthetic summary input, no runtime change).
* Existing non-memory outcomes preserved: other gate rows lack scope fields; enablement, rates, bindings unchanged (existing tests plus an assertion that bindings and non-memory gate rows keep their shape).
* Plain CLI prints the scope lines.

## Phase 4 validation

Commands in `/tmp/f2-164-venv` from `src/agents`: `PYTHONPATH=../core/tests python -m unittest tests.test_chat_eval tests.test_chat_heldout`; `ruff check` and `ruff format --check` on the changed files; `mypy` with the project config. Record exits, skips and identities in the changes record.

## Critique amendments (applied before implementation)

* CR-001: `serving_path_coverage` is `not exercised: no panel memory consumed` only when receipts exist and all carry `memory_used` false; no or incomplete receipts give `unknown: no serving receipts`; a true receipt gives a deviation statement.
* CR-002: the scope text qualifies the isolation memory assertions only; the gate row reports probes executed; test a memory-category scenario without a probe.
* CR-003: probe count held in a counter created before the try block so partial and constructor-failure runs keep completed counts.
