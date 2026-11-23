---
title: Issue 2008 close-out critique, 2026-11-23
ms.date: 2026-11-23
---

Executed once. Verdict: proceed.

* The plan reuses the 2026-11-22 Playwright script, pointed at this worktree. Compatible; applied.
* Risk: sign-in may fail on a changed login flow. Mitigation: the script records `landed_on_app_host` and stops with a blocker rather than claiming proof.
* Risk: printing secrets. The script redacts identity and password strings and the raw output is searched for `@` and `password` afterwards.
* No source change, so the focused tier applies and `rpi-checks.py --all` is not run.
* No Azure resource is created, so no cleanup is needed.
