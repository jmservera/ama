---
title: Issue 2257 live critique (run 084412Z)
ms.date: 2026-11-23
---

Executed once on the final candidate plan. Verdict: proceed with two amendments.

* Accepted: a manual retry button is safe for every failure type because the user chooses it; it needs a native button, hidden until a failure, and a notice that names it (content standard).
* Accepted amendment: the automatic redraw applies only to status-less network failures and runs at most once (4 s), reset on success or a manual retry; HTTP errors are never auto-retried, matching the pinned JSON 500 test.
* Accepted amendment: clear the timer on dispose and on every new draw so a route change or a newer request cannot trigger a stale redraw.
* Rejected: client auto-retry of a JSON 500 (conflicts with the confirmed design that application errors are shown).
* Risk: the visible control may mask a persistent outage; the notice still names the owner and the next action.
