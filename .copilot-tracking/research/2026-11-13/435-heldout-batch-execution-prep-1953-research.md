# Research: #435 held-out batch execution preparation (1953)

Task: `435-heldout-batch-execution-prep-1953`. Research disposition: executed (direct code and CLI inspection). Planning Readiness: Ready.

## Findings

* `src/agents/src/zava_forward/agents/heldout_batch.py` has no live adapter. `main(provider=None)` with `--execute-live` prints "no provider is configured" and exits 2. Confirmed in `/tmp/venv-435bp-1953`.
* `python -m zava_forward.agents.heldout_batch --dry-run` works offline: synthetic authorization, manifest (from `tests/heldout_freeze_fixture.py`) and proposals completed, labelled "dry-run simulation - not measured evidence". The baseline `tests/test_heldout_batch.py` has 40 passing tests.
* Provider contract: `Call(system, prompt, max_tokens, timeout) -> {outcome: "returned", usage: {prompt_tokens, completion_tokens, total_tokens, cached_tokens?}}`. Anything else is charged at worst case and stops the batch. `provider_model` must equal the authorized model.
* No held-out proposal JSON fixture is in the repository. `heldout_freeze_fixture.py` is synthetic test data only (case ids h1..). The real proposals must be supplied by the owner or coordinator from the frozen held-out set, as a JSON list of `{id, prompt, system?}`.
* `BatchAuthorization` is the authorization JSON already validated by `authorization_problems` (hard cap USD 5.00, max 50 calls, expiry, rates). Authority ref: `slide22_plus_qa_authorize_5usd_batch`.
* Existing repo auth precedent: `azure.identity.ManagedIdentityCredential` with scope `https://cognitiveservices.azure.com/.default` in `src/api/.../aoai.py`; `src/core/.../ai.py` uses urllib. The `az account get-access-token --resource https://cognitiveservices.azure.com` CLI route is the operator path.
* Target: Azure OpenAI resource `aif-cutover-test-rzsrg`, deployment `standard` (`gpt-4.1-nano`, GlobalStandard).

## Design implications

* Add a stdlib-only adapter (urllib, no new dependency) in a new module `heldout_aoai.py`. Token via `az account get-access-token` subprocess (argument list, no shell), or `ManagedIdentityCredential` when `azure.identity` is importable and `--auth managed-identity` is chosen. Token is never logged, stored or put in the report.
* Opt-in only: requires `--execute-live`, `--endpoint` (https, `*.openai.azure.com` or `*.cognitiveservices.azure.com`), `--deployment`, and an authorization that passes validation. Otherwise exit 2 as before.
* The provider model reported must match the authorization model; the CLI passes `--provider-model` equal to what the owner declares, validated by the gate against the authorization and manifest.
* Adapter must send `max_tokens` (`max_completion_tokens`), `temperature` 0, no retries, a timeout, and map any failure (HTTP, timeout, malformed JSON) to an unmeasured envelope. Usage comes from the response `usage` (`prompt_tokens_details.cached_tokens` to `cached_tokens`). Response model name is checked against the deployment's expected model prefix is not enforced (the deployment alias is `standard`), so the authorization model is the declared one.
* No live call in this worker; tests use mocked HTTP.
