---
title: Issue 216 plan details
date: 2026-11-17
---

# Details

Test asserts `kind == "refused"` through `ask()` for variants of unsafe requests, and `kind == "answer"` for the
two supported lookup phrasings. Expect pass on current code (gate hardening, no production change).
