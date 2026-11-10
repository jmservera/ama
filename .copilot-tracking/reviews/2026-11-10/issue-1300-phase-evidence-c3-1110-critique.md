# C3 critique (2026-11-10)
Single critique, lead-performed against the research evidence; no separate critique subagent was run (not claimed independent). Verdict: proceed.
* Check must resolve symlinks so a symlinked issue directory pointing into the repo is also refused: covered by `.resolve()`.
* Must run before directory creation: confirm in code before edit.
* Residual: check-to-open race unchanged (recorded in C2).
