---
title: Critique for #2302 (second live run)
date: 2026-11-23
---

Executed once. Verdict: proceed.

* Risk: treating "0" as Unknown could hide a genuine zero spend. Rejected: the backend contract (`_assert_not_zero_or_none_cost`) already forbids zero cost strings, so the renderer matches it.
* Scope stays to one function and one test; no framework or design change.
* Tier FULL because `src` changes; only targeted tests run.
