---
title: Issue 164 F2 correction1 research (receipt-declared wording and execution-completeness guard)
description: Prospective research for corrective RPI correction1 of candidate b2f35d06, written before the correction1 plan, critique or any source edit
ms.date: 2026-11-08
---

## Disposition

Research executed 2026-11-08 for a NEW corrective task. Planning Readiness: Ready. The original research, plan, critique, changes, Residual-work Review and state for candidate `b2f35d066a3923c084acdc4c00f44d050d7539b2` are preserved unchanged and remain adverse historical evidence. Nothing here backfills or replaces them. Issue #164 stays Refs only.

## Identity

* Start HEAD `b2f35d066a3923c084acdc4c00f44d050d7539b2`, branch `fix/chat-eval-traceability-164`, no tracked or untracked changes. Freshly fetched `origin/main` is `3c57a02d4d2ef61f6922436025b245c8a97e2694` (unchanged from the original base).
* Blobs at start: `chat_eval.py` 2ab1a9e0, `test_chat_eval.py` b9011650.
* Ignored directories present and protected, not cleaned: `src/agents/.mypy_cache`, `src/agents/.ruff_cache`, `src/agents/src/zava_forward/agents/__pycache__`, `src/agents/src/zava_forward_agents.egg-info`, `src/agents/tests/__pycache__`, `src/core/src/zava_forward/core/__pycache__`, `src/core/src/zava_forward_core.egg-info`. State is clean for tracked and untracked files only, not ignored-inclusive.
* `/tmp/f2-164-venv` imports `chat_eval` from this worktree (verified by `__file__`). No package install is needed.

## Inputs genuinely read for this task (honest ranges)

The original transcript did not establish the repository-mandated reading before original planning; this record starts from the reading below, done before the correction1 plan.

* `docs/case_study_48_original.md`: all 49 lines read; the display clipped long paragraph lines at 220 columns, so only their opening text was seen. Headings, agent table and governance lines were read.
* `docs/case_study_48_addendum.md` (1977 lines): lines 1-22 (purpose and status), 967-1000 (Responsible AI release position) and 1098-1130 (baseline acceptance and constructed evidence register), plus the full heading outline (every `##` and `###`), with lines clipped at 300 columns. Not read: the remaining body, including solution, economics and tokenomics sections, and the RAI section after line 1000. Relevant takeaway: constructed or source-tested evidence is bounded engineering, not actual-model quality, human review or release; held-out and human evidence stay separate gates.
* `docs/reference/README.md` (993 lines): lines 1-60 (purpose and usage start) and a grep for chat mentions. Not read: the rest of the index. No index row found describes this module's report fields.
* `docs/reference/memory.md` (67 lines): the whole file was displayed. Memory is context, not evidence.
* `src/agents/README.md` (1025 lines): lines 40-135 (chat consumption evidence, evaluation commands, the b2f README paragraph, threshold and authorisation sections, the isolation fixtures), plus the single chat evaluation bullet near line 415 read in the original task. Not read: the other sections.
* Review input: coordinator review of `b2f35d06` (Request changes), read in full.

## Evidence

* Reproduced RV002 on `b2f35d06` with valid temporary directories: `grounding-cited-follow-ups` passes with 3 receipts; `memory-poisoning-has-no-authority` with `cases=[]` fails with `check=unexpected` and 0 receipts. `memory_scope` over both says `not exercised: no panel memory consumed (receipts memory_used false)`. Surviving receipts certify a scenario that produced none.
* Result shape (`run_scenario`): the only path to `check=unexpected` is the outer `except Exception` around setup, `apply`, the loop and the non-AI probe. Expected assertion failures (for example a wrong `kind`) append `check=kind` and keep the run's receipts: reproduced with the golden scenario altered to expect `answer`: `passed` false, 2 receipts, failures `['kind']`, execution completed. `Run.ask` already catches per-turn errors, and refusals and permission errors are normal outcomes. So `passed` and `failures` must not be the guard; an explicit completion marker from `run_scenario` distinguishes an execution that stopped early.
* All 24 golden scenarios currently produce at least one receipt, but a scenario of only refused turns could legitimately have none; the guard therefore keys on execution completeness, not per-scenario receipt count. A report with no receipts anywhere remains unknown.
* RV001 confirmed: `chat_panel.py:402` sets `memory_used=False` as a literal (also `server.py:911`), so the statement is declared by receipts, not observed. The b2f text in `chat_eval.py` (`SERVING_NOT_EXERCISED`, the `OPEN_ITEMS` entry "serving-path memory is not exercised", `INTEGRATED_MEMORY`) and the README paragraph say "no panel memory consumed" or "not exercised", and the static open item asserts it even when the dynamic summary is unknown or deviation.
* Late partial-probe case: a probe increments `Run.component_probes` after `build_prompt`; a later exception leaves the run object bound, so counts survive (original design). Never tested at `b2f35d06`: the original critique claimed partial-execution coverage but the diff only contained constructor-failure and no-probe cases. That claim stays as history; correction1 identifies the added cases.
* Consumers: `chat_heldout.py` calls `run_scenario` and `summarise` and reads only rates and bindings, so added keys are harmless.

## Decisions

* Receipt-declared wording for every memory-use statement (false, true, unknown); component-only diagnostics stay separate from serving, retained and integrated acceptance.
* Add `execution_complete` to each `run_scenario` result (true only when the whole run finished without the unexpected exception). `memory_scope` reports unknown when any result is incomplete or lacks the marker, or receipts are absent or lack a boolean `memory_used`; list `incomplete_scenarios` and keep component probe counts.
* Make static `OPEN_ITEMS` and the README not assert observation; point to `summary.memory_scope` for the receipt-declared status.
* No change to outcomes, rates, gates, bindings, enablement or task state.

## Out of scope

Core, API, runtime memory wiring, golden or held-out data, thresholds, prices, approvals, provider or Azure, issue or board changes, primary checkout, ignored directory cleanup.
