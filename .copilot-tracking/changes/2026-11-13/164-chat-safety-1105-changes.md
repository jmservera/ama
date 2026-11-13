---
title: Changes 164 chat safety verification
task_slug: 164-chat-safety-1105
---

# Changes

Tracking-only. Initialised before implementation; results appended below.

## Environment

* `python3 -m venv --system-site-packages /tmp/venv-164-1105`; first `pip install --no-build-isolation --no-index -e` failed rc=1 (no `wheel`, "invalid command bdist_wheel"); after `pip install --upgrade setuptools wheel` all three editable installs rc=0.
* Verified `zava_forward.{core,agents,api}.__path__[0]` under `/home/azureuser/source/ama-demo-wt/child-164-chat-safety-1105/src/*/src/zava_forward/*`. (Before the fix the system had resolved to a different checkout, `/home/azureuser/source/ama`, so the check mattered.)
* `env -u ZF_DATA -u ZF_TEST_MSSQL`, `PYTHONDONTWRITEBYTECODE=1`, `python -m unittest -v`. No network, Docker, browser or live model call. `git status` shows no `src/`/`docs/` change.
* Agents first run rc=1: `test_chat_model` could not import `dataset` (lives in `src/core/tests`); a PYTHONPATH invocation error, not a product failure. Rerun with `src/core/tests` on the path rc=0.

## Results (true producer exit codes)

| Package | Modules (tests) | Total | rc | sha256 of verbose log |
| --- | --- | --- | --- | --- |
| core | ai_consumption 34, chat_case_answers 5, chat_case_funding_sources 4, chat_dpia_record 4, chat_memory 21, chat_panel 45, chat_privacy 29, chatthreads 27, regulatory_chat 25 | 194 OK | 0 | 4f2445fb...a811 |
| agents | chat_eval 45, chat_fixture 13, chat_heldout 11, chat_model 13, chat_provenance 1, regulatory_answers 7 | 90 OK (rerun; first run 78 + 1 import error) | 0 | 1799fa6c...0542 |
| api | ai_boundary 6, chat_fixture_roles 1, chat_isolation 22, chat_panel 55, regulatory_chat_api 12, resident_chat_api 51 | 157 OK, 1 skipped | 0 | d9acf831...0b2 (full) |

Total 441 tests, 0 failures. Only skip: `api test_chat_panel test_browser_warning_failure_keyboard_refusal_and_live_log` ("opt-in local Chromium"; not run by design). No SQL skips observed; SQL variants ran on the sqlite-backed store, not MSSQL.

Named executions passed: `core test_chat_memory::test_prompt_memory_is_non_authoritative_and_never_evidence` (ran twice in core: in-memory and sqlite-backed SqlStore variants; no same-named api test exists), `test_a_failing_injection_gate_fails_enablement`, `test_isolation_cases_cover_every_perspective_and_kind`, `test_thread_isolation_covers_exactly_the_eligible_owners`, `test_unavailable_case_and_foreign_thread_look_identical`, `test_every_role_against_every_chat_endpoint`, `test_memory_lifecycle_gates_the_prompt`.

## Acceptance mapping

* #164 grounding/evaluation/human-review boundaries: scripted offline (L2) proof only: chat_eval, chat_fixture, chat_provenance, chat_heldout (fixture structure), regulatory answers, isolation and role matrix. NOT performed: actual-model evaluation, human-labelled held-out set, human effectiveness (the eval report itself states "not evaluated"/"not produced"), live LLM calls, browser path.
* #157 no memory used as evidence: unit-level proof that prompt memory is non-authoritative and never evidence (core only) and memory lifecycle gates the prompt. Limitation recorded from `src/agents/tests/test_chat_eval.py:181`: memory poisoning is a component-only probe (2 scenarios), serving path not exercised, so integrated memory poisoning is unverified.
* #162: isolation and role-endpoint matrix unit proof only.
* Not covered: MSSQL-backed paths, hosted CI, human approvals, PR #1488 regression beyond the above named memory-evidence test (no mapping to the PR was independently verified).

Cleanup: `/tmp/venv-164-1105` and `/tmp/t164` removed after logs hashed; editable-install egg-info checked untracked-free.
