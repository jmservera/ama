<!-- markdownlint-disable-file -->
# Details: Issue #133 acceptance-criteria evidence audit

## Phase 2 test command

`python3 -m venv --system-site-packages /tmp/venv-133-1416`, then `pip install -e src/core -e src/agents -e src/api` with no dependency resolution beyond what is needed. Run `python -m unittest -v` on `test_aftercare`, `test_aftercare_intake`, `test_aftercare_store` from `src/core/tests` and `test_aftercare_screen`, `test_aftercare_served` from `src/api/tests` (with `PYTHONPATH=../core/tests:../agents/tests` for api tests as the repository guide states). Record per-module `Ran N tests`, `skipped=` reasons and the producer exit code. Check whether `test_aftercare_screen` needs a Node producer and record its exit.

## Critique amendments (see critique file)

* Execution: `unset ZF_RESIDENT_MSSQL`, `PYTHONDONTWRITEBYTECODE=1`; after installs run `git status --short` and remove only untracked build metadata produced by the installs; delete only `/tmp/venv-133-1416` (and any other `/tmp/venv-133-*` created here) before commit.
* AC4: separate the API payload from what `aftercare.js` renders (outcomes shown or not).
* AC3: claim limited to implemented safeguards; operational use is unobserved.
* FR-036: map each registry field (workflow scope, capability, prompt or options, source permissions, accountable reviewer, thresholds, abstention or fallback, enable state) to the `ai_registry` entry.
* AC5: inventory generated text and static JS strings separately and list denylist counterexamples.
* AC2: cite unknown-owner creation (`aftercare_intake.py:467`) and assignment (`673-691`).

## Phase 3 probes (read-only, executed from the venv with `python -c`, nothing written)

* AC5: call `neutral_text` with paraphrases such as "You'll save money", "this will cut your bills", "the tenant caused this", "resident is at fault" and record which pass.
* AC1/AC6: list `AftercareService._route` paths to show absence of a digital self-service intake and of a pack route.

## Phase 4 table format

For each AC: clause-by-clause breakdown, `file:line` implementation proof, test method names with the run result, verdict, and gate owner for any missing clause (assistive-technology test, evaluator role approval, DPO position, SQL/MSSQL evidence, model route and release evidence, human legal review). State that the coordinator ticks only criteria with verdict `PROVEN`.

## Phase 5

Independent `code-review` over the tracking-only diff; configure repo-local noreply email via `gh api user`; commit with the Co-authored-by trailer.
