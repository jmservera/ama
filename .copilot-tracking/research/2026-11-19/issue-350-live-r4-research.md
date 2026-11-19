---
title: Issue 350 live research (2026-11-19)
description: Opening research for the live DEMO recheck of the first unmet criterion
ms.date: 2026-11-19
---

Goal: find the first unmet DEMO criterion of #350 and implement it if it is source work. Prior notes: `docs/reference/research/issue-350-live-2026-11-19.md` (09:10 UTC) and `deployed-parity-live-r3-2026-11-18.md`. Disposition: recheck live (anonymous requests and `az containerapp auth show`, no credentials).

## Findings (retrieved 2026-11-19 10:49 UTC)

Anonymous requests to `ca-cutover-test-demo-api`: `/api/cases`, `/api/me`, `/api/staff`, `/cases.html`, `/app` return 401 to native curl and 302 to a browser User-Agent with `Accept: application/json`; `/healthz` returns 200 in both. Easy Auth `unauthenticatedClientAction` is `RedirectToLoginPage`. Identical to the 09:10 UTC recheck, so criterion 1 is the first unmet criterion and remains an edge (Easy Auth) behaviour that `src/api` code cannot change; the fix is infra and deployment (FULL tier, coupled to #349) and outside the owner authorisation (no production changes).

Research disposition: executed. Planning Readiness: Ready (docs-only record).
