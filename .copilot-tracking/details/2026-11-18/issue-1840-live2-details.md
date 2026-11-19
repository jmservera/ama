# Details: issue 1840 live2

Edit only `SubprocessEngine.run` and a module constant `ISOLATED_LAUNCHER` in `src/api/checks/old_image_sql_probe.py`. The docker path and worker are untouched. Skip option rejected: the fix is small and keeps the test meaningful.
