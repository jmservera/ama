---
title: Issue 82 funding reader consistency research (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Scope and disposition

Research disposition: `executed`. Planning Readiness: `Ready` for one bounded increment. Base `dc9fb68e024f280c435b97accbae2a8becde2786` (frozen candidate of task `server-gate-readiness-82-1112`), branch `research/demo-82-followup-2250`, clean worktree at start. Refs #82 only. Model: explicit Claude Sonnet 5.5. Child of `server-gate-readiness-82-1112` (parent task), follow-up rank 1 (Review RV-01).

Question: do `chat_case_answers.py`, `taskqueues.py` and `home_case.py` read `funding_ok` with a definition consistent with the canonical explicit-`True` definition, and if not, what is the smallest reuse-first fix?

## Authority and spent history

* Authority: the coordinator launch brief for this follow-up (not a new five-cycle pool, no exhaustion renewal). It admits only the three readers and directly related existing tests as write surface.
* Spent history preserved and untouched: original task `server-gate-readiness-82-1112` research, plan, critique, changes, review (RV-01 open, RV-02 corrected without re-review) and its adverse evidence; the independent assessment `rpi-82-refill-2236-result.json` (Pass, bounded; finding A-02 declares exactly this gap). No correction allowance is created.
* The original 1490 head or worktree is not modified.

## Canonical definition (reuse)

* `gates.booking_gates` (`gates.py:200`) passes funding only for an exact `bool` `True`; absent, `None` or non-boolean is `unknown`.
* `Store.gate_reasons` (`store.py:171`, delivered at the base) uses `c.get("funding_ok") is not True`.
* No shared helper exists. Adding one in `gates.py` or `store.py` is outside the exclusive write surface, so each reader applies the same one-expression definition inline. This mirrors the delivered store fix.

## Reproduction

Executed [probe-readers.py](../../evidence/2026-11-12/funding-readers-82-2250/probe-readers.py), output [repro-before.out](../../evidence/2026-11-12/funding-readers-82-2250/repro-before.out), on the base with the fictional building fixture (ZF-2, stage "Final checks before ordering"):

| `funding_ok` | home_case `funding_confirmed` | chat `funding_ok` fact | queue funding blocker |
| --- | --- | --- | --- |
| `True` | `True` | confirmed | none |
| `False` | `False` | not confirmed | present |
| `None` | `None` (not a bool) | not confirmed | present |
| `"yes"` | `"yes"` (passed through, UI shows "yes") | confirmed | none (reads as funded) |
| `1` | `1` (UI shows "yes") | confirmed | none |
| `"false"` | `"false"` (truthy, UI shows "yes") | confirmed | none |
| absent | `KeyError('funding_ok')` | no fact | present |

So three tightly coupled inconsistencies at the base:

1. `chat_case_answers.py:79`: truthy non-boolean reads "confirmed" in a resident- and staff-facing chat fact.
2. `taskqueues.py:295`: truthy non-boolean suppresses the funding blocker, so the queue says no funding stop while the server gate says unknown.
3. `home_case.py:156`: indexes `case["funding_ok"]`, so an absent key raises `KeyError` (the view fails for the case; the API treats `KeyError` as not found), and non-boolean values pass through and show "Funding confirmed: yes" in `app.js:1344`.

## Boundaries and out of scope

* All three are display and queue surfaces. No gate is weakened: `Store.advance` still applies `gates.booking_gates`, so a transition was never approved by these readers. The fix only removes false "confirmed" or "no blocker" signals.
* Not claimed: finance approval, grant compliance, any rule or role. Only the existing explicit-`True` definition is applied; `True` remains confirmed. No financial or template rule is invented, and the unreviewed exercise rule status of `gates.py` records is unchanged.
* Other readers of `funding_ok` outside the write surface (`export_fields.py`, `resident_preview_fixture.py`, `ai_eval.py`) are not changed; recorded as observation. `export_fields.chat_case` forwards the `detail` value that the chat reader classifies; the chat reader is the surface that renders "confirmed".
* Absent key in chat: `case_facts` emits no `funding_ok` fact (existing `"funding_ok" in detail` guard); retained, as stating nothing is already non-confirming.
* Not run: SQL Server suites, complete gate, hosted CI, browser harness.

## Planning readiness

Ready: smallest fix is three one-expression changes plus four focused regressions in existing tests.
