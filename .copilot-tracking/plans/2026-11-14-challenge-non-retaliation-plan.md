---
title: Challenge non-retaliation plan (issue 220)
ms.date: 2026-11-14
---

## Plan

* Phase 1: add `protected_snapshot`, `protected_changes`, `assert_no_retaliation`, `GUARANTEES` to `challenges.py`.
* Phase 2: wrap `challenge_open`, `challenge_resolve` and `nomination_correct` writers with the guard.
* Phase 3: expose `challenge_guarantees` in case detail (hidden from readers without challenge rights) and list it in `panels.js`, with no `aria-invalid` and no new `role="status"`.
* Phase 4: add `src/api/tests/test_challenge_non_retaliation_hazard_guard.py` (unit, HTTP, refusal and visibility), update `src/core/README.md`.
* Validation tier: focused. Targeted unit tests, mypy and ruff with /tmp caches in `src/core` and `src/api`.

## Critique (single pass)

* Guard must compare absent keys correctly: snapshot keeps absent keys absent. Applied.
* Guard must not block legitimate challenge records: `affected_challenges` and nomination records are excluded from the protected set. Applied.
* Rolling back relies on the writer's existing transaction semantics; proven by a patched retaliating writer test. Applied.
