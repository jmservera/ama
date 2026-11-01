# Research: issue 440 second stabilization checkpoint (2026-11-01)

Research disposition: executed. Planning Readiness: Ready.

## Question

Which #440 acceptance criteria remain unmet on `origin/main` 36a1d0da25cf73ca41f613a5c7a7df071d5b0771, and what bounded local slice moves them without a heavy gate?

## Evidence

* PR #461 delivered the coordinator "Stabilization checkpoints" section (`.github/agents/ama-backlog-delivery-coordinator.agent.md`), the `src/README.md` "Stabilization validation ladder" and the first checkpoint record in `docs/architecture/cutover-evidence-pack.md` (main 140d8f49, BRD 0.19.0, PRD 0.18.0). Criteria 1 to 6 are therefore met by merged text.
* Owner closure audit (2026-10-31 comment) lists criteria 7 and 8 as unmet. Criterion 7 gap: the PERF-440 benchmark finding (17383 ms against 1500 ms once, three focused repeats at 106-108 ms, root cause unknown) has no scoped issue. Criterion 8 gap: the native discovery result is coordinator-attested only and the seven behavior scenarios are simulated.
* Open-issue search (`60000`, `sql_reads`, `PERF-440`) found only #440 itself, so the benchmark finding has no existing owner. #349, #350, #360, #432 remain the owners of live-acceptance gaps; no duplicates are needed.
* Main has advanced from 140d8f49 to 36a1d0da. Documents at this pin: BRD 0.21.0 (draft), PRD 0.21.0 (in-review). The first checkpoint is historical for the older runtime.
* The shared heavy lock is held by another session (`rpi-checks.py --all` for issue 163, output /tmp/gate-163). Per the ladder it is not interrupted, read or duplicated; SQL Server and container groups are therefore blocked for this slice, and the owner's focused tier excludes the heavy gate anyway.

## Constraints

* Focused tier: relevant unit tests, ruff check, ruff format --check and mypy for touched projects. No code changes are planned, so project static checks are run read-only as checkpoint evidence only.
* No coordinator edit is planned. A coordinator edit would be a Major HVE change needing static, behavior and host validation, which is not feasible in this slice.
* No Azure, private data, paid model calls or secrets.

## Conclusion

Deliver a second bounded local checkpoint on the pinned main (focused suites, the benchmark selector repeated, static checks), file one scoped issue for the unattributed benchmark risk to close the criterion 7 gap, record results in the evidence pack, and use `Refs #440` naming criteria 7 and 8 unless the evidence proves them. Criterion 8 cannot be proven locally.
