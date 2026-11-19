---
title: Issue 79 live changes
ms.date: 2026-11-18
---

Refs #79. Tier FOCUSED: no source file under `src/` changed; `rpi-checks.py --all` not run. Evidence was gathered during Research before this record existed; the changes record was written afterwards and the witness `implement-start` therefore marks a documentation-only phase, not a source edit.

## Files

* docs/reference/research/issue-79-live-ranking-2026-11-18.md (new), its evidence folder (logs, driver scripts, job output, summary); the case-list screenshot was removed because it showed names and addresses.
* docs/reference/README.md (index entry), docs/reference/log.md (entry).

## Validation

* Core ranking tests 146 OK; API ranking tests 76 OK; orchestrator ranking tests 11 OK (logs retained).
* Live probe and throwaway-job outputs retained; mypy and ruff not applicable (no Python under src changed; evidence scripts are not packaged).
* Hosted CI not observed (no push by instruction).
* Azure: throwaway job and container deleted, listing recorded; ACR build probe failed with 403 and created nothing.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Same data and policy version give the same order | Proven (demo) | Two live reads identical, 443 entries, same snapshot_hash; in-job forward/reversed equal; tests pass |
| Policy file changes are versioned and hash-verified | Proven (demo) | Live content_hash equals repo hash; tamper tests pass; runner verifies |
| Named policy owner signs the first rule order | Unproven | Owner `to be named`, unsigned; shipped policy refused `approval_missing`; human act, cannot be proven for the demo |
| Ranking snapshot publication is scheduled and retained | Unproven (mechanics partly proven) | Create-only publish, idempotent repeat, verify ok with demo-only synthetic owner; no scheduler configured (live status `count: 0`), shipped entry point not deployable (ACR 403), no immutability policy on container |
