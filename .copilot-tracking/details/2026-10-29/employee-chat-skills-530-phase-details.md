---
title: Employee chat skills 530 phase details
description: Task boundaries and completion evidence
ms.date: 2026-10-29
---

## P01

P01-T01: C1-C4. Use optional skill argument to preserve legacy no-case behavior.
Expose all five advisory purposes from existing registry. Restrict skill facts
to relevant projected categories plus common case metadata, with trusted
workflow purpose/boundary sources. A skill never invokes proposal service.
General help is bounded by these sources, not invented organizational policy.
Audit thread ID, question sequence, selected skill and outcome, no content.

P01-T02: Strict field/skill validation at existing ask route; skill metadata
requires current chat authorization. Case/thread ownership is checked each turn.

Wire modes: absent skill = legacy behavior; "general" = trusted workflow
knowledge; each registry ID = that advisory purpose. Null, nonstring and unknown
values = 400 before storage/inference. No thread task schema changes.

## P02

P02-T01: Launcher in employee header, hidden before login and for contractors.
Native dialog with visible close control, labelled selector and question,
live answer/status, bounded transcript and source display. Context is snapshot
from current case route; navigation closes/removes the old dialog to prevent
stale answers or cross-case display. Login/session transitions and 403/404
denials also dispose transcript/context; abort old requests and suppress stale
completion and focus. No building record falsely called a home.

P02-T02: Keep chatCasePanel and regulatory panel untouched except shared answer
wording if needed. AsyncAction.run supplies busy/spinner state. No animation
introduced; use native Fluent token colors, responsive width and scroll bounds.

## P03

P03-T01: Extend test_chat_panel ownership (API/core) without deleting old tests.
One browser module reuses design_system_browser_check constructed server.
Use synthetic privacy references only inside test fixture environment.
Invoke `python -m checks.employee_chat_browser_check --axe <pinned-file>`.
Scan the actual open dialog subtree with pinned axe in answer and failure
states, including mobile reflow and keyboard focus checks.
Test actual missing-model fallback plus synthetic cited-answer rendering;
do not equate synthetic provider output to live model quality.

P03-T02: Install editable src distributions into /tmp/mv; set explicit
PYTHONPATH to this worktree src/test paths. Run API/core Ruff, format and mypy,
agents tests if adapter changes, focused and admitted full suites under
flock -n /tmp/ama-rpi-heavy.lock. Actual local SQL must use owned disposable
resources, never inherited database settings. Busy lock means targeted checks
only and explicit blocked full-suite evidence.

P03-T03: API README holds concise skills-vs-router design and visibility/
privacy/failure contract. Preserve original critique and Review verdicts.
Commit locally with authenticated noreply identity and required trailer.
No push, PR creation or az. Leave human/live approval unchecked. After original
Review and local commits, record the complete gate blocked: its az Bicep
commands are forbidden. Package/browser results never imply a full receipt.

## Implementation reconciliation

P01/P02 complete. Native dialog needs explicit boundary Tab wrapping in the
tested Chromium; implemented and verified, not assumed from native modality.
P03-T01 complete with eight added unit methods across current API/core panel
owners, one browser module, existing loader-test expectations updated and
explicit synthetic privacy fixture support in the constructed server helper.
No removed tests, generated output or pinned recipe changes.
P03-T02 partial: API/core Ruff/format/mypy and targeted tests/browser pass;
full suites and disposable SQL blocked by actual foreign heavy-lock ownership.
P03-T03 documentation and dated evidence prepared for one independent Review
and local-only commit. No full-plan or issue acceptance claim.

## P04 correction pass

P04-T01: A shared modal-local denial helper resets/removes case context and
posts workspace guidance, focusing the existing #app workspace. Both metadata
and submit catches use it for 401/403/404 only while current; api() already
owns 401 login transition, so obsolete catches cannot focus the workspace.
Test metadata, thread-create and ask 403/404; keep 401 sign-in coverage and
recoverable non-denial errors distinct.

P04-T02: Keep transport regression but wait for actual intercepted ask before
navigation. Separate controlled api wrapper holds a successful answer promise,
ignores abort deliberately, and exposes the whole form task for awaiting its
settlement. Exercise explicit close, navigation/replacement dialog and changed
session. Snapshot old/current transcript/status and active element before and
after success. Also audit metadata/thread stale completions where feasible.
Restore wrappers after each case. No sleeps, optional skipped response or
cancellation substitutes for a successful application completion.

P04-T03: Truncate fully redacted user content before store.chat_add_message;
reuse the exact masked bound for prompt construction. Test expanding postcode
mask at 8,000 characters and sibling identifier masks. Cover omitted skill,
general and the five registry skills; verify original identifier is absent and
question sequence remains correct. Add at most three unit methods using
existing synthetic fixtures; no real user data.

P04-T04/T05: Run installed /tmp/mv tools with explicit current-worktree source
and test paths, without mutating shared venv. Core discovery and API selectors
are the requested coverage; browser uses pinned axe and an owned synthetic
loopback server. Use nonblocking shared lock for heavy work; busy admission
blocks only that evidence. Retain external output in the current session.
One fresh critique and one independent Review for this later correction pass
append to existing artifacts without overwriting original verdicts. No push,
az, SQL claim, issue closure or human approval.

P04 implementation reconciliation: T01-T04 complete. Two regression methods
and one browser helper; no removed tests. The helper awaits the actual Ask
AsyncAction consumer task (or open() for metadata), asserts successful promise
fulfillment and prevents follow-on ask from obsolete thread creation. It checks
three awaits times close/route/session, with old and current transcript/status,
draft, workspace status and exact active-element identity unchanged. Actual DOM
removal is awaited before resolving; a role locator alone can stop matching a
closed-but-not-yet-disposed dialog before its close event aborts the controller.
Denials cover skills metadata/thread creation/ask times 403/404/401; 401 returns
to login without stale workspace guidance. All requested local static checks,
core discovery and selected API suites pass; final owned browser/axe passes.
Core discovery's 190 skips do not establish opt-in SQL integrations.
T05 independent Review Complete/Conformant, local-only commit 0dd763c5 complete. Original
P03-T02 whole-feature SQL/API/full-gate gaps remain outside this bounded scope.
P04-T01-T05 complete. Evidence-only closeout records actual commit completion;
no repeated Review or complete publication receipt is implied.
