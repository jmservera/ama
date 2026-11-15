<!-- markdownlint-disable-file -->
# Details: Issue #203 criteria 1 and 2

## Phase 1: checker

* Matcher: `mvp/` or `prototype/` not preceded by a word, `.`, `/` or `-` and not followed by `PoC` or `MVP`; `zavaforward_mvp` and `properwarm_mvp` as package tokens.
* Exempt: immutable/append-only/generated records and named regression guards or migration tools (explicit lists with reasons in the module).
* Path rule: archive tag `v0.21.0` in the first 60 lines or within 10 lines of the match. Package rule: only in listed dated documents.
* Links: inline and reference-definition targets, outside code, non-external, path existence only; scope is the diff against `origin/main`, working-tree changes and untracked files, or `--files`; `--all-links` is informational.
* Tests: `tools/test_check_legacy_references.py` with temporary git repositories.

## Phase 2: excalidraw sources

Map `mvp/zavaforward_mvp/{auth,server}.py` to `src/api/src/zava_forward/api/`, `token_store.py` to `src/orchestrator/src/zava_forward/orchestrator/`, other modules to `src/core/src/zava_forward/core/`, `mvp/web/` to `src/api/src/zava_forward/api/web/`, as in `update-architecture.mjs`. Verify each target exists.

## Phase 3: tag wording

Add "(archive `v0.21.0`)" to the live lines listed by the checker; dated documents keep their historical text.

## Phase 4: bookkeeping

Add a tool row to `docs/reference/README.md` and append one `log.md` entry.

## Phase 5: validation

`python3 tools/rename-zava-tests.py`; `python3 -m unittest tools/test_check_legacy_references.py`; `python3 tools/check-legacy-references.py --base origin/main`; `ruff check tools`; `git diff`.
