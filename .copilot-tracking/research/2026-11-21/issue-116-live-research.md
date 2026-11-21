# Issue 116 live research (2026-11-21)

Research disposition: reused plus targeted gap closure. Planning Readiness: Ready.

* Issue 116 shows one unticked box: allowlists at every provider boundary.
* Prior round 5 ([research note](../../../docs/reference/research/issue-116-live-r5-evidence-2026-11-20.md)) proved every enumerated boundary offline and merged (df9831da7). Its stated residue: `test_assistants_dispatch` was not runnable (no `opentelemetry`), and no live check of the deployed API.
* Gap closure: install the pinned dev dependencies into a throwaway target outside the repo, run the unrun test, rerun the spy and bounds suites at this head, and probe the deployed API read-only (role gate without credentials).

## Results

* Previously unrun `test_assistants_dispatch` now runs: api suites `test_assistants_dispatch`, `test_chat_panel`, `test_resident_aoai`, `test_ai_call_site_inventory` ran 104 tests, OK (1 skipped, opt-in Chromium). Pinned `opentelemetry` 1.45.2 was installed to `/tmp/otel116` (outside the repo, removed at the end).
* core `test_ai_provider_payload_spy` and `test_ai_input_bounds`: 24 tests OK at head 08fbe37ef.
* Live read-only probe of `ca-cutover-test-demo-api` without credentials: `/api/cases`, `/api/ai/assistants`, `/api/export`, `/api/audit` return 401; `/healthz` returns 200. No Azure resource created or changed.
* No product defect found; no src change is needed.
