---
title: Issue 1274 hosted CI release retrieval review
ms.date: 2026-11-08
---

Review executed once by the native issue1274 session on the implemented diff (base `0f05e9aa`). It is a native self-review, not the independent exact-head assessment, hosted CI or human approval; those remain future gates and nothing here asserts them.

Outcome: conformant for the owned actionlint scope; AWF scope routed as an open partial blocker. No material code finding open.

| Check | Result |
| --- | --- |
| Bounded retrieval resilient to 504 | Pass: 3 attempts x 2 official sources, delays, timeout and size cap; tests for 504 recovery and fallback. |
| Exact identity and checksum, fail closed | Pass: pinned ids, size, archive and checksums SHA-256; checksums file must list pinned digest; exhaustion, truncation, wrong digest, bad archive all leave no binary (tests). |
| No secret exposure | Pass: token only to api.github.com, dropped on foreign redirect (tested), never logged. |
| Names, permissions, pins | Pass: job and check names, `contents: read`, action pins unchanged. |
| Hash and selection coupling | Pass: `WORKFLOW_HASHES` updated; `ci-affected` and `paths` include new tools. |
| Generated lock untouched | Pass: no `rubric-score.lock.yml` edit. |
| Actual integration | Pass: real install exit 0, version 1.7.7, native workflows lint exit 0. |

Findings routed to later work:

* R1 (open, upstream): AWF 0.28.23 install 504 in `rubric-score.lock.yml` needs an upstream or recompile path; no repository hook. Owner: coordinator or maintainers.
* R2 (low): the checksums pin and archive pin must be changed together on an actionlint bump; documented in the installer constants.
* R3: dependent PRs #1243, #1271, #1273 need a base update and fresh hosted run after merge; not done here.
