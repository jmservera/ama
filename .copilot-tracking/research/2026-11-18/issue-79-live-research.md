# Issue 79 live research (2026-11-18)

Disposition: executed. Planning Readiness: Ready.

Unticked criteria: (3) named owner signs first rule order; (4) snapshot publication scheduled and retained.
Findings, commands and outputs: docs/reference/research/issue-79-live-ranking-publication-evidence-2026-11-18.md.
Repo checks: ranking tests core 146, orchestrator 11, api 58, all OK.
Live: scheduled job fired 08:50Z (failed: orchestrator image lacks ranking_publish); core runner via API image refused the unsigned policy, then published create-only with a DEMO-ONLY synthetic owner; throwaway job and container deleted.
