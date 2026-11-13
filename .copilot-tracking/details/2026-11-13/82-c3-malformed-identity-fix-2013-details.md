---
title: 82-c3 malformed identity fix details
ms.date: 2026-11-13
---

## Phase 1

* Grants: parametrised falsey (`0`, `False`, `[]`, `{}`, `0.0`) and truthy non-string `oid`, `email`, `code` on recorder, proposer and approver: verdict is `unknown` with a non-empty reason mentioning malformed identity.
* Grants end to end: a pending proposal whose stored proposer identity, or a registry approver record, holds a non-string field: `grant_approve` raises `ValueError`/`PermissionError` only (never `AttributeError`/`TypeError`), state stays Claimable.
* Finance sign-off: `_independent` with non-string identity values raises `PermissionError`.
* Gates: non-string evidence/quality items, blank/non-string reasons, non-iterable inputs return fail/unknown with non-empty reason.

## Phase 2

* `finance._norm`: `value.strip().lower() if isinstance(value, str) else ""`.
* `finance.identity_well_formed(identity)`: dict, `email` and `code` non-blank `str`, `oid` `None` or `str`.
* `_independent`: unknown-identity refusal when stored identity is not well formed; also refuse when the acting user's own identity fields are malformed. Keeps `PermissionError` contract.

## Phase 3

* `grants._complete` uses `identity_well_formed`; add `_malformed` reason branch before the unknown branch.

## Phase 4

* `gates._reason` helper: non-blank string else a fixed fallback; `GateResult` stays strict. `_outcome_gate` and `capacity_gate` use it. `_text_items` keeps only non-blank strings and flags any other item as malformed, so evidence/quality/booking gates return unknown (non-string) rather than raising or passing.

## Critique amendments (applied)

* Phase 2: `_independent` looks up the registry only when identity is `None` or `{}`; other malformed values refuse. `match_invoice` uses a `_same` helper requiring both strings.
* Phase 4: `safety_release_gate` recorders must be a non-string iterable of strings/None-free; otherwise unknown. `_text_items` returns `None` (unknown) for non-iterable, bare string or non-string items.
