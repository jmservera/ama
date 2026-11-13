---
title: "#144 C1 README heartbeat fix details"
ms.date: 2026-11-13
---

## P1 README

Row 1338 keeps status Unmet. New text: images and the digest pipeline are real; the agents entrypoint has a tested run loop, a stdlib Azure Queue adapter (scripted transport only) and, since #1523, a Managed Identity token source (`runtime.identity_token`), `ApiResultSink` post-back and `build_runtime` wiring, unit-tested locally. `serve` runs the loop only when `ZF_AGENT_RESULT_ROUTE=enabled`, which the Bicep omits, so the deployed worker runs a standby loop that keeps the heartbeat. No live pipeline deployment receipt, no live queue/API run; orchestrator entrypoint still only prints a version (unchanged claim, verify first).

Heartbeat sentence: the pulse is once per loop iteration; the limit is checked arithmetically against ONE provider call at the largest accepted task timeout (parsed via TaskMessage.from_json bounds) plus the larger of the fault backoff and idle wait, with 2x margin; several provider calls per task, queue, token, post and ack latency are not bounded.

Regenerate inventory: python -m zava_forward.core.synthetic.cutover_audit --write, then check mode.

## P2 Test

Derive max timeout: largest t in range where TaskMessage.from_json accepts t and t+1 is rejected (production bound, no literal). gap = max_timeout + max(ERROR_BACKOFF_SECONDS, IDLE_SECONDS); assert HEARTBEAT_MAX_AGE_SECONDS >= 2*gap. Test name states one-call check. replace_worker: wrap queue.receive-driven loop with an iteration cap via alive callback counting calls (fail with AssertionError when exceeded) and a stop timer; assert stop was set by ack.
