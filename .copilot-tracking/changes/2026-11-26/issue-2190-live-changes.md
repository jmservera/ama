# Changes: issue 2190 (Refs #2190)

Tier FULL (src edit), local commit only, no `--all` run. Planned: src/api/tests/test_rai_release_readiness_api_218.py (silence expected broken pipe); docs research note, index, log.

Done: test handler catches BrokenPipeError/ConnectionResetError; 218 suite 5 OK, no traceback in verbose output; ruff and mypy clean. Docs: [note](../../../docs/reference/research/issue-2190-live-20261126-note.md), index, log. Divergence: a first edit was made before implement-start and reverted, then reapplied after it (witness records a dirty-source qualification).

| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | Earlier notes plus residual noise reproduced and fixed |
| Fixed with a regression test | Proven for flakes 1 and 3; flake 2 repeat runs only (3 of 3), no deterministic test for a browser timing race | test_rpi_checks 133 OK; chat check 3 of 3 PASS; 218 suite OK |
| No check relaxed | Proven | Assertions unchanged |
| Hosted CI and complete local gate on this head | Unproven | Not run by instruction; nothing pushed |
