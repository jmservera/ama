# Changes: issue 2243 live probe (2026-11-22)

No source change. Tier: focused (documentation and probe scripts); basis: no src, workflow, Dockerfile or dependency edit. Hosted CI for the exact head was not observed; no local gate was run (rpi-checks.py --all is forbidden by the brief).

Added: docs/reference/research/issue-2243-live-probe-2026-11-22.md, its probe scripts, results and screenshots; README index and log.md entries.

Azure: read-only only (containerapp show, revision list, console logs). No throwaway resource created, nothing to delete. Sign-in values never printed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Derive EXPIRES from ZF_DEMO_EXPIRES_AT | Unproven | Only on the unmerged local branch; label change on revision 0000022 is consistent, but the registry is firewalled so digest-to-commit is unreadable |
| Add a test | Unproven | Fix branch work, not reviewed here |
| Rebuild and roll resident image | Partly proven | Revision 0000022, new digest, Healthy, 100% traffic |
| Resident chat answers with the model within caps | Unproven, currently failing | Both model-eligible questions return reason=usage_limit; probable cause is SQL resident_ai.budget.expires_at (2026-11-01 default), SQL is private and unreadable |

## Follow-ups

* After merge, run the post-merge probe plan in the research note; the owner-authorised SQL path must update resident_ai.budget.expires_at.
