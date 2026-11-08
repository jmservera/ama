---
title: Issue 530 C5 actual SQL and browser execution changes
ms.date: 2026-11-08
---

Manual targeted record, not a runner receipt, not a partial or FULL receipt. The failed r1 receipt (SHA-256 `15adeeff795d96375f186438b2f101759a8d6ecb8bf799383bdb6615dea104e8`) is preserved and not resumed. No source, test, checker, workflow, config, dependency or Bicep file changed.

## Identity

* Execution HEAD `b02f44925a5eb0c107bf7864513a3af110001521`, tree `fcdf7ef856ac1daa34d219764d2190a8b0474ddb`, Main `0f05e9aae70768def8d1d9c300215f9ee2f11638` (unchanged). Source bytes equal C4 `ce3f27f08` (records-only delta).
* Runtime root `/home/azureuser/.local/share/ama/gates/g530-c5` (root filesystem, new). Raw logs under `logs/`, outputs under `out/`, wrapper `run.sh`. Kept external.
* One non-queued holder of `/tmp/ama-rpi-heavy.lock` (`flock -n -o`) for setup, SQL, browser and cleanup. Lock verified free afterwards. No containers remain.
* Admission 09:51: worktree clean, no containers, no runner or sqlservr processes, root 21.15 GB free, RAM 8.56 GB available, 4 shared CPUs.

## Commands and exits

| Step | Result |
| --- | --- |
| git archive snapshot of HEAD, new venv | exit 0 |
| `pip install --require-hashes -r src/api/requirements.txt` | exit 0 |
| non-editable `pip install --no-deps` of snapshot core, agents, api | exit 0 |
| `pip install playwright==1.64.0` | exit 0; `pip check` exit 0 |
| Origin proof | tests and checker resolve under the snapshot; `zava_forward.core/agents/api` in venv site-packages, 128/19/24 files, zero hash differences against snapshot blobs |
| Loopback-only audit hook proof | refused non-loopback connect |
| Driver check (libltdl, libkrb5, mssql_python) | exit 0 |
| Owned SQL container | image `sha256:cf8f0ab2ebe6...`, label verified twice, `127.0.0.1:33295`, 3g, 2 CPUs, no pull, `SELECT 1` ok on attempt 6 |
| `python -m unittest -v test_mssqlstore.MssqlChatPrivacy test_mssqlstore.MssqlChatRoleProjection test_mssqlstore.MssqlChatDemoMeter` in `src/api` | exit 0, `Ran 21 tests in 13.984s`, `OK`, zero skip, failure or error |
| Exact owned container removal | `docker rm -f` exit 0 |
| Axe 4.10.3 fetch | exit 0, SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` matches |
| Playwright 1.64.0 dry-run | wants chromium v1248 (existing); no download |
| Maintained `checks.employee_chat_browser_check --axe ... --out out/employee-chat` via runner `BROWSER_ENTRY` | exit 0 |

## Outcomes

* SQL: 21 unique `ok` ids (Privacy 13, RoleProjection 4, DemoMeter 4), password redacted from the stored log.
* Browser: `PASS employee chat: real fallback; six selections; arrived transport; nine controlled late successes; metadata/thread/ask denials; route/session disposal; keyboard, focus, live, reduced motion, reflow and dialog axe`. `axe-results.json` (SHA-256 `593e30ac6c79508f571bbc30558973b3b69a34e55abc4df7613cbcb9b826d71d`) lists actual-model-unavailable, synthetic-cited-answer and demo-disclaimer-model-answer, each with zero violations and 20 passes.

## Limits

* Native Chromium egress is not confined (`unshare -rn` denied); only the maintained loopback and request-abort boundary applies, plus the Python audit hook. The axe fetch was the only external request.
* The model-answer state is a controlled fixture, not a real model.
* Historical API 2007 run is not claimed for this head. No hosted CI, runner receipt or independent assessment is implied.
