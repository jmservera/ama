---
title: Issue 2257 verify critique
ms.date: 2026-11-22
---

Critique executed once on the final candidate (test-only plus evidence). Verdict: proceed.

* Risk: a test that only restates the helper. Mitigation: it drives the real `api()` function against an `/api/map` URL, so removing `fetchReadRetrying` from the read path fails it.
* Risk: slicing `app.js` by marker strings is brittle. Mitigation: reuse the marker approach already used in `test_workspace_scripts.py`, and fail loudly if a marker is missing.
* Conflicts with confirmed decisions: none. No src change, so tier is focused, not FULL; `rpi-checks.py --all` is not run.
* Rejected: min replicas 1 or any Azure change; not authorised for this task, kept as a follow-up.
