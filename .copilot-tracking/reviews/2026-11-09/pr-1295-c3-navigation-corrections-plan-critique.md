<!-- markdownlint-disable-file -->
# Plan critique: PR 1295 C3 navigation corrections (2026-11-09)

* Task `pr-1295-c3-navigation-corrections`; executed once by an independent read-only `rubber-duck` reviewer against the real sources. Verdict: Revise. All findings are compatible with confirmed decisions and were applied directly or recorded as excluded residuals; no user decision is required. The critique is not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | QX `slides.json:3030` has `pages 9/16`; the planned pattern misses the slash endpoint (should become `9/17`) | Applied: `/` added as a range endpoint separator; literal test and expected-text proof added |
| 2 | Blocking | `Assert-CostSlide` and package verification reuse the production transformation, so changed-member counts do not prove note content | Applied: independent literal expected text for all five changed notes; byte equality of every other note part against the pre-change build |
| 3 | Non-blocking | `docs/capstone/demo/runbook.md:109` current resident-map/IoT/Fabric page numbers are baseline numbers (13, 46, 47 versus 14, 47, 48) | Recorded as an excluded residual and routed; outside the three-document scope and not covered by an existing authorization, so no edit and an owner decision is named in the handoff |
| 4 | Non-blocking | QX `slides.json:3029` says "All 54 page numbers and fixed native..." | Recorded: the source manifest text is outside this cycle's authorization (no `slides.json` edit); routed as an owner decision |
| 5 | Non-blocking | `Test-SourceHashes` does not check the delivered PDF or pitch files | Applied: explicit recomputation of PDF, both pitch hashes and preview-source hash against the receipt and pitch candidate hash lines |
