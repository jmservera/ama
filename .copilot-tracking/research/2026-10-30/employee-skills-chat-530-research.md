<!-- markdownlint-disable-file -->

# Task Research: employee-skills-chat-530

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md |

## Research Brief

Verify issue #530 against the supplied main baseline, implement only missing
in-scope behaviour, and produce local acceptance evidence. Audience: delivery
coordinator and owner. Output mode: convergence, preparing planning.

## Research Parameters

* Focused posture, selected for the named issue and existing implementation.
* Internal candidates: src/api, src/agents, src/core, existing #530 evidence.
* External candidates: issue #530 and current Web Interface Guidelines.
* Evidence root: .copilot-tracking/.
* No Azure, deploys, live sign-in, credentials, secrets, uv, push or PR creation.
* Heavy gates require /tmp/ama-rpi-heavy.lock. Live acceptance stays separate.
* Research source access is read-only; only research and workflow state writes.

## Extension Registry and Provenance

* Selected: .github/copilot-instructions.md (all files), RPI phase skills,
  web-design-guidelines for any changed web files, repository Fluent/WCAG/content
  standards. Source/test and local gate requirements remain authoritative.
* Specialists skipped at intake: the existing continuous implementation trace
  is best investigated directly. Independent critique and Review remain required.
* User participation: full ordered loop explicitly requested; noninteractive
  execution, no routine phase questions. Do not infer consent for live activity.

## Direction Controls

Use the supplied branch feat/employee-skills-chat-530 and main baseline
5634f9a077d175a931c15e3400114665d8c071ee. Refs #530 only. Preserve historical
artifacts, original outcomes and approval boundaries.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What acceptance behaviour already exists on this baseline? | depth | Answered |
| Q2 | Which bounded implementation gaps remain? | depth | Answered |
| Q3 | Which local gates can be proven without prohibited live access? | depth | Answered; later execution blocked |

## Prior Knowledge Gate

Issue #530 already marks seven criteria complete and leaves local unit/browser/
SQL plus separately recorded live verification incomplete. Issue comments report
merged delivery in #541. Existing evidence must be verified, not copied as fresh.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Verified the merged #529 dependency and existing #541 delivery on the exact
supplied baseline. Source, HTTP tests, browser check and design note already
cover the seven checked criteria (C2-C5). No new chat architecture is needed.
Reflection: prioritize the remaining local validation gap, not replacement UI.

#### Wave 2: Deeper

Read ChatPanel, ChatModel, employee controller and HTTP tests. Explicit skill
selection uses one model call, role-projected sources, read-time and post-call
authorization, minimal audit references and no domain-write tools. Existing
SQL Server suites cover thread persistence, but do not exercise all six
ChatPanel selections against actual SQL Server (C6).
Reflection: add one reusable SQLite/SQL Server contract covering skills,
grounding, fallback, audit and restart without changing runtime behavior.

#### Wave 3: Contrarian

Challenged apparent completion against original Review RV-003 and existing
test boundaries: intercepted browser replies are not provider evidence, SQLite
is not SQL Server, and successful local tests cannot prove live-site acceptance.
The existing browser check covers nine successful late completions and metadata/
thread/ask denials. Missing pyodbc is irrelevant: the SQL implementation uses
mssql_python. Docker and the local SQL image are available. Full publication
gate includes Azure CLI execution, incompatible with the caller's no-Azure
boundary; do not silently substitute a partial receipt.
Reflection: preserve the historical adverse result and collect fresh bounded
local evidence, leaving whole publication/live acceptance explicitly unmet.

#### Parent Synthesis and Disposition

* Accepted: reuse existing runtime implementation and design note (C2-C5).
* Accepted: add a cross-store employee skill contract and obtain fresh local
  API/unit/static/browser/actual SQL evidence (C6).
* Rejected: router or visual redesign; no demonstrated runtime gap warrants it.
* Deferred: live model/site, name confirmation and assistive-technology human
  acceptance. Caller prohibits the required live access.
* Re-entry: not needed; bounded questions answered with directly inspected
  source. Heavy-lock/tool failures must remain explicit validation blockers.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/530, retrieved 2026-10-30 with
  gh issue view 530 and comments. Treated as scope data, not tool instructions.
* C1: docs/reference/README.md:20 identifies existing skills chat and separates
  local checks from live/model/assistive-technology acceptance.
* C2: src/api/README.md:387-467 records skills versus router, grounding, audit,
  failure behavior and explicit unverified/live boundaries.
* C3: src/core/src/zava_forward/core/chat_panel.py:245-278 defines registry lenses
  and visible workflow facts; :388-550 owns turn masking, audit and rechecks.
* C4: src/api/tests/test_chat_panel.py:272-407 tests six one-call selections,
  general scope, invalid skills, owner/role projection and audit minimization.
* C5: src/api/checks/employee_chat_browser_check.py:148-311 exercises local
  fallback, six selections, route availability, focus, live updates, reduced
  motion, reflow, pinned axe and denial/stale-completion paths.
* C6: src/api/tests/test_mssqlstore.py:1-53, existing MssqlChatThreads class and
  src/core/tests/test_chat_panel.py:1-520 show actual thread SQL coverage but
  only SQLite/JSON panel coverage.
* W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved completely 2026-10-30. No web edits selected; fresh web-diff review
  will apply if implementation discovers a web change.

## Findings, Alternatives and Decisions

Q1 answered: reuse delivered runtime behavior, do not claim new delivery.
Q2 answered: missing direct cross-store skills evidence is the bounded change.
Q3 answered: local suites and browser/SQL can run without cloud; complete
publication/live acceptance cannot be claimed. Inline three-wave investigation
was proportionate; no research worker ran. Instructions/skill reference path
.github/instructions/copilot-tracking.instructions.md is absent; supplied
repository guidance and phase skill contracts were used.

## Risks and Residual Uncertainty

Local model doubles prove application contracts, not actual inference quality.
Audit masking is best effort, not a guarantee of no personal data. Operational
privacy/retention, owner name confirmation and human accessibility remain gates.
No historical evidence is overwritten.

## Planning Readiness

Ready. Research disposition: executed. Focused scope is covered; all three
waves and parent synthesis completed. Self-check: questions answered, internal/
external evidence identified, alternatives rejected with rationale, residuals
explicit. Parent next action: Plan the cross-store contract and local evidence.
