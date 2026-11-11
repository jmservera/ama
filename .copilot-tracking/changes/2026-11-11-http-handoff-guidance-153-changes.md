---
title: Issue 153 pending-handoff HTTP refusal and error guidance changes
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Identity

* Branch `fix/demo-handoff-http-guidance-153-1111`. Planning head `99f01d7b9`, merged `origin/main` `e5168fe9eaca0d168df010da6e8e8b8eb5dd8270` (includes merged #1444) by ordinary merge `7965d6a38`, no conflict, planning ancestry kept. The unmerged #440 docs topic was not merged.
* Source imports asserted from this worktree: `zava_forward.api.server` -> `src/api/src/zava_forward/api/server.py`, `zava_forward.core.store` -> `src/core/src/zava_forward/core/store.py` (explicit PYTHONPATH from details Phase 0). Host editable installs point elsewhere.
* Raw logs: `.copilot-tracking/changes/logs/2026-11-11/issue-153-http-handoff-1111/` (originals also in `/tmp/zf-153-http-handoff-1111/logs/`).

## Changes (exactly the critiqued slice)

* `src/api/src/zava_forward/api/web/app.js:755-774`: new fixed `HANDOFF_DENIED`; `pendingHandoffs` gets a single `fail` paint helper (one `role="alert"`); a non-array successful body now paints `HANDOFF_READ_ERROR` instead of hiding the card; catch keeps abort silent and the 401 text, uses `HANDOFF_DENIED` for 403 and `HANDOFF_READ_ERROR` for every other error. No server `e.message` reaches the page except the existing fixed 401 string. Success markup, both download links, empty hiding and loading text untouched.
* `src/api/tests/test_handoff_read_guidance.py`: Node cases for 403, 500/404/429/generic HTTP, malformed `{}`/`0` (and preservation `"x"`/null), lexical guards, source-shape guard; constructed Chromium cases (route installed before first navigation) for 403, 500, text and `{}` 200, one GET, no POST, no retry, and manual reload recovering real backend rows. Two intended contract changes: the old 500 server-text expectation and the old `HANDOFF_READ_ERROR` count.
* Not changed: API, server, roles, schema, CSV, #83 screen, README, log, content standard.

## Validation (focused tier; commands from `src/api`)

| Check | Result |
| --- | --- |
| Red before, retained base `app.js` in scratch copy, Node class | 8 failures: 403, http/404/429/generic server text, `{}`, `0`, source guard; `"x"`/null did not fail (preservation only). `red-before.log` |
| Green Node class after change | 8 passed |
| Non-browser focused set (11 modules incl. `test_handoff_waiting_view`) | Ran 149, OK, skipped 13 (opt-in browser classes). Final log and a pre-format log kept |
| Browser, download UI, run WITHOUT outer lock (self-locks) | 6 run, OK, 0 skips |
| Browser, new module, under non-queued `flock -n /tmp/ama-rpi-heavy.lock` | 15 run (8 Node + 7 Chromium), OK, 0 skips; rerun after formatting also OK |
| Browser, `test_handoff_waiting_view` WITHOUT outer lock (self-locks via helper) | 10 run, OK, 0 skips |
| `node --check`, Ruff check, Ruff format check, mypy (changed test), `git diff --check` | pass after format |

## Adverse and process outcomes retained

* Browser attempt 1 (`browser-attempt1-adverse-outer-lock-and-card-assertion.log`): 5 failures from my own overbroad assertion (`Pat Test` legitimately appears in the case list outside the card) and the waiting-view browser class skipped because I wrapped it in an outer lock although it self-locks. Corrected in the test (card-scoped check) and by running it unlocked; no source change. No environment repair or install.
* First `ruff format --check` failed on one wrapped assertion; formatted that file only (`static-attempt1-format-adverse.log`). One verification command lacked `PYTHONPATH` and errored; rerun with it.

## Web Interface Guidelines (fetched complete 2026-11-11)

`app.js:755-774`: error copy has a fix/next step (pass); alert is native `role="alert"` (pass); no new interactive element; empty state kept; active voice, second person (pass). `...` in the unchanged loading text and ASCII copy follow the repository ASCII standard over the generic typography rule. No other findings. No conformance, assistive-technology or human wording claim.

## Boundaries

No push, PR, issue, board or remote write. Refs #153 only; C2, C3 (universal), C5 unproved; named human wording review not performed.
