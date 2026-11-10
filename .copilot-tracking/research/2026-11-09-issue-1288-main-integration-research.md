<!-- markdownlint-disable-file -->
# Research: #1288 ordinary main integration (after E7)

Task: issue-1288-main-integration (parent issue-1288-e7). Research disposition: executed (bounded, read-only git inspection). Planning Readiness: Ready.

## Identities

* Candidate start: 84b1a6d06a609aa7edca9400f1d42a912e36c68a, tree f92f27cd5bbab7aaee9a64c1cb17b51fcb45e5b4, branch feat/demo-recovery-quality-1288-1109, worktree clean.
* Fetched origin/main: cd687abadd9d18befe19089e65ba7373771b767f (PR #1328, ranking Blob archive and Bicep wiring). Merge base: 5c3b8b4be (the E6 main merge). Main is 228 paths ahead of the base; origin/main equals the PR #1328 merge commit, nothing newer at fetch time.
* `git merge-tree --write-tree HEAD origin/main` projects a clean tree 01ab114b3 with no conflicts. The projection is not semantic acceptance.

## Actual main delta since merge base (source, infra, tests)

* infra: README.md, main.bicep, main.test.bicepparam, modules/{containerapps,guard,storage}.bicep, tests/test_bicep_policy.py.
* core: ranking.py (typing only), ranking_archive_blob.py (new), ranking_publication.py, ranking_publication_runner.py, store.py (`_ranking_archive`, status and publish paths), README.md; tests ranking_blob_fixture.py (new), test_ranking_archive_blob.py (new), test_ranking_publication.py, test_ranking_publication_runner.py.
* api: server.py (one hunk in the `/api/ranking/publish` handler, new `ArchiveWriteUncertainError` branch), tests/test_ranking_publication_wiring.py.
* The rest is tracking state files, docs/architecture/cutover-evidence-pack.md, docs/reference README and log.

## Overlap with this candidate

* Both sides edited `server.py` and `src/core/README.md` in different hunks. This candidate's server.py edits are in the simulation lane, quality and endpoint code; main's is the ranking publish handler.
* This candidate edits ai.py, ai_transport.py, simulation_lane.py, assistants.py, assistant_release.py, sensor_consumer.py, sensor_view.py, ai_consumption.py, dispatch.py, web JS, and pyproject.toml of core and api. Main does not touch these. Main's store.py and ranking*.py are not touched by this candidate.
* Dependencies: the Blob archive module imports from core only, with Azure SDK imports expected lazy or behind the `blob` extra. Whether the core SDK-free profile still imports cleanly is to be verified by the complete Core profile, not assumed.
* The pyproject.toml files are unchanged on main, so the dependency and config inputs of the type, lint and format profiles come from this candidate only.

## Impacted-input conclusions (to be proven by running, not assumed)

* Ranking/Blob initialization and the store: run main's own ranking suites (core test_ranking_archive_blob, test_ranking_publication, test_ranking_publication_runner; api test_ranking_publication_wiring) on the merged tree.
* Quality call sites: the merged server.py and store.py must still satisfy the AI call-site inventory and role endpoint inventory (`test_ai_call_site_inventory`, `test_role_endpoint_inventory`) and the simulation lane suite.
* Earlier E7 results (deadline 7, lane 30, consumption, assistants, c7, e2, ai_tasks, sensor consumer) are historical at 2c2fc7298. They may be reused only for modules whose inputs are unchanged. ai_transport, ai, assistants, assistant_release and the consumption modules are unchanged by main, but the shared server.py and store.py are changed, so the lane, inventory, assistants and deadline suites are rerun cheaply where they exercise the merged App.
* SQL: main does not change SQL schema for assistants or sensor code. The ranking archive is Blob/local; whether ranking SQL tests exist is checked from the test files. No SQL admission unless a selected suite requires an SQL Server.
* Bicep: infra changed on main; this candidate has no infra edits. The infra policy tests are main's own and unchanged input, run only if cheap and without Azure.

## Limits carried forward

* Real-provider simulation route stays code-disabled; no provider call, credential, deployment or financial activation.
* Ordinary assistants post-fence suspension race, local-only socket shutdown (no remote cancellation) and the final SQL audit-persistence qualification remain open. Whole #1288 and actual-model demo acceptance are not claimed.
* Counters: E1-E7 spent, E8-E10 remain. An unchanged-source main integration does not consume E8.
