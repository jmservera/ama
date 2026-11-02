---
title: Issue 691 review
date: 2026-11-02
---

Review executed once. Outcome: conformant for the scoped test addition.

* AC1 (leaflet 500 cause identified with evidence, fixed, regression test): NOT proven. Cause unproven; hardening and tests exist (#741, this change).
* AC2 (403/503 classified, expected shown plainly): met by #694 and verified by reading the callers in `web/chat.js` and `web/app.js`.
* AC3 (live re-check): pending next deploy.

PR uses `Refs #691`. Follow-ups: Log Analytics access (or NSP rule) to read `/vendor/` warnings; live re-check.
