<!-- markdownlint-disable-file -->
# RPI Changes: Workbook fuzzy-union correction

## Metadata

* Task ID: issue-146-pr-512-fix-cycle-1
* Task slug: monitoring-146-pr512-fix-cycle-1
* Date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md
* Details: .copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md
* Start head: 5fc4ccc44a5ea15595560ea53e9941c1dd178fe6
* Refs #146; PR #512 fix cycle 1. No closing keyword.

## Execution Status

Declared scope: Full plan. Status: Complete locally. Completed: Research, Plan, P01/P02 and all task markers.
Remaining active-plan work: None. Automatic session remains at Follow-up with no child work selected.

## Approved Scope and Critique

Workbook two initial statements, one new unittest module with one method/two subtests, concise infra README explanation, and dated task evidence/state. No removals or generated delivery targets.
Single critique execution Complete / verdict Revise preserved. PC-001 rejected because its worker-only filesystem bans do not apply to parent; no comparable restriction exists in caller/parent instructions. External session logs and existing /tmp/mv tools follow parent guidance. No repeated critique.
No material divergence or user decision needed.

## Validation Intent

Red-before-green source regression; JSON parsing; five existing infra modules plus workbook module with compiler required and zero skips; isolated changed-file Ruff lint and format; unchanged downstream query suffixes and git diff --check.
Logs will use /home/azureuser/.copilot/session-state/eeb654cd-1167-4496-949a-fa4c88b183bd/files/.

## Completed Work

### P01-T01: Regression, source fix and documentation

Added infra/tests/test_monitoring_workbook.py: one unittest method with requests/availability subtests asserts each exact initial samples statement. It checks fallback schema, bare table and outer projection together.
Before modifying the workbook, ran `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s infra/tests -p test_monitoring_workbook.py -v`: exit 1, two assertion failures (one for each old form); workbook-red.log.
Changed only the initial samples statements in infra/monitoring-workbook.json, removing parentheses around the table pipeline so the union consumes a bare table and project follows union.
Same unittest command after fix: exit 0, one test with both subtests passing; workbook-green.log.
Compared parsed workbook to `git show 5fc4ccc44a5ea15595560ea53e9941c1dd178fe6:infra/monitoring-workbook.json`: both query suffixes after the first semicolon, all panel metadata and all other workbook content are unchanged.
Added a concise fallback/source-test-limit explanation to infra/README.md.

Initial static batch: JSON parse passed; Ruff reported E501 on the new comprehension (101 > 100), exit 1 before format check. Ran existing `ruff format --isolated --line-length 100` on the new module, then isolated lint passed. No unrelated formatting or Python changes. Final static batch used the corrected file.

### P01-T02: Scoped Validation

All commands ran from the repository root, against the task source changes on the starting head. No installs, cloud operations, deployments or remote writes.

| Exact command | Result | External log |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=infra/tests REQUIRE_AZ_BICEP=1 python3 -m unittest test_monitoring_workbook test_bicep_policy test_iothub_module test_container_contract test_governance test_secret_lifecycle -q` | Exit 0; 92 tests passed in 71.576s, zero skips | workbook-infra-tests.log |
| `python3 -m json.tool infra/monitoring-workbook.json > /dev/null` | Exit 0; valid JSON | workbook-static-final.log |
| `/tmp/mv/bin/ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_monitoring_workbook.py` | Exit 0; all checks passed | workbook-static-final.log |
| `/tmp/mv/bin/ruff format --isolated --line-length 100 --check infra/tests/test_monitoring_workbook.py` | Exit 0; one file already formatted | workbook-static-final.log |
| `git diff --check` | Exit 0 | workbook-static-final.log |

Combined shell groups used `set -o pipefail` and tee. Logs live under the external session directory declared above. Existing test compiler commands only compile Bicep locally. Full infra discovery/full publication gate/live Kusto not run or claimed.

### External Evidence SHA-256

* workbook-red.log: 82e5fe9d4eee466914b6f0b24ad929cf7d0339c32f9da67822513ee26b9619ac
* workbook-green.log: 83145283b6d64b4a3547f520032a21f502ee888b0cb3819bb35ff0c31063d344
* workbook-infra-tests.log: 0bd67a63276f138f88837968e32671b6c6da84945bfcea198d865978029aee3c
* workbook-static-final.log: ce04ce92b16073000b77c97a42c00b98b96305692d9d5ed4dcfa5a9ca9ea62d6

### P02-T01: Single Independent Review

Execution: Complete. Outcome: Conformant. Zero RV findings or local blockers.
Canonical record: .copilot-tracking/reviews/logs/2026-10-29/monitoring-146-pr512-fix-cycle-1-review.md.
Assessed precommit source/evidence delta from starting HEAD, not final-head publication. Reviewer independently checked regression, JSON, diff hygiene and all unchanged workbook suffixes/content; inspected the four original logs without redundantly rerunning expensive tests. Original critique and historical adverse operational findings preserved.

### P02-T02: Local Commit Preparation

Post-Review task paths inspected; no unrelated changes. gh api user freshly returned id 8036360/login jmservera. Configure repository-local privacy-safe identity for author/committer, stage the finite ten task paths and commit source/evidence with Refs #146 and exact Copilot trailer. A metadata-only finalization commit will record actual commit verification and completed state without changing the assessed source. No remote write.

### P02-T02: Verified Local Commit and Finalization

* `git config --local user.name jmservera` and repository-local privacy-safe email configured from the fresh gh response. Commit command also explicitly set both identity values; no global configuration changed.
* Finite `git add` staged workbook, test, infra README and seven current dated RPI artifacts only; cached diff and state JSON checks passed.
* Local source/evidence commit: 64096930e0c219184500fa00015d29f54e942c3f, `fix(infra): preserve absent-table workbook fallbacks`, exactly ten files.
* `git status --short`: clean after commit.
* `git log -1 --format=...`: expected privacy-safe author/committer, Refs #146, no closing keyword, exact `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer.
* This final metadata-only commit updates plan, details, changes and state with the actual outcome. No assessed source changes or repeated Review. Its final SHA is verified externally rather than embedded recursively.
* Final verification checks clean status, exact source equality with the implementation commit, ten finite task paths across both commits, state JSON and both commit identities/trailers. Any failure blocks the final success report.

## Implementation-Time Plan and Detail Updates

None; no approved intent changed.

## Pre-Review Reconciliation

Plan/details show P01 complete and P02 pending; source, regression and checks complete; no unresolved local blocker or implementation task. Handoff prose, validation and historical follow-up boundaries reconciled. Ready for exactly one independent Review against the task delta from starting head, including current untracked evidence/test. Review must not imply final-commit/publication assessment.

Post-Review reconciliation: P01/P02 complete with actual local commit evidence. Review original execution Complete / Conformant is preserved unmodified. No new findings, blockers or follow-ups; all historical operational boundaries remain explicit.

## Blockers

None.

## Follow-Up Items

No new work. Historical operational/privacy/runtime/cost findings remain open, not delivered by this correction.

## Publication Boundary

Local commit only. No Azure operations, latest.json edits, push or full publication receipt. Required full local/exact-head/hosted/human gates remain prerequisites before any later publication.
