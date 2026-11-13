# Review: issue 107 changed-binding process candidate

Date: 2026-11-12. One independent post-implementation Review (`code-review` subagent, model `claude-sonnet-5.5`) of local commit `a56b995f6` (since amended to `cfab498810aa58dd5e6d04842a4de6d7967b2215` for finding 1). Execution: executed. Outcome: Approve with comments. Raw return preserved below (only the "What I checked" bullets are lightly condensed; findings are verbatim).

## Raw independent return

**Outcome: Approve with comments**

I found no correctness or vacuity problems. I ran the whole `SqliteUnleasedRevocation` class (7 tests) three times and all passed, in 20-31 s per run. `ruff check` is clean and `mypy` reports no issues on both files. The diff touches only the two test files under `src/api/tests`, so no production code changed.

**Findings**

1. **Low, formatting only.** `src/api/tests/test_assistant_release.py:1195-1197` leaves two blank lines before the new `stored_release` method inside `ProcessRaces`. `ruff format --check` flags this file, but the diff also shows reformatting of unrelated lines such as the docstring spacing at line 1 and `DependentPolicyRelease` at lines 35-51. The file was already unformatted before this commit, so the commit doesn't make it worse. I'd drop the stray blank line and nothing more.

2. **Low, variation is not checked in the changed worker.** `assistant_process_worker.py:52-53` applies the variation only when `spec["variation"]` is set. The test never confirms in the changed worker that the binding really differs from the original, for example by reading `runtime_binding` there. This is not vacuous. The assertions that the changed worker returns `[False, True]`, that the release is revoked, and that `invalidated["triggers"]` and `invalidated["fields"]` contain the expected trigger and field would all fail if the mutation had no effect. The control wave also proves the original binding works. So this is a robustness comment only.

3. **Low, run time.** Each new test spawns three OS processes and adds roughly 3-5 s. That fits the existing `ProcessRaces` style. The coordination is barrier- and file-based, with no sleeps that carry assertions, and I saw no flakiness in 3 runs.

**What I checked**

* Isolation: `vary()` mutates `assistants.RULES` and `assistants.REGISTRY` only inside the spawned worker process, so the parent test process and the fresh workers keep the original binding.
* Expected outcomes: the changed process denies the persisted release, disables the task and revokes the release with the right trigger and field; three unrelated capabilities keep their releases `active` with no `invalidated` entry; the fresh process with a larger allowance and later expiry still denies the held task with the same revoked record and no refill; the pool checks and provider-call counts of 1, 2 and 3 are meaningful.
* Duplication: distinct from the existing race tests (#1255/#1268/#1271).
* Honesty: comments say "Constructed runtime-binding differences... not an old image or a real serving change"; no overclaims in names or docstrings.

## Author routing (no second Review)

* Finding 1: fixed (one stray blank line removed; the commit amended; ruff, mypy and impacted tests rerun, `14-impacted-postreview.log`). The reviewer's claim that `ruff format --check` flags the file does not apply under the project configuration, where the file is excluded and the check exits 0 (`11`); the remaining unrelated formatting is pre-existing and untouched.
* Finding 2: accepted as nonblocking. The two mutation checks (`08`, `09`) show the assertions fail without a real variation or without persisted invalidation. Not added, to keep the test minimal.
* Finding 3: accepted; run time fits existing style.

Open material findings: none. Not Approved by a human, hosted CI or SQL evidence; those remain with the coordinator.
