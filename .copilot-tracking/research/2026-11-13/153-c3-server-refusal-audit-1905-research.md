# Research: issue 153 server refusal lexical guard

* Rebase 017620d62e onto fa494a7aef succeeded cleanly (3 commits, no conflicts).
* AST scan of every `raise` in core `signoffs.py` and `workflows.py` (58 raises): no string literal contains gate, hold, provenance, trace, snapshot or envelope. Only `GateError(why)` (a class name, not message text) matches.
* Sign-off `why` lists (signoffs.py ~L117) are plain wording, banned-word free.
* Existing neighbouring guards use regex over source; a stricter AST-based guard is feasible with stdlib `ast`.
* No user-facing wording needs to change, so no existing test assertion is at risk.
* Planning readiness: Ready. Disposition: executed.
