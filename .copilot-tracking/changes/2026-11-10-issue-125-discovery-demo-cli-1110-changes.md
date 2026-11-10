<!-- markdownlint-disable-file -->
# Changes: issue 125 fixed synthetic discovery-demo CLI

* Plan: [.copilot-tracking/plans/2026-11-10-issue-125-discovery-demo-cli-1110-plan.md](../plans/2026-11-10-issue-125-discovery-demo-cli-1110-plan.md)
* Implementation opened (actual tool UTC): 2026-11-10T03:04:55Z or later, before any source edit. Pre-transition state persisted first; this record precedes edits.
* Base: main `a61bebe6b71e7f33560e2dee74b38834e4f55c0e`; branch `feat/synthetic-discovery-cli-125-1110`.

## Planned file changes (none made at the time of writing)

* `src/core/src/zava_forward/core/discovery_assistant_demo.py` (new)
* `src/core/src/zava_forward/core/__main__.py` (dispatch)
* `src/core/tests/test_discovery_assistant_demo.py` (new)
* `src/core/README.md` (existing discovery section only)

## Implementation results (actual tool UTC 2026-11-10T03:06:38Z at completion of validation)

* Created `discovery_assistant_demo.py` (module, fixed fixture, constructed EXPECTED constants, `run_demo`, `render`, `main`).
* Edited `__main__.py`: `discovery-demo` first argument dispatches; all other argv (none, `--version`) prints the version as before.
* Created `tests/test_discovery_assistant_demo.py` (14 cases incl. subprocess of installed package, expectation mismatch, repeatability failure, no env/open access).
* Edited only the discovery section of `src/core/README.md` (slice 4 paragraph and command); no 185 content.
* Critique amendments applied: DENY derived from readiness; env/open/home access patched in tests; full literal fallback text.
* Divergences: none from plan. Minor: shortened the `basis` string to satisfy E501; added a per-decision `note` that decisions are policy-only.

## Validation (unique venv `/tmp/zf125disc1110-venv`, editable install of this worktree's `src/core`)

* `python -m unittest discover -s tests -p 'test_discovery_*.py' -q`: 60 tests OK (includes all existing discovery suites and the 14 new cases).
* `test_version.py`: 3 OK; `test_dependency_rule.py`: 2 OK.
* `ruff check src tests`: pass; `ruff format --check src tests`: 232 files formatted; `mypy`: no issues in 286 files; `pip check`: no broken requirements.
* CLI: `discovery-demo` exit 0; `discovery-demo x` exit 2; no-argument and `--version` print the version.
* Not run (by owner direction): full or `--changed` gates, hosted CI, SQL/browser/cloud. No skips in the run scope.
