# Plan: #229/#230 renderer verification

* [ ] P1 Create `/tmp/venv-229-1105` (`--system-site-packages`), `pip install --no-deps -e` src/core, src/agents, src/api; verify `__file__` inside worktree.
* [ ] P2 Run existing modules: test_programme_screen, test_data_operator_screen, test_data_operator_ai_state, test_exception_register_screen, test_role_screens, test_role_screens_conformance; save exit code to file.
* [ ] P3 Run ad hoc Node VM harness (under /tmp, not committed) for #230 pager: page 1, middle, last page, Next at end, Prev at start, empty (total 0), single page; record button attributes and status text. Run #229 data-operator render with empty input.
* [ ] P4 Record results, hashes and exit codes in the changes file; remove the venv and harness.
* [ ] P5 Independent code-review, review file, commit with Refs and trailer.

Write surface: `.copilot-tracking/` only. No src/docs edits.

## Critique amendments (see critique file)

* Harness asserts and exits non-zero on mismatch.
* pip uses `--no-build-isolation --no-deps`, `PYTHONDONTWRITEBYTECODE=1`; clean egg-info and verify `git status --short` shows tracking-only changes.
* Empty #229 coverage: data-operator `render({id: "C-2"})` (existing test) and exception-register empty test.
* Report mocked-`h()` limits; no browser/AT/WCAG claim.
