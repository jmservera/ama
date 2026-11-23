# Critique (one pass, final candidate plan) 2026-11-23

Verdict: proceed.

* Narrowing `changed_groups` too would break docs-only selection tests; keep it. Applied: separate function.
* Partial receipts keep current docs handling (hosted CI is their gate); only ordering of the candidate-changed check changes. Applied directly.
* Risk: docs moves now force a full rerun. Accepted: soundness over speed; reported by verify wording.
