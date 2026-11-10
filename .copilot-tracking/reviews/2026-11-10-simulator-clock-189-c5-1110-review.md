---
title: Issue 189 simulator-admin HTTP test-clock review (C5)
ms.date: 2026-11-10
task_id: 189-expiry-c5-1110
---

<!-- markdownlint-disable-file -->

## Review execution

Executed once 2026-11-10 after implement-done, on the uncommitted candidate diff over parent `d38bad4b76e4aec40c247086a22078e885f5b2c2` (test file sha256 `bb92944e3740c28615df76df816781d11e75021ccd28539147fc5e12c0ef80c3`). Same-agent review: no nested agents were allowed, so it is NOT independent. Root's independent exact-head review remains required before publication. Not repeated for this task.

Boundary assessed: `git diff` of `src/api/tests/test_simulator_admin.py`, the changes record, the external proof logs and the owned-venv static results.

## Outcome

Accepted with no blocking finding. Material findings open: 0. One Low residual is routed to later work; the correction allowance is spent (C5, 5/5), so no automatic follow-on exists.

## Checks against the brief

| Requirement | Assessment |
| --- | --- |
| Only `src/api/tests/test_simulator_admin.py`; production, configs, helpers byte-identical | Met: diff limited to the test file plus `.copilot-tracking`; empty diff over all other `src`, toml and workflow paths |
| Only `simulator_admin.datetime` bound; subclass keeps construction and type; installed before the server thread; restored after shutdown and join | Met: `patch.object(simulator_admin, "datetime", ...)` in `bind_clock` called before the thread; cleanup order `shutdown`, `server_close`, join with aliveness assertion, then clock restore |
| No handle, check_window, provider, session or response patching; real HTTP, auth, lock, file and audit | Met: the only patch is the module-local name; the view-only test's `patch.object(simulator_admin, "handle")` is the pre-existing assertion that denial precedes the module |
| Original red reproduced deterministically with only the module clock at 10:04:47Z | Met: 400 `CONTROL_WINDOW_INVALID`, no `changed`, no file, 0 start audit entries |
| Two original methods pass under the ambient post-deadline clock; removing only the fixture binding restores the failure | Met: green with binding, red without (both exits recorded) |
| Clock advance: just before valid, at expiry GET expired, expired Start 400 with unchanged bytes and audit | Met by `test_expiry_boundary_is_valid_before_expired_at_and_refuses_a_start` |
| View-only 403 before module, CSRF, wrong role, owner/reference/cap/maximum window, direct explicit-now coverage retained | Met: unchanged and passing (30 module tests) |
| Status asserted before indexing `changed` | Met; the removed-binding run now reports the `CONTROL_WINDOW_INVALID` body |
| Targeted tier only; configured tool versions | Met: mypy 2.4.0, ruff 0.17.1 in an owned venv; no full gate, SQL, browser, cloud |

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| F1 | Low | `SimulatorClock.current` defaults to `NOW` on the shared base; only per-test subclasses are mutated today, but a future test that mutates the base would leak | Not blocking; later cleanup only if the helper is reused. No change in this task |
| F2 | Low (residual) | Other fixtures with absolute dates elsewhere may be time-bombed; none was audited or claimed | Separate unadmitted discovery; not part of this correction |
| F3 | Informational | The plan checkboxes remain unchecked: the plan was observed at plan-done and is kept unchanged by Root's brief; completion is recorded in the changes record and state | None |
| F4 | Informational | The first test-file edit used a Python heredoc instead of the edit tool (recorded in the changes record); the diff above was reviewed in full | None |

## Routing and limits

Hosted CI for PR1374, PR1375 and PR1376 stays a separate observation each; nothing here proves them green. No whole-#189, live owned-run, time-limit or budget-alert acceptance is made. Refs #189, #1373, #80 and #129 only; no closing keyword.
