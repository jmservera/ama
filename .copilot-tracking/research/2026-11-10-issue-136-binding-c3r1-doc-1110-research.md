---
title: Research for issue-136-binding-c3r1-doc-1110
description: Read-only research for the README seal-lifetime wording correction
ms.date: 2026-11-10
---

## Scope

One documentation correction in `infra/README.md` (line 3915): "A seal minted before a restart cannot be verified after it." Frozen input HEAD `62c0dc1cb9750d27dbb2208e853e9e3cf32dc767`, tree `c3cd905f815c667d29318c1de79cc6c4b316ac4d`, base `d52f20a5`.

## Evidence

* `src/core/src/zava_forward/core/simulation_lane.py` (blob `5c26cfb06`, unchanged): `Lane.verify` checks the HMAC with the lane key, the `store_id`, the payload digest, expiry and a persisted `sim_seals` nonce row that is consumed once. Nothing in it invalidates a seal because of a restart as such.
* `infra/tests/test_public_simulation_startup.py` (C1, four actual-image tests): a second valid start retains the `store_id` and readings. No test mints a seal and verifies it across a restart, so retention is evidenced, a cross-restart seal run is not.
* The rendered recipe reuses a valid pair without reset. The lifetime is replica-local and volatile: replica replacement or scale to zero loses the store and key.
* Independent Readiness finding 1 (Medium, nonblocking) at `infra/README.md:3915` reports the overclaim; the Functional reviewer agrees.

## Conclusion

The sentence contradicts the valid-pair reuse statement above it. Seal invalidation should be tied to loss or replacement of the store or key; a restart that retains the valid pair does not itself revoke a seal, and expiry and single-use checks still apply.

## Planning Readiness

Ready. Research disposition: executed, read-only. Not covered: a new cross-restart seal runtime test, which is out of scope for this documentation tier.
