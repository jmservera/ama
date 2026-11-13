---
title: Issue 82 deterministic gates details
ms.date: 2026-11-13
---

## P1 Gate functions

* Rules reuse `_UNREVIEWED`, effective date 2026-11-13, version "1"; sources cite BRD RULE-001/002 and PRD FR-008 with FR-019 (grants/finance) as exercise fixtures.
* `eligibility_gate(state, owner, on)`: wraps `check`; only `True` passes, None unknown, False fail.
* `finance_gate(state, reason, on)` and `authority_gate(state, reason, on)`: same pattern as `capacity_gate` (True via `check`, False fail with reason, None unknown with reason).
* Typed errors `FinanceGateError(ValueError)` and `AuthorityGateError(PermissionError)` carry `.state` and `.result` and keep message text.

## P2 Registry

`CONTROLLED_RULES: dict[str, GateRule]` maps each of `GATE_KINDS` to its rule; safety maps to `SAFETY_RELEASE_RULE`, others to booking/quality/capacity/new rules. Test asserts keys equal `GATE_KINDS` and each record has non-empty four fields and `reviewer` starts with "Unreviewed" (no invented reviewer).

## P3 Wiring

* `_fin_commit_raise`: budget missing or not a dict with a status -> state None only if the budget field is unreadable (not dict); no budget (None) or not Approved -> False; over-budget -> False. Message text unchanged.
* `require_authority`: unreadable designation (not a dict, wrong keys, bad dates, malformed permissions) -> state None; readable but not Active/expired/out of scope/not matching subject/production -> False. Message `denied` unchanged, type PermissionError subclass.

## Critique amendments

* Registry `CONTROLLED_RULES` is a tuple of every rule object (safety release, four booking rules, quality, capacity, eligibility, authority, finance); test covers every `GATE_KINDS` entry and metadata validity; a separate test reports unreviewed status.
* Finance: no budget or not Approved or over budget is fail; unreadable budget or commitments is unknown; gate evaluated on success with `on` date semantics; no mutation on refusal.
* Authority: gate evaluated on success too; unchanged denial text.
* Add regression assertions for messages and a pre-effective date unknown.
