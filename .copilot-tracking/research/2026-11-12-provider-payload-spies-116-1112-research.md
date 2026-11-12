---
title: Issue 116 offline provider-payload spies research
ms.date: 2026-11-12
task_id: provider-payload-spies-116-1112
---

## Scope and disposition

Research disposition: `executed`. Planning Readiness: `Ready`. Base `139176fa0382add781b1830b1ac9db785ed086fe` (main), branch `test/demo-provider-payload-spies-116-1112`, worktree clean at start. Refs #116 only. Bounded owner-directed demo lane: offline test doubles and synthetic canaries, no provider, network, credential, deployment or spend. This is not a production assurance programme and does not implement the whole of #116.

Authority check: issue #116 (open) comments were read through the 5 November closure audit. They record that provider-boundary engineering continues independently of the OD-14/OD-19 human decisions, record no spent authority for this lane and impose no restriction that conflicts with test-only offline work. The cost ledgers under `.copilot-tracking/changes/2026-10-27/` concern separate live-resident acceptance and are not touched. No conflicting historical restriction found.

## Source map (current main)

* `src/core/src/zava_forward/core/ai.py`: `Ai.provider_body` is the only body serializer (`messages` system+user, `max_tokens`, `temperature`, ASCII JSON). `_request` builds the HTTP request (URL carries the deployment, the bearer token travels in a header). `_chat` fixes temperature 0.3, `evidence` fixes temperature 0 and max 600 by default, `run` calls `_chat` (700 tokens), `look_at` selects text (first 6000 characters after the instruction) or an approved image (`image/png`, `image/jpeg`, at most 4 MiB, base64 data URL) and calls `_chat` with 500 tokens.
* Refusals defined by current source: `InputRefused` for a text body above `MAX_TEXT_BYTES`; `look_at` template return for oversize or unapproved image types and for unsupported MIME types; `export_fields.scalars` raising `ValueError` for malformed `name`/`mime`; `export_fields.prompt_case` raising `ValueError` for malformed case fields before `ai_run`; `ai_tasks.require_registered` and the `ai_run` task check for unknown tasks.
* `src/core/src/zava_forward/core/assistants.py`: `capture(capability, case, ...)` is a closed field allowlist per capability (`REGISTRY[...]["categories"]`), `build_request(task)` returns `(SYSTEM, canonical({capability, purpose, evidence}))`, and role projection is expressed by `projection.can_see_reason` and `projection.status_only` (appointment outcomes held for capabilities whose roles are not all reason roles).
* Legacy role projection: `Store._facts(c, reason_ok)` and `ai_tasks.source_labels(c, reason_ok)` keyed by `projection.can_see_reason(user)`.

## Gap confirmation

Existing tests and what they assert:

* `core/tests/test_ai_input_bounds.py`: size and image-type refusals use the meter and `urlopen` mock; no body-equality assertions.
* `core/tests/test_sensor_privacy.py`: `test_actual_legacy_transport_body_is_closed` decodes one `summary` request body and checks two sensor sentinels and the role order; no exact-equality, no keys, no other roles.
* `api/tests/test_assistants.py`: canaries are asserted absent from the stored proposal, not from the bytes handed to the transport; the `Provider` double never sees wire bytes.
* `api/tests/test_ai_consumption_api.py`: a fake HTTP server records payloads, but canary assertions target durable meter records and request counts, not the request body.

Confirmed real gap: no test asserts exact permitted wire-body equality, the closed set of body keys, header-versus-body separation or hidden-canary absence in bytes for `Ai.run/_chat`, `Ai.evidence`, `Ai.look_at`, the assistant serializer per capability, or the legacy per-role projection. Size and refusal tests exist and are not repeated except where a wire-level zero-request assertion adds new coverage.

## Constraints carried into the plan

* Tests only; new uniquely named module `src/core/tests/test_ai_provider_payload_spy.py`. No edit to `ai.py`, `assistants.py` or any production file.
* Expected values come from source-defined contracts (`provider_body` shape, `ai_prompts.render`, `REGISTRY`, closed `capture` lists, `build_request`), never an invented approved-field manifest. Reason-role payloads reflect current default behaviour and are not approval of OD-14/OD-19.
* If a test exposes a real leak or undefined field contract, preserve the failing evidence and report it in #116 only; no patch.
* Remaining #116 criteria stay unproved: OD-14/OD-19, output/citation rechecks, approved processing manifests, document derivatives, real authority and the whole compound criterion.
