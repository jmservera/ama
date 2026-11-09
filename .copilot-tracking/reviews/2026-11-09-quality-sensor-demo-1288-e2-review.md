# Review: issue 1288 extension E2

Execution: one post-implementation review (code-review agent) over the working-tree diff against `c772364`. Outcome: no high-confidence defects found. Not an independent closure; the same independent reviewer closes the current defects.

## Result

* F1: no path found where a real `Ai` sends captured readings. One dead attribute `honours_dispatch_gate` on `Ai` was noted and removed; E1/C7/E2 tests were rerun (179 OK).
* F2: cursor logic sound (empty cursor distinct from none, advances by last id, short page completes, SQL placeholder order correct).
* F3: forecast writes nothing on the release side; adoption writes gated by observe.
* F4: no remaining deletion claim.
* Reviewer did not read `snapshot`, `authorize`, `continuity` line by line. The forecast purity test covers all related tables regardless.

## Residual and owner decisions (routed, not fixed here)

* Free-text chat and direct `Ai` use outside the captured-readings context cannot be classified without inferring provenance. Disclosed; owner decision needed (for example a lease-enforcing egress proxy or a provenance architecture).
* `sends_no_bytes` is a composition declaration about the sink, not data provenance, and is honour-system against hostile in-process code.
* Impact: a real Quality AI receives no captured IoT readings, so a separately authorised real-AI demo has no sensor-grounded flag and live acceptance criteria needing real-AI use of IoT values stay unproven. Mock and synthetic engineering paths still work.
* Late adoption after the first window is by id order, not newest (documented).
* New test file adds untyped-test mypy debt of the same class as existing test files.
