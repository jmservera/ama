---
title: Issue 531 derive retry counts research
ms.date: 2026-11-03
---

* Research disposition: reused (read-only review of the issue, comments and merged PRs #538, #581, #604, #628, #685, #725, #758, #812, plus the 2026-11-03 retry-check drift review on current main e10766a70).
* Planning Readiness: Ready.
* Evidence: criteria 1 to 6 of #531 are delivered by merged work. Criterion 7 (live verification on the employee site) is owner-run; the issue comments say no new live Azure tick is allowed. No agent can sign in to the live site.
* Smallest coherent slice: the routed follow-up from the prior review. The loading browser check hard-coded the script attempt count (4), which drifted once (#812). Derive it from `SCRIPT_RETRY_DELAYS` in `app.js`.
* Not in scope: live verification, screen-reader and voice-control acceptance, product behaviour.
