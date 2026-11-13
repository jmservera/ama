# Details: 521-azure-preflight-pack-1444

* Step 1: git cherry-pick -n of the three SHAs; paths are disjoint under .copilot-tracking.
* Step 2: replace the Pending sentence at infra/README.md ~4621 with: read-only observation 2026-11-13 shows ca-resident-demo ZF_DEMO_EXPIRES_AT 2028-01-01T00:00:00Z; live SQL constraint and row verification remains pending; no closure of #521. Refs #521, #133, #152, #360, #440.
* Step 3: after all edits and staging: python -m zava_forward.core.synthetic.cutover_audit --write --root . then rerun without --write; exit 0. Date-qualify the earlier live-window text in the README.
* Step 4: log entry under docs/reference/log.md, ASCII only.
