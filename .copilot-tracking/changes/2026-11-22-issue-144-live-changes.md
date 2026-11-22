# Issue 144 live changes (2026-11-22)

Changed: added docs/reference/research/issue-144-live-hosting-2026-11-22.md, a README index line and a log entry. No src change; focused tier. No Azure change; no throwaway resource.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven: digest-pinned real images, but zero src-deploy runs and registry unreadable |
| Scale rules, probes, limits, revision rollback (ticked) | Not re-proven here; live scale rules and probes observed |
| Hardening enforced in deployed app | Partly proven: non-root and no effective caps live; read-only FS disproved; no securityContext |
| Load test recorded (ticked) | Not re-proven |
| Single replica and restart with audit persistence (ticked) | Not re-proven |
| Tokenomics load-test usage drivers (ticked) | Not re-proven |
