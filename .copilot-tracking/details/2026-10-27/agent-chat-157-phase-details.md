<!-- markdownlint-disable-file -->
# RPI Phase Details: agent-chat-157

Task ID 157; 2026-10-27. Parent plan:
.copilot-tracking/plans/2026-10-27/agent-chat-157-plan.md.
Research: .copilot-tracking/research/2026-10-27/agent-chat-157-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Implemented, targeted regression evidence | P01-T01 |
| P02 | Implemented, Chromium and eval evidence | P02-T01 |
| P03 | Targeted validation and Review preparation complete | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Bound and unify turns
<!-- rpi:task id=P01-T01 -->
### P01-T01: Admission, receipt and guards

Targets: core chat_panel.py, chat_isolation.block, agents chat.py and API
server.py. Keep injected callable model boundary; add typed per-call result
carrying text, validated usage and fixed outcome with no last-call global.
Failure carries metadata, never raw provider text. Validate numeric token counts
(reject bool, negative, inconsistent totals). Store metadata event per completed
turn and return it for reporting. No prompt or text in event.

Use untruncated source JSON with an explicit final prompt ceiling. Retain at
most twelve user messages with an aggregate 4,000-character history bound;
do not resend assistant answers or memory. Oversized new input falls back,
not silent truncation for inference. Re-read current user, thread and case
projection after callback; changed/revoked access or sources withholds output.
No lock is held during the provider call.

Wire existing release gate into server-owned ChatModel admission. Missing gate
or unregistered/unapproved conversational task denies; test admission overrides
exist only in explicit synthetic harnesses. Route legacy HTTP /messages through
panel, preserving reply/label/model/withheld keys. Other direct core isolation
helpers are not new activation paths.

Proof: adapter denial and malformed usage, exact bounds, current permissions,
cross-user tests, calls/metadata isolated across invocations and source completeness.
Admission is rechecked after completion too; denial discards text and retains
incurred usage. Metadata receipt is written once before rethrowing completion
authorization/not-found failures; evaluator reads those ledger events without
releasing the forbidden content. No shared last-result mutable state.

<!-- rpi:phase id=P02 -->
## P02: Warning and report
<!-- rpi:task id=P02-T01 -->
### P02-T01: Canonical warning and consumption

Targets: permitted chat status GET endpoint, web/chat.js, chat_eval.py.
Status gives warning, unknown retention and engineering limits, not approval.
Disable entry until received; associate warning via aria-describedby; native
form/details/log remain. Preserve refusal workflow text instead of labelling it
unavailability. Expose error if assistant proposal registry fails to load.

Evaluator accumulates each panel receipt, zero actual calls (scripted calls
reported separately), explicit Unknown tokens/cost and missing inputs, counts
per scenario and per answer passing runtime filter. No claim of independent
human labelling or quality benefit. Development golden known failure preserved.

Proof: API role authorization/inventory, UI structure and rendered DOM if
available, eval deterministic reporting and negative controls.

<!-- rpi:phase id=P03 -->
## P03: Validation and evidence
<!-- rpi:task id=P03-T01 -->
### P03-T01: Regression, documentation and Review preparation

Run focused tests first, then affected package suites/static checks. Update
existing DPIA synthesis plus index/log and component contracts. Do not select
numeric legal retention or provider terms. Review one complete candidate with a
fresh independent reviewer; preserve findings and route them as later work, no
repeat Review. PR uses Refs for all five issues.
New material implementation findings block publication and are routed as later
work; accepted human evidence residuals are distinguished from code defects.
Preserve the original assessed boundary and never imply later-head independent
acceptance. PC-003's claimed /tmp prohibition was not present in the caller or
active instructions and is rejected; the isolated external venv remains valid.

Initial environment test failed because namespace packages were missing;
isolated /tmp/ama-chat157-venv now installs editable core/agents/api and declared
dev tools via pip. No private data or cloud access.

Completion evidence: actual commands/results in changes artifact; known eval
failure distinct from unit suite pass; named human blockers in Review and PR.
Targeted API/browser suite 80 passed; full agents 109 passed; all three
packages Ruff/format/mypy passed; node syntax passed; migration tests 25 passed
after restoring declared missing dependencies with pip. Supplemental full
core/API discovery remains in progress. This is not a claim those suites pass.
The subsequent lifecycle Review owns the one read-only independent assessment.
