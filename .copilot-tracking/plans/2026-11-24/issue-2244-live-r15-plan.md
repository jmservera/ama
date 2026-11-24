---
title: Issue 2244 live r15 plan
ms.date: 2026-11-24
---

* [x] Phase 1 research and live evidence (done, see research).
* [ ] Phase 2 implement read-only `_migrate` fast path plus unit tests.
* [ ] Phase 3 local validation: `src/core` tests, mypy, ruff.
* [ ] Phase 4 live re-proof on the throwaway database (needs a new image; if none can be built and deployed within demo authority, record as unproven for the new code and prove the diagnosis only).
* [ ] Phase 5 cleanup of throwaway jobs and database; research note under docs/reference/research; log and index; review; commit.

Details: [details](../../details/2026-11-24/issue-2244-live-r15-details.md). Tier: FULL for src change; this run does not run `rpi-checks.py --all`.
