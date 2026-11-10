# Review: issue 954 C3 strict mypy on the photo-flag checker (2026-11-09)

Execution: one review of the final candidate after implementation (self-review; independent exact-head assessment and hosted CI remain required). Boundary: checker diff versus the merged main base plus the C3 tracking. Outcome: conformant for the checked scope, with one open validation gap.

## Findings

* Typing: the five hosted errors reproduce under the CI install profile and clear (mypy exit 1 then 0, 200 files). Only typed aliases, a typed callback and one real `int()` conversion were added; no `Any`, `cast`, ignore, config or CI change.
* Behavior: the dialog callback keeps append-then-dismiss; the aliases call the same constructors; HTTP 503/403 handling, assertions, negative control, overlay detector and quiet definition are not in the diff. The `int()` conversion is stricter for a non-integer result and is disclosed (critique B2).
* Open gap (blocking for a browser-pass claim, not for the typing result): the one nonqueued admission found the shared heavy lock held by a prior 1292 diagnostic, so the actual Chromium run of the composed checker did not execute. Prior C2 quiet observations remain historical and are not reused as fresh bindings. A later single admission is required before the browser claim.
* Merge: ordinary merge, no conflicts; final source delta versus the main base is the checker only. The shared `origin/main` ref has advanced since; the coordinator decides whether to merge it.
* Web guidelines: not applicable, no web UI file changed.

## Routing

Open work goes to a later user-selected task: one nonqueued browser admission on the frozen head (C4 only if a defect is reproduced), independent exact-head review and hosted CI. Original adverse outcomes and earlier reviews are unchanged.
