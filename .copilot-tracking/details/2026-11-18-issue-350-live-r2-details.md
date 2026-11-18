# Details: issue 350 live parity proof, re-run r2

## Phase 2 files

* docs/reference/research/deployed-parity-live-r2-2026-11-18.md (note) and its folder (raw/, screens/, scripts/).
* docs/reference/README.md: one index row after the run 1 row.
* docs/reference/log.md: one append-only entry.
* .copilot-tracking/ research, plan, details, critique, changes, review, and rpi-sessions state.

## Phase 3 checks

* Relative links resolve; no credential, token or email appears in raw output (grep and exact-string scan of the sign-in id).
* git status shows no __pycache__ or caches; /tmp/state-*.json removed.
* Tests, mypy and ruff do not apply (no source change).
