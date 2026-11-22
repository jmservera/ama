# Plan: issue 2192 live proof r4 (focused tier, no src change)

1. Copy the r3 probe to docs/reference/research/issue-2192-live-r4-2026-11-22/, add a before/withheld/restored sequence plus map and chat-label checks.
2. Run once against ca-resident-demo--0000024 and the API; restore the resident to its original state.
3. Write the dated note, index and log entries; run link check and diff review.

Critique (single pass, 2026-11-22): compatible findings applied. (a) Record the employee state before, after withholding and after restore, so the probe sets the resident to withheld explicitly whatever the initial state; (b) never print credentials; scrub emails; (c) the chat check must not lift the suspension or make production changes; (d) report the AI chat suspension honestly if present. No conflict with owner decisions. Verdict: proceed.
Details: see issue-2192-live-plan.md (same steps). Tier: focused, no src change.
