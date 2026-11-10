# Research: align #107 test candidate onto final main (continuation)

Task `assistant-release-integrity-107-align`, parent `assistant-release-integrity-107` (candidate 4aa717009d2a0c785b66a2426ff2ba38f31a658f, base add72cc90). Research disposition: executed (git and gh read only).

## Findings 2026-11-07

* origin/main is 312fa3dcc4866deadf51336f840954852f0ec061 (fix(employee) #1245, Refs #891), one commit ahead of the candidate base add72cc90. The owner's "891312fa3dcc" does not resolve as an object; it reads as "#891" followed by the 312fa3dcc hash, which is what main is.
* Rubric run 42361331168 (Capstone Rubric Scorer) targets head 312fa3dcc and was in_progress at 2026-11-07T09:5x. It may add a score-only commit that moves main; wait is bounded and the base is refetched before freeze.
* Candidate touches only `src/api/tests/test_assistant_release.py` and `.copilot-tracking/`; #1245 is employee UI/tests, so a conflict is not expected.
* Formatter: to be established from the repository configuration (see plan Phase 2), comparing baseline file with the candidate's added block. No inference without running the configured command.

## Planning Readiness

Ready. No production change, no push, no full gate, no SQL, images or scanners, no heavy lock.
