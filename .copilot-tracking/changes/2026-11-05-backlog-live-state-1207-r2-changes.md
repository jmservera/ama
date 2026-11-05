# Changes r2: positive, negative and Unknown activity (Refs #1207)

Original changes artifact is preserved as adverse history (it recorded omission from `--active` and `--active none` as demotion evidence).

* tools/backlog-sync.py: `--active` is positive evidence only; new `--inactive N,N` is the sole per-issue negative evidence; `--active none` removed; unlisted issues are Unknown and kept In Progress (listed as unverified); open PR and closed-issue precedence unchanged; overlap, non-open or unknown numbers exit before any write; invalid-format errors name the option and expected format without echoing the value.
* tools/test_backlog_sync.py: replaced the #90 demotion expectation (now: subset never demotes), removed the `hasattr` shape test, added explicit-inactive, open-PR-over-inactive, contradictory and non-open input refusal, and no-echo tests (11 tests).
* .github/workflows/src-ci.yml: existing "Local gate orchestration contracts and strict checks" step gains the unittest selector, the test in ruff check/format lists and `mypy --ignore-missing-imports` for the test and tool; paths filter gains both files. No job/check name or permission change.
* docs/reference/log.md: correcting entry appended.

Validation (base ead177ef9, origin/main re-fetched unchanged; PYTHONDONTWRITEBYTECODE=1, caches in /tmp):
* `python3 -m unittest discover -s tools -p test_backlog_sync.py` exit 0 (11 OK); `-p test_ci_affected.py` exit 0 (19 OK).
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/test_backlog_sync.py` exit 0; `ruff format ... --check` exit 0; `mypy --ignore-missing-imports tools/test_backlog_sync.py tools/backlog-sync.py` exit 0.
* `actionlint .github/workflows/src-ci.yml` exit 0, no output; YAML parse OK.
* `backlog-sync.py --active 'x;secret'` exit 1, message has no echo; `--inactive 5 --active 5` exits 1 before any gh write.
* Not run: rpi-checks gate and heavy suites (#188 lock), hosted CI, live board. Legacy E501 lines in the tool are unchanged scope; the tool is not ruff-linted in CI.

Closure: F1 closed by the evidence model and tests; F2 closed by the CI wiring.

Recommended coordinator prompt (#1204 owns the agent): "Reconcile the whole backlog at the start of every run and every scheduled check. Verify activity first: `tmux ls` for running `rpi-<N>` sessions and any frozen unpublished local candidate. Run `python3 tools/backlog-sync.py --active <N,N,...>` for issues with positive evidence, and add `--inactive <N,N,...>` only for issues you have individually confirmed have no session and no frozen candidate. Omission from `--active` is Unknown, not finished: the tool keeps such In Progress issues and lists them as unverified. Review the audit, then rerun with `--apply`. A worktree, missing upstream or empty tmux list is not proof of inactivity."
