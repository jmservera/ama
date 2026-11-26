# Changes r15

## Files

* `docs/reference/research/issue-107-live-r15-in-environment-real-ai-2026-11-25.md`, `docs/reference/README.md`, `docs/reference/log.md`: evidence note, index, log.
* `.copilot-tracking/evidence/107-live-r15/`: redacted runner payload, MSI probe, harness report.
* No `src/` change; focused tier (documentation and evidence). `rpi-checks.py --all` not run; no tests needed.

## Azure changes (demo, resource group ama)

* None persisted. One `az containerapp exec` session ran the merged harness once in the demo API replica using its managed identity; temp files removed. Spend: 258 tokens (USD 0.000039 at demo rates).

## Divergences

* `azure.identity` failed in the exec shell; the runner called the identity endpoint directly.

## Per-criterion table

| Unticked criterion | Status | Evidence |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images/restarts cannot restore revoked approval or replenish finite allowances | Unproven (11 of 13 fields on constructed fixtures per r12; no real older image run) | r12 note; r15 note |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Proven for the demo within limits: five releases in force (r14) and measured real-AI tokens per assistant, 258 total. Not proven: app-generated proposals (invoke path off, no allowance), OQ-017/018/019 clearance | r15 note; `harness_report.txt` |
