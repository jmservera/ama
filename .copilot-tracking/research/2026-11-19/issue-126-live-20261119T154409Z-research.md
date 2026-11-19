# Issue 126 live research (2026-11-19)

Task issue-126-live. Research disposition: reused. Planning Readiness: Ready.

Evidence reused: docs/reference/research/issue-126-live-2026-11-19.md (base d51383c20), re-checked on this base:
`src/core` `tests.test_governance` run again in this worktree: 88 tests OK, 18 skipped (opt-in loopback SQL class).
`src/core/src/zava_forward/core/governance.py` already holds the 22-finding register (`_rai_view`, `dispositions_complete`),
assessment binding to commit, task and release version, five disposition tiers and Unknown/Unappointed/Unverified decision-maker states.

Remaining unticked criteria: approval of protocol, DPIA and lawful basis (named human); populated 22 dispositions (evidence, constructed
claims only); fresh assessment run; qualified-owner decisions; real AI/SQL/Azure contract (SQL scope forces the full tier).
Conclusion: none is a buildable code gap for the demo. No Azure resource created, nothing written live.
