# Changes: issue 144 live (2026-11-23)

Added: infra/scripts/deployed_hardening.py (offline verifier for az specs and /proc/1/status receipts), infra/tests/test_deployed_hardening.py (7 tests, pass), docs/reference/research/issue-144-live-hardening-receipt-2026-11-23.md, README index line, log entry. Focused tier (new infra tool and test, no src change). Validation: unittest 7 OK, ruff check and format clean, mypy clean on the script. Hosted CI not observed (no push). No Azure change, no throwaway resource; no credential read.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven: digest-pinned real images deployed, but no src-deploy run and registry tags unreadable |
| Scale rules, probes, limits, rollback (ticked) | Not re-proven |
| Hardening enforced in deployed app | Proven except read-only root: guard enforced on all apps and jobs; live PID 1 uid 10001, NoNewPrivs 1, empty CapInh/Prm/Eff/Amb. Root FS rw (platform has no setting): needs owner exception |
| Load test recorded (ticked) | Not re-proven |
| Single replica and restart with audit persistence (ticked) | Not re-proven |
| Tokenomics load-test drivers (ticked) | Not re-proven |
