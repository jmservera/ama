---
title: Issue 530 focused-gate refresh r3 critique
ms.date: 2026-11-08
---

* Executed: once, on this r3 plan before merge or implementation, rubber-duck agent. Verdict: proceed with changes. Earlier critiques are unchanged and not rerun.
* Confirmed: three-dot selection excludes incoming Main changes after the merge; inert-only paths select `preflight,namespace,static`; a merge commit is not rejected (identity needs the base to be an ancestor of HEAD).
* Finding 1 (blocking): verification without `--exact-base` may accept a relaxed moved base. Disposition: accepted; details add `--exact-base` and a stop if Main differs. Flag verified at `tools/rpi-checks.py` lines 3075-3089.
* Finding 2 (blocking): attribution omitted `chat-widget.js` and `chat.js`. Disposition: accepted and verified present; details compare both.
* Finding 3: stop on failed or interrupted gate, failed verification or proof. Disposition: accepted in the plan.
* Finding 4: three-dot explanation wrongly relied on merge-base equality. Disposition: accepted; research corrected.
* No conflict with a confirmed user decision.
