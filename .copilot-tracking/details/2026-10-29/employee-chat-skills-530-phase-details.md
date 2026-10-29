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
