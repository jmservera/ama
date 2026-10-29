---
title: Resident logout browser-check correction changes
ms.date: 2026-10-28
---

Task: PR-525-PRRT_kwDOUU8JX86xVDWZ.
Scope: P01 implementation and P02 review/publication from the dated plan.

## P01 Implementation

Completed P01-T01, P01-T02 and P01-T03 after one critique, with PC-001 rejected for an
unsupported filesystem restriction and PC-002 applied to strengthen the oracle.
Existing runtime logout and unit contract remain unchanged.

Added `signed_in_session` preconditions and one shared `check_signed_out`
oracle, used by normal logout and all three retry scenarios. Both require
original cookie retention, exact protected-view 401 with original session
fence, and HTTP 200 session state with exactly false/null fields. Independent
replay now also carries the original fence; Bob's success remains checked.
Added four helper regression tests, with invalid status/body subtests and exact
request-argument checks. Updated the existing API browser documentation.
Split one pre-existing 102-character SQL fixture string to honor caller limit 100;
the concatenated SQL is unchanged.

The wider Python test/check search under `src/` and `tools/` found no other
logout deletion expectations. Failed-login no-cookie assertions and unrelated
test-reset/probe-cookie clearing remain unchanged.

## Validation Evidence

Existing external gate venv import failed with ModuleNotFoundError for
zava_forward; a separate task-owned venv was installed successfully at
`/tmp/ama-525-logout-20261028-venv` using the existing project dependency pins.
No prior receipt environment was modified.

All following commands completed with exit 0 from `src/api` using the task-owned
venv's Python. `PYTHONPATH=tests:../core/tests:../agents/tests` supplies only shared
test fixtures; all application imports use installed src distributions.

| Check | Command / evidence | Result |
| --- | --- | --- |
| Relevant API units | `python -m unittest -q tests.test_resident_demo_api tests.test_resident_demo_check tests.test_resident_chat_api tests.test_resident_assistant_api` | 68 tests, 41.716s, OK; no skips |
| SQLite browser | `python -m checks.resident_assistant_browser_check --out /tmp/ama-525-logout-validation-20261028/assistant-browser` | Passed actual Chromium chat/callback flows, including delayed logout replacement-cookie protection |
| Account browser | `python -m checks.resident_account_check` | Passed actual Chromium account, logout/failure retry and expired-session checks |
| SQL browser | `python -m checks.resident_demo_browser_check` with task-generated loopback-only process credentials | Passed full real SQL/HTTP/Chromium flow, both corrected paths, all 403/503/abort retries, replay and other-resident isolation |
| Ruff | `python -m ruff check --line-length 100 checks/resident_demo_browser_check.py tests/test_resident_demo_check.py` | Passed |
| Explicit line limit | `python -m ruff check --isolated --select E501 --line-length 100 checks/resident_demo_browser_check.py tests/test_resident_demo_check.py` | Passed, including previously exempt check file |
| Types | `python -m mypy checks/resident_demo_browser_check.py tests/test_resident_demo_check.py` | Success, 2 source files |
| Whitespace | `git diff --check` | Passed |

Browser drivers do not support `--mssql`. The assistant's agenda is SQLite and
the demo browser is always SQL-backed; both storage boundaries were exercised
without inventing a CLI option. Axe was not requested/provided: assistant report
explicitly says `Not run`; no accessibility acceptance claim is made.

Heavy validation was admitted with `flock -n -E 75` on the parent-held descriptor
for `/tmp/ama-rpi-heavy.lock`. First attempt busy; one 10-second retry succeeded.
The monotonic acquisition deadline was 2400 seconds, never an indefinite wait.
The lock was held for the complete unit/browser sequence and released on exit.
Actual SQL fixture: task-owned container `ama-525-logout-7c152be6355b`,
`127.0.0.1:33260`, 3 GiB / 2 CPU limit; SQL responded to SELECT 1 before use.
The check dropped its unique database and the wrapper removed exactly that
container in finally. No foreign resource was accessed or stopped.

External evidence root: `/tmp/ama-525-logout-validation-20261028/`, with
`results.json`, `resident-units.log`, `assistant-browser-sqlite.log`,
`account-browser.log`, `demo-browser-mssql.log` and the assistant browser report
and images. These are focused evidence, not a complete exact-head receipt.

## Amendments and Divergences

No material scope change. Pre-logout authenticated view and exact request-fence
checks implement compatible critique PC-002.

## Remaining Work and Publication Boundary

P01 complete. Original independent Review executed once: Complete / Residual
work. Its source-correction assessment is Conformant with no source defects;
RV-001 HIGH is the existing publication gate blocker. The reviewer independently
ran the four helper tests plus AST-only precondition/mutation probes, but could
not access external `/tmp` logs under its own worker restrictions; original
record preserves this limitation. No repeat Review is inferred.

The original Review assessed the three changed file fingerprints at starting
HEAD `32877254ec92a6aba409a1f43b26a66a52c706e1`. Immediately before committing,
remote advanced to bot commit `132e4d80` (`chore(rubric): record score 77/100`),
touching only `.github/rubric/scores/latest.json`. Executed `git pull --ff-only`
successfully as requested. All three source fingerprints still exactly match
the independent Review:

| File | SHA256 |
| --- | --- |
| `src/api/checks/resident_demo_browser_check.py` | `296302e280230e69d274ca413c959daf267d998e86155265359e4757840349c6` |
| `src/api/tests/test_resident_demo_check.py` | `f3507e4dd4ac319d781b8efcf9e32ca4633ec2319c9113f57545859f4409f398` |
| `src/api/README.md` | `149f5e88445e3e6dfb882419e54f056ddedc857cd1de9c9e99bed44562d82c1c` |

This accompanying Conventional Commit preserves the corrected source and all
dated original RPI evidence. P02-T02 uses its explicit record-blocker branch,
not a full-gate success. P02-T03 remains blocked and incomplete.
Mandatory complete publication gate invokes az, expressly excluded by the caller.
No full receipt, push or thread resolution is claimed. No Azure operations,
secrets/.env reads, runtime changes or issue closure are authorized.
PR #525 remains open with `Refs #520`; its text was not changed. The named
thread remains open rather than falsely reporting a published correction.
