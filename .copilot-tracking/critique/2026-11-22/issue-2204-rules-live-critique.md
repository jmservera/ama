# Critique: issue 2204 rule actions live plan (2026-11-22)

Executed once, by the worker, against the final candidate plan.

Verdict: approve with direct dispositions.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | A second app registration change could affect the shared estate | Limit to env vars on the demo API and one blob container; no Bicep, no Key Vault, no SQL SKU change. Applied |
| 2 | Enabling the law store caused one failed revision and brief downtime | Recorded as observed; rollback executed; retry succeeded. Kept in evidence. Applied |
| 3 | Throwaway Entra user could trip MFA or conditional access | Fallback: single-account proof (author 201, owner approve refused 409 as designed) and state the distinct-person approval as unproven. Applied |
| 4 | Approving or activating cards persists synthetic state in the demo SQL | Cards are labelled exercise cards with simulated approval; retire the test card at the end; document that history is append-only and stays. Applied |
| 5 | Role assignments of the test account must be restored | Reuse the restore-in-finally pattern; confirm the final Graph read shows ProgrammeManager only. Applied |
| 6 | Credentials and throwaway password must not be stored | Read at run time, scan evidence for literals. Applied |
| 7 | Source-code change not planned, so Tier is focused | Confirmed; escalate to FULL only if src changes |

No conflict with owner decisions; no user decision required.
