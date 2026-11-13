---
title: Issue 157 memory-as-evidence boundary details
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Harness

* `ApiTests` (real `App`, real `SqlStore`, local `Provider` double, release fixtures). Chat approval references set with `patch.dict(os.environ, ...)` (synthetic `SYNTH-*` values) for the test only.
* Subclass-free: a method `test_active_memory_cannot_reach_a_chat_proposal_or_its_evidence` on `ApiTests`; the provider double records the system and user text it is given.

## Steps

1. As the Programme Manager user, opt in and add a memory item containing a unique synthetic canary for task `funding-evidence`; confirm `memory_status` active, the item id begins `CM-`, and `prompt_memory` returns the item (so the memory really is live).
2. Start a thread on `ZF-1` and post `/proposals` with `funding-evidence`. Expect 202; execute the task; expect `ready`, `approved` false, `provider.calls == 1`.
3. Assert the canary is absent from the provider system and user text, the task snapshot and citations, and the stored proposal; assert every snapshot citation key is `source:*` or `sensor_reading/*`, and none begins `CM-`.
4. Assert the thread's last message carries `evidence == [proposal id]`, that id does not begin `CM-`, and no memory item content is stored in thread messages.
5. Assert `store.chat_add_message(..., evidence=[memory id])` raises `ValueError` and that a provider output citing the memory id is refused as an unsupported citation (provider `bad="citation"` style with the memory id), leaving the task not `ready`.
6. Assert case records are unchanged: compare the case-record slices of `self.domain()` (cases, procurement meta, recommendations, staff; not the audit chain, which the chat route extends) from after step 1 to the end, and that the proposal is not accepted and `relied_on` is false.

Amendments from the critique ([critique](../plans/critiques/2026-11-12-memory-evidence-boundary-157-1112-plan-critique.md)): the test wraps `provider.evidence` to record system and prompt text and to return a proposal citing the memory id for step 5 (two provider calls in total); it scans the whole serialised task detail; it uses a canary with no phone or email shape and asserts it is stored verbatim; it uses only public `request`, `service` and `store` calls so the inherited MSSQL variant stays dialect-neutral.

## Validation commands

* From `src/api` with the worktree distributions installed in a venv: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_assistants.py`, then `test_chat_isolation.py`, `test_chat_panel.py`; from `src/core` `test_chat_memory.py`.
* `ruff check`, `ruff format --check` and `mypy` on the touched file under the api project configuration.
