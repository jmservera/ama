---
applyTo: '.copilot-tracking/changes/2026-11-13/521-azure-sync-preflight-1416-changes.md'
---
# Plan: Azure sync preflight (Refs #521, #360, #891, #435)

Research: ../../research/2026-11-13/521-azure-sync-preflight-1416-research.md. Details: ../../details/2026-11-13/521-azure-sync-preflight-1416-details.md.

* [x] Phase 1: Re-verify read-only observations in the research file (az metadata only, no secrets) and run safe dry-run of resident_showcase_sql.py (no --apply) to confirm the rendered cutoff is 2028-01-01T00:00:00.
* [x] Phase 2: Record the preflight outcome (go/no-go per item a, b, c) in the changes file; no source or README edits (README contradiction flagged, not resolved).
* [ ] Phase 3: Independent review, then clean commit (tracking files only).

Tier: Focused (tracking-only, documentation-class). Stop rules: any mutation, secret exposure, or `.env` read stops the work.

Critique dispositions (rubber-duck, Revise, applied directly): allowlisted `--query` probes only and suppressed stderr; ids withheld from artifacts; (a) target ambiguity (`workload=forward`) recorded and NO-GO; (c) requires pricing-aware hard cap runner; go/no-go derived from fresh probe results; dry-run checks exact `2028-01-01T00:00:00` and both exit statuses on Python 3.12.
