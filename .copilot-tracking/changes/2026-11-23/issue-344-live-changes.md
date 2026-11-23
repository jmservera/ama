---
title: Issue 344 live changes record (2026-11-23)
---

Refs #344. Tier: focused (documentation and evidence only). No source, infrastructure or Azure estate change; no resource created, so nothing to delete.

## Changes

* Added `docs/reference/research/public-browser-access-live-r10-2026-11-23.md`.
* Added an index row in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-23/issue-344-live/` (probe scripts, JSON results, screenshots; `signin-stall.png` is absent because the stall did not recur).

## Per-criterion proven and unproven table

Compared with `main` at `ed9500a188` and live revisions API 0000054 and resident 0000026.

| # | Criterion | Issue box | Status | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Public landing, Entra sign-in, protected pages need auth, anonymous API 401 not redirect | Open | Partly proven | Landing 200 and sign-in reaching Entra proven; 401 proven for non-browser clients; a browser User-Agent gets 302 under `RedirectToLoginPage`. Remedy (`Return401` redeploy) is owner-gated and not authorised |
| 2 | Edge follows #143 | Ticked | Re-confirmed | Environment external (`internal` false) |
| 3 | `/healthz` public; anonymous API 401 | Open | Proven for the demo | 200 and 401 in `probe_result.json` |
| 4 | SQL private, public Disabled, no policy bypass | Open | Proven | `publicNetworkAccess` Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with the MVP matrix | Open | Unproven | 13 of 13 destinations render for one role; MVP retired so no like-for-like comparison; other roles not walked; Blocked rows #349/#350/#210 remain; `/api/ai/report` 500 and `/api/account/photo` 503 cause not isolable (no Log Analytics workspace) |
| 6 | Browser sign-in smoke | Ticked | Re-confirmed | Passed on rerun after one automation timeout |

Owner-gated: the `Return401` choice and redeploy (criterion 1). Not needed for the demo: Azure billing reconciliation, DPO and Legal approval, person-run assistive-technology testing. No issue checkbox was edited.

## Validation

Documentation link and diff review; no unit tests apply. Hosted CI applies at the exact head.
