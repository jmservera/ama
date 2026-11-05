<!-- markdownlint-disable-file -->
# Changes: issue 96 r9 diagnostic evidence

Refs #96. Evidence only; no source, tooling or test change. Added only `.copilot-tracking/research/2026-11-05/issue-96-r9-browser-failure-diagnosis-research.md` and this file.

Retained external diagnostics, none deleted: `/tmp/g96-diag-main-c6` (read-only c6 snapshot, with a `.venv` scratch directory created by the existing check), `/tmp/g96-diag-out` (`run.log` failed on my pre-created directory, `run2.log` the diagnostic, `cj-main-c6/`), `/tmp/g96-diag-run.sh` (runner). Original `/tmp/g96-c6-1105a` receipt, logs, snapshot (with its `__pycache__`) and images untouched.

Commands: `git archive c6d5a8f3c ... | tar -x`; `bash /tmp/g96-diag-run.sh /tmp/g96-diag-main-c6 /tmp/g96-diag-out` twice (exit printed 1 each: first FileExistsError, second the 1676.40625 assertion). Heavy lock held nonblocking for the run; no holder observed. No SQL, Docker, installs, network or cloud use.
