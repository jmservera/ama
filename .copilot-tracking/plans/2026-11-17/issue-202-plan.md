---
title: Issue 202 plan
date: 2026-11-17
---

Tier: FOCUSED (documentation plus one unit test; no SQL, security, infra or deployment).

* [x] Phase 1: correct README archive paragraph to state the tag is published on origin and no release exists yet.
* [x] Phase 2: add regression test in `tools/test_epic_legacy_path_retirement.py` that README does not call the tag local or unpublished and still names tag and target SHA.
* [x] Phase 3: append a log entry; run targeted test, link check.

Critique (single pass, self): compatible; no change to issue checkboxes, no deletions, no #1818/#1641 scope. Verdict: proceed.
