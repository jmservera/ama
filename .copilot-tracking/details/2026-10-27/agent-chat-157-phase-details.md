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

## Correction cycle 1 details (2026-10-27)

<!-- rpi:phase id=P04 -->
### P04: Correct and validate the disclaimer browser contract
<!-- rpi:task id=P04-T01 -->
#### P04-T01: Harness-only targeting and local validation

Research C8-C10 reproduces the strict-mode failure: both the original disclaimer
and new `#chat-privacy` are direct `.muted` children. Use the existing structural
position `#chat-panel > summary + p.muted`, assign it to `disclaimer`, assert
exactly one visible match, and retain the two original `to_contain_text`
assertions. No `.first`, expected-text filtering, broad panel assertion,
privacy-warning removal or production UI edit.

From `src/api`, prepend `/tmp/ama-chat157-venv/bin` to PATH, using the existing
installed Python 3.12.3 distributions/tools. This is equivalent to invoking
`python3` from the isolated environment; no manifest/dependency change.

* `python -m checks.design_system_browser_check`
* Fetch axe from the workflow's exact cdnjs 4.10.3 URL, using the same fail,
  retry and timeout flags into the session files directory.
* `PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.regulatory_ux_check
  --axe <session-files>/axe-4.10.3.min.js --out <session-files>/chat157-correction1-after.json`
* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q`
* `ruff check . && ruff format --check .`; `mypy`.
* Run workflow's isolated strict Ruff check and format check for the changed
  harness as well, since project config exempts browser harness formatting.

If existing Chromium is unavailable, install only after that failure with
Playwright's documented install command; no preemptive reinstall. A real pinned
axe run is required; an omitted axe argument is only failure reproduction.
No heavy `rpi-checks` run: this is a small selector correction.

Completion: updated P04 markers, exact local outcomes/skips in changes, original
verdicts untouched, one independent bounded correction Review appended, same
draft PR updated. Remote recheck/rebase is conditional on actual divergence.
No scope change, live acceptance or human decision is inferred.

P04 completion: the single harness edit is implemented exactly as planned.
Both browser modules with pinned axe passed (19 regulatory states, zero
violations); negative missing/hidden/label/review-boundary controls all failed
as intended. API discovery OK, 1129 tests / 315 skipped in 472.030s; API Ruff,
format/mypy and isolated strict browser Ruff/format passed. Details and changes
agree; generated JSON remains external. No remaining in-scope implementation.
Original human/semantic/accounting/stabilization work is outside this correction.
