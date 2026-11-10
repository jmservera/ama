# Issue 1258 C6 details (2026-11-09)

Phase details for `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-c6-plan.md`.

## Phase 1

Commit only the four prospective `.copilot-tracking` files. Author and committer use the repository-local privacy email; Conventional Commit with the Copilot trailer.

## Phase 2

`git fetch origin main`, record the SHA, `git merge --no-ff origin/main` with a descriptive message. In `server.py` and `store.py` keep both main's new routes and typed interfaces and this branch's ranking Blob wiring. Never replace a main file with an old whole file. If a conflict is not mechanical, abort the merge and report the exact conflict.

## Phase 3 (files)

* `src/core/tests/ranking_blob_fixture.py`: annotate `FakeBlobContainer.__init__(self, page_size: int = 100, mixed_case: bool = False) -> None`, attributes `blobs: dict[str, bytes]` (`_put` narrows the optional body explicitly: a missing body is a 400 response, as a real Put Blob without content would be refused; no assertion weakened), `meta: dict[str, dict[str, str]]`, `calls: list[tuple[str, str, dict[str, str], bytes | None]]`, `put_faults: list[int | str | tuple[int, str]]`, `get_faults: dict[str, int]`, `list_status: int`, `list_body: bytes | None`, `put_gate: Callable[[], object] | None`; `__call__` and `_put`, `_get`, `_list`, `requests` return `tuple[int, dict[str, str], bytes]` or the call list. Behaviour unchanged.
* `src/core/tests/test_ranking_archive_blob.py`: annotate `opened`, `assert_clean`, every `setUp`/test method with `-> None`, nested `run`, `no_token`, `page`, `blob`, `uncertain` helpers with concrete types.
* `src/core/tests/test_ranking_publication.py`: annotate `snap` (return `dict[str, Any]`); its module is in the existing `ignore_errors` override, which is not edited.
* `src/core/src/zava_forward/core/ranking.py`: annotate only the `snapshot` signature (`cases: Sequence[Mapping[str, Any]]`, `policy: Mapping[str, Any]`, `as_of: str` returning `dict[str, Any]`) so the typed test calls at lines 74, 232 and 304 and `snap` have a genuinely typed boundary; the body, behaviour and the module's override are untouched. Verified after the edit with strict mypy; if a caller mismatch appears, fix the annotation rather than suppress.
* `src/api/tests/test_ranking_publication_wiring.py`: run the project formatter, fix the I001 import order, and manually wrap the over-long docstring at line 361 (formatter does not wrap docstrings) with identical text; confirm the diff is whitespace, wrapping and import order only, then confirm `ruff check .` and `ruff format --check .` exit 0.
* Typing must come from real types (`Callable`, `Mapping`, `unittest.TestCase`), not `Any` or casts. If an annotation exposes a genuine mismatch, fix the source of the mismatch, not the error.

## Phase 4 (commands, each from the project root with the owned venv on PATH, capturing stdout, stderr and exit)

* core: `ruff --version`, `mypy --version`, `ruff check .`, `ruff format --check .`, `mypy`.
* api: the same three checks.
* core tests (no optional SDK): `python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner -v` from `src/core/tests`, and the project `unittest discover` for impacted modules if time-bounded.
* api tests (SDKs present): from `src/api`, `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_ranking_publication_wiring.py' -v` (the CI path form, run in the api venv with SDKs); the core Blob, publication and runner regressions run in BOTH the core venv (no optional SDKs) and the api venv (SDKs present), with narrower coverage documented if any module is not run; plus, after the merge, tests for main's changes in `server.py` and `store.py` (simulator controls 1313, photo 1315, chat validation 1320, lifecycle 1240) selected by the files main changed. Compare merged `server.py` and `store.py` hunks to both parents with `git diff` against each, including auto-merged regions.
* Record versions, counts, skips and exits. No SQL, browser or Docker.

## Phase 5

Changes file with before and after counts, one authored Review, state JSON, handoff `handoff-1258-c6.md` in the coordinator files directory, raw logs outside the repository with hashes.
