---
title: Issue 1274 axe-core CI download research (code run)
ms.date: 2026-11-18
---

Research disposition: executed (extends the 2026-11-18 audit run). Gap found: `src-ci.yml` downloads axe-core 4.10.3 from cdnjs with `curl --retry 2` and no digest check, while `tools/rpi-checks.py` pins `AXE_SHA256` locally. Planning Readiness: Ready. Scope: add a fail-closed SHA-256 check and bounded retry to that CI step, update WORKFLOW_HASHES, add a regression.

## Evidence (2026-11-18)

* Real download of cdnjs axe-core 4.10.3 with the CI curl flags: exit 0, sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, equal to `AXE_SHA256` in `tools/rpi-checks.py`. So adding the check to CI is safe.
* Retained logs (read via `gh api --allow-escape-sequences .../jobs/<id>/logs`, 504 lines observed, no secrets):
  * 1271 head `0639b6e3d`, run 42464552756 attempt 2, job 128684597601 `src-namespace`: step `Native workflow actionlint` `curl: (22) ... 504`, exit 22. The earlier `ModuleNotFoundError: No module named 'absent_rpi_package'` line is expected negative-test fixture output, not the failure.
  * 1271 scorer run 42464552761 attempts 1 and 2, jobs 128683494622/128681102295 (agent), `Install AWF binary`: five repeated `curl: (22) ... 504` at about 10 s spacing.
  * 1273 head `c1628cb50`, run 42470092288 attempt 1, job 128698647692: actionlint step `504`, exit 22; scorer run 42470092220 attempt 1, job 128698790743 `Install AWF binary`: repeated 504. Cause of the 1273 failures is therefore the same two bootstraps, not a unit fixture.
  * Latest attempts for these heads concluded success.
