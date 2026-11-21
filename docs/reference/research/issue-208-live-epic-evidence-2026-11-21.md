---
title: Epic 208 demo proof, per-criterion results (live run 2026-11-21)
description: Refreshed proven and unproven results for the three unticked acceptance criteria of the regulatory compliance assistant epic, with a live demo smoke check
ms.date: 2026-11-21
ms.topic: reference
---

Refs #208, Refs #440. Scope: synthetic demo, desktop only; owner decisions of 2026-11-18 apply. No credential was read, no Azure resource was created or changed, and no `src/` change was made (FOCUSED tier, documentation only). Supersedes the 2026-11-19 note, [issue-208-live-epic-evidence-2026-11-19.md](issue-208-live-epic-evidence-2026-11-19.md), where state changed.

## Result

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Stabilization checkpoint (#440) before closure | Partly proven | Regulatory regression passes locally and the deployed demo is healthy and auth-gated (below). #215 and #216 are now closed with no unticked criteria. #440 remains open with two unticked criteria (finding triage into issues; PR artifacts and independent review) and unresolved owner retention and privacy decisions on its checkpoint candidate. An owner pivot or defer decision is not agent-provable |
| 2 | Decision accepted, amended or epic closed | Proven in repository evidence | #209 closed 2026-10-16T16:11:45Z; ADR 0005 Status: accepted for synthetic development only, 2026-10-16. Ticking is left to the coordinator |
| 3 | Children accepted in ADR phase order | Not met as stated | ADR phasing: law store (#210), rule cards and engine (#211, #212), chat (#214), change monitoring (#213). Observed closure: #210 2026-10-15, #217 2026-11-18, #213 and #211 2026-10-27, #214 2026-10-31, #212 2026-11-04, #216 2026-11-19, #215 2026-11-19. #213 closed before #214 and #212, and #214 before #212; no owner note accepts the deviation |

## Evidence

Run on base `9c3fe9dcb`, 2026-11-21, sequentially, with PYTHONPATH pointing at this worktree.

* core: test_rulecards, test_rule_engine, test_regulatory_chat, test_regulatory_output_guard, test_regulatory_eval_gates_216, test_regulatory_privacy, test_regulatory_privacy_audit_217, test_regulatory_usage: 145 tests OK.
* api: test_lawstore, test_regulatory_chat_api, test_regulatory_watch_guard_api, test_regulatory_ux_check, test_regulatory_a11y_cues: 71 tests OK, 14 skipped (browser or SQL prerequisites; not passes).
* agents: test_regulatory_gates, test_regulatory_answers, test_regulatory_non_advice_guard: 30 tests OK.
* `python3 -m unittest tools.test_epic_208_child_order`: 6 tests OK.
* Live demo, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` reports Running, latest revision `ca-cutover-test-demo-api--0000038`, Healthy; `GET /healthz` returns 200; unauthenticated `GET /api/regulatory/rule-cards` returns 401. `ca-resident-demo` is on revision `ca-resident-demo--0000015`.

## Unproven and why

* Criterion 1 remainder: #440 triage and review criteria, and its retention and privacy decisions, belong to the owner and independent reviewers. An authenticated live Playwright walk of the chat was not repeated; earlier live proofs are recorded in [chat-breakglass-live-proof-2026-11-18.md](chat-breakglass-live-proof-2026-11-18.md) and [assistant-ux-live-159-2026-11-18.md](assistant-ux-live-159-2026-11-18.md). Azure-only residuals beyond the smoke check were not exercised.
* Criterion 3: only the owner can accept or amend the delivery order.
* No defect was found, so no source change or regression test was added.
