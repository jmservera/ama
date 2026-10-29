<!-- markdownlint-disable-file -->
# RPI Phase Details: agent-chat-157-refresh

## Metadata

* Task ID: pr-503-refresh-2026-10-29
* Task slug: agent-chat-157-refresh
* Related plan: .copilot-tracking/plans/2026-10-29/agent-chat-157-refresh-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/agent-chat-157-refresh-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Reconcile branch | Complete | P01-T01 |
| P02 | Validate and commit | Complete; ca5cb010 | P02-T01 |
| P03 | Review and handoff | Review Complete / Conformant; persistence and gate handoff | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Reconcile branch

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and resolve semantic conflicts

Context: common ancestor f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc;
topic 949aafaf7260965671297eabd6335a0311b9b45d;
main 5653547507f3056f09a726a18516237728da5e5b.
Before mutation, inspect git status --short, branch, in-progress rebase state
and PR lifecycle again. Only this loop's new evidence may be untracked.
Fetch origin main and record immutable pre-rebase HEAD and fetched base SHA.
Use git rebase with that captured origin/main SHA and noninteractive editor;
record each actual
conflict and inspect stages before editing. In a rebase, ours is rebased main,
not the topic: do not confuse checkout side semantics. Explicitly retrieve
rubric and manifest from the captured main SHA instead of assuming stage labels.
Require byte equality; a failing frozen-source test blocks the criterion and
does not authorize manifest edits.
Read chat_panel, server and browser overlap in context, preserving rejection,
privacy and employee-chat behavior. Preserve both log/index contributions.
No artifact or historical finding deletion. Evidence: rebase result, ancestor
test, no unmerged paths, source diff and snapshot equality.

<!-- rpi:phase id=P02 -->
## P02: Validate and commit

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute focused checks and persist evidence

Before any validation, resolve actual selectors into a working-directory /
exact command / behavior coverage table in the changes artifact. Confirm
import origins for core, agents and API point into this worktree using the
same explicit PYTHONPATH. This bounded resolution is mandatory, not optional.
Run /tmp/mv/bin/ruff check ., ruff format --check . and mypy from each
affected component core, agents and API. Execute unittest selectors with
PYTHONPATH=src:tests plus sibling core/agents/API sources/tests as applicable.
Include test_scenario_manifest even with main's snapshot. Include API chat
panel, isolation, role inventory and employee chat; core chat, admission,
memory/privacy and agents model/eval checks selected from actual module names.
Run API checks.employee_chat_browser_check and checks.regulatory_ux_check when
their reconciled source/checks change; include design-system checks if their
contract requires delegation. Record missing browser/axe prerequisites as a
blocked check, never a pass. Before web edits, load web-design-guidelines,
fetch the current rules and review changed web source, without redesign.
Do not run full API suite: no lock needed for focused modules. If a full suite
becomes necessary, require flock -n /tmp/ama-rpi-heavy.lock true and hold the
same lock throughout actual execution to avoid races.
Keep transient logs in session files or explicit external scratch, not tracked
generated output. Changes evidence records all failures, remediation and
successes. Commit with authenticated numeric-id noreply address and trailer.
Publication full-gate evidence is separate: never claim it from focused checks.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and local handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review once and route remaining work

Fresh independent worker receives exact candidate/base, research, plan,
critique and changes pointers. Write only the dated Review artifact.
Check intent preservation and truthful validation/publication boundaries.
Record execution separately from outcome. Human approval remains unchecked;
new Review findings become later work, not another implementation/review loop.
Persist Review and state in a separate local evidence commit if necessary.
Final handoff reports no push and any remaining hosted/full-gate blocker.
