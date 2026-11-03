---
title: Issue 223 sheet integrity details
date: 2026-11-03
---

* review_effectiveness.py: compare sheet version with the golden version; compute answers minus scenario proposal ids and refuse when not empty.
* tests: _sheet helper carries the version; new tests for stale, missing version, unknown id, blank worksheet refusal.
* README: one sentence.
