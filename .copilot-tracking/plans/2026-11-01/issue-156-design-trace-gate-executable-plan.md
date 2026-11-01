# Issue 156 plan: executable design traceability gate (2026-11-01)

Research: [../../research/2026-11-01/issue-156-design-trace-gate-executable-research.md](../../research/2026-11-01/issue-156-design-trace-gate-executable-research.md)

* [ ] P1 Add `tools/check-design-trace.py`: parse 74-row register, require issue link, journey link resolving to a defined reference or existing file, nonempty flow and design cells; classify design supplied vs NOT SUPPLIED; text and `--json` output; exit 0 pass, 1 blocked, 2 malformed.
* [ ] P2 Add `tools/test_check_design_trace.py` (unit tests incl. real register).
* [ ] P3 Document the command in the register section, index in `docs/reference/README.md`, append `docs/reference/log.md`.
* [ ] P4 Focused validation: unittest, ruff check, ruff format --check, mypy on the two files.
* [ ] P5 Critique (single, recorded in this plan's review), commit, push, PR `Refs #156`.

Critique (single pass, self-applied): the gate must not turn into approval; verdict `blocked` is the truthful current result; do not count `H`/`E` historical links as supplied designs (only a design cell without NOT SUPPLIED counts, and then still requires human review). Applied.
