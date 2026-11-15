---
title: Issue 432 per-call join across all worker modes plan
ms.date: 2026-11-13
---

Refs #432. Focused tier, test-only.

* [ ] Phase 1: extend `call_join` with exact configuration, prompt, root, attempt, model, case type; optional `output=None` for failed/fenced calls asserting zero eligible output rows and an attempt + root settlement.
* [ ] Phase 2: apply it to every mode of the worker test with exact expected values and content-free canaries (worker + chat).
* [ ] Phase 3: add a real worker retry test (attempts > 1, retries >= 1).
* [ ] Phase 4: exact field join for the legacy draft; resident-demo documented out of scope by the inventory test.
* [ ] Phase 5: validation (tests, ruff, mypy), independent review, commit.
