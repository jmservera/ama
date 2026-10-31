# Research: #360 correction1 (Blob credential binding and operation budget)

* Date: 2026-10-22. Parent state: `.copilot-tracking/rpi-sessions/2026-10-22/demo-transport-blob-360-state.json`
* Trigger: independent exact-head review of 829890010f69 (NEEDS CHANGES, two blocking findings). Run5 receipt stays historical evidence for that head only.
* Posture: focused (bounded internal task, named source targets, supplied failure evidence). Output mode: convergence. Extensions: repo instructions (selected), no web work (web skills skipped, backend only), no subagents (tightly coupled, inline).
* Non-goals: Azure/tenant actions, role changes, live runs, results truncation, parser relaxation.

## Questions

1. How does ARM auth select its operator context, and can Blob reuse it?
2. Which Blob operations lack an overall deadline, and how can cleanup stay bounded?

## Wave 1 (wider)

* C1 `infra/scripts/staff_azure.py:25-31` builds `ContainerClient(..., credential=DefaultAzureCredential())`: ambient chain (env, managed identity, CLI default profile), not the selected operator profile.
* C2 `infra/scripts/setup-entra.py:129-136` `Azure.environment()` sets `AZURE_CONFIG_DIR` for each `az` subprocess only; `setup-entra.py:323-335` `contexts()` swaps `operator` to the isolated tenant-profile `Azure` on login fallback. So `cli.profile` is the single source of operator context.
* C3 `infra/scripts/staff_azure.py:252-254` preflight runs before `deadline` (line ~308); `:339` `read_result` is a synchronous call inside the deadline loop; `staff_blob.py:143` `list_blobs` and `:196` `download_blob().readall()` use SDK defaults (no explicit timeouts; default retry policy).
* C4 `staff_azure.py` finally block (~362-405) gives cleanup its own 90 s `cli.deadline`; it only runs if the read returns or raises.
* W1 azure-core documents `connection_timeout`/`read_timeout` as per-socket limits and `retry_total`, `retry_backoff_*` policy kwargs on clients (azure-core 1.41 installed, read from installed package, retrieved 2026-10-22). Per-socket timeouts do not bound a multi-page list or a slow trickling body.

## Wave 2 (deeper)

* Credential: `az account get-access-token --resource https://storage.azure.com/` run through `cli.call` inherits `cli.environment()` and thus the selected/fallback profile, deadline and sanitized error mapping (`setup-entra.py:140-175`). A small `TokenCredential` adapter (`get_token(*scopes)`) returns `AccessToken(token, expires_on)`; the token is never logged; failures map to a generic error.
* Budget: sync SDK calls cannot be interrupted, so an overall deadline needs a worker thread with `join(timeout)`; on expiry the thread is abandoned (daemon) and the call raises, letting cleanup proceed. Combine with explicit per-socket timeouts and bounded `retry_total`.

## Wave 3 (contrarian)

* Alternative A: `AzureCliCredential` with process-wide `AZURE_CONFIG_DIR`: rejected, mutates ambient env for ARM and Blob and races with `Azure.environment()`; it is also an SDK-owned subprocess without the repo's sanitization.
* Alternative B: per-socket timeouts only: rejected per the review; not an overall deadline.
* Alternative C: `signal.alarm`: rejected, not thread-safe and not portable.
* Risk: abandoned thread may finish later; harmless because it only reads, and its result is discarded. Keep read-only (no state mutation after timeout).
* Risk: `az` token for storage requires the operator to hold data-plane read; still unverified live (unchanged prerequisite).

## Decisions

* D1 `default_container(url, cli)` uses a `ProfileCredential(cli)`; client timeouts `connection_timeout=5`, `read_timeout=15`, `retry_total=2`.
* D2 `staff_blob` list/download run through `_bounded(fn, deadline)`; preflight budget 45 s, per-read budget 45 s capped by the job deadline; expiry raises `StaffJobError` (unverified outcome) and the existing finally cleanup runs.
* D3 Tests: real `ContainerClient` construction with fallback `Azure` profile and patched `subprocess.run` (no network, no token output), plus slow/failing container tests and cleanup-after-stall test.

Research disposition: executed. Planning Readiness: Ready.
