---
title: Issue 159 live changes
ms.date: 2026-11-18
---

Refs #159. Tier FOCUSED (docs and evidence only; no src change; no `rpi-checks.py --all`).

## Files

* `docs/reference/research/issue-159-live-chat-experience-evidence-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/evidence/2026-11-18/issue-159-live/` (driver, JSON, screenshot)
* `.copilot-tracking/{research,plans,details,challenges,changes,reviews,rpi-sessions}` dated artifacts

## Per-criterion table (issue 159)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Panel available from a permitted case, never required | Already ticked | Panel opened from case workspace; unchanged |
| Cited, labelled answers, abstain, "AI suggestion, not approved" | Already ticked; re-observed | Research note, #164 note |
| Follow-ups keep case context, re-check permissions | Already ticked; follow-up observed | Thread turn 2 of 30 |
| Proposal-only, no controlled-record change | Already ticked; consistent | "No record was changed" |
| Model failure falls back to workflow-only | Already ticked; observed | Fallback status and message |
| Keyboard operable | PROVEN for demo (desktop) | Live Playwright run, axe 0 violations |
| Announces new messages | PROVEN programmatically (live-region semantics and additions); speech not tested | `live_chat_a11y_probe.json` |
| Screen-reader tested | DEFERRED, unproven (person-run AT waived for demo) | Not run |
| Tokenomics per turn | Already ticked; re-observed | Per-turn calls/tokens/outcome and 2 of 30 bound |

The combined unticked criterion stays unticked. Residue: chat threads deleted; no Azure resource created; no secret retained (literal scan clean).
