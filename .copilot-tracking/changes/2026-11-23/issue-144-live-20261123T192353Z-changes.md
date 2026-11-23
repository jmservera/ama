# Changes: issue 144 live (2026-11-23, run 20261123T192353Z)

Added WorkerImageMapping (3 tests) to infra/tests/test_container_hosting_completeness.py; research note docs/reference/research/issue-144-worker-image-mapping-2026-11-23.md; README index and log entry. Focused tier: test-only, no src change. Validation: 21 tests OK; mutation of pipeline mapping fails the new test; ruff check and format clean. test_pipeline smoke test errors identically without the change (host lacks installed API). Hosted CI not observed (no push). No Azure change, no credential read.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven: mapping/module contract now tested; no src-deploy run, registry tags unreadable |
| Scale rules, probes, limits, rollback (ticked) | Not re-proven |
| Hardening enforced in deployed app | Proven except read-only root (see 2026-11-23 receipt); owner exception needed |
| Load test recorded (ticked) | Not re-proven |
| Single replica and restart with audit persistence (ticked) | Not re-proven |
| Tokenomics load-test drivers (ticked) | Not re-proven |
