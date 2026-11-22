---
title: Details for issue 2188 shard retry
date: 2026-11-22
---

* Only sharded suites retry (flaky-test cost is highest there). Retry unit is the shard (a set of test modules), the nearest safe unit to "test class".
* A retry is never silent: the failed log stays in the output directory, is hashed in `files`, and is listed in `receipt["retries"]`.
* Timeouts, missing tools and interrupts are never retried.
* Retry count is fixed at one. Full-tier coverage is unchanged: the passing rerun must satisfy the same matrix identity and skip checks.
* Not changed: image build concurrency (docker_lock), wall-time measurement.
