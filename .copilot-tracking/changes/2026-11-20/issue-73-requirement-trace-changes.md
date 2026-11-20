# Changes: issue 73 requirement trace

Refs #73. Tier: FOCUSED (docs and tools only; no `src` change; no SQL, security, infrastructure or deployment scope). No Azure action; no live resource created.

## Files

* docs/reference/research/issue-73-requirement-trace-2026-11-20.md (new)
* tools/test_epic_73_requirement_trace.py (new)
* docs/reference/README.md, docs/reference/log.md (index and log entry)

## Validation

* `python3 -m unittest tools.test_epic_73_requirement_trace tools.test_epic_73_child_disposition`: OK
* `ruff format --isolated --line-length 100 --check` and `ruff check` on the new test: pass
* Cited src tests run per file (core 8+9+39+88 with 18 skipped; api 65): all OK
* mypy and src-ci jobs: not applicable (no `src/<project>` change). `rpi-checks.py --all`: not run by instruction.

## Per-criterion table

| Criterion | Proven for demo | Basis |
| --- | --- | --- |
| 1 Stabilization checkpoint (#440) | Unproven | Needs owner-recorded checkpoint |
| 2 All children closed or deferred | Unproven | #76, #79, #80 open; owner deferral or human signature needed |
| 3 Requirements trace to check or deferral | Partly proven | Ten requirements traced to passing tests (partial coverage stated); BG-011 deferral needs owner recording |

Adverse: no test cites FR ids, so the trace is a curated engineering mapping; a passing test shows only its slice.
