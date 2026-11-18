---
title: Plan for #462 synthetic showcase demo recheck
ms.date: 2026-11-18
---

* Tier: FOCUSED. No `src/`, infra or Azure resource change; no throwaway resource is planned.
* [x] Phase 1: Azure read-only facts (revision, ingress, identity roles, scale, actual cost by service) saved as JSON under the evidence folder.
* [x] Phase 2: one Playwright script (Chromium, 1280x900, public HTTPS URL) running the criterion 7 journeys: sign-in page, wrong password, unknown email, missing CSRF, foreign origin, rate limit, staff probes, forged cookies, correct login, case summary, query and header overrides, cookie flags, projection canary scan, session cookie expiry attribute, logout and replay. Credentials are read at runtime and asserted absent from output and screenshots.
* [x] Phase 3: write `docs/reference/research/resident-showcase-live-recheck-2026-11-18.md` with a per-criterion proven/unproven table (criteria 1, 2, 6, 7 plus the ticked ones re-observed), update the knowledge base index and log.
* [x] Phase 4: changes record, single review, commit locally. No push.
* Stop conditions: Azure cost unreadable, any resource mutation needed, or credentials appearing in output (stop and disclose).
* Details: [details](../details/2026-11-18-issue-462-demo-recheck-details.md). Critique: [critique](../critiques/2026-11-18-issue-462-demo-recheck-critique.md).
