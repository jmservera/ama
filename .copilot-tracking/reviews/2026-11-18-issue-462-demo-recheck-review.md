---
title: Review of the #462 synthetic showcase demo recheck
ms.date: 2026-11-18
---

* Execution: one review of the final candidate, by the implementing session (not independent; independent coordinator assessment stays separate).
* Boundary: docs candidate plus evidence folder; no `src/` change, so FOCUSED tier holds.
* Checks made: every table value against `live-checks.json`, `override-diagnosis.json`, `azure-app.json`, `azure-roles.json` and the cost files; relative links resolve; credential values scanned for in `.copilot-tracking/` and the note (none found); no Azure resource created or changed.
* Findings: (1) the first run's override comparison read as a mismatch; diagnosed and recorded as a correction (only `sensors.freshness.age_seconds` varies). (2) The first browser run failed on a wrong sign-out selector and the second completed; the failure is kept as history, not hidden. (3) The rate-limit count is qualified in the note because earlier failures shared the budget. No open material finding.
* Outcome: conformant for a documentation and evidence candidate. Criterion 2 (hosted rubric), the image source commit and the forward cost forecast remain unproven and are stated so; #462 must stay open.
* Routed work: hosted CI and rubric run on a pushed head (coordinator); owner may shorten the 2028-01-01 expiry.
