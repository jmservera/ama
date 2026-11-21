---
title: Issue 1258 live critique (2026-11-21)
description: One-pass critique of the plan
ms.date: 2026-11-21
---

Critique executed once. Verdict: proceed with changes.

* Finding 1: a mutation check edits src temporarily; it must be restored byte for byte and `git status` must show no src diff. Applied.
* Finding 2: criterion 5 cannot be proven without a push and the forbidden `--all` gate; the plan must state that rather than imply it. Applied.
* Finding 3: no src change means FOCUSED tier. Applied.
