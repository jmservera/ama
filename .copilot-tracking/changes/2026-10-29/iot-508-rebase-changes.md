---
title: PR 508 current-main rebase changes
description: Commands, conflict dispositions and validation results
ms.date: 2026-10-29
---

Task ID: pr-508-rebase-2026-10-29. Slug: iot-508-rebase.
Scope: full plan P01-P03. Original evidence is preserved.

## Intake and planning

`git status --short`: empty. `git branch --show-current`:
feat/iot-consumer-110. `git fetch origin`: exit 0.
Intake head 09bd0a791e58acfcee9ddeb4f1eb05da173c62f5;
reviewed main 5653547507f3056f09a726a18516237728da5e5b.
`gh pr view 508 --json state,isDraft,headRefName,baseRefName,title,body`:
OPEN, isDraft false, expected branch/main. No PR metadata changed.
`gh pr checks 508`: exit 1, no checks reported.
`gh api user`: id 8036360/login jmservera. Repository-local privacy-safe
email set; no global config changed.

`/tmp/mv/bin/python --version`: 3.12.3. `pip show` confirms core/API editable
distributions point to this worktree. No package install required at intake.
Exactly one plan critique: Complete / Revise; PC-001 resolved by exact test
commands in details, no source changes or second critique.

## P01: Rebase

`GIT_EDITOR=true git rebase origin/main`: stopped (exit 1) at original
46a292de with append-at-EOF conflict in docs/reference/log.md. Removed only
conflict delimiters, keeping main's entire scenario entry then topic IoT entry.
`git add docs/reference/log.md && GIT_EDITOR=true git rebase --continue`
advanced to rubric conflict (exit 1).

At original 8a34cba1, 883ed609 and 19fb66a6, used
`git restore --source=origin/main --staged --worktree -- .github/rubric`
then `GIT_EDITOR=true git rebase --continue`. Intermediate exits 1 represented
the next rubric conflict, not a failed resolution. Final continue exit 0.
The two rubric-only commits became empty and were omitted; the correction
commit retained its implementation and dropped its rubric delta.
Rebased implementation head: 8f689555.

`git diff --exit-code origin/main -- .github/rubric docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`:
exit 0; manifest unchanged, including pinned sources, but its tests rerun anyway.
`git merge-base --is-ancestor origin/main HEAD`, `git diff --check`: exit 0.
`git range-diff 09bd0a79~10..09bd0a79 origin/main..HEAD`: exit 0, only expected
log-context/rubric changes. All eight substantive commits retained.
`git diff --exit-code 09bd0a79 HEAD -- src/api src/core/pyproject.toml src/core/src/zava_forward/core/synthetic/sensor_stream.py src/core/tests/test_sensor_stream.py`:
exit 0, exact original IoT bytes retained. README/index/log diff confirms
main scenario additions and topic entries both survive.

## P02: Validation

Commands below run after rebase with `/tmp/mv`, Python 3.12.3, existing
installed distributions. All exit 0:

| Directory | Command | Result |
| --- | --- | --- |
| src/core | /tmp/mv/bin/ruff check . | All checks passed |
| src/core | /tmp/mv/bin/ruff format --check . | 108 files already formatted |
| src/core | /tmp/mv/bin/mypy | 161 files, no issues |
| src/core | PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_sensor_stream test_sensor_consumer test_sensor_scenarios test_scenario_manifest test_historical_backfill test_dependency_rule -q | 81 tests in 25.111s, OK, no skips |
| src/api | /tmp/mv/bin/ruff check . | All checks passed |
| src/api | /tmp/mv/bin/ruff format --check . | 58 files already formatted |
| src/api | /tmp/mv/bin/mypy | 109 files, no issues |
| src/api | PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests /tmp/mv/bin/python -m unittest test_iot_stream test_sensor_ingestion test_dependency_rule -q | 71 tests in 45.680s, OK, no skips |
| repository | /tmp/mv/bin/python -m pip check | No broken requirements |

No full API discovery run: focused selectors suffice and no heavy-lock
admission was needed. No dependency installation, cloud access or private data.
Subsequent edits are documentation/evidence only, not executable inputs.

Final post-documentation checks: `git diff --check`, authoritative rubric/
manifest comparison and main-ancestor check all exit 0. Inline Python local
checker validated added documentation links/heading anchors, absence of conflict
markers, byte-exact main log prefix and unchanged IoT source; exit 0.
No executable failure required a fix or test amendment.

## P03: Review and commit

Single independent Review executed: Complete / Conformant, zero findings.
Original review:
.copilot-tracking/reviews/logs/2026-10-29/iot-508-rebase-review.md.
Reviewer independently verified integration, byte preservation and links;
static/test executions were assessed from the original command results, not
misrepresented as independently rerun. No source or test change follows Review.

Precommit `gh api user` reconfirmed id 8036360/login jmservera.
`git fetch origin main` exit 0: main still
5653547507f3056f09a726a18516237728da5e5b. Ancestry, authoritative main files,
whitespace and state JSON checks exit 0. No second Review.
P03-T02 commit is next. No push or Azure operations authorized or performed.

## Amendments and remaining boundaries

Local-judgment integration reconciliation: main's new two-stage guide said
no publisher/rate limiter existed, inconsistent with the preserved topic source.
Clarified the separate local opt-in SDK/pacing implementation versus unverified
live operation and unchanged scenario integration gates in core README, existing
research synthesis and index; appended the knowledge log without rewriting history.
No tests added/removed or source behavior changed. No material plan amendment.
Local checks do not establish hosted CI, live IoT/SQL acceptance,
publication receipt, owner approval or merge readiness on the remote branch.
Coordinator owns publication and subsequent hosted checks.
