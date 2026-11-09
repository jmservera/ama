---
title: Issue 164 F2 changes record
description: Implementation and focused validation record for the memory probe scope reporting correction
ms.date: 2026-11-08
---

Base `3c57a02d4d2ef61f6922436025b245c8a97e2694`, branch `fix/chat-eval-traceability-164`. Written after the research, plan, details and critique files existed.

## Changes

* `src/agents/src/zava_forward/agents/chat_eval.py`: constants for the component-probe scope, serving-path and integrated-coverage statements; `Run.component_probes` counted only when the isolation prompt is built; `run_scenario` returns `component_memory_probes` (the run is bound before the try block so a failed or never-constructed run reports executed probes only, 0 when none); new `memory_scope(results)` in `summarise`; `memory-poisoning` gate row carries `component_probes`, `memory_assertion_scope`, `serving_path_coverage` and `integrated_memory_poisoning`; `evidence.memory_scope`; one open item; two plain-CLI lines.
* `src/agents/tests/test_chat_eval.py`: three behavioral cases (component-only label with unchanged gate pass and serving not exercised; serving coverage unknown without or with partial receipts and deviation when a receipt shows memory used, including a report lacking `memory_scope`; scenario without a probe and a failed constructor run) plus two CLI assertions.
* `src/agents/README.md`: one paragraph in the chat evaluation section.

## Critique dispositions applied

CR-001 (receipt-derived tri-state), CR-002 (qualify memory assertions, report probes executed) and CR-003 (count survives failure) implemented as accepted. Deviation from the details wording: a pre-try `run = None` binding replaces a separate counter holder; behavior is identical.

## Not changed

Core, API, `ChatPanel`, golden data, `chat_heldout.py`, thresholds, prices, labels, registry, `bindings`, enablement outcome, `missing_evidence`, KB index and log (no durable KB page changed).

## Validation (CI-first focused tier, no FULL gate)

* Environment: Python 3.12.3; the pre-installed `zava-forward-*` editable installs point at `/home/azureuser/source/ama` (HEAD `50c5a09`), not this worktree, so an isolated venv `/tmp/f2-164-venv` was built with `pip install -e src/core -e "src/agents[dev]"` (exit 0; not a missing-dependency failure). ruff 0.17.3, mypy 2.4.1.
* Baseline before edits, from `src/agents`: `PYTHONPATH=../core/tests python -m unittest tests.test_chat_eval tests.test_chat_heldout`: 50 tests OK.
* After edits, same command: 53 tests OK, no skips.
* `ruff format` applied to the two changed Python files (one reformatted); `ruff check src tests`: all checks passed; `mypy` (project strict config): no issues in 45 source files.
* Outcome preservation: `python -m zava_forward.agents.chat_eval --json` at base versus after, with the new fields removed, compared equal (results, summary, bindings, gates, enablement, evidence). CLI exit 0, enablement `insufficient`, task `disabled`.
* Not run: other agents suites, core/api suites, SQL, browser, scanner, image, FULL gate, hosted CI. They remain publication gates with independent exact-head assessment.
