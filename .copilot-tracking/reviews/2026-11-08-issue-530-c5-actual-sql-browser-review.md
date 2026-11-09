---
title: Issue 530 C5 actual SQL and browser execution review
ms.date: 2026-11-08
---

Authored once after execution. Outcome: conformant for the bounded C5 scope.

## Assessment

* Plan conformance: the amended plan (critique F1-F7) ran as written: single non-queued lock hold, new external root, snapshot with non-editable distributions, origin and blob proof, owned loopback container removed before browser, pinned axe hash verified.
* Evidence: 21 of 21 selected chat SQL tests executed and passed (0 skips); all three dedicated chat browser states passed with zero axe violations and positive passes. See the changes record.
* Deviation: the runner's `docker pull` was omitted because pulls were not authorised; the already-local image was used. F3 egress confinement was only partly achievable (native Chromium egress unconfined).
* Adverse evidence preserved: failed r1 receipt unchanged; no new failures occurred.

## Limitations

* Manual targeted record, not a runner receipt; it cannot be verified with `--verify-receipt` and is not a partial or FULL receipt.
* The model-answer state is a controlled fixture, not a real model or grounded live AI.
* Hosted CI on the exact head, independent exact-head assessment and named human approvals remain required. Real sign-in, private-runner authority, price and budget, serving attestation, named agent confirmation, assistive technology, resident and legal approvals remain unmet. Whole #530 stays open.

## Follow-ups

1. Independent exact-head assessment, then authorised publication and fresh hosted CI.
2. Native CI parity for the dedicated chat browser check (hosted CI does not run it).
