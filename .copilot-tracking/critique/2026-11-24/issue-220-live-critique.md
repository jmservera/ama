---
title: Issue 220 critique
---

Executed once. Verdict: proceed.

* Risk: a live mutating challenge would create hazard-intake data on the shared demo. Disposition: use a non-mutating live probe only.
* Risk: claiming the live probe proves behaviour. Disposition: it proves route deployment and authentication only; behaviour rests on tests at this checkout.
* Risk: duplicate test. Disposition: none added, existing coverage maps to each of the three promises.
