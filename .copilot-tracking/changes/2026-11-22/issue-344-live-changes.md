---
title: Issue 344 changes record (2026-11-22)
description: Changes and per-criterion proven or unproven table for the ninth live reconciliation pass of issue 344
ms.date: 2026-11-22
---

Refs #344. Tier: focused (documentation and evidence only; no `src/` or `infra/` change, so FULL is not triggered). Status: implemented.

## Changes

* Added `docs/reference/research/public-browser-access-live-r9-2026-11-22.md`.
* Added an index row in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-22/issue-344-live/` (`probe.py`, `probe_assistants.py`, `probe_gaps.py`, JSON results, 15 screenshots).
* No Azure resource created or changed; nothing to delete.

## Validation

* Ran: live curl and Playwright probes, read-only `az` queries, relative link review of the new note, Git diff review.
* Not run: unit tests and `rpi-checks.py` (no executable change; `--all` is forbidden for this worker). Hosted CI for the exact head is not observed, because nothing was pushed.

## Per-criterion table

| # | Criterion | Result | Reason |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous protected API 401 not redirect | Unproven (partly proven) | Landing, sign-in and the non-browser 401 proven; a browser User-Agent gets a 302 under `RedirectToLoginPage`; `Return401` needs an owner decision and an infrastructure redeploy |
| 3 | `/healthz` public; anonymous API 401 | Proven | `/healthz` 200 and `/api/*` 401 for non-browser clients (browser-style requests are criterion 1) |
| 4 | SQL private, public Disabled, no policy bypass | Proven | Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with the MVP matrix | Unproven | 13 of 13 destinations render for one role and 27 of 30 web files match; the MVP is retired, other roles were not walked, and gaps remain Blocked (#349, #350, #210) |
| 2, 6 | Already ticked | Unchanged | Re-observed: external environment; sign-in passes again |

No issue checkbox was edited.
