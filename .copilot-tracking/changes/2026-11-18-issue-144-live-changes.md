# Changes: issue 144 live proof (documentation only, FOCUSED tier)

Refs #144. No `src/` change, so FULL tier is not triggered and `rpi-checks.py --all` was not run. Live Azure actions were read-only plus one exec probe and one 60 s load run; no resource was created, so nothing needed deleting.

Divergence recorded: the research note and index/log entries were drafted during Research, before the `implement-start` witness call; they are documentation, not source.

Files: docs/reference/research/issue-144-container-hosting-live-evidence-2026-11-18.md (new), docs/reference/README.md (index paragraph), docs/reference/log.md (entry).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Real and versioned proven; pipeline unproven | Digest-pinned ACR images everywhere; `src-deploy.yml` has no runs and needs private runners; ACR is private. Stays unticked. |
| Scale rules, probes, limits, revision rollback (ticked) | Re-observed | Config read and scale 0 to 4 under load. |
| Hardening enforced in the deployed app | Non-root proven; read-only fs and dropped capabilities unproven | uid 10001, CapEff 0, but CapBnd default, NoNewPrivs 0, rw overlay; no securityContext in schema 2025-07-01 or 2025-02-02-preview. Stays unticked. |
| Load test recorded without production claim (ticked) | Re-observed at demo scale | 15,819 requests, p95 1.31 s, all 200, 4 replicas. |
| Single-replica restart with audit persistence (ticked) | Not re-run | Drills excluded by owner. |
| Tokenomics per-unit drivers (ticked) | Partly re-observed | Requests and replicas recorded; price unknown. |

## Validation

* Link and diff review of the three documentation files.
* No unit tests, mypy or ruff apply (no Python change).
