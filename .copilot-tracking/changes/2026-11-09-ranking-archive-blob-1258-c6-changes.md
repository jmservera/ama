# Issue 1258 C6 changes (2026-11-09)

Refs #1258. Implements the plan after prospective commit `03a7969c5309b034dfe6e26114a4e86abb99dcf1` (research, plan, details, independent critique). Owner extension C6 to C10 (comment 6747925505): **C6 is spent** (source edited); **C7 to C10 remain, 4 unused**. C1 to C5 stay spent.

## Identities

* Prospective commit `03a7969c`, made before the merge and any source edit.
* Fetched `origin/main` `5c3b8b4bed4bef82b53b15274fdbbb27d9eaba74`; ordinary `git merge --no-ff`, merge commit `cf8dbc285e9cfe0ab6780826817513bbe67e5cf7` (tree `d69ee988fc0c1474c97d385df9871511e3034797`). No conflict, no rebase, amend or force.
* Merge preserved both intents: main's `simulator_admin` routes, `record_validation_refused`, `quality_evidence_gate` and `ComplaintsReceiver` typing in `server.py` and `store.py` are present, and the branch's ranking Blob wiring is intact.
* Final head and tree are recorded in the handoff after the implementation commit.

## Environment (owned, no global change)

`/tmp/c6-1258-9Hvy6k` (`core-venv`, `api-venv`, Python 3.12.3), editable installs resolving to this worktree. Core profile: `pip install -e ".[dev]"` (no Blob or SQL SDK). Api profile: `pip install -e ../core -e ../agents -e ".[dev]"`, which brings the declared `azure-storage-blob` 12.31.0 and `mssql-python` 1.15.0 through the api dependency. Pinned ruff 0.17.1, mypy 2.4.0 (compiled). Raw logs and SHA-256 manifests are outside the repo: `/tmp/c6-1258-9Hvy6k/{base,postmerge,final}/SHA256SUMS`.

## Baseline versus new profile (project config, run from project roots)

| Check | Baseline pre-merge (red kept) | Post-merge pre-fix | After C6 |
| --- | --- | --- | --- |
| core `ruff check .` | exit 0 | exit 0 | exit 0 |
| core `ruff format --check .` | exit 0 | exit 0 | exit 0 (226 files) |
| core `mypy` | **exit 1, 84 errors in 2 files** | exit 1, 84 | **exit 0, 279 files** |
| api `ruff check .` | **exit 1, 10 errors** (9 E501, 1 I001) | exit 1, 10 | **exit 0** |
| api `ruff format --check .` | **exit 1, 1 file** | exit 1, 1 file | **exit 0 (127 files)** |
| api `mypy` | **exit 1, 9 errors in 1 file** | exit 1, 9 | **exit 0, 203 files** |

The 84 core errors were 41 `no-untyped-def` and 43 `no-untyped-call` in the Blob fixture and its test; the api 9 are the same fixture reached through `mypy_path`. Main added no new finding.

## Source changes (typed, no suppression)

* `src/core/tests/ranking_blob_fixture.py`: typed `FakeBlobContainer` (`Response`, `Call` aliases, typed attributes and methods); `_put` returns 400 for a missing body.
* `src/core/tests/test_ranking_archive_blob.py`: annotated helpers and tests; typed fault-case list; no assertion changed.
* `src/core/tests/test_ranking_publication.py`: `snap() -> dict[str, Any]`.
* `src/core/src/zava_forward/core/ranking.py`: only the `snapshot` signature annotated (`Sequence[Mapping[str, Any]]`, `Mapping[str, Any]`, `str` to `dict[str, Any]`); behaviour unchanged. Required by critique finding 1.
* `src/api/tests/test_ranking_publication_wiring.py`: project `ruff format`, import order (I001), and a wrap of the over-long docstring (reference moved to a `Refs #1258.` line).
* No pyproject, workflow, override, ignore, `noqa`, `type: ignore` or cast change. The only `Any` uses are the signature annotations above.

## Targeted checks (demo tier, no blanket gate)

| Command | Env | Exit | Result |
| --- | --- | --- | --- |
| core `unittest discover -s tests -p 'test_ranking*.py'` | core-venv, no SDK | 0 | 127 OK |
| same | api-venv, SDKs present | 0 | 127 OK |
| core `test_priority_order.py` | core-venv | 0 | 142 OK, 65 skipped (opt-in SQL Server, not used) |
| api `test_ranking_publication_wiring.py` | api-venv | 0 | 35 OK |
| api `test_ranking_policy.py` | api-venv | 0 | 13 OK |
| api `test_simulator_admin.py` | api-venv | 0 | 27 OK |
| api `test_live_control.py` | api-venv | 0 | 34 OK |

The "hard links unsupported" stdout in the wiring test is intentional failure injection.

## Limits

* The fake Blob transport is a contract mock, not Azure durability, WORM, retention or live acceptance. No cloud, private data or identity use.
* No SQL, browser or Docker run; the 65 skips are not evidence. No blanket gate or hosted CI observed. Nothing pushed.
* Children 1259 and 136 untouched; no child test result adopted. Whole #1258 stays `Refs`.
