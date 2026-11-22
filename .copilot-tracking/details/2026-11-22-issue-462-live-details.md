# Details: issue 462 live recheck (2026-11-22)

## Phase 1

Script `evidence/2026-11-22-resident-showcase-live/live_r5.py` (copy of r4). Credentials from `~/.ama-resident-test-user` at runtime. Azure reads: `az containerapp show` for `ca-resident-demo` and `ca-cutover-test-demo-api`, `az resource list -g ama`.

## Phase 2

`docs/reference/research/resident-showcase-live-r5-2026-11-22.md`; one row in `docs/reference/README.md`; one entry in `docs/reference/log.md`.

## Phase 3

Changes record, one independent-style review, commit with `Refs #462`.
