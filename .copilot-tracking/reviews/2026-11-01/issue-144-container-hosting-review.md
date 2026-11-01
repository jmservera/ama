# Review: issue 144 container hosting slice (2026-11-01)

Review execution: executed once, self-review of the diff against the plan. Outcome: conformant for the delivered slice; #144 criteria remain unmet as listed.

## Findings

* Medium: worker images are real but entrypoints still print a version (criterion 1). Routed to a follow-up: queue adapter, API claim/post-back endpoint and orchestrator job.
* Medium: hosted hardening cannot be expressed on Container Apps (criterion 3); stays Partial per the README.
* Low: the load run is 120 s, 53,821 events, SQLite in one process with the client sharing it; reported as an observation, not a pass. After the PR review fixes the re-recorded warm p95 values (7.1 to 7.7 s) exceed the NFR-002 thresholds on every route; resident memory 708 MiB nears the 1 GiB limit; re-measure hosted.
* Low: no Azure restore or live rollback exercised.

## Criteria

| Criterion | Proven |
| --- | --- |
| Real worker images deployed via pipeline | No |
| Scale, probes, limits, rollback defined and tested | Defined and compile-tested; no live rollout |
| Deployed hardening | No |
| Load test recorded without production claim | Partly: short local run, no claim |
| Single-replica restart with audit persistence | Locally yes; no Azure proof |
| Tokenomics cost drivers recorded | Yes (cost Unknown) |

PR uses `Refs #144`.

Second PR review (2026-11-01): four Copilot findings on `scale_load.py` (deadline overrun, latency from dispatch, cleanup on failure, workload claim ignoring achieved rate) were valid and fixed; see the changes record. Original review outcome unchanged.

## Third review pass (2026-11-01)

Three further Copilot threads on scale_load window/throughput semantics and README timing wording were valid and fixed; scale tests (7) and ruff pass.
