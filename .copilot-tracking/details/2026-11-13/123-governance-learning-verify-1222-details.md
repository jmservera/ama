# Details: Epic #123 verification

Commands (run from src/<pkg>, `env -u ZF_DATA -u ZF_TEST_MSSQL`, venv python, logs in /tmp/v123-logs, rc saved with `echo $? > file` directly after producer):

* core: `python3 -m unittest -v tests.test_<module> ...` for the 16 core modules
* agents: PYTHONPATH=../core/tests 10 modules (incl. fixtures)
* api: PYTHONPATH=../core/tests:../agents/tests 4 modules

Verification: `zava_forward.core/agents/api` `__path__[0]` inside the worktree src/. Record per-package ran/OK/skipped counts, explicit skip reasons, log sha256 and rc. Failures are recorded, never fixed (no src edits). Fallback if a module needs a missing sibling test path: add that path to PYTHONPATH only (never mvp).

## Critique revisions (rubber-duck, verdict Revise; all applied)

* Inventory adds core/tests/test_governance.py (protocol/benefits/release gates): core 17 modules, agents 10, api 4 (test_case_journey runs local node DOM harness only; no browser or network).
* Imports: run modules by bare name with PYTHONPATH set to the package tests dir plus sibling tests dirs (never mvp); verify module __file__ inside the worktree.
* Offline: PIP_NO_INDEX=1, PYTHONDONTWRITEBYTECODE=1; egg-info is gitignored; confirm git status clean of src changes.
* Record import errors and skips separately from OK counts; verify HEAD and src cleanliness first.
