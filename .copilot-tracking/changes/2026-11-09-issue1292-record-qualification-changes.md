---
title: Issue 1292 original-load record qualification changes
description: Additive dated qualification of the original-load diagnostic record at frozen head f1f73d23
ms.date: 2026-11-09
---

Refs #1292 only. No acceptance criterion is ticked. This is a record-only, additive qualification of the current claims in the original-load diagnostic record at `f1f73d23f269415f74427350ec7018c234ee799b`. It does not state that the older records were accurate, does not authorize any past amendment and removes no evidence. Plan: `.copilot-tracking/plans/2026-11-09-issue1292-record-qualification-plan.md`, committed with its research, details, critique and state before main was merged.

## Qualifications

| Id | Qualification (supersedes the current claim only) | Evidence |
| --- | --- | --- |
| RQ-1 | The P2 observer run supports ONLY "no reported harness error" (`harness_errors=[]`) and "no observed new error". The recorder does not guarantee harmless operation or exhaustive error reporting: `wrap()` appends the `enter` event before and the `exit` event after its guarded block, so those appends are unguarded; the trace callback `trace()` silently swallows `BaseException` without calling `harness()`; and `harness()` itself suppresses its own failure. Universal harmlessness and exhaustive reporting are therefore unproven. The primary guarded `open_store` exception capture (`patch_open_store`) is distinct from these secondary event recorders. `_open` is installed through `trace_open()`, not through the listed `wrap()` loop. No cause and no explanation of the original plain failure is implied. The details sentences "Every recorder fault is appended to `harness_errors`" and "never silently suppressed", plan criterion PC-004 and the authored conformance assessment inherit this limit. | `observer_core.py` lines 34-38 (`harness`), 64-79 (`patch_open_store`), 82-107 (`wrap`), 110-132 (`trace_open`, `trace` at 119-126), 146-161 (`main`); `P2.observer.json` |
| RQ-2 | The "Wall" column in the earlier pair table (120.4, 174.9, 115.9 and 145.6 s) is the unittest-reported duration, not process wallclock. Process wallclock from the `.meta` start and end epochs (role start to end, so it includes shell setup) is given below. P1 API started 0.000593 s before P1 Core, so API overlapped nearly the whole of its own run with Core (about 121.756 s in P1, 117.147 s in P2), not literally inside Core. The 420 s cap conclusion and the outcomes are unchanged. | `P1.api.meta`, `P1.core.meta`, `P2.api.meta`, `P2.core.meta` |
| RQ-3 | The external log directory holds 26 manifest members plus `SHA256SUMS` itself (27 entries), measured with `awk 'END{print NR}'`, `sha256sum -c` (26 of 26, 0 failures) and `ls`. The earlier statement of 25 files is wrong; the Readiness review figure of 27 members and 28 entries differs from the measured count and is not copied. The manifest digest `634ceca206c1a077e57cb8d421e2d5e9f63d30ad495cd2af8c7918e0f91566de` remains valid (coordinator check exit 0, re-checked read-only). No evidence was removed. | `SHA256SUMS` |
| RQ-4 | The review line "ran only after a plain PASS (design)" is corrected: the design (plan P4, `driver.sh` `classify_core` and gate) allowed P2 after a Core PASS or REPRODUCED, with a plain reproduction unable to preserve a trace, the disclosed partial PC-003 disposition. In the actual campaign P1 was a PASS and P2 followed it. The REPRODUCED branch was not exercised. The design is not relabelled as PASS-only, and no trace or reproduction is created. | `driver.sh` lines 68-89; plan P4 |

### Timings (UTC, 2026-11-09, unchanged outcomes)

| Pair | Process | unittest duration | Process wallclock (`.meta`) | Exit |
| --- | --- | --- | --- | --- |
| P1 plain | API | 120.4 s | 121.756 s | 0 |
| P1 plain | Core | 174.9 s | 177.081 s | 0 |
| P2 plain | API | 115.9 s | 117.147 s | 0 |
| P2 observer | Core | 145.6 s | 147.510 s | 0 |

## Counts kept separate

* The original single `database is locked` failure in the fifth execution, given four later passes, stays as recorded.
* The earlier startup diagnosis: 0 of 6 attempts. This diagnosis: 0 of 2 original-load pairs (P1 plain, P2 with Core observer). These are three distinct denominators and are never aggregated or treated as one unit denominator. Plain and observer runs are not equivalent.
* Cause UNKNOWN. No flake, waiver, load necessity or sufficiency, source-fix, human-approval or acceptance claim. All whole-issue #1292 criteria stay unticked and open.

## Source and preservation

* After the planning commit `80267ed888b8b06eb7737635368475b1af2013e2` the fetched `main` `2b6d80a2580444751d4b85fc8eaa2c15f367855d` was merged with an ordinary `--no-ff` merge (no rebase, force, stash or amend). The merged source (`src infra tools .github pyproject.toml`) equals main and the current lifecycle source `3a9767d5c`; the historical diagnosis source `8d6f029ca` is distinct and still the only source under test for the diagnosis. Nothing is retested or accepted here.
* The 21 earlier records, the 29 raw members of the startup diagnostic packet and all Reviews are byte-identical (git blob comparison; `baseline-prior.sha256` 0 failures; earlier raw manifest 29 of 29).
* Not performed: any experiment, harness or source change, test, SQL, browser, gate, service, cloud, push, PR, issue or board action. E5 is NOT authorized; the four spent E4 source corrections and the one unchanged remaining source correction are not altered.
