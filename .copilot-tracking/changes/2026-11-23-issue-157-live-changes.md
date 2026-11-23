# Changes 2026-11-23: issue 157

* Source: src/core/src/zava_forward/core/chat_privacy.py `start_thread` now resolves the case through `store.detail(case_id, user)` and raises ChatNotFound for hidden or missing cases.
* Test: src/core/tests/test_chat_privacy.py `test_thread_cannot_be_bound_to_a_case_the_role_cannot_see` (fails on both stores without the fix).
* Docs: docs/reference/research/issue-157-case-scoping-2026-11-23.md, index row, log entry.
* Validation: core chat tests 198 OK; api chat tests 550 OK (1 skipped); ruff clean; mypy 3 pre-existing environmental errors outside changed files. Tier FULL by src change; no rpi-checks --all run (coordinator owns gates). Not pushed.

## Per-criterion table

| Criterion | Verdict | Reason |
| --- | --- | --- |
| Complete #440 stabilization checkpoint | Unproven | #440 criteria 7 and 8 need owner approval, a PR and a non-worker reviewer; this is one bug disposition |
| If accepted, child features are accepted | Unproven | Remainders need excluded human, legal or real-model steps |
| Decision accepted (ticked) | Not reopened | ADR 0004 |
| No memory as evidence (ticked) | Not reopened | Unchanged |
| Consumption bounded (ticked) | Not reopened | Unchanged |
