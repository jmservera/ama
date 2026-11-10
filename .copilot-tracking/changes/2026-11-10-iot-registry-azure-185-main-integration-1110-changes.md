<!-- markdownlint-disable-file -->
# Changes: #185 main integration (2026-11-10)

## Prospective declaration (before implement-start; source clean at E1 head)

Planned: one ordinary `--no-ff` merge commit of `origin/main` `06374dfcac47cf6bcce9e7b91f573e8565ab45e8` into the topic, no hand source edit, plus these dated records. Any conflict resolution is mechanical and preserves both intents. No new logic and no dependency change beyond what main contributes. Original C7, E1 and adverse records are untouched.

## Authority

E1 is spent, extension remaining 4, no E2 selected, no new grant. This task integrates and validates the selected E1; it is not a correction.

## Implementation (2026-11-10T14:24Z, after witnessed implement-start 14:23:38Z)

* Ordinary `--no-ff` merge of `06374dfcac47cf6bcce9e7b91f573e8565ab45e8` into E1 `105d479aec8f4b19705356c53bd9d554f14e577d`: no conflict, merge commit `01a5e6429966c1f80b56ecc22d903228885107ae`, tree `4c9bfbbc13962b38d864f49fc930a2972f24382f` (equal to the pre-merge `merge-tree` prediction). No hand edit, no rebase, reset, amend or force.
* Adapter blob `5add5e34d4d4ba8c96c0fa99e901344fdee5fe65` and test blob `954c8a206c9de919d0092751717fd97496124960` are identical to E1. `pyproject.toml` blob `1c2d73533df469686eb89eba90ecf343e184c323` parses with tomllib (extras `sql`, `blob`, `iothub`, `dev`); the `iothub` and `dev` pins are intact. The README keeps the adapter section and main's `discovery-demo` addition.
* Process note: `research-open` and `plan-done` were recorded in one call, 0.1s apart, after a single preflight, rather than one preflight per marker. Preflights were strict-unique and rc 0; no phase was backdated.

## Validation (own venv `/tmp/i185venv`, azure-iot-hub 2.7.0, six 1.17.0, ruff 0.17.1, mypy 2.4.0; raw logs in `ROOT/checks-185-main-integration-1110`)

| Command | Exit | Result |
| --- | --- | --- |
| unittest adapter, identity, provision, dependency_rule | 0 | 89 tests OK, 0 skips |
| Root `reproduce_functional_findings.py` | 0 | 2 tests OK |
| `ruff check .` | 0 | all checks passed |
| `ruff format --check .` | 0 | 237 files formatted |
| `mypy` (full Core config) | 0 | 290 source files, no issues |

Provenance: SDK from the venv site-packages; adapter from this worktree. Not run: full Core discover (earlier timeout, not a pass), API selector, full or `--changed` gate, browser, image build, hosted CI, any live Azure operation. No additional directly impacted caller found, so no extra selector.

