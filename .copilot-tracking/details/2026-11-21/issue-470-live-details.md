# Details: issue 470 gate scan count

* `tools/rpi-checks.py` line 1634: `!= 87` becomes `!= 91`.
* `tools/test_rpi_checks.py`: fixture `range(87)` becomes `range(91)`; negative cases become `* 90`, `* 92`, and the serious-violation case `* 91`.
* Strictness unchanged: exact count, no skipped, no page errors, no serious or critical violation.
* Rejected: shared constant exported by the browser check (gate tool cannot import playwright-dependent module; larger blast radius).
