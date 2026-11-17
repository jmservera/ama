---
title: "Review: resident-integration-462"
description: "Single independent post-implementation review of the Issue #462 continuation (non-rewriting main integration and readiness record)"
ms.date: 2026-11-17
---

| Field     | Value                                                                  |
|-----------|------------------------------------------------------------------------|
| Reviewer  | code-review agent (independent context, read-only), one pass           |
| Boundary  | Staged index of the in-progress merge (candidate `926b20a8`, `MERGE_HEAD` `1c9ac230`) plus continuation artifacts, before the review record and final state were added |
| Execution | executed once; no repeat Review for this task                          |
| Outcome   | Findings (0 Critical, 0 High, 0 Medium, 1 Low), corrected as a documentation-only post-review qualification |

## Review output (verbatim summary of the reviewer's return)

Checks 1, 2, 3, 4, 6 and 7 passed; check 5 had one defect.

* Check 1: the merge is clean, `MERGE_HEAD` is `1c9ac230`, `926b20a8` is an ancestor of HEAD. Against main only `.copilot-tracking`, `docs/reference/README.md`, `docs/reference/log.md`, the two threat-model documents and `src/api/README.md` differ. No source, runner, Bicep, Dockerfile or policy file differs.
* Check 2: the original 2026-11-16 #462 artifacts and the threat model are byte-identical to `926b20a8`.
* Check 3: factual claims match the code (`showcase_view` adds `freshness`, `source` and `calibrated: False`; `sensor_freshness` states and the 15-minute and 24-hour boundaries; `renderSensors` returns early on empty history, skips the badge when stale and shows a caution, builds text with `el()`). The reviewer did not itself re-verify the 17-column allowlist or the #1826 attribution.
* Check 4: no acceptance, live, FULL or score claims; the SQL, image, browser and Bicep gaps and the blocked FULL receipt are stated honestly.
* Check 5: update document and README row use `*` lists and ASCII; links resolve.
* Check 6: no credential or secret.
* Check 7: the changes artifact matches the retained logs.

Finding R-001, Low: in the merged `docs/reference/log.md` the candidate's `## [2026-11-16] add | Resident demo threat model ...` entry is followed directly by main's `## [2026-11-16] update | Plain-language paper ...` heading with no blank line (markdown structure, MD022 risk). Fix: add one blank line.

## Disposition and post-review qualifications

* R-001: corrected by inserting one blank line before that heading in `docs/reference/log.md`. This is a whitespace-only change to a merge seam, made after the review snapshot and therefore stated here as a post-review qualification. No wording of any log entry changed.
* Items the reviewer did not verify were checked by the worker afterwards: `len(COLUMNS)` in `resident_showcase_sql.py` is 17 and `len(ROW_KEYS)` in `resident_showcase.py` is 16, consistent with the preserved 2026-11-16 statement of 17 named columns and a row-key allowlist; the #1826 attribution follows from `git log 5e0c7f74..1c9ac230` (`fa8329d5`). This is a worker check, not independent review.
* The review covered documentation and the merged tree. It is not an accessibility, security, SQL, image or browser acceptance and does not replace the coordinator's independent exact-head assessment, the complete gate or hosted CI.

## Routed later work (not done in this task)

* Coordinator: current-base complete gate with external receipt, verification, exact-head assessment, hosted CI.
* Named missing local checks: SQL parity, Docker non-root image, resident browser journeys, Bicep-compile tests (no Docker socket, SQL Server or Azure CLI in confinement).
* Make the login limiter atomic and send `Retry-After` on 429 (original review R-003).
* Operator verification of the live SQL view and principal grants; owner pre-spend approval and gated deployment (issue criteria 6 and 7).
