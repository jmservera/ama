# Critique: issue 144 standalone worker plan (1315)

Executed once by independent `rubber-duck`. Verdict: Revise. All findings compatible; applied directly, no user decision needed.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Dockerfile `CMD serve` breaks no-argument harness and CI | Accepted: keep image default (version line); the agents Container App sets `command`/`args` to `serve`. Contract test asserts the Bicep command. |
| 2 | `Ai` has no consumption meter, so real calls cannot succeed | Accepted as fail-closed: unmetered `Ai.evidence` returns `financial-held` with no network call; test composes the provider and asserts that. Metering wiring is a follow-up. |
| 3 | Absent API result route leads to release then poison | Accepted: startup refuses unless `ZF_AGENT_RESULT_ROUTE=enabled` (not set by Bicep) so no message is consumed before the route exists. |
| 4 | Allowance expiry only checked structurally | Accepted: startup rejects expired limits and `serve` takes an `alive` check each loop; expiry stops the worker (exit 3). |
| 5 | Redirect refusal on identity opener; sanitise exception chains | Accepted: token opener refuses redirects; errors raised with fixed text `from None`; tests use sentinel secrets. |
