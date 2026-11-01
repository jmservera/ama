# Plan: #142 secret lifecycle slice (2026-11-01)

* [ ] P1 Inventory: add resident demo secrets; owner = repo-recorded owner (Juan Manuel Servera), pending confirmation.
* [ ] P2 secret_lifecycle.py: `rotation_timeline` model (old valid until delete; app refresh lag) + `rotation-simulate` command; `review-status` command (signed, no pending, not overdue).
* [ ] P3 Tests in infra/tests: inventory covers every vault secret in Bicep/scripts; no-downtime model passes, delete-first fails; review-status cases.
* [ ] P4 Docs: infra/README lifecycle section, docs/reference/log.md.
* [ ] P5 Validate: unittest infra/tests, ruff check, ruff format --check, mypy on touched file.

Critique (single pass): compatible. Do not claim live rotation or executed review; keep "Refs #142".
Details: tasks are the P-items above; no separate details file needed for this size.
