# Issue 1830 live details

P1: `--preflight` is a repeatable argument in the mode group. `preflight_unit(root, value)` reuses `extra_selector`, requires a tracked `src/<project>/tests/<module>.py`, runs `python -m unittest -v <selector>` with `test_paths` PYTHONPATH in `src/<project>`; parses `Ran N tests`; N==0, skips, or nonzero exit fail closed. No receipt, lock or output dir; banner states "preflight, not a receipt".
P2: tests for rejection of malformed selector, untracked module, zero tests, pass path, and parser not requiring --base.
P3: README subsection under Local RPI gate.
