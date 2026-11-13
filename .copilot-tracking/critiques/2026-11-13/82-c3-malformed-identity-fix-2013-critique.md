---
title: 82-c3 plan critique
ms.date: 2026-11-13
---

Executed once by an independent rubber-duck agent. Verdict: Revise (all findings compatible; applied directly, no user decision).

* PC-001 safety_release_gate non-iterable recorders or `[None]` can raise or pass: applied (unknown on malformed recorders; tests).
* PC-002 shared type-safe `_norm` would let malformed supplier/work order values match in `match_invoice`: applied (`_same` requires both strings; identity normalisation separate in effect).
* PC-003 legacy lookup ambiguity: applied (lookup only for `None`/`{}` identity; any other non-well-formed identity refuses; both stores and SQL re-check tested).
* PC-004 iterable boundary: applied (non-iterable or bare string input is unknown; non-string items unknown).
* PC-005 compatibility tests: applied (missing/None `oid` staff still works; actual finance sign-off tests).
