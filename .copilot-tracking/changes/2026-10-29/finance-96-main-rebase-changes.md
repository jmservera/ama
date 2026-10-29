<!-- markdownlint-disable-file -->
# RPI Changes: finance-96-main-rebase

Date: 2026-10-29. Task ID / slug: finance-96-main-rebase.
Scope: full plan, P01/P02.
Plan: .copilot-tracking/plans/2026-10-29/finance-96-main-rebase-plan.md.
Details: .copilot-tracking/details/2026-10-29/finance-96-main-rebase-phase-details.md.

## Execution Status

P01-T01/P01-T02/P02-T01 complete; P02-T02 evidence commit pending.
Independent critique Complete / Pass, no findings.

## Commands and Results

* git status --short; git branch --show-current; git status --porcelain=v1 -b:
  clean docs/finance-96, no rebase in progress.
* git log -5 --oneline; gh pr view 510 --json state,isDraft,headRefName,baseRefName,title,body:
  local 373ab192, two finance commits; PR OPEN / draft, main target.
* gh api user --jq '{id,login}': authenticated 8036360 / jmservera.
* git fetch origin; git rev-parse origin/main:
  succeeded, main 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
* git diff --stat origin/main...HEAD; git log --oneline origin/main..HEAD:
  finance slice is 18 paths, 1995 insertions/7 deletions, e114bc45/373ab192.
* gh pr checks 510: old Source CI jobs passed; rubric conclusion failed,
  rubric/score pending; command exits 1 for failed check.
* gh run view 40582472769 --log-failed: conclusion reports daily workflow
  AIC guardrail exceeded, no source CI failure. No remote repair attempted.
* /tmp/mv/bin/python --version; python -m pip show ruff mypy zava-forward-core
  zava-forward-api: Python 3.12.3, Ruff 0.17.1, mypy 2.4.0; editables point at
  a different worktree. Explicit local PYTHONPATH required, no reinstall.
* git config --local user.email 8036360+jmservera@users.noreply.github.com;
  git var GIT_AUTHOR_IDENT; git var GIT_COMMITTER_IDENT:
  both use authenticated privacy-safe address.
* git rebase origin/main: reproduced real conflicts in six files:
  docs/reference/README.md, docs/reference/log.md, src/core/README.md,
  src/api/README.md, src/api/src/zava_forward/api/server.py and
  src/api/tests/test_role_endpoint_inventory.py. Initial exit 1 is retained.
* Manual resolution kept all main and finance documentation blocks; retained
  ai_registry plus form_review imports; retained chat/status plus form-review
  GET inventory entries. Existing POST finance inventory addition retained.
  Store private fields and narrow core typing override auto-merged correctly.
* git diff --check; git add <six resolved paths>;
  GIT_EDITOR=true git rebase --continue: passed; replayed commits c5bc0ea4 and
  11181fa8. No stash, skip, reset, abort, remote write or global side selection.
* git range-diff 09099ecd..373ab192 origin/main..HEAD: only expected additive
  integration context changed; metadata commit patch unchanged.
* git merge-base --is-ancestor origin/main HEAD: passed.
* git diff --exit-code origin/main -- .github/rubric
  docs/reference/research/retrofit-synthetic-data/scenario-manifest.json: passed;
  no branch-only rubric/manifest changes, main copies preserved exactly.
* git diff --exit-code 373ab192 -- <seven original 2026-10-27 finance artifacts>:
  passed; original research/plan/details/changes/critique/Review/state bytes
  preserved, including adverse outcomes.
* Python byte-prefix/subsequence assertions: main log retained byte-for-byte
  as prefix; all main reference/core/API README lines retained in order.
* Local import assertions with explicit PYTHONPATH: core forms, API server and
  agents chat resolve to this fin96 worktree, not installed sibling editables.
* From src/core with
  PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests:
  /tmp/mv/bin/python -m ruff check .; python -m ruff format --check .;
  python -m mypy: all passed, 112 files formatted, 165 type-checked.
* From src/api with
  PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests:
  /tmp/mv/bin/python -m ruff check .; python -m ruff format --check .;
  python -m mypy: all passed, 59 files formatted, 112 type-checked.
* From src/core:
  PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests
  /tmp/mv/bin/python -m unittest test_form_review test_form_staging
  test_finance_match_controls test_finance_signoffs test_grant_lifecycle_controls
  test_change_provenance test_document_rescan test_scenario_manifest
  test_dependency_rule -q: passed, 209 tests in 66.558s, 54 existing optional
  SQL Server skips (155 executed). Failure-injection rollback/rescan logging
  is expected test output, not test failure. Manifest validation passed with
  main's unchanged pinned manifest and the combined source.
* From src/api:
  PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests
  /tmp/mv/bin/python -m unittest test_form_staging_api test_finance_match_api
  test_role_endpoint_inventory test_dependency_rule -q:
  passed, 28 tests in 18.586s, no skips. Tiny fixture logs unavailable law
  store/rule checks; the checks remain explicitly Unknown, not silently passed.
* Full API discovery not selected or run. No heavy-lock probe/acquisition
  performed or claimed; focused modules cover the integration.
* git diff --check origin/main...HEAD: passed; no new legacy code paths.
* Five finance documentation relative-link/anchor assertions: passed.
  Changed-text conflict-marker and source/test placement assertions: passed.
* git fetch origin main; git rev-parse origin/main: refreshed base unchanged,
  356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7.
* git ls-remote origin refs/heads/docs/finance-96: remote unchanged at
  373ab1924b2a54338e09aa1693b969589dfe1688.
* gh api user --jq '{id,login}': authenticated identity reverified before commit.

## Plan and Evidence Reconciliation

All source integration and selected checks are complete; no finance behavior
was intentionally changed beyond additive replay. Original adverse review
bytes and current-main controls remain intact. No new tests, exemptions or
manifest/hash changes. P02-T02 commits the dated evidence before the single
independent Review; the later closeout commit records that Review without
source changes or another Review.

The commit skill's staged-change tool is unavailable in this CLI; use explicit
task-only staging and available Git staged inspection instead. Copilot
co-author trailer remains the final trailer as explicitly required.

## Implementation-Time Decisions

Requested rebase authorizes only local rewriting of these finance commits.
Keep main rubric/manifest, additive docs/configuration and all original review
evidence. No feature repair of historical RV-001/002.

## Validation Boundaries

No Azure, private data, hosted rerun, push, issue mutation or financial approval.
Full publication gate/receipt and fresh hosted CI are not claimed.

## Remaining Work

P02-T02 local evidence commit; independent post-implementation Review and
local final handoff. No local test blocker remains. Hosted rubric budget,
publication receipt and original Finance/Board/Review boundaries remain
external or inherited, not newly solved by this rebase.
