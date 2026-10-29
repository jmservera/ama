---
title: Employee chat skills 530 changes
description: Implementation evidence and validation boundaries
ms.date: 2026-10-29
---

## Scope and status

Full P01-P03 implementation under explicit full-loop direction. Research Ready;
one critique Complete / Revise, dispositions applied in plan, no repeated critique.
Source implementation complete; validation partial; ready for independent
Review. Source baseline d70ee60ab3d7346a9991cf64382d9985f4d09f2e.

## P01-P02 implementation

P01: ChatPanel accepts explicit general or five registry skill IDs, retains
legacy omission behavior, narrows skill categories over existing projected
case facts, adds trusted workflow sources and visibility limits, and records
question sequence/skill/outcome without raw question text in the ledger.
Existing agents ChatModel adapter reused unchanged.
P02: Header launcher and native modal across employee routes; existing case
and regulatory panels preserved. AsyncAction busy feedback, abort/disposal on
route/login/denial, bounded latest exchange, labelled cited/unverified answers.

## Validation and blockers

Focused API/core chat tests: 37 passed. Initial test failure used the wrong
audit fixture location; corrected to actual audit_entries. Initial core mypy
found mixed registry value inference; public purpose now explicitly string.
API/core Ruff and formatting pass; core 157 files and API 107 files pass mypy.
Initial browser/axe found invalid list role and nested scroll region; fixed
with native list inside live-region wrapper and one outer dialog scroll.
Next browser run reached focus assertions; replaced unsupported exact native
wrap assumption with actual in-dialog traversal assertions.

Nonblocking heavy lock initially admitted targeted browser runs. A subsequent
`flock -n /tmp/ama-rpi-heavy.lock ...employee_chat_browser_check...` exited 1
with no test output: busy admission. No queued/repeated full-suite admission,
foreign container use or interruption. Full suites and actual disposable SQL
are blocked by shared lock; continue independent targeted checks only.
Actual lock owner observed with lslocks: PID 771340, python3, canonical path.
Do not inspect/reuse its evidence or container.

Final permitted results, all explicit worktree source/test PYTHONPATH:

* From src/api: /tmp/mv/bin/ruff check .; ruff format --check .; mypy:
  all pass, 107 source files typed.
* From src/core: /tmp/mv/bin/ruff check .; ruff format --check .; mypy:
  all pass, 157 source files typed.
* API unittest selectors test_chat_panel test_chat_isolation
  test_chat_fixture_roles test_role_endpoint_inventory test_workspace_scripts:
  82 tests pass. Initial workspace test failure was an obsolete case-only
  chat.js readiness expectation; corrected for global staff chat.
* Core unittest selectors test_chat_panel test_chatthreads test_chat_privacy:
  54 tests pass, including JSON/SQLite storage, not real SQL Server.
* Agents unittest selectors test_chat_model test_chat_provenance test_chat_fixture:
  16 tests pass; existing adapter unchanged.
* New employee_chat_browser_check with pinned axe-core 4.10.3 SHA-256
  880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb:
  pass on constructed loopback server. Actual unavailable-model fallback;
  six intercepted selection/rendering states; global route reachability;
  case/no-case disclosure; keyboard containment/Escape/return focus;
  320/390/1280px reflow; reduced motion; route/session/403/404 disposal;
  aborted delayed response does not populate replacement context.
  Two actual dialog-scoped axe states each have zero violations and 20 passes.
  No live model or site inference.
* JavaScript syntax and git diff --check pass. Public scenario-manifest
  SHA-256 pins all match; none of its pinned sources was edited.

Browser output and logs retained externally under session
8df83efd-d268-4456-99f8-d2978b1a7a23/files, not committed generated assets.
Earlier failures remain recorded above; no receipt or whole-suite pass implied.
Full publication gate blocked by no-az
direction; do not invoke runner that executes az. No push or live verification.
Screen-reader, voice-control and human approvals unclaimed.

## Amendments and divergences

No router. Critique PC-004's alleged /tmp prohibition rejected as unsupported;
user explicitly names /tmp/mv and canonical shared lock. Explicit worktree
PYTHONPATH used. Initial editable install completed successfully.
Related existing harness updates are current-state amendments, not scope
expansion: global script readiness and opt-in constructed privacy admission.
Fresh Web Interface Guidelines retrieved again before final review; repository
plain ASCII and sentence-case standard takes precedence over generic copy.

## Review handoff

Plan/details/changes reconciled. One independent post-implementation Review
assesses the full working candidate against origin/main baseline above, with
full-suite/SQL, publication, live and human acceptance explicitly unmet.
