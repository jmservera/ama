# Issue 188 research: demo fixture dependency (2026-11-03)

Disposition: executed (reuse of 2026-11-01 and 2026-11-02 research plus fresh PR check).

## Delivered so far (merged PRs, all Refs #188)

* #508 (#110 consumer), #587 (consistency model), #645 (operator verifier `sensor_handover_verify`), #698 (local demo), #791 (re-validation).
* Issue 188 comments: all three criteria need a live Hub to Azure SQL run, blocked on owner decisions for #110 (tier, sizing, cost, exposure, credential owner) and Azure access.

## Unmet acceptance criteria (unchanged)

* Live and backfill series queryable together per home ID: proven on constructed SQLite and local SQL Server only.
* No handover discontinuity beyond declared tolerance: proven on constructed climate only.
* Window re-run idempotent: proven locally only; live Azure SQL restart unproven.

## Open follow-ups from the #698 review

1. Run the verifier on Azure SQL after a live stream: owner-gated.
2. Real pinned climate in the demo: the real climate source is recorded as blocked (`docs/reference/research/climate-paired-source-blocker-178.json`).
3. Demo imports test fixtures through a long PYTHONPATH: actionable now.

## Selected slice

Follow-up 3, minimal form: the demo locates `src/core/tests` itself, so it runs with package paths only. No criterion changes state. Planning Readiness: Ready. No security, infrastructure, SQL or deployment surface is touched (SQLite-only demo, README text), so the focused tier applies.
