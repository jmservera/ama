---
title: Issue 1292 original-load record qualification plan
ms.date: 2026-11-09
task_id: 1292-record-qualification-1109
---

## Task metadata

* Research `.copilot-tracking/research/2026-11-09-issue1292-record-qualification-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-issue1292-record-qualification-details.md`. Critique `.copilot-tracking/plans/2026-11-09-issue1292-record-qualification-critique.md`.
* Branch `test/demo-startup-diagnostic-1292-1109`, frozen `f1f73d23f269415f74427350ec7018c234ee799b`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`. Refs #1292 only. Local only: no push, PR, issue or board write.
* Main: fetched `2b6d80a2580444751d4b85fc8eaa2c15f367855d`. After this plan, critique and details are committed, merge it with an ordinary `--no-ff` merge (no rebase, force, stash or amend), preserving both intents. Report an unresolved intent conflict instead of choosing a shortcut.

## Requirements

* One bounded corrective pass: one new dated qualification record (changes), one authored Review, a state record, a bounded additive note in `docs/architecture/cutover-evidence-pack.md`, a row in `docs/reference/README.md` and an append-only `docs/reference/log.md` entry.
* The 21 earlier records, 29 raw members plus the new manifest members and all Reviews are unchanged byte for byte (blob equality).
* No experiment, harness or source change; no test, SQL, browser, gate, service or cloud action. Validation: diff, link and ASCII review, source-equality and read-only hash checks only.

## Phases and criteria

* QC-1 (RQ-1) recorder: no reported harness error in P2 only; unguarded `enter` and `exit` appends, suppressed trace-callback and reporting failures; universal harmlessness and exhaustive reporting unproven. Primary guarded `open_store` capture stays distinct. `_open` through `trace_open`. No cause or plain-failure explanation. Inherited by PC-004 and the authored conformance assessment.
* QC-2 (RQ-2) label 120.4, 174.9, 115.9 and 145.6 s as unittest durations; give process wallclocks (role start to end from `.meta`, including shell setup) 121.756, 177.081, 117.147 and 147.510 s; API nearly the whole overlap (0.000593 s earlier start); cap conclusion unchanged.
* QC-3 (RQ-3) measured 26 manifest members plus the manifest itself (27 entries), neither the earlier 25 nor the review's 27/28, after re-counting the exact manifest lines; digest `634ceca2...` valid; no evidence removed. Also verify the earlier raw packet (29 members) against its own manifest, read-only.
* QC-4 (RQ-4) P2 design allowed PASS or REPRODUCED (disclosed partial PC-003); actual P1 was PASS; REPRODUCED branch not exercised; no relabel of design, no manufactured trace or reproduction.
* QC-5 Counts kept separate: the original single failure in the fifth attempt given four passes, the 0 of 6 earlier attempts and the new 0 of 2 pairs are never aggregated or used as one denominator. Cause UNKNOWN; no waiver or flake claim.
* QC-6 Source: final source equals main (historical diagnosis source `8d6f029ca`, distinct from the current lifecycle source `3a9767d5c`); no retest, no acceptance. Verify each stated exact line and count before writing.
* QC-7 Integration: the 0 of 2 UNKNOWN and these qualifications enter the pack as a bounded additive note; index row; append-only log. All #1292 criteria stay unticked; no E5, source fix or approval.
* Order: commit research, plan, details, one critique and state first; merge main; write the qualification and integration; one authored Review; update state; commit; handoff. If the Review still blocks, report and pause the affected record; start no new cycle.
