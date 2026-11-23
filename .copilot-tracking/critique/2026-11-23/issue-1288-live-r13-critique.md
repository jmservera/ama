# Issue 1288 r13 critique (executed once)

Verdict: compatible. Findings applied directly:

* Log only exception class name and raise site; never `str(exc)` (may carry connection strings).
* Response body and status unchanged so the existing UI wording test and human route stay intact.
* Do not touch the release gate or add a bypass; that would present non-actual-AI output as authority.
* Reuse the existing `http-error` log style and a shared helper for both handlers; no new module.
