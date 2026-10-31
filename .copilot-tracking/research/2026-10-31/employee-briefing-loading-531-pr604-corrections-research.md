---
title: Issue 531 PR 604 review-thread correction research
description: Focused diagnosis of seven unresolved review findings after merging main
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Continue issue #531 on feat/employee-briefing-loading-531 and repair PR #604.
Audience: implementation and independent reviewers. Output mode: convergence,
preparing planning. Scope: seven named unresolved threads, requested main merge,
relevant API validation, non-force publication and thread disposition. Non-goals:
new UI behavior, rewriting historical outcomes, live verification, deployment,
secrets, issue closure or complete local gating.

## Research Parameters

Focused posture selected from the bounded caller request and supplied findings.
Resolved root: .copilot-tracking/research/2026-10-31/. No external research is
needed beyond authenticated GitHub issue/thread metadata. Existing parent
artifacts remain historical, including adverse Review and exhausted gate waits.

## Direction Controls and Extensions

Repository instructions govern branch, identity, evidence retention and test
commands. rpi-research supplies three-wave evidence protocol. Caller explicitly
authorizes merge/push/thread resolution and replaces the complete local gate
wait with API tests, Ruff, mypy and hosted CI. No human acceptance is implied.
No UI design/accessibility skill applies: the findings concern Markdown only.
No specialist lane is needed for this small, coupled investigation.

## Questions and Candidate Areas

* Q1: Are all seven findings valid, and do any require runtime changes?
* Q2: How should artifact destinations resolve without changing historical prose?
* Q3: Which current API commands validate the retained employee implementation?

Candidate inputs: six nested review/critique inventories, publication phase
details, tools/rpi-checks.py, src/api/README.md and src/api/pyproject.toml.

## Research Cycle Log

Cycle 1 Wider: fetched PR reviewThreads and issue acceptance state; inventoried
the seven affected artifacts and current test/CI instructions.
Cycle 1 Deeper: verified all 53 repository-root targets exist and all 53
destinations fail from their containing Markdown directory. Confirmed argparse
declares separate integer options --jobs and --lock-timeout. A nearby changes
record also omits the separator for --lock-timeout; correct only its typography.

Cycle 1 Contrarian: checked whether the inventories could intentionally rely on
root-relative resolution. They have no leading slash and standard Markdown
resolves them from the containing file, so that alternative fails. All findings
are documentation defects; runtime/test modifications would be unrelated.
Root-absolute URLs would bind evidence to a remote branch; file-relative
destinations work both locally and on GitHub. Preserve labels and adverse prose.

Parent synthesis: accept all seven findings, correct the nearby option typo,
and stop after one complete cycle because all named questions are answered.

## Evidence Log

* W1: PR #604 reviewThreads, retrieved 2026-10-31 via gh api graphql:
  https://github.com/jmservera/ama/pull/604. Seven unresolved threads: one CLI
  syntax finding and six file-relative link findings. No runtime bug is alleged.
* W2: https://github.com/jmservera/ama/issues/531, retrieved 2026-10-31.
  AC7 live verification remains unchecked; keep Refs #531.
* C1: .copilot-tracking/details/2026-10-31/employee-briefing-loading-531-publication-harness-phase-details.md:41
  uses --jobs3 --lock-timeout1800.
* C2: Six inventories under .copilot-tracking/reviews/{logs,plans}/2026-10-31
  contain 53 repository-root destinations incorrectly used as relative URLs.
* C3: src/api/pyproject.toml defines pinned development tools and configured
  Ruff/mypy scopes; src/api/README.md documents API test discovery.
* C4: tools/rpi-checks.py:2335-2336 declares --lock-timeout and --jobs as integer
  arguments. No parser change is needed.
* C5: .copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-publication-harness-changes.md
  has a related --lock-timeout1800 typography error; keep original failed
  attempts and results unchanged.
* C6: Focused loading test probe ran 2 tests successfully. The API distribution
  is not installed in system Python; application-backed validation needs
  installed project distributions, not a source-path workaround.

## Findings Mapped to Questions and Evidence

Q1: all seven are valid documentation findings (W1, C1-C2, C4).
Q2: preserve labels and change destinations using the file parent's relative
path to existing targets (C2); counts are 18/10/9 reviews and 7/4/5 critiques.
Q3: run loading, workspace scripts, case journey, AI tasks and release tests
with test-fixture paths only, plus configured API Ruff/format and mypy (C3, C6).

## Alternatives and Decision State

Prefer destination-only correction preserving visible workspace-relative labels,
historical verdicts and findings. Do not add runtime changes without a valid
runtime finding. Reject rewriting original gate outcomes or using closing
keywords for the still-unmet live criterion.

## Open Questions, Risks and Residual Uncertainty

No remaining research gap for the seven findings.
Hosted CI and live acceptance remain separate from local validation.

## Planning Readiness

Research disposition: executed (Complete). Planning Readiness: Ready.
No delegated work; all waves inline. Self-check: all questions answered,
53 exact targets checked, historical evidence preserved, no runtime edits.
