---
title: Issue 164 F2 research (memory probe scope in the synthetic chat evaluation)
description: Prospective research for a narrow offline report traceability correction, written before any plan or source edit
ms.date: 2026-11-08
---

## Disposition

Research executed 2026-11-08, before the plan, critique or any source edit. Planning Readiness: Ready, for the bounded offline report clarification only. This is a traceability gap, not a reproduced runtime defect. Issue #164 is Refs only: nothing here ticks or closes it.

## Source identities re-established (not assumed)

* Worktree HEAD and freshly fetched `origin/main`: `3c57a02d4d2ef61f6922436025b245c8a97e2694`; branch `fix/chat-eval-traceability-164`; working tree clean at start.
* The readiness assessment pinned `e73d421046d00565f610fb671a80e683d2981874`. `git merge-base --is-ancestor` confirms it is an ancestor of `3c57a02`, and `git diff --stat e73d421..3c57a02` shows one file, `.github/rubric/scores/latest.json`. No chat source moved.
* Blob ids at `3c57a02`: `chat_eval.py` 9c62b954, `test_chat_eval.py` 171e0de1, `evals/chat_golden.json` e0ae98cd, core `chat_panel.py` 5f7c5786, core `chat_isolation.py` b8a33880.
* Environment: Python 3.12.3. The pre-installed `zava-forward-*` distributions are editable installs of a different checkout (`/home/azureuser/source/ama`, HEAD `50c5a09`), so they do not test this worktree. Validation therefore uses an isolated temporary venv (`/tmp/f2-164-venv`) with `pip install -e src/core -e src/agents[dev]` from this worktree. This is environment isolation, not a missing-dependency failure. Baseline in that venv before any edit: `unittest tests.test_chat_eval tests.test_chat_heldout` ran 50 tests, OK.

## Evidence

Issue and readiness evidence read in full: the issue's memory criteria ("Memory poisoning and prompt-injection scenarios pass before enablement"; held-out, actual-model, human and approval criteria) stay unticked and out of scope. The readiness note is evidence for scope, not authorisation.

* `chat_eval.py` `_check_turn` (about lines 235-242): when a turn has `isolation_contains` or `isolation_forbid`, the evaluator calls `run.iso.build_prompt(...)` and asserts on that separate prompt. It is a component probe of `ChatIsolation`, not of the prompt the panel sends.
* `chat_isolation.build_prompt` (lines 105-117) includes `memory_for(...)` output as a `memory` block. `chat_panel.py` has no `memory_for` call; its receipt records `memory_used=False` (line 402). The serving panel prompt is built from sources, user history and the question only.
* Golden `memory-poisoning` scenarios: `memory-poisoning-has-no-authority` (isolation probe turn plus a serving refusal turn; also asserts the seeded text is absent from the serving prompt via `prompt_forbid`) and `memory-special-category-rejected` (isolation_forbid probe plus a serving answer turn). Only these two use isolation assertions.
* `gate_results` reports the `memory-poisoning` category pass/fail by aggregating those scenarios with no scope, so a passing gate row can read as integrated memory-poisoning coverage. `summarise`, `evidence` and the plain CLI likewise never name the boundary.
* Existing truthful qualifications to retain unchanged: scripted/development set, `actual_model_evaluation` and `human_effectiveness` "not evaluated", `held_out` "not produced", benefit claim "not permitted", enablement `insufficient`/`disabled`, thresholds "not approved".
* Consumers: `chat_heldout.py` calls `chat_eval.run_scenario` and `chat_eval.summarise` and reads only `rates` and bindings; adding keys cannot change its outputs (to be confirmed by running its tests). `src/agents/README.md` describes the chat evaluation in two places and is the only directly dependent document; the knowledge-base index and `docs/reference/log.md` do not describe this module's report fields, so no index or log change is required for a code-and-README correction.
* Existing tests that constrain the change: `test_report_binds_versions_and_states_what_is_not_evaluated` (report equality across two runs, so any new fields must be deterministic), `test_per_category_gates_are_explicit_and_insufficient_when_absent`, `test_consumption_is_reported_...` (receipts `memory_used` false), CLI tests.

## Decisions

* Add reporting fields only: a per-scenario count of isolation probes executed and serving receipts' `memory_used` turns; a summary `memory_scope`; scope fields on the `memory-poisoning` gate row; an `evidence.memory_scope` statement; one open item; two plain-CLI lines and a README paragraph.
* Derive the serving statement from receipts: report "not exercised, no panel memory consumed" only when no receipt has `memory_used` true, otherwise report the deviation instead of asserting it.
* Leave outcome values, thresholds, `bindings` (including `memory_version` and `policy_version`), `missing_evidence`, registry state and all runtime code unchanged. A passing component probe keeps its current pass; the report adds the qualification.

## Out of scope, kept

Wiring memory into `ChatPanel`, any Core/API change, new scenarios or labels, held-out data, model or provider calls, Azure, thresholds, prices, approvals, issue or board mutation, push, PR.

## Unresolved

* #108 and #159 remain complete-acceptance dependencies; #164's status labels are inconsistent and are not touched here.
* Integrated memory-poisoning coverage cannot be produced until memory is genuinely consumed in the serving path, which needs separate privacy, release and owner decisions.
