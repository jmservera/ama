<!-- markdownlint-disable-file -->
# Discovery CLI checkpoint 440 phase details (2026-11-10)

Plan: `.copilot-tracking/plans/2026-11-10-discovery-checkpoint-440-1110-plan.md`.

## P1 environment

New venv under `/tmp/i440-disc-1110`, `pip install -e src/core` only (no network use by the product; pip may fetch nothing if build deps are cached, a failure is reported as not run). Print `zava_forward.core.__file__` with `env -i`; it must lie under this worktree `src/core/src`.

## P2 matrix (cwd `src/core`, `env -i PATH HOME=<scratch home> TMPDIR LANG`, `timeout`)

* D1 `python -m unittest discover -s tests -p 'test_discovery_assistant_demo.py' -v` (README command; 14 cases expected).
* D2 the other discovery suites: `test_discovery_assistant_boundary`, `_drafting`, `_evaluation`, `test_discovery_register`, `test_discovery_flow` (affected helper contracts).
* D3 `test_version` and `test_dependency_rule` in Core (package and import boundary).
* D4 CLI readback: `python -m zava_forward.core discovery-demo` twice from a scratch cwd; exit 0; byte-identical output; JSON parsed by a constructed assertion script that reads only the captured stdout: status `NOT_READY`, missing_count 10, `company_connection` DENY, every authority decision refused and `dispatched`/`attempted` false for `write_source_system`, `contact_resident`, `rank_properties`, `read_company_dataset`, `model_used` false, comparison `criterion_met` false and empty `human_result_pointers`, `approved_solution` false, `overall_passed` true.
* D5 CLI argument and no-arg boundary: no argument prints the version line (exit 0); `discovery-demo extra` and `discovery-demo --path x` exit 2 with the stderr message and no stdout.
* D6 side-effect boundary: run D4 under a poisoned environment (`ZF_DATA`, `ZF_*` and provider-like names set to non-existent or marker values, constructed, not real secrets) and compare stdout bytes with the clean-environment run; scratch directory listing before and after is identical; `strace -f -e trace=openat,connect,execve` is read for connect calls and for opens of paths other than the interpreter, stdlib and package (only if `strace` works; otherwise reported as not run).
* D7 static on the delivered files only: `ruff check`, `ruff format --check`, `mypy` per the Core configuration, if the tools exist at the pinned versions; a version mismatch is reported.

Manual-unavailable check: the output field `manual_path` is present and the demo runs with no model, credential or service (D4 under `env -i`).

Classification of outcomes: observed, skipped (with reason) or not run; a failure is kept with its log.
