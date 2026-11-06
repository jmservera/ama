---
title: Review for #188 sensor test-fixture reset isolation
ms.date: 2026-11-06
---

* Review execution: executed once, author-only, after the checks and after reading the final diff (2 files, +42/-1). Outcome: locally conformant for constructed SQLite; MSSQL effect pending. Not independent; human review checkbox left unchecked.
* Chronology: Research, Plan and details were committed as f6920bc4 before any test or helper edit; the regression was written and captured RED before the fixture fix. Earlier chronology failures (original ingest post-hoc, r11 planning) are preserved and not repaired. My earlier r13 opening sentence "no unit ran under real SQL Server" is false (65 ran on a verified MssqlStore) and is qualified in the new Research.
* Acceptance: (1) reset clears the five consumer tables, SQLite shown by the regression, MSSQL by code only; (2) reopen preserves, shown by the regression's first half; (3) RED then GREEN shown; (4) no runtime, schema, assertion, selector or threshold change, confirmed in the diff; (5) 199 constructed tests OK, 0 skips.
* Findings: (a) MSSQL `_Conn.execute` commit semantics are assumed from the existing `cases` delete pattern and are unproven until the owned run; (b) the new test relies on `retained_envelopes` and SQL counts, not constants; (c) one process note: I ran `rm -f ../x` on an empty probe path I had just created in `.copilot-tracking`; it never existed as tracked or user data, but it was a deletion command against the instruction and is disclosed here; (d) Ruff E501 first failed and was fixed by formatter, log preserved.
* Residual: owned MSSQL rerun, FULL tier, `--changed`, independent exact-head review, hosted checks are pending. No whole-188, statistical, live, owner or calibration claim.
