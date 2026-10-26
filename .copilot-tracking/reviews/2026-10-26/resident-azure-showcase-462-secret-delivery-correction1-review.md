# Independent review: secret-delivery correction 1 (issue 462)

The original review file is preserved unchanged. One independent read-only code-review pass, 2026-10-26T07:17Z, over the uncommitted correction delta on `a29a3849` and the SH-001 diagnosis.

Outcome: **Conformant**. No findings. Scoped to this delta; not a whole-issue pass.

## Reviewer return (unaltered, condensed to its verdicts)

* (a) O_NONBLOCK at resident_demo_secrets.py:75: a FIFO opens immediately and the fstat S_ISREG check rejects it; the test is bounded (daemon thread, join(5)).
* (b) The assertion at test line 246 is now a real check.
* (c) README line 3158 matches behaviour.
* SH-001 verified by reading code, no runner change needed: namespace_static_infra reinstalls the five editable projects from the live snapshot and runs the infra suite with that Python; a retained env with stale editable paths fails when run directly. Caveat: reusing an old env path relies on pip overwriting the stale .pth; a fresh output directory avoids that.
