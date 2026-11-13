<!-- markdownlint-disable-file -->
# Plan details: demo infrastructure readiness

Plan: [.copilot-tracking/plans/2026-11-13/demo-infra-readiness-0548-plan.instructions.md](../../plans/2026-11-13/demo-infra-readiness-0548-plan.instructions.md).

## Phase 1: record dispositions

* Files: tracking artifacts only under `.copilot-tracking/` dated 2026-11-13.
* Rejected candidate slices:
  * #137 offline guard for empty check references: already present (README 1024; infra/tests/test_bicep_policy.py asserts empty profile references and synthetic references; tests not executed here).
  * #146 console-export routing: paused; would disable two severity-1 ledger alerts.
  * #144 worker wiring: allowance exhausted and necessity undecided.
  * #148 rebuild adapter/dry run: delivered by #1348 and #1410.
  * #189 expiry/owner/time-limit tests: delivered; C5 exhausted.
* Validation: git diff review only; no executable gate (documentation-only).
