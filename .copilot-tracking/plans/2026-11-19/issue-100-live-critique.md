---
title: Issue 100 live critique
ms.date: 2026-11-19
---

# Critique (single pass, final candidate)

* Risk: showing priced zero as Unknown could hide a real zero cost. Disposition: server asserts unpriced never yields zero; a priced zero is rendered when given as a non-numeric money string. Accepted, covered by a test.
* Risk: duplicating server rules in JS. Disposition: the helper only formats; no cost is computed client side.
* Risk: sponsor/coordinator Overview only; role screens untouched. Accepted for demo scope.
* Verdict: proceed. No conflict with owner decisions.
