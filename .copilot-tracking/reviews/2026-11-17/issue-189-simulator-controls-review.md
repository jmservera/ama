# Issue 189 review

Review executed once after implementation (worker self-review of the diff, `git diff` of two source files; not an independent exact-head review, which the coordinator still owes before publication).
Outcome: conformant for the assessed boundary; no material findings open. Tier FOCUSED.

## Checks

* Behaviour: `parse` now refuses `nobody`, `<owner>`, over-160-character and placeholder owner/approval text with `CONTROL_INVALID`; short real values (`o`, `r`) still pass. Admin `_clean` is unchanged and stays stricter.
* Fail-closed consequence: an existing control file with a template or over-long owner now decides INVALID for the simulator and receiver, which means no sending. This is the intended direction for a run control.
* Evidence: red run 7 failures on old code, green 172 + 42 tests; ruff and mypy clean (see changes file).
* Scope: no Azure, SQL, infrastructure or deployment edit; #1818/#1641 scope untouched.

## Routed follow-ups (not done here)

1. Live owned run, time limit and budget alert (issue 189 criterion 3, #146): needs Azure and owner action; unproven.
2. `check_capacity` counts messages not retried attempts; retry headroom is covered only by the 40,000-unit reserve (observation, unmeasured against live hub).
