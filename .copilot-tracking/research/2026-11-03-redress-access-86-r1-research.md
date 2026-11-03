# Research: resident redress access under holds (Refs #86, R1)

Issue #86 criteria 1-3 are ticked and proven by merged PRs #319, #326, #338, #406 (resident_decisions.py: scoped decisions, representative authority fields, pause/withdrawal isolation, independent recorder safeguards). Criterion 4 (independent human review and formal complaints route without detriment) is unmet.

Finding: tests prove an Independent review can open after a Paused decision and a Complaint after case closure. No test proved the routes stay open when a decision is Withdrawn, representative authority is Disputed, a tenure hold is active and retention has expired together.

Disposition: executed. Planning Readiness: Ready for a test-only slice. Named complaints/Resident Engagement owners and an accessible resident acceptance session cannot be supplied by code; they remain human-owned.
