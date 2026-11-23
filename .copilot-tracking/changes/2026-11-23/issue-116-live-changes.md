# Changes 2026-11-23, issue 116 live

Tier: focused (documentation only, no src change). Files: `docs/reference/research/issue-116-live-r8-evidence-2026-11-23.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists at every provider boundary (unticked) | Proven offline for each enumerated boundary; live payloads unproven | 125 tests green (24, 45, 56) at ac58e5c451; r7 matrix; live payload invisible from deployed apps |
| Every role against every endpoint | Ticked; not rerun live (no credentialed sweep this round) | Prior rounds |
| Contractor view has no vulnerability reason | Ticked; not rerun live | Prior rounds |
| Free-text redaction decided | Ticked | Prior rounds |
| Roles allowed vulnerability reason (OD-14, OD-19) | Ticked | Prior rounds |
| Provider-spy tests zero canaries | Ticked; rerun green | Spy suite |
| Unknown task/field, excess input fail visibly | Ticked; rerun green | Bounds suite |
| Output/citation/export recheck | Ticked; not rerun live | Prior rounds |
| Document AI derivative or exception | Ticked; rerun green | Spy suite |
| Source permissions, proposal-only, consent | Ticked; not rerun live | Prior rounds |
| Reuse current wrappers | Ticked | Shared `approved_payload` |

Live probe unauthenticated: 401, 401, 200. Unproven: live payloads, independent review, hosted CI. The owner ticks the box after review.
