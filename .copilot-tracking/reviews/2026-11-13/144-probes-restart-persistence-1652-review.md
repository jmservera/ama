---
title: "Review 144 probes and restart persistence"
ms.date: 2026-11-13
---

Execution: complete (code-review agent, one pass). Outcome: conformant after fixes.

* README overclaim "the API dedupes": corrected to state API dedupe is not built or tested.
* Vacuous same-id assertion: test renamed to redelivers_and_reposts, idempotency implication removed.
* Manual lease release: README now says manual lease release.
Tests rerun after fixes.
