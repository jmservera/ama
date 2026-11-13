# Research: integrate #521/#133/#152 packages and fix stale expiry sentence

* Three path-disjoint commits (ac7c73a07, ca26d3b6b, e13d3516c) share parent dafed6a27 and touch only .copilot-tracking files; cherry-pick onto 1ccfae438 is expected to be conflict-free.
* infra/README.md line 4621 says the live app expiry move to 2028-01-01 remains Pending. The 521 research package records ca-resident-demo env ZF_DEMO_EXPIRES_AT = 2028-01-01T00:00:00Z (read-only, 2026-11-13). SQL constraint and rows are unverified.
* Editing infra/README.md may shift offsets in docs/architecture/cutover-reference-inventory.tsv; regenerate via cutover_audit and verify --root exits 0.
* Planning Readiness: Ready.
