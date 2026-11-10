---
title: Issue 153 pending-handoff read-failure guidance plan
ms.date: 2026-11-10
task_id: 153-handoff-read-guidance-1110
---

## Objective

When the pending-handoff read rejects at transport level, the "Handoffs waiting for you" card states the reason, the existing owner and a safe next action, without raw technical text and without implying an empty queue. Initial scope only; no repair allowance, no fresh five.

## Scope and boundaries

* Change: `src/api/src/zava_forward/api/web/app.js`, `pendingHandoffs` catch and one adjacent constant. Nothing else in the file, including the frozen #130 nomination hunk.
* Add: `src/api/tests/test_handoff_read_guidance.py` (Node VM cases on the real function source and opt-in served-browser cases).
* Out of scope: HTTP error bodies, other panels, `api()`, `fetchReadRetrying`, `ops.js`, `panels.js`, active checkers (#231, #230, #233), Core, schema, auth, infra, knowledge-base audit tables.
* Tier: focused (targeted tests, static checks, one focused browser run under the nonqueued canonical lock). No full or `--changed` gate. Registered recipe: unchanged, so manifest recipe SHA is N/A.

## Phases

1. Source: add `HANDOFF_READ_ERROR` (reason, owner, next action, ASCII, plain words) beside `pendingHandoffs`. In the catch: return silently on `AbortError`; render the constant when the error has no HTTP `status`; keep `Could not load handoffs: ${e.message}` when it has one (HTTP and session-ended paths unchanged). Keep `role="alert"`, element, class and structure.
2. Regression: Node VM cases on the extracted function for rejection (canary absent, guidance present, one `api` call, no mutation), abort (nothing painted), HTTP error (unchanged text), session ended (unchanged), success (rows listed), empty (hidden), plus lexical guard (ASCII, banned words, no raw message). Opt-in browser cases serve the real app with synthetic data: success, empty, constructed fetch rejection with canary, request count and no POST, navigation away during a pending read.
3. Validate: red against base `app.js`, green after; existing handoff and content tests; `node --check`; Ruff and mypy on the new test; `git diff --check`; web-guidelines review of the changed hunk with `file:line` output.
4. Evidence and commit: changes record, review (author, one pass), witness events, local commits with privacy-safe identity and trailer.

## Success criteria

* Constructed rejected GET shows reason, owner "application support" and next action; canary text absent; card not hidden; no "no handoffs" inference.
* Success and empty behaviour identical to baseline; HTTP, 401 and abort behaviour identical or safer (abort paints nothing).
* One GET per render; no retry loop, extra request or POST.
* No layout, style, framework or global API change.
