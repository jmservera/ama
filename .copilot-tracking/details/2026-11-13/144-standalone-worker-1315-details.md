# Details: issue 144 standalone agents worker (1315)

## Interfaces

* `runtime.identity_token(resource, env, opener)`: ACA `IDENTITY_ENDPOINT`+`IDENTITY_HEADER` (header `X-IDENTITY-HEADER`, api-version 2019-08-01, `client_id` from `AZURE_CLIENT_ID`); returns a caching callable; raises `RuntimeError` without endpoint.
* `runtime.ApiResultSink(base_url, token, transport)`: `post(ResultMessage)` POSTs `to_json()` to `{base}/api/agent-results` with bearer; status other than 200/201/202/204 raises (so the message is released, never acked); https only, no redirects (reuses `queue_azure.urllib_transport`).
* `runtime.build_runtime(env)` -> `Runtime(queue, worker, sink, limits)`; raises `ConfigError` whose message lists missing variable names only: `QUEUE_ENDPOINT`, `TASK_QUEUE`, `POISON_QUEUE`, `API_BASE_URL`, `API_AUDIENCE`, `FOUNDRY_ENDPOINT`, valid `ZF_ASSIST_*` limits. Ai endpoint and deployments map from `FOUNDRY_ENDPOINT`, `MODEL_DEPLOYMENT_DEFAULT/CAPABLE`.
* Heartbeat: `beat(path)` writes the time to `$ZF_STATE/worker-heartbeat`; `serve` takes an optional `beat` callable called each loop turn; `health(path, max_age, now)` -> bool.
* `worker.main`: `serve` -> build, install signal handlers, serve, return 0; `ConfigError` -> exit 2; `health` -> 0/1; default version line.

## Safety

No secrets or values in messages. Acknowledge only after post (existing `run_once`). SIGTERM sets the stop event; in-flight work finishes or is released.

## Critique revisions (see critique file)

* Dockerfile CMD unchanged; Bicep agents container gets `command: ['python','-m','zava_forward.agents']`, `args: ['serve']`.
* `build_runtime` requires `ZF_AGENT_RESULT_ROUTE=enabled`; refuses expired limits; `serve(alive=...)` stops on expiry (exit 3).
* Unmetered `Ai` fails closed (`financial-held`); tested.
* Token opener refuses redirects; fixed-text errors `from None`.
