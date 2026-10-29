---
title: PR 538 correction phase details
description: Task-level implementation and validation expectations, refs 531
ms.date: 2026-10-29
---

Task ID: `538-review-corrections-2026-10-29`.
Plan: `.copilot-tracking/plans/2026-10-29/loading-briefing-review-538-plan.md`.

<!-- P01 -->
## P01: Correct parser and startup

### P01-T01

C1/C2: shield citation contents before splitting. Change horizontal-only
trailing whitespace to line-break-aware whitespace, including whitespace
between successive references. Protect recognized abbreviation periods using
a distinct temporary marker and restore exact text before `analyse`.
Do not flatten unrelated newlines or infer a missing citation.
Exercise the exact LF example, CRLF/multiple groups, title/medial-abbreviation
variants, separate cited/uncited sentences, and explicit newline boundaries.
Record baseline red before source changes and green after.
Execution: complete. New regression command failed before source changes;
both supplied cases and title/medial/terminal examples now pass. Normalization
also flattens whitespace inside the captured reference group before moving
the final punctuation; otherwise retained newlines split punctuation away.
PC-001 disposition: supported titles Mr./Mrs./Ms./Mx./Dr./Prof./Rev./Sr./Jr.
and medial e.g./i.e./vs./cf. require a following same-line word.
Approx./etc. require a lowercase/digit continuation. St. is a name prefix at
statement start, after lowercase context or before a possessive proper name;
ambiguous uppercase street-suffix context is a boundary. This is intentionally
conservative, not general English disambiguation.
Exact discriminators: `Dr. Smith checked the case. [[First source]]` and
`St. Mary's needs repairs. [[First source]]` each stay intact, whereas
`The address is High St. Repairs are due. [[Second source]]` yields uncited
address and cited repairs. Include terminal etc. versus medial etc. and
assert full text/citations/unresolved, retaining the original user fixtures.

### P01-T02

C3/C6/C8: let the dependency predicate handle `me === null` and include
`/async-action.js` for every workspace destination. Bootstrap awaits
`requireWorkspaceScripts` before account helper listeners and `start()`.
Use captured session identity during recovery so null bootstrap does not
silently bypass readiness and expired session routes still cannot dispatch.
On bootstrap exhaustion use existing explicit dependency error and native
reload. Healthy service errors retain Try again; never reinstall lexical
scripts after uncertain evaluation.
PC-002 disposition: call `requireWorkspaceScripts("", false)` in bootstrap.
All role-specific predicates require an authenticated `me`, regardless of
deep link. Null-session overview/case predicates select only the helper if
missing, nothing otherwise. Unchanged null identity must still run readiness
checks; changed identity returns to the existing stale-session guard.
Exhaustion, timeout and loaded-without-readiness reject at bootstrap; start
and helper account listeners are not reached. Terminal native reload is
announced through the alert/status and is keyboard-operable.

Extend Node harness with a healthy AsyncAction stand-in for existing scenarios,
actual missing-helper cases, null bootstrap, concurrency/budgets/readiness.
Browser intercepts helper, aborts first download (and optionally a retry), then
permits shipped helper; require login, case navigation and working account
action without page errors or document reload. Exhaustion and missing-global
Execution: complete source/test changes. Node executes shipped loader and
bootstrap, proving helper-only null overview/case/screens selection, no
listener/start before readiness, eventual account actions, cached exhaustion,
missing-global/timeouts and existing route/session isolation.
Chromium scenarios authored for one/two failed downloads, exhaustion and
loaded-without-readiness, with sign-in, resident case actions and sign-out.
Actual browser execution is blocked by nonblocking heavy admission. Exhaustion and missing-global
cases require bounded requests and keyboard-native reload after unblocking.
Existing full loading/briefing browser run retains axe and action regressions.

### P01-T03

Document helper boot recovery and parser boundaries in API README, without
claiming general language parsing or human acceptance. Compare changed files
with scenario-manifest sources; update SHA pins only if a pinned input changes.
Execution: complete. API README updated in place. None of the four pinned
inputs changed; all 11 existing needs-inventory checks pass without pin churn.

<!-- P02 -->
## P02: Validate and preserve

### P02-T01

Source-first `PYTHONPATH` includes this worktree's core/agents/API src and tests.
Focused selectors: `test_ai_statement_sources`, `test_loading_feedback`,
`test_workspace_scripts`, `test_ai_tasks`; JS `node --check`.
Core and API each: `/tmp/mv/bin/mypy`, `/tmp/mv/bin/ruff check .`,
`/tmp/mv/bin/ruff format --check .`.
Full admission: `flock -n /tmp/ama-rpi-heavy.lock`; record busy admission and
targeted fallback, never queue/poll or interrupt another owner.
When admitted, editable-install core/agents/API in `/tmp/mv`, run each package's
`python -m unittest discover -s tests -q`, and both
`checks.loading_briefing_browser_check` (pinned axe and external output) and
`checks.workspace_scripts_browser_check`. Record exits and existing skips.
No private/default dataset, Azure invocation or full cloud/publication gate.
Execution: user-authorized targeted fallback. Full admission exit 75, current
owner PID 661156 at admission; no queue, polling, shared install or browser run.
83 focused tests passed with no skips. Core mypy 157 files, API mypy 101 files,
Ruff check/format both packages, JS syntax and Git whitespace checks pass.
Use current-worktree source-first paths with the existing `/tmp/mv`; fresh
editable setup is deferred rather than mutating the shared venv without lock.

### P02-T02

Changes artifact records files, amendments, divergences, actual commands/exits,
residuals and phase reconciliation. Resolve GitHub identity through `gh api user`
and set repo-local noreply email before commit. Conventional messages contain
`Refs #531` only and the mandated Copilot coauthor trailer.
Commit implementation and dated original evidence, dispatch exactly one
independent Review, then persist its unchanged outcome and route any findings
to later work. Stop local as explicitly requested; no push or automatic child.
Current reconciliation: source changes complete, static/targeted evidence
current, full/browser residual explicitly routed to FU-001. Candidate and
dated original evidence committed locally as `0e910aa1`. P01/P02 Complete;
independent Review owns its own phase. No further implementation is pending.
