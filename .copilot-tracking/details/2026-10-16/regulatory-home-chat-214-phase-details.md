---
title: Home chat phase details
description: Evidence and completion boundaries for issue 214
ms.date: 2026-10-16
---

## P01-T01

Reuse C1-C6 from research. Do not reuse C7 arbitrary-prose validation.
API builds a bounded bundle from current law-store provisions and active
simulated cards, using shared source eligibility. Project the case first, then
select structured fields by question purpose. Agents accept data only and
render attributed excerpts and facts, not new legal prose. Store the full
response envelope as an assistant message with IDs in evidence.

## P02-T01

Separate regulatory endpoint so existing case chat behaviour is preserved.
Synthetic mode is off by default. The optional panel exposes cited answer,
status/date metadata, doubt button and owner-only inbox. Reauthorise on every
read/turn/referral. Copy only a selected question/answer, not the entire thread
or memory, inside one existing repository transaction. Missing/ambiguous owner
is an explicit failure, never a success-shaped notification.

## Final critique dispositions

* PC-001: Require ZF_REGULATORY_CHAT=synthetic-demo, a matching dataset marker,
  non-production mode and SYNTH-prefixed existing privacy references on every
  regulatory operation. No provider is wired into this offline path.
* PC-002: Low-level repository writes in one transaction, source row-version
  comparison, idempotent receipt and JSON pre-image restoration on failure.
  Audit remains metadata only; a post-commit audit failure is surfaced explicitly
  with a retryable committed receipt, not described as rolled back.
* PC-003: Resolve exactly one provisioned staff name Juan Manuel Servera, using
  its server-side user key; no client recipient. Bind selected assistant seq to
  preceding user seq. Both principals must retain the stored role and case
  access. Regulatory history is read through guarded endpoints; generic chat
  reads reject regulatory threads on role changes too.
* PC-004: JSON schema regulatory-chat-v1 in message content, strings only in
  evidence. Snapshot fact IDs include a value hash and observed-at date;
  effective date is explicitly unknown. Bound sources/cards/facts and reject
  oversized envelopes before persisting. Sources are attributed excerpts, not
  findings about legal applicability.
* PC-005: Supported purposes are hazard and automated-decision source lookup.
  Question matching is deterministic; unknown/mixed unsupported and legal
  interpretation requests refuse. Same-purpose card safe-action/clock
  disagreement and changed approved source versions are potential conflicts,
  shown together without resolution, requiring explicit human handoff.
* PC-006: Independently specified expected question/outcome cases, exact
  citation/excerpt equality and refusal rates on a development set. Compare
  home-context fragments and lookup steps against identical cards/links;
  no claim about staff time, model semantics or business benefit.
* PC-007: Eight issue rows each mapped to tests and explicitly qualified in
  API README/review; issue checkboxes stay untouched.
* PC-008: Loopback app checks cover health, case, regulatory answer, persisted
  history, doubt and owner inbox. Panel structural tests cover keyboard/status
  and actual endpoint wiring; real browser/human accessibility remains untested.

## P03-T01

Test valid grounding, question minimisation, role/case/user isolation, changing
facts, missing/partial/stale/future/unapproved sources, legal refusals, injection,
conflicts, no model-negative alert suppression, persistence/restart, owner
handoff/rollback and deterministic card comparison.

## P03-T02

Run absolute per-project PYTHONPATH unittest, ruff and mypy. Local loopback
HTTP harness is the app exercise; it must check responsive health/case/chat.
Record exact counts and unmet full acceptance in READMEs/review. Use only
temporary synthetic datasets, never private runtime defaults.
