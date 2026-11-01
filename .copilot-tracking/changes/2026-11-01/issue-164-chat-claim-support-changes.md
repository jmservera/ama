---
title: Issue 164 chat claim-support changes
description: Implementation evidence for the chat claim-support check
ms.date: 2026-11-01
---

## Changes

* `src/core/src/zava_forward/core/chat_panel.py`: `STATUS_CLAIM`, `unsupported_claims`, and its use before an
  answer is kept; module docstring updated.
* `src/agents/evals/chat_golden.json`: removed `known_gap` from the unsupported-claim scenario.
* `src/agents/tests/test_chat_eval.py`: golden run passes with no open gap; enablement is `insufficient` and
  disabled; direct `unsupported_claims` assertions; CLI exit codes follow.
* `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`: updated.

## Validation (focused tier)

* `chat_eval`: 24 scenarios, 61 turns, 0 failures, enablement insufficient, task disabled.
* agents unittest suite (PYTHONPATH=../core/tests): 142 tests OK. core chat panel tests OK; full core suite run
  was still in progress when this was recorded and CI is the evidence.
* ruff check, ruff format --check and mypy: clean for src/core and src/agents.
* No JS touched. No Azure live resource, secret or model call.

## Criteria status for #164

* Unchanged and still unmet: approved thresholds and reviewer, memory-poisoning pass "before enablement"
  (needs approval), held-out set, actual-model and human exercises, tokenomics actual-call limits.
* The unsupported-claim grounding critical gap is closed in scripted evidence only.
* PR uses `Refs #164`.
