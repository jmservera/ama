---
title: Issue 440 live stabilization closure push research
description: Research record for the closure-push checkpoint of epics 81, 89, 93, 109 and 113 on pinned main
ms.date: 2026-11-24
---

## Scope and opening state

Refs #440. Closure-push checkpoint for epics #81, #89, #93, #109 and #113 on head `7023da86d8` (read 2026-11-24). Synthetic demo, desktop only. Research disposition: `executed` (opened 2026-11-24T07:10Z). Results are filled in below as checks run and are copied into the dated evidence note under `docs/reference/research/`.

## Findings

* Evidence note: [issue-440-closure-push-live-2026-11-24.md](../../../docs/reference/research/issue-440-closure-push-live-2026-11-24.md).
* Local: 24 tool audit tests, 324 core tests (26 skipped, 1 expected failure), 175 api tests, all OK; six core import errors were wrong module paths of mine and were re-run in `src/api`.
* Azure read-only: both apps Healthy, `/healthz` 200, anonymous `/api/cases` 401, IoT Hub to Event Hub counts match (about 12.4k per six hours).
* Signed-in probe: all read endpoints 200; sensor routes return draft-state only.
* Epics #81, #89, #93, #109 have only the checkpoint box unticked; #113 also has open children #115, #116, #117, #121 and the deferred production box.
* Planning Readiness: Ready. No source change required.
