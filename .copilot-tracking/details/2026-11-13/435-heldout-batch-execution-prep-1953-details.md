# Details: #435 held-out batch live adapter (1953)

## heldout_aoai.py

* `ENDPOINT = ^https://[a-z0-9-]{2,64}\.(openai|cognitiveservices)\.azure\.com/?$`, `DEPLOYMENT = ^[A-Za-z0-9._-]{1,64}$`, `SCOPE_RESOURCE = https://cognitiveservices.azure.com`, `API_VERSION = 2024-10-21`, `MAX_RESPONSE_BYTES = 1 MiB`.
* `class AdapterError(Exception)`: messages are fixed strings, never carry tokens, headers or response bodies.
* `az_cli_token(run=subprocess.run) -> str`: list-argv `az account get-access-token --resource ... --query accessToken -o tsv`, 30 s timeout, `capture_output`, no shell; non-zero, OSError, timeout or empty output raises AdapterError.
* `managed_identity_token(credential_factory=None) -> str`: lazy `azure.identity.ManagedIdentityCredential().get_token(SCOPE + "/.default")`; ImportError or failure raises AdapterError.
* `make_provider(endpoint, deployment, model, token, opener=None) -> Call`: validates endpoint and deployment (ValueError). Default opener has a redirect handler that refuses redirects. The call POSTs `{messages: [system?, user], max_tokens, temperature: 0}` with `Authorization: Bearer`. Returns `{outcome: "returned", text: None, usage}` only when the body is a JSON object, the `model` field starts with the declared model, and usage has int prompt and completion tokens; cached tokens from `prompt_tokens_details.cached_tokens` (default 0); total taken from provider `total_tokens` if int else sum. Any other path returns `{outcome: "failed"}`; exceptions never escape with sensitive text.

## heldout_batch.main

* New args `--endpoint`, `--deployment`, `--model`, `--auth` (default `az-cli`).
* Live with injected provider: unchanged. Live without: all three of endpoint, deployment, model required else exit 2 with the existing style message; invalid endpoint or deployment format exits 2.
* Authorization loaded; if `authorization_problems` is empty, fetch token (failure exits 2 before any call) and build the provider with `provider_model=args.model`; otherwise pass a never-called stub so `run_batch` refuses with the problems (exit 1).
* Adapter imported lazily inside `main`.

## Tests (mocks only)

* token: az success/failure/empty/timeout/OSError and no secret in error; managed identity success, import failure.
* provider: request URL, headers, body, max_tokens and no redirects; success with cached tokens; model mismatch, HTTP error, malformed JSON, bad usage, oversize body, invalid endpoint or deployment.
* CLI: live missing args exits 2 with no HTTP; invalid authorization (> USD 5.00) refuses, no token fetch, no HTTP; success path through `main` with patched opener and token reports `measured held-out batch` and no token in output; dry-run makes no adapter or network use.
