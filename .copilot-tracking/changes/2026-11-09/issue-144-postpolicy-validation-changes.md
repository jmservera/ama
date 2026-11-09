# Changes: issue 144 post-policy validation (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09/issue-144-postpolicy-validation-plan.md`. Source and tests: no change. Only these records are added: research, plan, details, this file, the review and the state file for `issue-144-postpolicy-validation`.

## Observed results (run 2026-11-09 from `src/agents`, `PYTHONPATH=$PWD/tests:$PWD/../core/tests`, venv `/tmp/c1venv`)

| Check | Result |
| --- | --- |
| `python -m unittest test_queue_azure test_worker test_dispatch test_dependency_rule -v` | `Ran 49 tests`, OK, exit 0, zero skips (no `skip` text in output) |
| `python -m unittest test_queue_azure -q` | 24 tests OK |
| `python -m unittest test_queue_azure.RequestDateTests -v` | 3 tests OK, exit 0 |
| `ruff check .` (0.17.1) | all checks passed, exit 0 |
| `ruff format --check .` | 43 files already formatted, exit 0 |
| `mypy` (2.4.0) | no issues in 47 source files, exit 0 |
| Negative check on a temporary copy outside the repo with the `x-ms-date` line deleted | `QueueError: Queue receive failed with status 403`; `RequestDateTests` FAILED (errors=1), exit 1; the copy was deleted and the repository source is unchanged |

No bare `discover` was used. No Azure credential, token or network request was used: the tests use the injected transport.

## Target-base evidence

| Item | Value |
| --- | --- |
| HEAD at validation | `63d7f8c180ee995121144cf593e8eca7cb94bd4d`, tree `f08a112691ed6658a881f932f1ca2f3f71396837` |
| Current `origin/main` | `9814cf6b236be1f2e86c4401973b8e834be927bc`; previous base `b46a9ad9`; one main commit (#1301) in between |
| Main delta in source, tools, infra, workflows, dependency manifests | none (docs, policy, `src/README.md` and tracking only) |
| Overlap with candidate diff | `docs/reference/log.md` only (both append) |
| `git merge-tree --write-tree HEAD origin/main` | exit 0, tree `985d09b2892aa3aec8b634ee922f9e6ba4823e09`; `src/`, `tools/`, `infra/` and workflow paths identical to HEAD |
| Old remote head `1a9616d4e9ab89d93a72204d82ee26c70baee06c` | ancestor of HEAD (80 commits); also merges cleanly into main; fetched, not moved |
| PR 1141 | open, target `main` (unchanged), mergeability reported `UNKNOWN` by GitHub |

Because the merged tree has the same source as HEAD, the results above also describe the source that would result from merging current main; this is inference from the identical paths, not a separate run on a merged checkout.

## Deviations

None. No amendment to the plan, no source change.
