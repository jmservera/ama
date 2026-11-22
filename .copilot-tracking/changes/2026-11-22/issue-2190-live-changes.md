# Issue 2190 changes (2026-11-22)

Tier: focused (documentation and evidence only; no src, tool, workflow, dependency or Dockerfile edit).

Changes: research note docs/reference/research/issue-2190-live-20261122-note.md with evidence files, index and log entries, RPI artifacts.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | 2026-11-21 note; fixes in c9350f3a3b |
| Fixed with a regression test: flake 1 | Proven | tools.test_rpi_checks, 123 tests OK |
| Fixed with a regression test: flake 3 | Proven | 218 module, 5 tests OK incl. budget test |
| Fixed with a regression test: flake 2 | Unproven as deterministic test | 6 of 6 loaded runs pass; race is real-browser timing |
| No check relaxed | Proven by inspection | c9350f3a3b diff and passing rejection tests |

Not run: rpi-checks.py --all, hosted CI.
