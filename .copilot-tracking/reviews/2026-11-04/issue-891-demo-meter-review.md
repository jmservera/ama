---
title: Review for #891 demo meter seeding
ms.date: 2026-11-04
---

* Review executed once by the implementing agent (not independent). Outcome: conformant for the slice; independent exact-head review and hosted CI remain required.
* Checked: default deny without the switch (test); no records without the switch (test); live synthetic-price hold intact outside the demo (test); one call per request root (test); records labelled synthetic, expiring daily, low cap.
* Residual risk routed to follow-up: the real Azure response must include `prompt_tokens_details.cached_tokens`, otherwise the completion records `liability-unknown` and the meter holds later calls; a fixed placeholder price is not a finance decision; the seed adds one ledger read per chat message in the demo only.
* Acceptance criteria for #891: criteria 1 to 5 were delivered earlier (#892, #995) or are unchanged; criterion 6 (live model answer on the demo app) is NOT proven by this PR and stays unmet until a redeploy and owner live check. Use `Refs #891`.
