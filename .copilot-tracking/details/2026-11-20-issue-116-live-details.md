# Issue 116 live details (2026-11-20)

## Phase 2

Add `test_proactive_task_sends_the_same_closed_payload` to `AssistantSerializer`. Build a task with `dispatch={"trigger": "proactive", "as_of": None, "note": "PRIVATE-DISPATCH-CANARY"}` and compare the wire body with the requested one for every capability; assert the canary is absent and that exactly one request is made.

## Phase 3

From `src/core`: `PYTHONPATH=src:tests:../agents/src:../api/src:../agents/tests:../api/tests python3 -m unittest test_ai_provider_payload_spy -q`; `python3 -m mypy`; `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on the test file.

## Phase 4

Note carries a per-criterion table (all boxes except the provider-boundary box already ticked) and a per-boundary matrix.
