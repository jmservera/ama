---
title: Issue 2303 report latency research (2026-11-25)
ms.date: 2026-11-25
---

Research disposition: executed. Planning Readiness: Ready.

## Question

Why did GET /api/ai/report take 73.5 s (API) and 93.4 s (UI) on revision 0000072, and what bounded change brings it well under 5 s?

## Findings (code profile, local, synthetic data)

The handler in `src/api/src/zava_forward/api/server.py` (route `/api/ai/report`) runs two full evaluations on every request, with no cache:

| Step | Wall time on this host | Notes |
| --- | --- | --- |
| `ai_eval.run_eval()` | 1.1 s first call, 3.3 s second | scenario replay in temp stores; output includes measured latencies, so it differs per run |
| `chat_eval.run_eval()` | 8.4 s first, 4.1 s second | 33 scenarios, 117 chat asks; cProfile shows `projection.redact_staff_detail` and `withheld_case_values` at about 2.9 s of 5.8 s, store saves 1.4 s |
| `heldout_eval` suite plus token comparison | 0.1 s plus 0.25 s | cheap |
| `ai_registry.registry()` | under 0.01 s | cheap |

Both evaluations are CPU replays of fixed golden files (`ai_priority_golden.json`, `chat_golden.json`) through temporary stores. On this host they cost 5 to 12 s per request; the demo container has a fraction of a vCPU and serves requests on threads that share the GIL with other traffic, which is consistent with the observed 73.5 s. I did not profile inside the container, so the share due to CPU starvation is unproven; the code-level cause (recomputing about 150 scripted turns per request) is proven.

`chat_eval.run_eval()` is deterministic for fixed golden bytes (two runs one second apart were identical). `ai_eval.run_eval()` embeds per-run latency measurements, so a cached snapshot is a measurement taken once, which the report already treats as scripted evidence (no actual model calls).

## Options

* Cache each evaluation result keyed by function identity and golden-file SHA-256, single-flight under a lock, returning deep copies. Chosen.
* Warm the cache in a background thread at server start so the first request after a restart does not pay the cost. Chosen.
* Move evaluation out of the request path entirely (nightly job). Rejected: larger change, no benefit over a warmed cache for a fixed golden file.

## Constraints

* Existing test `test_ai_tasks` patches `chat_eval.run_eval`; keying on function identity keeps that working.
* A cold first request while the warm-up is still running waits for the single computation instead of starting a second one.
* Tier: FULL, because `src` changes. The coordinator runs the gate; `rpi-checks.py --all` is not run here.
