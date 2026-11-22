# Plan critique: issue 2186

Executed once. Verdict: proceed.

* Finding: blanket docs/ relaxation is unsound for a full receipt if tests read the moved file. Disposition: accepted as residual risk matching the owner-set issue text and the existing partial relaxation; documented, not widened (src/ markdown stays blocked, code/tool/image invalidate).
* Finding: do not weaken identity checks. Disposition: applied; only the base-equality refusal changes.
