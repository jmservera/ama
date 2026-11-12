---
title: Issue 116 offline provider-payload spies plan
ms.date: 2026-11-12
task_id: provider-payload-spies-116-1112
---

## Objective

Add one focused offline test module, `src/core/tests/test_ai_provider_payload_spy.py`, that spies the bytes handed to the transport by the real `Ai` wrappers and asserts exact permitted payload shape and hidden-canary absence. Research: [research](../research/2026-11-12-provider-payload-spies-116-1112-research.md). Details: [details](../details/2026-11-12-provider-payload-spies-116-1112-details.md). Refs #116 only.

## Phases

* [x] Phase 1: one independent critique of the final candidate plan; apply compatible findings.
* [x] Phase 2: write the module (wrapper bodies, look_at, assistant serializer per capability and role projection, legacy `ai_run` per role, wire-level refusals).
* [x] Phase 3: focused validation: the new module, then the neighbouring AI core tests; ruff check, ruff format --check and mypy on the new file only.
* [x] Phase 4: changes record, one original Review, local commit with repo-local privacy-safe identity.

## Boundaries and stop rules

* Tests only, one new file plus RPI evidence. No edit to `ai.py`, `assistants.py` or any production file; no new serializer, allowlist, approval policy, role or permission change.
* Offline: `urllib.request.urlopen` and `_token` replaced by test doubles, a mock meter, synthetic canaries only, no network or credential.
* A failing assertion that exposes a real leak or undefined contract is retained as evidence and reported in #116 (no new issue, no production patch, no silent weakening).
* No push, PR or issue edits, no ticks, no automatic correction renewal; one candidate only.
