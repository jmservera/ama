---
title: Phase details for #462 live proof
ms.date: 2026-11-18
---

* Phase 1 (done during Research): one Playwright script outside the repository reads `~/.ama-resident-test-user` at runtime, asserts that neither value appears in its output, and writes `live-checks.json` plus four desktop screenshots. The login limiter (5 failures per 10 minutes per source) shaped the run order and forced reruns, recorded in the note.
* Phase 2: spend from the Cost Management query (actual cost, resource group `ama`); resources from `az resource list`; grants from `az role assignment list` for `id-resident-demo`; dependencies from `gh`.
* Phase 3: add a `docs/reference/README.md` index row and an append-only `docs/reference/log.md` entry.
