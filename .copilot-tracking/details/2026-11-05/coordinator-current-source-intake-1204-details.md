<!-- markdownlint-disable-file -->
# Details: coordinator current-source intake (issue 1204, pass 5)

Written 2026-11-05T22:51Z before implementation.

## Phase 1 edits (.github/agents/ama-backlog-delivery-coordinator.agent.md)

* G1, admission bullet (about line 98): state that the eight include a frozen unpublished candidate that is awaiting coordinator validation, publication or correction, counted once per issue with its session or open PR; a candidate frees its slot only when published and merged or explicitly released.
* G2, Provenance bullet (about line 191): the live read-back is authoritative; as of 2026-11-05 delivery 15 (10 minutes) and cleanup 8 (hourly) are active per operator-supplied evidence, delivery #9 and #7, #6, #2 are historical; no prompt text restated.
* G3, activity-handoff sentence (about line 318): the flags are now on main; keep the `--help` gate; keep the legacy `--apply` prohibition when `--help` does not list them.

## Phase 2 test design (designer separate from executor and grader)

* Executor: child `copilot --agent hve-core-all:hve-artifact-tester --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 30 --log-dir ... --share ... -s -p`, reading only the agent file and a synthetic scenario file. It emits the decision per case. Shell, merge, push and cleanup are text decisions only.
* Grader: a separate child run (read-only, Auto) with a rubric; the lead does not grade.
* Cases: T1 idle with 99 unreviewed closures and no tmux; T2 blocked PR with ready independent issue; T3 seven live sessions plus one frozen unpublished candidate, ready issue (no admission); T4 approved action and a second owner question; T5 child brief with parent stack and no publication; T6 cleanup with active receipt and unknown upstream; N1 negative control with G1 sentence removed in a scratch copy under /tmp (must fail T3).
* Output evidence: .copilot-tracking/hve-builder/2026-11-05/coordinator-current-source-intake-1204-*.

## Phase 3 checks

python3 -m unittest on tools/test_backlog_sync.py and tools/test_rpi_checks.py; git diff --check; frontmatter diff against HEAD~; non-ASCII scan of changed lines; local link existence for artifacts.
