---
title: Critique of issue 2188 plan
date: 2026-11-22
verdict: Proceed with changes
---

* C1 (compatible, applied): a retry that hides a deterministic failure is acceptable only if recorded; so receipt `retries` and hash binding are mandatory.
* C2 (compatible, applied): do not pop-and-reuse log indices; use a monotonic index to avoid overwriting concurrent shard logs.
* C3 (compatible, applied): never retry timeouts or interrupts.
* C4 (scope): parallel image builds and before/after timing are not attempted; recorded as unproven rather than half-built.
* C5 (compatible, applied): validate that each recorded retry has a failing exit code, otherwise a forged "retry" could excuse nothing but also could hide extra files; validate shape strictly.
