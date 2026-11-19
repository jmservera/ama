# Details: issue #124 live audit, second pass

Phase 2: the note states method, retained evidence, per-criterion proven and unproven columns and the owner-only list. Counts must equal `probe.json`.

Phase 3: add an index sentence after the existing #124 entry in `docs/reference/README.md`; append a log entry at the end of `docs/reference/log.md`, leaving earlier entries untouched.

Phase 4: relative-link check, `git diff --stat`, scan of the evidence for `@` and credential patterns, rerun `test_discovery_*`. `rpi-checks.py --all` is not run; `src` is unchanged, so mypy and ruff are not applicable.
