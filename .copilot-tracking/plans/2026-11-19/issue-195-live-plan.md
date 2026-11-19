---
title: Issue 195 live plan
---

* [x] 1. Add `zava_forward/api/build_info.py` (validated commit from `ZF_BUILD_COMMIT`, else `unknown`) and log `build: commit=<sha>` at server start.
* [x] 2. Dockerfile: `ARG ZF_BUILD_COMMIT=unknown` and ENV; src-deploy build passes `--build-arg ZF_BUILD_COMMIT=$GITHUB_SHA`.
* [x] 3. Unit tests in src/api/tests/test_build_info.py.
* [x] 4. Live proof of current deployment, record per-criterion table. No rebuild (registry network-disabled).

Details: .copilot-tracking/details/2026-11-19/issue-195-live-details.md. Critique: .copilot-tracking/critique in research note (single pass, applied).
