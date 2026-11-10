---
title: Issue 1292 original-load record qualification research
ms.date: 2026-11-09
task_id: 1292-record-qualification-1109
---

## Disposition and readiness

* Research executed (read-only, no reruns). Planning Readiness: Ready.
* Trigger: independent Readiness review of `f1f73d23f269415f74427350ec7018c234ee799b` (tree `6ba8f48d0889302948d96b5e19ad6844b7fdac28`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`), verdict approve_with_comments: one Medium (RQ-1) and three Low (RQ-2..RQ-4) record issues. The earlier 72ca findings are recorded as addressed; E4 source corrections are spent (four) and one source correction remains unchanged; E5 is NOT authorized here.
* Scope: ONE record-only corrective pass. A new dated qualification is added; the 21 earlier records, the 29 raw members plus the new manifest members and every Review stay byte-identical. No rewrite, amendment or retroactive approval. No experiment, harness or source change, test, SQL, browser, gate or cloud action.

## Evidence verified read-only (exact lines and bounded metadata)

* RQ-1 recorder: `observer_core.py` in the external log directory. `harness()` (lines 34-38) appends inside its own `try` and silently passes any `BaseException`. `wrap()` (82-107) appends `enter` before its `try` and `exit` after it, so those appends are unguarded; its `raise` branch is guarded. `trace()` (119-126) swallows every `BaseException` without calling `harness()`. `trace_open()` (110-132) installs the `_open` seam. `main()` wraps `__init__`, `_initialize`, `_migrate_recommendations`, `_audit_evidence`, `_backfill_zero_ordinals`, `_review_priority_order` with `wrap()` and wraps `_open` through `trace_open()`, not through the loop. The primary `patch_open_store` capture of the `open_store` exception (64-79) is guarded and distinct.
* RQ-2 timings: process metadata `.meta` start and end epochs (written by `driver.sh` `role()` around each role, so they include shell setup and bookkeeping) give API 121.756 s and Core 177.081 s (P1), API 117.147 s and Core 147.510 s (P2). The existing 120.4, 174.9, 115.9 and 145.6 s are unittest-reported durations. P1 API started 1794243376.945999623 and Core 1794243376.946592929, 0.000593 s apart, so API ran for nearly the whole overlap (about 121.756 s P1, 117.147 s P2), not literally inside Core.
* RQ-3 inventory: the manifest `SHA256SUMS` lists 26 member files (`awk 'END{print NR}'` 26; `sha256sum -c` 26 lines, 0 failures); the directory has 27 entries including the manifest. The Readiness review states 27 members and 28 entries and the earlier records state 25; the measured count is used and the difference is reported, not copied. Its sha256 is `634ceca206c1a077e57cb8d421e2d5e9f63d30ad495cd2af8c7918e0f91566de`; `sha256sum -c` reports 0 failures.
* RQ-4 design: plan P4 and `driver.sh` (lines 68-89) permit P2 after a Core PASS or REPRODUCED, with a plain reproduction unable to preserve a trace (the disclosed partial PC-003 disposition). The actual campaign ran P2 after a plain PASS; the REPRODUCED branch was not exercised.

## Limits

* The qualification addresses the current claims only. It does not state that the old records were accurate, does not authorize any past amendment and removes no evidence.
* Cause stays UNKNOWN. No flake, necessary-load, sufficient-load, source-fix, human-approval or acceptance claim. The recorder limitation does not explain the original plain failure.
* Whole-issue #1292 criteria stay unticked and open.
