---
title: Research for issue 2188 live evidence refresh
date: 2026-11-22
---

## Scope

Issue 2188 criteria: wall time before and after on the same tree; receipt records retries; verify rejects tampered evidence. Requested changes: drop `--no-cache`, concurrent image builds, api shards, one retry.

## Findings

* Research disposition: executed against head 3219004e90.
* `tools/rpi-checks.py` already has layer cache mode (`image_build_argv`, `require_fresh_images`), api shards (`SHARDED_PROJECTS`, `plan_shards`), shard retry (`SHARD_ATTEMPTS`, `record_retry`, `validate_retries`) and `receipt["retries"]`.
* Image builds are serialised by `docker_lock` in `dispatch`; the `--jobs` pool runs other groups concurrently.
* The 2026-11-21 research note states retry is unimplemented; that is stale since #2272.
* Planning Readiness: Ready. Documentation-only evidence refresh, FOCUSED tier, no src or tools edit.
