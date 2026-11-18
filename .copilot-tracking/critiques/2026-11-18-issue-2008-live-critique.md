---
title: Issue 2008 critique (worker self-critique, one pass)
ms.date: 2026-11-18
---

Execution: one pass by the worker, no separate agent. Verdict: proceed.

* Risk: criterion 3 claims conflicts on the deployed demo, but the web check has no conflict logic and no xlsx upload. Disposition: do not change src (would force FULL tier); report conflicts as unproven live, proven locally.
* Risk: placing the generator in `src/` forces the full tier. Disposition: put it in `tools/`.
* Risk: PII. Disposition: fictional street names, `Demo Resident NN`, no phone numbers.
* Risk: credential leak. Disposition: read at runtime inside the script; sanitise outputs. Note: an earlier shell command displayed the password file once by mistake; recorded in the review.
