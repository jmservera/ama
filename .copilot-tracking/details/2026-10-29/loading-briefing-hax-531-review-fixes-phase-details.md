<!-- markdownlint-disable-file -->
# RPI Phase Details: loading-briefing-hax-531-review-fixes

## Metadata

* Task ID: 531-review-fixes-2026-10-29
* Task slug: loading-briefing-hax-531-review-fixes
* Related plan: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Parser and review harness | complete; focused regressions pass | P01-T01 through P01-T03 |
| P02 | Helper recovery | complete; unit pass, browser unperformed due busy lock | P02-T01 |
| P03 | Validation and local persistence | complete; targeted fallback, original Review and local evidence retained | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Parser and review harness

Context: C2-C4 reproduce exact defects; existing title/medial behavior is required.
Boundaries: no new tokenizer dependency, no inferred sources, no historical edits.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Repair dispatch activation

* Target: src/api/tests/test_case_journey.py existing dispatch matrix.
* Select Edit button, call onclick({currentTarget: editButton}); retain reference
  to submit and call submit for post-history-barrier retry, never buttons[1].
* Expected evidence: same eight-outcome matrix actually reaches dispatch,
  preserves newer dirty values, blocks duplicate writes and completes once.
* Dependencies: critique disposition only. Unresolved items: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Closing-delimiter boundaries

* Targets: src/core/src/zava_forward/core/ai_tasks.py and owning parser tests.
* Introduce one regex fragment for sentence punctuation plus zero or more
  closing ASCII/curly quotes and )]} delimiters. Relocation moves protected
  citations before the entire ending, preserving quote/bracket order.
* Use that same fragment in segmentation without dropping ending characters;
  keep newline-only boundaries and abbreviation shielding intact.
* Tests: exact supplied sentence; .!?; ASCII/curly quote, apostrophe, )]},
  nested closers; references before and after punctuation; unknown references;
  first uncited, second cited; separators including newline.
* Expected evidence: full exact dictionaries, no citation stealing or quote loss.
* Dependencies: critique disposition; no unresolved schema question.

Original supplied golden (PC-002), sources = {"ZF-1": ["First source", "Second source"]}:

```python
text = 'The status is "Survey booked." [[First source]] Repairs are due. [[Second source]]'
expected = [
    {"text": 'The status is "Survey booked."', "citations": ["First source"], "unresolved": []},
    {"text": "Repairs are due.", "citations": ["Second source"], "unresolved": []},
]
```

<!-- rpi:task id=P01-T03 -->
### P01-T03: Terminal suffixes

* Targets: existing abbreviation callback and parser tests.
* Treat Jr./Sr. after a capitalized name pair before an uppercase next claim
  as terminal before period shielding. Preserve lowercase continuation
  ("John Smith Jr. is available") and titles ("Contact Jr. Jones").
* Test both Jr./Sr., terminal first sentence uncited, first-only/second-only
  references, and a medial suffix with a cited first sentence followed by
  separately cited repairs. Preserve current title matrix.
* Conservative limitation: not full English sentence inference; ambiguous
  uppercase continuations can split rather than lend unverified support.
* Expected evidence: exact text/references for each statement.
* Dependencies: P01-T02 shares parser surface; implement coherently.

Original supplied goldens (PC-002), with the same source mapping as P01-T02:

```python
for suffix in ("Jr.", "Sr."):
    text = f"Contact John Smith {suffix} Repairs are due. [[Second source]]"
    expected = [
        {"text": f"Contact John Smith {suffix}", "citations": [], "unresolved": []},
        {"text": "Repairs are due.", "citations": ["Second source"], "unresolved": []},
    ]
```

<!-- rpi:phase id=P02 -->
## P02: Helper recovery

Context: C5-C6; bootstrap validates readiness but its error renderer does not.
Boundary: no redesign/copy churn; native recovery remains usable without helper.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Guard and exercise terminal renderer

* Targets: app.js h(), test_workspace_scripts.py, existing loading/briefing
  browser helper_bootstrap_check(), and src/api/README.md.
* Add typeof AsyncAction.handler === "function" to existing listener wrapper
  readiness check. Do not silently suppress the startup error.
* Unit: evaluate actual h()/startupFailed() with a minimal DOM, defined {} and
  non-callable handler; verify heading, alert, live status, native listener and
  reload execution. Also absent helper pass-through and healthy wrapper.
* Browser (PC-001): fulfill every injected helper evaluation with replay-safe
  `var AsyncAction = {};` (never const). The initial and recovery requests both
  evaluate in the same document; expect exactly two requests, stable after the
  existing wait, no pageerrors or /api/me. A non-callable variant may use
  `var AsyncAction = {handler: true};` under the same contract.
  Remove route interception before keyboard-triggered native reload so the
  original healthy helper loads. Assert visible terminal recovery, bounded requests,
  no /api/me, keyboard native reload, then real sign-in/account action behavior.
* Expected evidence: no pageerror and reload recovers into actual workspace.
* Dependencies: critique; no unresolved product decision.

<!-- rpi:phase id=P03 -->
## P03: Validation and local persistence

Context: C7-C8 and exact user commands. Original failure evidence is immutable.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Requested validation

* First targeted units: test_ai_statement_sources, CaseJourney dispatch method,
  test_workspace_scripts, test_loading_feedback, relevant API test_ai_tasks.
* Source-first PYTHONPATH includes this worktree's src/api/src/tests,
  src/core/src/tests and src/agents/src/tests; PYTHONDONTWRITEBYTECODE=1.
* Under flock -n /tmp/ama-rpi-heavy.lock, install -e src/core -e src/agents
  -e src/api into /tmp/mv then full unit discovery in core/API and loading/
  briefing browser with existing pinned axe. If busy, no waiting/polling;
  run targeted/static checks and report exact unmet broad validation.
* Strict checks in each component: /tmp/mv/bin/mypy,
  /tmp/mv/bin/ruff check ., /tmp/mv/bin/ruff format --check ..
* Check final changed files against scenario-manifest sources, update pins only
  if a pinned input changes. Current planned files are not pinned.
* Heavy generated results in new external directory; no retained-output cleanup.
* Expected evidence: exact commands, exits, skips, interpreter/import identities,
  browser outputs, diff check; no hosted/human acceptance claim.
* Actual evidence: 103 correction tests plus 11 manifest checks pass; mypy
  (157 core / 101 API source files), Ruff lint and format pass. Nonblocking
  heavy command exited 75 before setup/suites/browser; PID 679022 held lock.
  No broad/browser run, no editable mutation and no queue/retry/poll. Explicit
  source-first imports resolve core/API/agents to this worktree.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local commits and one Review

* Resolve gh api user, configure repository-local noreply email from id/login;
  use author/committer identity and exact required trailer.
* Commit implementation and original research/plan/details/changes evidence.
  Run one independent rpi-review for this correction diff against intake HEAD;
  preserve adverse findings and route them to later work, never repeat Review.
* Commit original Review, reconciled state and final evidence locally.
* No push, az, force-push, merge, or closing keywords. Publication and hosted/
  human approval remain separate; no publication gate bypass or receipt claim.
* Dependencies: completed P01/P02 and recorded validation.
* Expected evidence: clean local worktree, local commit IDs and original Review.
* Completion evidence: implementation commit
  2b37261be30e61cf8baf7494561def0607693e0d; original independent Review at
  .copilot-tracking/reviews/logs/2026-10-29/loading-briefing-hax-531-review-fixes-review.md
  is Complete / Residual work, no source defect identified. Independent 11-test
  regression run passed; RV-001/FU-001 retains full/browser validation and
  RV-002/FU-002 retains owner approval boundaries. Final local evidence commit
  follows; no further source changes or repeated Review.
