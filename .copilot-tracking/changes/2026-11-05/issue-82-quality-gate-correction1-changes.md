---
title: Issue 82 quality gate correction 1 (2026-11-05)
ms.date: 2026-11-05
---

Original commit 8cdb1f676, its changes record and its review are preserved unchanged.

## Cache cleanup

* Manifest `/tmp/ama82-cache-manifest.txt` (external, 102 entries): `git ls-files --others --ignored` listed only `__pycache__/*.pyc` under src/agents, src/api, src/core (src and tests) and `.ruff_cache/*` under src/api and src/core. No symlinks, no unknown content.
* Authority: this run created the worktree and the caches (earlier test, ruff runs without `PYTHONDONTWRITEBYTECODE`); no receipt exists. Each file was resolved under the worktree `src/` and removed individually, then the emptied cache dirs. `git status --short --ignored` is empty. Later runs use `PYTHONDONTWRITEBYTECODE=1` and external ruff and mypy caches.

## Recovery trace (synthetic fixtures, reproduced)

* Accepted record, evidence blanked: handover refused by the gate; the existing `submit_quality` replacement supersedes it and the new record is accepted by an independent inspector. Existing path suffices. Regression added: `test_accepted_record_with_missing_evidence_recovers_by_supersession`.
* Submitted, Returned or Fixed record, evidence blanked: `return_quality` and `record_fix` work, but `record_fix` never rewrites checklist items so acceptance stays refused, and `submit_quality` rejects a replacement ("already has a quality record in progress"). Dead end, reproduced. Only reachable for stored non-conforming data, since `submit_quality` validates items.

## Owner question (one)

Should `submit_quality` be allowed to supersede an in-progress (Submitted, Returned or Fixed) record whose stored evidence is incomplete or unreadable, by a quality role, with an audited event and a new record that must be independently accepted? Alternatives: (a) that, narrowly; (b) let `record_fix` re-capture checklist evidence; (c) leave as a manual data-correction escalation. Evidence: `quality.py` submit_quality in-progress check and TRANSITIONS. The gate is not weakened meanwhile.

## Validation

`test_gates` 17 tests OK; ruff check and format check clean; mypy no issues in 266 files. Broad suites not repeated. SQL and optional-service skips from the earlier run remain unresolved. Full gate pending (#188 holds the lock).
