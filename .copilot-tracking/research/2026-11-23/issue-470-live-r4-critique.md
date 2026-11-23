# Critique, issue 470 live r4

Executed once on the final candidate. Verdict: compatible.

* Scope is a `--markdown` flag on `rpi-gate-timing.py compare`; it adds no gate semantics and no receipt change, so tier FOCUSED holds (tools only, no src).
* The `--allow-tree-delta RUNNER_ONLY` rule limits tree changes to `tools/rpi-checks.py` and its test; this change touches only `tools/rpi-gate-timing.py`, so it must land outside a measured before/after window. Recorded as a note, not a blocker.
* Rendering must not hide NONCOMPARABLE: print reasons, exit code 3 unchanged.
* Claim limit: this makes recording easier; it does not prove criterion 4.

Disposition: all findings applied directly.
