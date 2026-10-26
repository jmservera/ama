---
title: Resident Azure release 462 - review (2026-10-26)
description: Review of PR 465 diff against the cap change. Performed after the interim deployment.
ms.date: 2026-10-26
---

Scope: the PR 465 source diff (8 files), reviewed by the implementing session after the interim ungated deployment. This is not an independent review; hosted review and the full gate remain required.

## Findings

* Bounded: `build_identity_map` and `list_rows` still refuse more than `MAX_MAPPINGS`; the SQL read fetches at most `MAX_MAPPINGS + 2` rows. The cap stays fail-closed.
* Used once at startup only; no per-request cost grows with the cap.
* Tests: both cap tests now use the constant and cover the boundary (cap passes, cap + 1 fails). Core and API resident tests passed; ruff and mypy strict clean on changed files.
* Admission log: `522 residents admitted (0 excluded)` observed in the deployed startup log; the count is logged without emails.
* Documentation: the core README and SQL comment were updated. Historical tracking files that mention 25 are original evidence and were left unchanged.
* Limit: 1000 exceeds the current 980 cases but is a fixed constant; larger datasets need a deliberate change.
* The identity map is held in memory (about 1000 small entries); acceptable.

## Outcome

No open source findings from this review. Not yet performed: independent review, hosted review, full gate on the final head, and the owner's positive login and cross-case isolation tests.
