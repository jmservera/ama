<!-- markdownlint-disable-file -->
# Plan: full behavior evidence at abd6b3f5f (issue 1204, pass 7)

Research: .copilot-tracking/research/2026-11-05/coordinator-behavior-evidence-abd6-1204-research.md. Details: .copilot-tracking/details/2026-11-05/coordinator-behavior-evidence-abd6-1204-details.md.

## Phases

* [ ] 1 Sandbox, run-state, source blob pre-check.
* [ ] 2 Independent generic design subagent (black-box scenarios, IDs, success signals); lead validates and persists.
* [ ] 3 Native Automatic-profile execution per scenario in isolated repos, plus broken-copy negative control.
* [ ] 4 Lead finalizes test-log; fresh independent generic grader; lead writes test-review.
* [ ] 5 Durable behavior report; focused checks with direct exits; source blob post-check.
* [ ] 6 Evidence-only review, state, NEW commit, final frozen-head recheck.

## Constraints

Source file byte-unchanged; no tracked edit after the commit; no cleanup or deletion; sandbox and /tmp/h1204 retained; no heavy lane; no push.

## Critique (single, before implementation)

Risks: the designer must not see prior scenarios or expected answers; the grader must not be the lead or the designer; scenario text must not name the target or leak the wrapper; negative control must use an isolated copy only. A failed scenario is preserved and reported, not rerun silently. Verdict: proceed.
