---
title: Generator coverage review repair evidence
description: PR 312 findings, exact validation and publication evidence
ms.date: 2026-10-15
---

## Scope and State

Refs #167. Task `167-review-fixes`, slug `generator-coverage-review-fixes-167`,
parent `167` / `src-generator-coverage-167`. Existing PR #312, branch
feat/src-generator-coverage-167, base main. Initial worktree clean.

Research reused/Ready from caller findings, direct source/tests, public needs
inventory/provenance and issue #167. No new research artifact. Plan and
details ready; exactly one independent critique Complete/Pass, no findings.
P01/P02 complete. One post-implementation Review Complete, outcome Conformant
for these bounded repairs. Fix commit 0f1b556 pushed to the existing branch;
PR #312 updated, remote head verified. No blockers. This is not full issue
#167 acceptance; CI and owner merge remain separate.

## Evidence Pointers

* Plan: .copilot-tracking/plans/2026-10-15/generator-coverage-review-fixes-167-plan.md
* Details: .copilot-tracking/details/2026-10-15/generator-coverage-review-fixes-167-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-15/generator-coverage-review-fixes-167-plan-critique.md
* State: .copilot-tracking/rpi-sessions/2026-10-15/generator-coverage-review-fixes-167-state.json
* Review: .copilot-tracking/reviews/logs/2026-10-15/generator-coverage-review-fixes-167-review.md
* Original baseline evidence: .copilot-tracking/changes/2026-10-15/src-generator-coverage-167-changes.md

## P01 Implementation and Decisions

Approved repair uses the user's honest shape-only alternative: existing public
metadata has no complete issue registry. Remove routing_validated, expose
routing_shape_validated and issue_existence=not-assessed; no claim of actual
GitHub issue existence or child delivery. Missing or deferred needs remain open
gaps with CLI exit 1. Covered and delivered must agree in both directions.
Canonical partial child baseline retains exit 0 without declaring acceptance.

No private data, generated output, SQL, dependency manifests or forbidden
configuration paths are changed. No material divergence or new owner decision.

## Validation Commands and Results

All commands ran in /home/azureuser/source/ama-wt/issue-167 on the requested
branch. No dependencies were installed and no manifest was changed.

| Command | Result |
| --- | --- |
| `git status --short && git branch --show-current && gh pr view 312 --json state,headRefName,baseRefName,body && gh api user --jq '{id,login}'` | Clean initial worktree, required topic branch; PR OPEN against main; account 8036360/jmservera |
| `gh pr view 312 --json state,headRefName,baseRefName --jq . && gh issue view 167 --json body --jq .body && gh api user --jq '{id,login}' && tail -20 docs/reference/log.md` | Confirmed issue criteria, publication identity and append location |
| `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p test_generator_coverage.py -v && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy` | Nine tests pass; lint pass; format check finds one line needing reformat, so mypy not reached |
| `cd src/core && /tmp/zf164/bin/ruff format tests/test_generator_coverage.py && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q && /tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy` | One test file formatted; all 307 core tests pass in 61.008s, no skips; lint pass; 17 files formatted; mypy pass, 70 files |
| `git diff --check && git --no-pager diff --stat && git --no-pager diff -- docs/reference/log.md && git status --short && git ls-files 'docs/adrs/0006*'` | Whitespace clean; log entry appended, not inserted into history; only intended changes |

The full suite emitted existing ResourceWarnings for unclosed sensor-test input
files in test_sensor_backfill.py; the suite completed successfully. No warning
was introduced by the coverage tests and unrelated tests were not changed.

### Mutation and Regression Results (P01-T01)

* Unknown route `#99999`: accepted as syntax only, with
  `routing_shape_validated=true`, `issue_existence=not-assessed`, and no
  `routing_validated` field. This deliberately does not validate issue existence.
* Partial with deferred closure and no issues: open_gaps=["SN-01"]; JSON report
  retained, CLI exit 1, no stderr. Rationale is not falsely called owner approval.
* Covered with child closure: ValueError; CLI exit 1, stderr diagnostic, no JSON.
* Partial flipped to missing without changing its child route:
  open_gaps=["SN-01"]; CLI exit 1 with explicit JSON.
* Covered/deferred and partial/missing delivered are also rejected.
* Canonical v1.2.0 remains two covered/eleven partial, open_gaps empty, CLI
  exit 0 and byte-for-byte repeatable JSON. No inventory mutation.
* Reversed rows/issues and multiple missing IDs produce deterministic reports,
  including sorted open_gaps. Normal TemporaryDirectory() cleans test files.

### Documentation and Boundaries (P01-T02)

Core and pack READMEs, knowledge index and appended log now describe shape-only
issue checks, inverse consistency and open-gap exit behavior. Existing canonical
inventory, scenario manifest and provenance register remain unchanged. No
generator, SQL, live service, real AI/Azure or human acceptance evidence is claimed.

## Unmet Issue Acceptance

* [ ] Owner ratification of routes, proposed owners, scope and volume decisions.
* [ ] Complete generator seed/identifier/per-record is_synthetic conformity.
* [ ] Private-register reproduction, full profile/SQL-scale and real-platform
  evidence and human acceptance.

These remain outside the review repairs; Refs #167 does not close the issue.

## P02 Review and Publication

One Review executed Complete, outcome Conformant for the two findings; no
in-scope defects or material divergence. Full issue acceptance remains open.
Publication targets the existing feat/src-generator-coverage-167 branch and
PR #312 only. No new PR, main push, force push, merge or amend.

Final review commands:

```bash
git diff --check
git --no-pager diff -- src/core/src/zava_forward/core/synthetic/coverage.py src/core/tests/test_generator_coverage.py src/core/README.md docs/reference/research/retrofit-synthetic-data/README.md docs/reference/README.md docs/reference/log.md
git diff --exit-code -- docs/reference/research/retrofit-synthetic-data/needs-inventory.json docs/reference/research/retrofit-synthetic-data/scenario-manifest.json docs/reference/research/retrofit-synthetic-data/provenance-register.json
git branch --show-current
gh api user --jq '{id,login}'
git status --short
```

Pass: focused implementation/docs diff reviewed, append-only log preserved,
canonical metadata unchanged, required branch and 8036360/jmservera identity
confirmed; no unexpected changes.

Executed publication commands:

```bash
git config --local user.email 8036360+jmservera@users.noreply.github.com
git add -- src/core/src/zava_forward/core/synthetic/coverage.py src/core/tests/test_generator_coverage.py src/core/README.md docs/reference/README.md docs/reference/log.md docs/reference/research/retrofit-synthetic-data/README.md .copilot-tracking/plans/2026-10-15/generator-coverage-review-fixes-167-plan.md .copilot-tracking/details/2026-10-15/generator-coverage-review-fixes-167-phase-details.md .copilot-tracking/changes/2026-10-15/generator-coverage-review-fixes-167-changes.md .copilot-tracking/reviews/plans/2026-10-15/generator-coverage-review-fixes-167-plan-critique.md .copilot-tracking/reviews/logs/2026-10-15/generator-coverage-review-fixes-167-review.md .copilot-tracking/rpi-sessions/2026-10-15/generator-coverage-review-fixes-167-state.json
git diff --cached --check
git --no-pager diff --cached --stat
GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -m 'fix(core): report generator coverage gaps honestly' -m 'Refs #167' -m 'Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>'
git push origin feat/src-generator-coverage-167
```

Pass: commit 0f1b55607d503103b30c41e72ae930e4d51028a9 contains source,
tests, docs and all six repair RPI artifacts, 12 files total; push succeeded.

Executed verification and existing-PR update:

```bash
gh pr edit 312 --body-file .copilot-tracking/changes/2026-10-15/generator-coverage-review-fixes-167-changes.md
gh pr view 312 --json number,state,headRefName,baseRefName,headRefOid,url
git status --short
git --no-pager log -1 --format='%h %s%nAuthor: %ae%nCommitter: %ce%n%b'
git ls-remote origin refs/heads/feat/src-generator-coverage-167
git rev-parse HEAD
```

Pass: PR remains OPEN, base main, requested head branch; PR head, remote branch
and local HEAD all match 0f1b556. Worktree clean. Both author and committer
use 8036360+jmservera@users.noreply.github.com; Copilot trailer present.
PR body preserves Refs #167 and unmet criteria unticked.

### Tracking Closeout

This final evidence-only update marks all plan tasks complete and records
publication in state, details and this ledger. No source/test behavior changed
after the successful checks or the one Review.

Closeout command group:

```bash
git add -- .copilot-tracking/plans/2026-10-15/generator-coverage-review-fixes-167-plan.md .copilot-tracking/details/2026-10-15/generator-coverage-review-fixes-167-phase-details.md .copilot-tracking/changes/2026-10-15/generator-coverage-review-fixes-167-changes.md .copilot-tracking/rpi-sessions/2026-10-15/generator-coverage-review-fixes-167-state.json
git diff --cached --check
GIT_AUTHOR_EMAIL=8036360+jmservera@users.noreply.github.com GIT_COMMITTER_EMAIL=8036360+jmservera@users.noreply.github.com git commit -m 'docs: record generator coverage review repair delivery' -m 'Refs #167' -m 'Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>'
git push origin feat/src-generator-coverage-167
gh pr edit 312 --body-file .copilot-tracking/changes/2026-10-15/generator-coverage-review-fixes-167-changes.md
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/feat/src-generator-coverage-167
gh pr view 312 --json number,state,headRefName,baseRefName,headRefOid,statusCheckRollup
```

CI observations are not treated as local test evidence or owner approval.
No automatic follow-up work or merge is authorized by this closeout.
