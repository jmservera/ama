---
title: Regulatory security and privacy research
description: Local implementation evidence for issue 217
ms.date: 2026-10-16
---

## Identity and disposition

Task: 217 / regulatory-security-privacy-217. Research executed through direct
inspection. Planning Readiness: Ready for the bounded synthetic implementation,
not operational acceptance.

## Evidence

* Issue 217 requires a DPO DPIA, retention alignment, minimisation, separate
  Entra capabilities, audit, adversarial tests and named human reasons.
* ADR 0005 was accepted for synthetic development only on 2026-10-16.
  Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
* The clean topic branch contains merged PRs 328, 331 and 348. Reuse it.
* core/regulatory_chat.py already gates synthetic use, projects and minimises
  facts by purpose and role, masks questions and uses the existing chat tables.
  No separate reg_chat_turn table exists: each question/answer pair is two
  chat_message rows in a regulatory-prefixed chat_thread.
* agents/regulatory_chat.py is an offline extractive composer with no model or
  tool access. Quoted source instructions are untrusted data.
* Rule cards, checks, alerts and source reviews already have immutable,
  transactionally written SQL records. Chat turn audit is currently a later,
  separate write, so a committed turn can lack its audit event on failure.
* TrustedProxyProvider maps separate RuleAuthor and RuleOwner claims, but there
  is no separate regulatory-chat capability or registration for these roles.
* ChatPrivacy owns shared retention references but thread/message expiry is not
  implemented. Check/alert retention periods are not approved. Inventing numeric
  defaults or deleting immutable ledger evidence would be unjustified.
* The deterministic significant-decision check currently accepts evidence without
  recorded reasons. Tighten that bounded contract and invalidate old checkpoints.

## Boundaries and gaps

No private data, deployed service, paid inference or actual tenant assignment
is necessary for these local checks. DPIA completion, DPO-set periods, operational
retention/erasure, provider terms, tenant roles, real human decisions and Azure SQL
ledger validation remain unmet. Legal snapshots are design references only;
this work makes no new current-law or legal-compliance assertion.
