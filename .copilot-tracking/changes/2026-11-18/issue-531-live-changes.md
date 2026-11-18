---
title: Issue 531 live verification changes
description: Changes record and per-criterion proven or unproven table for issue 531 live demo verification
ms.date: 2026-11-18
---

Refs #531. Focused tier: documentation and retained evidence only; no `src/` file changed, so the FULL tier does not apply and `rpi-checks.py --all` was not run.

## Changes

| Path | Change |
| --- | --- |
| `docs/reference/research/issue-531-live-demo-evidence-2026-11-18.md` | New per-criterion live evidence note. |
| `docs/reference/README.md` | Index row added. |
| `docs/reference/log.md` | Entry appended. |
| `.copilot-tracking/evidence/2026-11-18/issue-531-live/` | Probe, JSON output, asset hashes and ten screenshots. |
| `.copilot-tracking/{research,critique,plans,details,changes,reviews,rpi-sessions}/` | Dated RPI artifacts. |

Sequence note: the evidence note and index entries were drafted during Research because the research product is the note. The witness `implement-start` call follows; no source file is edited in any phase.

## Per-criterion table

| # | Criterion | Status for the demo | Basis and limit |
| --- | --- | --- | --- |
| 1 | Loading state before scripts and per panel, live region, slow-load hint, retry | Proven (re-observed; timing paths simulated) | Static shell with JS disabled; 4 s hint and Try again; 15 s message; per-panel busy status; 200 ms spinner. |
| 2 | Cold-start simulated, no blank page | Proven by simulation; real cold start unproven | Held `app.js` run on the live site. No scale-from-zero was forced or observed. |
| 3 | AI, rules and sources distinguished; HAX note | Proven for rules path; AI path simulated only | Live briefing is rules-derived (release admission denied). Design note not re-read. |
| 4 | Outcome-based actions; behaviour unchanged and tested | Wording and reason rules proven; recorded-review behaviour unproven live | No review submitted (irreversible). Tests stay local. |
| 5 | Sources, refresh time, unverified labelled | Proven for sources and time; unverified simulated | Rewritten response in the browser. |
| 6 | Browser and axe checks pass; no SR or voice claim | Proven (live axe 0 violations); SR and voice not claimed | axe 4.10.3, WCAG 2.2 AA tags, briefing and page. |
| 7 | Live verification recorded separately | Proven for the demo build with stated limits | Real employee session; no real cold start, no recorded review, no AI-written briefing; live `app.js`/`style.css` behind main (no briefing or loading diff). |

## Validation

* Live probe: `python3 live_531_probe.py` from the evidence folder; all steps completed; JSON retained.
* Secret scan: neither credential value found in retained JSON or scripts; no e-mail in the JSON.
* Link check, `git diff --check` and staged-file check passed; see the review record.

## Unmet or limited items

Real scale-from-zero, recorded review behaviour on the live site, AI-written briefing, screen-reader and voice-control acceptance (waived), and live observation of main's assets (deployed build trails main).
