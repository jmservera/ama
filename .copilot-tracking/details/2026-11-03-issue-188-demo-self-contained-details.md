# Issue 188 phase details (2026-11-03)

## Slice 1

* `src/api/checks/sensor_handover_demo.py`: append `src/core/tests` to `sys.path` (relative to the script) before importing the fixtures; file-level `# ruff: noqa: E402`; docstring updated.
* `src/api/README.md` (Local handover demo): the run command needs only `src/api`, `core/src` and `agents/src` on `PYTHONPATH`; the unittest command is unchanged.
* Success: the demo exits 0 on a clean run and 1 with `--seam 1.5`; existing demo tests pass; behaviour and evidence label unchanged.
