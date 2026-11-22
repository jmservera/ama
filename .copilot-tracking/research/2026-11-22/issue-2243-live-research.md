# Research: issue 2243 live probe (2026-11-22)

Disposition: executed. Planning Readiness: Ready.

Canonical note: docs/reference/research/issue-2243-live-probe-2026-11-22.md

Findings:

* ca-resident-demo is on revision 0000022 (14:30 UTC, Healthy); ca-cutover-test-demo-api on 0000050.
* Resident chat falls back with reason=usage_limit (console log), no longer "expired".
* Likely cause: resident_ai.budget.expires_at defaults to 2026-11-01 (infra/sql/resident-assistant.sql). SQL is private; unreadable from here.
* ACR is firewalled, so image-to-commit mapping is unreadable.
* Employee chat 500-then-200 and deterministic answers persist (issue 2245).
