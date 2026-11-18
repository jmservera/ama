---
title: Issue 350 live parity r3, plan
ms.date: 2026-11-18
---

Details: `.copilot-tracking/details/2026-11-18/issue-350-live-r3-details.md`.

Tier: FOCUSED, docs and retained evidence only; no src change (a src change would need FULL and stop).

* [x] 1. Anonymous matrix (curl native and browser UA, JSON and HTML Accept) over protected API and page paths.
* [x] 2. Staff sign-in with Playwright (credentials read at runtime, never printed), GET-only probes, render of 13 routes plus law viewer, 16-asset check, agreement checks (list, CSV, map, stats), documents, time status.
* [x] 3. Read-only Azure CLI: app config (secrets redacted), Easy Auth, Foundry deployments, Event Hub, jobs, revisions, container logs.
* [x] 4. Resident app sign-in and showcase page screenshot.
* [x] 5. Write research note docs/reference/research/deployed-parity-live-r3-2026-11-18.md with per-criterion table; index and log entries.
* [x] 6. Delete the local session files. No Azure resource is created, so nothing to delete.

Critique (executed once; recorded in `.copilot-tracking/critiques/2026-11-18/issue-350-live-r3-critique.md`): Approve. Applied: GET-only, no secrets in output, keep adverse results (criterion 1 fails, time status 500), state r2 comparison honestly, do not claim hash match to head.
