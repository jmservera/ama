# Critique 2026-11-23 r2 (issue 2186), executed once

Verdict: proceed with the narrow change.

* Making `docs/presentations` inert would be unsound: secrets, legacy-reference and preflight checks read every tracked file. Rejected.
* A test-only addition is low value alone but pins the boundary the follow-up probed; keep it to one case.
* Do not claim speed gains for docs moves; do not claim end-to-end proof.
