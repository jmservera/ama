# Critique: 470 tools verification plan

Execution: independent rubber-duck, read-only, before any test run. Verdict: Revise. Dispositions:

* Locks: test_rpi_checks.py and test_rpi_phase_witness.py touch locks. Inspected: heavy_lock tests patch HEAVY_LOCK_PATH to temp paths or redirect os.open to a temp file (line 1698-1712); witness tests use per-repo temp locks. Accepted, no canonical lock expected; verify /tmp/ama-rpi-heavy.lock mtime is unchanged by the run.
* False success: test_tracking_retention.py is pytest style. Applied: run with pytest -p no:cacheprovider and require a nonzero count.
* Imports: test_check_demo_feedback.py needs zava_forward core and api. Applied: scratch venv with editable installs, verify paths inside the worktree.
* Bytecode: applied PYTHONDONTWRITEBYTECODE=1 on every command, check ignored files with git status --ignored.
* Command form: unittest discover -s tools -p <file> for unittest modules; rename-zava-tests.py run directly.
* Cleanliness: baseline git status taken before execution, compare tracked and ignored after.
