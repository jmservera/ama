---
title: Issue 157 memory-as-evidence boundary changes
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Summary

One test method added: `ApiTests.test_active_chat_memory_is_never_evidence_for_a_chat_proposal` in `src/api/tests/test_assistants.py`. No production file changed. Refs #157; the criterion "No memory is used as evidence for a controlled decision" is not ticked.

## What the test proves (simulated provider, synthetic fixtures)

* Memory is genuinely live: opt-in, a `CM-` item for task `funding-evidence`, stored verbatim, status active.
* A chat proposal through the real `/api/chat/threads/{id}/proposals` route returns 202; the task executes to `ready`, `approved` false, `relied_on` false, one provider call.
* The memory canary and id are absent from the system and user text handed to the provider, from the serialised task detail and from the thread; every snapshot citation key is `source:*` or `sensor_reading/*`.
* The thread's assistant message evidence is exactly `[proposal id]`; `chat_add_message` refuses the memory id ("never evidence").
* A provider output citing the memory id fails like any citation outside the captured sources (`failed`, no output, not relied on).
* Case, procurement, recommendation and staff records are unchanged across the proposal (audit excluded because the chat route legitimately extends it).

## Non-vacuity

Temporary mutations, each reverted with `git checkout`: disabling the `CM-` guard in `chatthreads._clean_evidence` fails step 5 ("ValueError not raised"); removing the `x not in snapshot["citations"]` check in `assistants.py` fails the citation refusal. Neither production file is modified in the candidate.

## Validation (pip-installed editable worktree distributions in an external venv; no source PYTHONPATH substitution)

* `test_assistants` 122 run, OK (59 skipped: MSSQL variants, including the inherited copy of the new test); `test_chat_isolation` 32 OK; `test_chat_panel` 55 OK (1 skipped); core `test_chat_memory` 21 OK.
* `ruff check` and `mypy` (strict config) on `tests/test_assistants.py`: clean. `ruff format --check` reports the file as needing reformatting both before and after this change (pre-existing, not touched).
* Not run: full gate, MSSQL variant, browser, any real provider, model or deployment. Hosted CI for the exact head is unobserved.

## Boundaries and ownership

`test_assistant_release.py`, `assistant_process_worker.py` (#107), `app.js` and its copy tests (#153) and `store.py` (#82) untouched. No push, PR, tick or board change.

## Divergences

Critique PC-001 to PC-005 were applied. The count of citation failures uses state `failed` as the existing test does. No significant divergence.
