---
title: Issue 1292 startup lock diagnostic review
ms.date: 2026-11-09
---

## Execution and outcome

* One authored Review, executed once after Implement; not an independent review. Outcome: diagnosis incomplete and unresolved, process conformant. No source defect is confirmed and no correction is indicated by evidence.

## Assessment against the plan

* Caps respected: six attempts (3 isolated, 3 concurrent), no retry, Core attempts under 17 s, no stress tool, no suite, no SQL service. One harness defect is disclosed and not counted because the target test did not run.
* The failure did not reproduce, so the retained failure's exception location, thread and statement remain UNKNOWN. A passing attempt does not prove a flake, nor absence of a defect.
* The baseline `ba5cc74b8` lacks the test; no comparison made.

## Findings (routed as later work, none repeated here)

* R1 Candidate mechanism (H1) measured: write-lock hold 3.05-3.25 s versus a 5.0 s wait limit, with a COMMIT of 1.8-2.0 s. Scope if a source correction were ever indicated: `SqlStore._migrate_recommendations` write section (`sqlstore.py` about 350-375) or the busy timeout; unconfirmed, and the test itself asserts two simultaneous openers within that limit. The coordinator decides separately whether existing E5 applies.
* R2 A reproduction needs either the six-module API contention or I/O pressure; both exceed the planned bounds. Not performed.
* R3 This review is not independent; hosted CI of the PR head ran the test green once (per the 440 handoff). No new hosted evidence was read.
