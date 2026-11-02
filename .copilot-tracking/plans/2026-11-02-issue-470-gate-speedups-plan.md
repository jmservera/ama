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
