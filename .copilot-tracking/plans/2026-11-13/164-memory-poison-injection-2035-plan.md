---
title: "Plan: #164 criterion 3 memory poisoning and prompt injection gate"
ms.date: 2026-11-13
task_slug: 164-memory-poison-injection-2035
---

## Objective

Make criterion-3 evidence explicit and fail-closed in `chat_eval`, and extend the golden set with memory-poisoning and direct/indirect/cross-case/cross-role injection scenarios, all passing deterministically.

## Phases

1. [ ] Failing-first tests in `src/agents/tests/test_chat_eval.py` (details file, section A).
2. [ ] Add summary fields `critical_errors`, `memory_poisoning_passed`, `prompt_injection_passed` and gate fail-closed logic in `chat_eval.py` (section B).
3. [ ] Add golden scenarios in `chat_golden.json` (section C), bump `version`, update registry version string.
4. [ ] CLI output, README note, validation (ruff, mypy, test_chat* in core, agents, api).
5. [ ] Remove `/tmp/venv-164p-2035`, commit `Refs #164`, record `commit-complete`.

## Decisions

* The harness stays in `agents`; no `core` or `api` runtime change is needed (guards already pass).
* No `pass` outcome is introduced; enablement stays `insufficient` at best.
* One critique, one review.
