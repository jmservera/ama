---
title: Issue 116 offline provider-payload spies details
ms.date: 2026-11-12
task_id: provider-payload-spies-116-1112
---

## Harness

* Real `Ai` with `endpoint="https://provider.invalid"`, `model_version="unattested"`, a `Mock` meter (`reserve` returns 64 hex characters), `_token` patched to a synthetic token and `urllib.request.urlopen` patched with a spy returning a fixed envelope. The spy stores each `Request`.
* Wire assertions decode `request.data` and compare with literal expected bodies or values from source-defined contracts.

## Test groups

* Wrapper bodies: `run/_chat` (fast and strong deployment, 700 tokens, temperature 0.3), `evidence` (600 default, temperature 0), exact key set and message order, ASCII escaping, URL deployment path, token only in the header, template and task name absent from the body.
* `look_at`: text slice at exactly 6000 characters (tail canary absent), `application/json` and `text/csv` accepted, PNG content-list shape, 500 tokens and strong deployment, name only in the instruction. Refusals with zero spy requests: unapproved image type, oversize image, unsupported MIME type, malformed `name`/`mime` (`ValueError` before provider, canary absent from the message).
* Assistant serializer: for each `REGISTRY` capability a constructed case with canaries (vulnerability reason, resident contact details, notes, handoff note, document name and AI summary, unlisted `monitoring` and `home.diagnostics` fields, finance amount for non-funding capabilities) goes through `capture`, `build_request` and `Ai.evidence`. Expected: system equals `SYSTEM`, user equals the canonical `{capability, purpose, evidence}` object, the evidence source keys equal `REGISTRY[...]["categories"]`, and no canary appears in the bytes. Role projection: `works-resident-coordination` appointment outcome free text held (`projection.NOTE_HELD`) while a status value passes; with `ZF_REASON_ROLES` covering every role of that capability the existing override passes the free text (current source behaviour, not an approved policy).
* Legacy `ai_run`: a reason role and a non-reason role (role string changed on a copy of the constructed user) request `summary`; the body equals the literal prompt expectation for each role and the canaries absent for the non-reason role; the reason-role difference is limited to the documented adjustment and contact-outcome positions. Refusals with zero spy requests: unknown task and malformed `home.address`.

## Validation commands

* `cd src/core && python3 -m unittest tests.test_ai_provider_payload_spy -q`, then `tests.test_ai_input_bounds`, `tests.test_sensor_privacy`, `tests.test_ai_consumption_safety` as neighbouring checks.
* `ruff check`, `ruff format --check` and `mypy` on the new file only (core `pyproject.toml` configuration).
