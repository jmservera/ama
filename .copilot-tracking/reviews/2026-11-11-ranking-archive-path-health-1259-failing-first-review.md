---
title: Issue 1259 failing-first verification review
description: One author review of the source-unchanged replay increment
ms.date: 2026-11-11
---

Review execution: Complete (author, single pass, not independent). Outcome: Conformant for the bounded increment, with residual gates. Boundary: the added 2026-11-11 tracking records and raw evidence.

* Plan before observation: respected; research, plan and details were committed before the first run. Selectors, blobs and method matched the plan; the only deviation (AST parse instead of `py_compile`) is disclosed.
* Evidence sufficiency: the previously durable evidence was a prose summary and external logs. This record adds raw durable logs showing the exact main tests fail against the real pre-fix main parent (7 failures in 6 tests, defect assertions) and pass against current main, with absent-directory controls green on both. That closes the literal evidence gap for criterion 4's "demonstrate failure before fix", as a today's replay.
* Source, tests, tools and workflows unchanged; no new test manufactured; no production data, credentials, Azure, containers or full gate.
* R1 (Medium) Criterion 5 remains unmet: current FULL receipt, independent exact-head assessment, hosted checks. Not waived.
* R2 (Low) Replay is dated 2026-11-11 and is not prospective chronology; criterion 4 should be ticked only by the owner after independent exact-head review.
* R3 (Low) Residuals unchanged: mocked stat failure, check/use race, Store overdue/fallback, 226 unanalysed skips, only selected tests run.

Routing: independent exact-head review; the owner decides on ticking criterion 4. Correction count: none consumed; finite counts untouched. Refs 1259, 1258, 79, 1231; nothing closes.

## Superseded in part (2026-11-11 documentary C3)

Qualified additively by [the C3 changes record](../changes/2026-11-11-ranking-archive-path-health-1259-doc-c3-changes.md) and [the C3 review](../reviews/2026-11-11-ranking-archive-path-health-1259-doc-c3-review.md). The text above is preserved as originally written; where it differs, the C3 record governs (old-red reach, run counts, run.sh and manifest, process conformance).
