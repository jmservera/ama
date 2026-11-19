---
title: Issue 531 live verification research
description: Opening research record for live demo verification of the employee loading feedback and Today's briefing redesign
ms.date: 2026-11-18
---

## Scope

* Issue #531, only criterion 7 is unticked: "Live verification on the employee site is recorded separately."
* Synthetic demo, desktop only. Live Azure authorised per owner decisions of 2026-11-18; no drills, no rotation, no production change.
* Research disposition: executing (findings appended below).

## Evidence base read

* Issue #531 body, owner comment 2026-10-28 and closure audits of 2026-10-31, 2026-11-04 and 2026-11-05: criteria 1 to 6 ticked, criterion 7 open; 2026-11-02 independent employee session in `docs/architecture/cutover-evidence-pack.md` predates later redesign.
* Source: `workspace-shell.js`, `index.html`, `app.js` (briefing panel, `requireWorkspaceScripts`, `SCRIPT_RETRY_DELAYS`), `async-action.js` (200 ms spinner), `checks/loading_briefing_browser_check.py` (local synthetic check, reused as the wording reference).
* Precedent: `docs/reference/research/issue-159-live-chat-experience-evidence-2026-11-18.md` for the live Playwright method.

## Findings

* Live app `ca-cutover-test-demo-api`, revision `--0000031`, `minReplicas` 0, two replicas running; natural scale-from-zero not safely forceable (shared with other workers; scale change is a config change).
* Deployed `workspace-shell.js` and `async-action.js` equal the branch; `app.js` equals `fa8329d51`, `style.css` equals `14296ce86`; the diff to main holds no briefing or loading change.
* Live briefing is rules-derived because release admission is denied (no approved release); AI-written path and unverified path need simulation.
* Review submission cannot be undone, so no review is recorded live; validation and wording are observable without submitting.

## Result

Probe run 2026-11-18 (driver and outputs under `.copilot-tracking/evidence/2026-11-18/issue-531-live/`). All planned observations passed; the per-criterion record is [issue-531-live-demo-evidence-2026-11-18.md](../../../docs/reference/research/issue-531-live-demo-evidence-2026-11-18.md).

Planning Readiness: Ready. Research disposition: executed.
