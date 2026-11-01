---
title: Issue 184 credential hygiene plan
ms.date: 2026-11-01
---

## Plan

* [x] Add src/api/tests/test_iot_credential_hygiene.py: repository text scan (src, infra, docs, .github) for shared-access key, signature, device connection string and private key patterns, with scanner self-test; source guard against connection-string client factories and logging in iot_stream.py.
* [x] Runtime leak test: fake-SDK publish with marker pass phrase, captured DEBUG logs, truth records, wire payloads, reprs, hostile failure text and timeout.
* [x] Add test module to the existing mypy untyped-call override in src/api/pyproject.toml.
* [x] Record the evidence in the research plan table and knowledge base log.
* [x] Focused validation: new and iot_stream tests, ruff check, ruff format --check, mypy.

## Critique (single, final candidate)

Complete / Pass. Scope is tests and docs only, no source behaviour change, no new dependency. Risk: scan false positives in docs; mitigated by specific patterns and a run over the repository. Claims limited to constructed local evidence; criteria 1 and the actual lifecycle evidence of 3 stay unmet.

## Correction cycle 1 (PR 704, 2026-11-01)

* Research: two unresolved Copilot threads on `src/api/tests/test_iot_credential_hygiene.py`, both valid: dotenv files (`.env`, `.env.local`) skipped by the suffix filter; `run_publisher` swallowed `StreamError` when no failure was injected.
* Plan/Changes: added `is_scanned` and `scan_directory` helpers plus a temp-directory dotenv regression test; re-raise `StreamError` unless a failure was injected.
* Review: ruff check and format clean; mypy shows the same 14 pre-existing `azure.iot.device` stub errors as before the change; 35 `test_iot*` tests pass in a local venv. No Azure access.
