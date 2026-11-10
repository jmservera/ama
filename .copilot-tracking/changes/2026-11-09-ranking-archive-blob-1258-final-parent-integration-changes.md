# Changes: final integrated #1258 parent candidate (2026-11-09)

Refs #1258, Refs #1259, Refs #136. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-final-parent-integration-plan.md` (amended by the critique). Native record; not the independent coordinator review. No source, infra, tool, workflow or manifest file was edited.

## Identities

* Prospective records commit `d93d8de139837c10890c9ee32b88ca16be44b669` (tree `ac27cd766c9dd212a98b4da072d3a190b49369b7`), made before either merge. Prior local head `99814198079c7c8fcd641497826986c706627b0f` (C6).
* Pre-merge check passed: remote topic `ac41cce5b1a7ded6a33fe5c57786affbca4783c0` and `origin/main` `2be660e9d290f95ff05fc5a56d6539768576732b` equalled the pinned ids and the worktree was clean.
* Merge 1 `2d4feeeb107cebe99bdb5f941c49b42d9e743d3d` (tree `ca815d486e6cb9c353b89bc9150c5fbb99e7ad1a`): ordinary `--no-ff` merge of ac41 by commit id; no conflict.
* Merge 2 `e827742c61b7f534cc824d69e263015c9b872f70` (tree `1909c39b068ed0086029dede28d27d0617a5eac7`): ordinary `--no-ff` merge of main `2be660e9` by commit id; no conflict. Main is merged because its documentation (cutover pack, reference index and log) belongs in the final document set.
* No rebase, amend, reset, force, discard or sibling code import. Author and committer `8036360+jmservera@users.noreply.github.com`, Copilot trailer. Ancestry of `99814198`, `03a7969c`, `cf8dbc28`, `fbf0a0ab`, `ac41cce5`, `2be660e9`, `d93d8de1` confirmed.
* The final record commit and frozen head are stated in the handoff.

## Bindings (git tree ids; raw output `identity-1.txt`)

| Input | Tree id at merge 2 | Equals |
| --- | --- | --- |
| `src` | `f0df7dc4246694b6828f14b352bcaa8ff9ab671a` | qualified ac41 and `136-combined-target-binding.txt` prospective/src |
| `infra` | `d94040329d5497aee252300972cb3c7497689d25` | ac41 and the binding file prospective/infra |
| `src/agents` | `237bf28b67cc78b0d88f1912d13a40b6b3e2739b` | main, ac41, C6 |
| `tools` | `74ad3cb586dbff7f08ed3ba78301b9596a31ca86` | main, ac41, C6 |
| `.github/workflows` | `29eb03ea759ea6717e334d8f0949915d5ba37a90` | main, ac41, C6 |
| `src/core/pyproject.toml` | `88598decb2dd7f571b0cb0f3f6a14d1b294c19b1` | main, ac41, C6 |
| `src/api/pyproject.toml` | `9b261f29fdcc99c84aafaad4a4705cfcd08c2355` | main, ac41, C6 |
| `docs` | `1191a55f6229e6f605b1d3207fa3c5d324bf1d0c` | main `2be660e9` |

* Merge-tree prediction `git merge-tree --write-tree ac41cce5 2be660e9` is `5f45a5491e9d2ecf4a846e6cba7f840d2c4f9a23` (equals the coordinator figure). Against it the candidate differs by 0 non-tracking paths.
* Diff against `ac41cce5` (non-tracking): only `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` (main's additions; +1481 insertions, 0 deletions in total including tracking, 43 files). Against `2be660e9` (188 files, +7812/-79) the non-tracking set is exactly the C6, #1259 and #136 source paths below. Against C6 `99814198` (145 files, +4812/-4).
* Tracking records modified or deleted relative to ac41, main and C6: 0 of 0 each. Original C6, #1259 and #136 records and both append histories (main's log and README additions, the children's records) are intact and additive.
* `git diff --check` exit 0; `git status` clean after the merges.

## Full manifest of non-tracking paths versus main (19)

`infra/README.md`, `infra/main.bicep`, `infra/main.test.bicepparam`, `infra/modules/containerapps.bicep`, `infra/modules/guard.bicep`, `infra/modules/storage.bicep`, `infra/tests/test_bicep_policy.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ranking_publication_wiring.py`, `src/core/README.md`, `src/core/src/zava_forward/core/ranking.py`, `src/core/src/zava_forward/core/ranking_archive_blob.py` (new), `ranking_publication.py`, `ranking_publication_runner.py`, `store.py`, `src/core/tests/ranking_blob_fixture.py` (new), `test_ranking_archive_blob.py` (new), `test_ranking_publication.py`, `test_ranking_publication_runner.py`. The rest of the 188 are tracking records.

## Union read at the actual files

* Flag off: `Store._ranking_archive` returns the local `ranking-archive` folder; flag on (`ZF_RANKING_ARCHIVE=azure-blob`) returns the Blob adapter and the docstring and code state it never falls back (store.py 243-251); Blob configuration errors are reported as `BlobArchiveError` status problems, local `OSError` separately.
* Bicep: `ZF_RANKING_ARCHIVE=azure-blob` and `ZF_RANKING_BLOB_CONTAINER` are added only when `rankingArchiveContainer` is non-empty; the container is conditional on `enableRankingArchive`; immutability policy only when days greater than 0 (default 0, no policy) and the pilot guard requires configured retention only in pilot with the flag on. No approved WORM, migration, delete-role narrowing or provisioning is implied; defaults are off.
* Runner status keeps unknown versus due computation (`unknown` gives `due=None`); direct publication and listing admission are separated by the tests named in the child reviews.
* This is source reading plus the independent reviews, not a new behavioural run.

## Checks

| Check | Command, env | Result | Evidence |
| --- | --- | --- | --- |
| Live Markdown links (the one input that changed on this candidate: main's new documentation) | `python -m unittest discover -s tests -p test_live_doc_links.py -v` from `src/core`, owned core venv (Python 3.12.3, no Blob or SQL extras) | exit 0, 2 tests OK | `/tmp/final-parent-1258/live-doc-links.log` sha256 `0900ad1ed253aa2f...`, exit file `9a271f2a...`, manifest `/tmp/final-parent-1258/SHA256SUMS` (sha256 `a62b95e6fc16e53d...`) |

## Reused evidence and its identity (historical child results, not CI of this candidate)

* C6: Core `test_ranking*` 127 (with and without SDKs), API wiring 35, project-root ruff 0.17.1 and mypy 2.4.0 clean on `99814198`, raw logs `/tmp/c6-1258-9Hvy6k/`; independent review approve, 0 findings (`independent-1258-c6/functional-findings-final.json`).
* #1259 / #1325: Core 146, API 36, lint, format, mypy; hosted CI 10 of 10 on PR head `c8cb220c` (merged `fbf0a0ab`, tree `2131877a`); independent review approve.
* #1327 / #136: infra 100, Bicep build and lint, parameters, pinned ruff; hosted CI 10 of 10 (API 15m36s, MSSQL 6m23s, Core 5m5s) on PR head `96f69163`, merged as ac41 with tree `81480e6c8...`, the independently qualified prospective tree; `combined-target-findings.json` approve, 0 findings, no new dependency check needed for the combination. The 136 run's C6 raw logs are by attribution only.
* Limits on reuse: the #136 PR head carried a different `src` tree and the #1259 head a different `infra` tree than this candidate, and the hosted merge ref was not observed, so the CI is evidence about each child's own identity and the recorded ac41 tree binding, not a run of this head. `src` and `infra` are byte-identical to ac41; the only added inputs are main's documentation.
* Doc-reading tests elsewhere were not rerun: their docs inputs equal main `2be660e9`, and no other input changed from a qualified identity. Not asserted as passing here.

## Not run and limits

SQL Server (including the 1292 campaign), browser (1288), Docker, `rpi-checks`, the full gate, any new hosted CI of this head, Azurite, Azure, model calls, deployment, role grants, WORM or retention activation, push, PR, issue, board. Fake Blob contracts are not Azure durability, WORM or live acceptance. Unmerged quality 1288 is excluded. Duplicate `NextMarker` is not asserted as a blocker. Whole #1258, #1259 and #136 stay open, `Refs` only.

## Correction budget

C6 spent; C7 to C10 four remain. This integration made no source change, is not a productive correction and resets nothing.
