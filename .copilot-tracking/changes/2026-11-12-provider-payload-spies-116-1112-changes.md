---
title: Issue 116 offline provider-payload spies changes
ms.date: 2026-11-12
task_id: provider-payload-spies-116-1112
---

## Changes

* Added `src/core/tests/test_ai_provider_payload_spy.py` (14 offline tests, tests only). No production file, workflow, dependency, SQL or documentation index changed. `ai.py` and `assistants.py` are untouched.
* Wrapper bodies: exact `run/_chat` and `evidence` wire bodies (keys, message order, 700/0.3 and 600/0 bounds, ASCII escaping, deployment in the URL, token only in the header, template and task name absent), `look_at` text slice (first 6000 characters), PNG content list, name only in the instruction, and zero-request refusals for unapproved or oversize images, unsupported MIME types and malformed `name`/`mime`.
* Assistant serializer: for all five `REGISTRY` capabilities, independent literal expected `sources` per capability from a constructed case with 20 synthetic `PRIVATE-*` canaries (including unlisted nested fields); exact evidence key set, citation keys, closed body keys and bounds, canary regex absent from bytes, finance amount absent outside `funding-evidence`. Appointment outcome free text is held unless every role of the capability is a reason role (characterisation of the current `ZF_REASON_ROLES` override, not approval).
* Legacy `Store.ai_run` summary: exact prompt for a non-reason role (no canaries) and a reason role (only the adjustment and contact-outcome canaries differ); unknown task and malformed selected field refuse before any provider request.

## Plan deviations and amendments

* Critique PC-001/PC-002 applied: expected nested values are literal per fixture, the legacy citable list is literal (the first 14 labels exclude the role-dependent labels for this fixture) and both role scenarios are labelled characterisation.
* PC-003 recorded as not covered: the optional `sensors` source and dispatch-time `as_of` state need the SQL-backed `sensor_view` capture and keep their existing sensor tests; no sensors branch is asserted here.
* PC-004 applied: `setUp` clears `ZF_REASON_ROLES`, `ZF_AI`, `ZF_DATA_PROCESSING` and `AI_MODEL_VERSION` and restores the environment.
* The first run used the repository-level editable install (`/home/azureuser/source/ama`); results below use `PYTHONPATH=src:tests` so the worktree source is imported.

## Validation (planned versus actual)

| Check | Result |
| --- | --- |
| `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ai_provider_payload_spy` | 14 tests OK (also OK under `discover -s tests -p test_ai_provider_payload_spy.py`) |
| Neighbours `test_ai_input_bounds`, `test_sensor_privacy`, `test_ai_consumption_safety` | 6, 17 (1 skipped, pre-existing) and 2 OK |
| `ruff check`, `ruff format --check`, `mypy` on the new file | pass |
| Mutation sanity by temporary in-process monkeypatch (not committed) | extra body key: 12 failing; `pick` leaking a note: 4; `status_only` passthrough: 2; `can_see_reason` always true: 3 |

Not run: the complete local gate, hosted CI, SQL, browser, provider or any network call. Classification: focused tier (tests-only, no gate tool, workflow, dependency or deployment change).

## Findings for #116

No real product leak or undefined field contract surfaced; every assertion passed against current source. Characterisation, not approval: reason roles currently send the free-text adjustment and contact outcome to the provider (OD-14/OD-19 unresolved). Remaining #116 criteria stay unproved: OD-14/OD-19, output/citation rechecks, approved processing manifests, document derivatives, real authority, sensors branch, proactive scan paths and the whole compound criterion. No issue tick or closure.
