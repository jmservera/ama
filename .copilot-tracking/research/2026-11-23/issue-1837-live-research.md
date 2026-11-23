---
title: Research issue 1837 live close-out 2026-11-23
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready. Base `342fad401d` (origin/main). Synthetic demo, desktop only.

## Findings

* Main carries the fix: the standalone route page posts JSON with the CSRF header (#2110 and earlier); no open PR overlaps; nothing to implement, so no source change.
* Live revisions confirmed before and after the probes: API `ca-cutover-test-demo-api--0000054` (100%, healthy), resident `ca-resident-demo--0000026`.
* Live empty-field submit of the real challenge form: `application/json`, CSRF header sent, HTTP 400 with field validation, not `Could not read that.`; case JSON unchanged (this run; the earlier r2 qualification did not recur).
* Live negative probe: urlencoded 400 (with and without header), JSON without header 403, malformed JSON 400, unknown case 404, body/URL mismatch 400, case unchanged.
* Local: 66 unit tests OK; axe journeys route forms and challenge passed first run; nomination journey failed twice on a 5 s loopback client timeout under host load average about 10, then passed on the third run with zero violations. Treated as load-induced flakiness, recorded, not hidden.

Evidence: `docs/reference/research/issue-1837-live-2026-11-23/`.
