---
title: Issue 156 process D1 research (2026-11-10)
ms.date: 2026-11-10
---

Research disposition: executed (compact, read-only on old bytes). Refs #156 #230 #149. One D1 process diagnostic; not a source correction, waiver or old-balance reconciliation.

Subject: witness log `phase156-independent-record-evidence-1110/issue-156/events.jsonl` (sha256 `9ed0edc8baf4d430900bbd6ce442aead489029203a2c28b083d32d5f7bf8d8ce`, 8 records), commit `d8d103ffc95a7b47376b4095be6fe8276b3066e0`.

Observed (re-run of `verify` in this task, process exit 1, matching the Root result):

* Verdict QUALIFIED, exit 1, not pass: seq 6 `implement-done`: review artifact changed after observation.
* Notes only: state artifact changed after observation at seq 3 to 7; changes artifact at seq 5.

Cause from the recorded hashes (review artifact):

* seq 6 `implement-done` observed review sha256 prefix `9e512ae1`.
* seq 7 `review-done` and seq 8 observed `dbfd26e6`, which is the current file.
* Chronology: the old task created the review record and pointed state at it before `implement-done`, then appended a self-check section after that observation. That is the producer's sequencing fault, not a witness fault.

Other facts:

* Two launch events exist: seq 1 recorded by Root (08:41:21), seq 2 by the producer (08:41:57). The old handoff did not make this distinction clear.
* The old handoff `handoff-156-independent-record-1110.md` described verification as passing with notes. That claim is wrong: the actual verify exit was 1. The handoff is preserved unedited.
* Old numbering note: in the old handoff "seq 1 to 8 all ok" is accurate as outcomes, but ok outcomes do not mean verify passed.

Retained: earlier 156 review BLOCKED (context loss); later independent `approve_with_comments` with two Medium (M1 empty-page ambiguity unresolved and not implementation-ready; M2 local-only context); coverage limited to the supplied patch and changed hunks. The same reviewer allows publication only as PROPOSED, PARTIAL, NOT APPROVED, NOT IMPLEMENTATION-READY. No implementation, whole-156, human, AT or CI acceptance.

Planning Readiness: Ready.
