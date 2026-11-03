---
title: Issue 470 gate speedups plan
ms.date: 2026-11-02
---

Plan (one pass, owner-approved scope):

1. `--jobs` defaults to 0 (auto from CPUs, memory, cgroup); API unit tests run as up to 3 shards when 2 or more workers are admitted; shard rows are re-ordered to the contract order and the trusted matrix re-derives shards from the tree.
2. `selection.skipped` and receipt `skipped` record each skipped group with a reason.
3. `--fresh-images` toggles `--no-cache`; default reuses layers; receipt `image_cache` is verified (unknown value fails).
4. `base_relaxation` plus `clean_identity(reviewed_base=...)`: partial receipts only; fast-forward only; gated-ancestor or inert/disjoint paths; the gate tool, workflows, unmapped paths, changed paths and dependent projects block; `--exact-base` disables it; run-time still needs the exact base.
5. `--stack` (ordered PR heads, last is HEAD) recorded in the receipt and re-validated; `--stack-member` at verify.
6. Docs: `src/README.md` gate speed controls; coordinator agent policy text.
7. Tests: selection and skip records, shard partition and fail-closed layouts, required-check expansion and policy validation, row ordering, relaxation matrix, stack validation, full-scope and exact-base refusal.

Validation: `python3 -m unittest discover -s tools -p test_rpi_checks.py`, ruff and mypy on the two tool files, and a `--changed` selection dry run. The complete gate is not run (owner instruction).

Critique executed once against the final candidate plan: verdict accept. Findings applied directly: keep schema 4 with defaulted optional fields so old fixtures and fail-closed defaults (`fresh`, no shards) hold; block gate-matrix moves from relaxation; keep SQL and image builds serial. No conflict with a confirmed owner decision; no user decision required.

## Correction plan (2026-11-03)

Author-run critique note: the critique above was performed by the plan's author and is not independent. Independent review of PR #792 returned Pass with fixes; this correction pass (one pass, no further critique) plans: (1) block relaxation for moves read by universal groups, tooling, extras, markdown under `src/`, and for docs-only candidates; (2) fail-closed shard completeness guard from unittest discovery; (3) ancestor check in `--stack-member` and plain stack documentation; (4) stronger ordering and relaxed-path tests; (5) document resume, receipt format and image-cache policy, enforcing fresh images for full scope in verify; (6) correction notes in these artifacts. Validation: unit tests, ruff and `mypy --strict` only; the coordinator runs the complete gate.
