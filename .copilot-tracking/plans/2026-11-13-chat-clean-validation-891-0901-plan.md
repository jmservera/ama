# Plan: chat-clean-validation-891-0901 (2026-11-13)

Scope: validation evidence only. Admitted work: one focused run of the recovered module in an owned venv with installed distributions, full output and real exit status captured.

1. Record which tested files are equal between pins and which imported dependencies differ (done in research; no whole-module equality claim).
2. Build owned venv, install the three local distributions. README form is editable (`pip install --no-deps -e`); this attempt used a non-editable install, a deviation recorded in the changes file.
3. Run `python -m unittest test_ai_consumption_api -v` from `src/api` with helper-only `PYTHONPATH`, direct output to a file, capture exit.
4. Record origins (interpreter, module `__file__` probe, with the caveat that a probe does not prove each import of the run).
5. Stop on failure; no rerun, no repair, no generic suite.

Excluded: source/test/fixture edits, model calls, full gate, issue changes, fallback-attribution semantics.

Planned critique: independent subagent, one pass (see critique file).
