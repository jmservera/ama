# Changes: issue 79 live evidence (Refs #79)

Tier: FOCUSED (documentation only; no src, infra, SQL or workflow change; no rpi-checks.py run).

Files: docs/reference/research/issue-79-live-ranking-publication-evidence-2026-11-18.md (new), docs/reference/README.md (index), docs/reference/log.md (entry).

## Per-criterion table

| Criterion | Proven for demo | Notes |
| --- | --- | --- |
| Same data and policy give same order (ticked) | Not re-opened | Ranking tests pass (core 146, orchestrator 11, api 58) |
| Policy changes versioned and hash-verified (ticked) | Not re-opened | Same tests |
| Named policy owner signs first rule order | Unproven | Policy owner "to be named"; live publish refused `approval_missing`; human act, no person named |
| Publication scheduled and retained | Partly proven | Schedule fired 08:50Z but the deployed orchestrator image lacks `ranking_publish` (failed); create-only Blob publication, idempotent repeat and verify proven with a DEMO-ONLY synthetic owner via the core runner; Blob immutability not proven |

## Live actions and cleanup

Created `job-demo79-ranking-publish` and container `ranking-archive-demo79`; both deleted and verified absent. No secrets printed. Driver and output: phase-witness evidence dir `live-run/`.
