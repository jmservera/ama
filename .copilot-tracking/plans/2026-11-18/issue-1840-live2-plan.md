# Plan: issue 1840 live2

1. Rebase candidate, keep both sides of tracking/README conflicts (done in research).
2. Self-test: launch the worker with `-I -B -c` launcher that prepends the parent's sys.path, so isolation stays but no pip-installed checkout is needed.
3. Validate: probe tests, bare mypy, ruff; per-criterion table in changes.
4. Commit one clean commit; no push.
