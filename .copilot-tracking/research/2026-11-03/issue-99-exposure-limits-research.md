<!-- markdownlint-disable-file -->

# Task Research: issue-99-exposure-limits

| Field | Value |
| --- | --- |
| Date | 2026-11-03 |
| Status | Complete; Planning Readiness Ready |
| Research disposition | reused (earlier finance-96-98-99 research) plus a fresh check of merged PRs |

## Findings

* PR #510 (merged 2026-10-29) delivered OD-12 and OD-15 as held ledger entries in `form_review.py` with null approved inputs and a diagnostic-only pause. No criterion was ticked.
* No code records an envelope or tolerances as human-approved inputs, and nothing evaluates exposure against them.
* BRD RULE-011 requires a Board-approved envelope before acceleration; RULE-012 names six tolerance dimensions (safety, resident, quality, capital, grant, capacity) and requires a breach to escalate and block new acceleration. Restart needs control owner and Board approval.
* No company figures exist; the issue states it depends on company data.

## Selected slice

A pure core module that (1) records limits only with an approval record (approver, role, date, evidence reference, restart owner) and (2) turns exposure versus limits into a pause signal for a human decision. Missing limits or exposure are Held or Unknown, never within limits. Not wired to store, API or UI.

## Out of scope

Company figures, persistence, API and UI, containment of live activity, verifying approver authority, restart workflow.
