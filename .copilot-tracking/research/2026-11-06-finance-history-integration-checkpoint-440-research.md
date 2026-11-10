---
title: Finance history integration checkpoint 440 research
description: Research for the post-integration #96 history-export checkpoint
ms.date: 2026-11-06
---

## Identity and admission

Local documentation RPI, same native session, new task `finance-history-integration-checkpoint-440`, branch `docs/finance-history-integration-checkpoint-440`, worktree `docs-parent123-history-checkpoint`, ignored-clean at intake. Pins re-resolved after `git fetch` on 2026-11-06 (approx 07:1xZ):

* Governance target `feat/discovery-assurance-integration-123` `7ed4a33f543bf7e1eed4aa351712734c743867b7`, tree `04d2e99a85ce26a59395d1ccfa60cae5a842308c` (equals HEAD; matches the brief).
* Finance source parent `feat/finance-integration-93` `4642b55fdbafec564b67803420439b91d7ea8ce1`, tree `e2628422d13ae87df3a6b7ecfdd12f24a4fc1052`, direct parent `0472fd5d5625bb610b5ac65ad177026953802830`. Subject "feat(core): include review history in Held exports (#1233)". Matches the brief; source has not moved.
* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, unchanged.
* The finance source parent commit is NOT an ancestor of the governance target (`git merge-base --is-ancestor` negative). Three separate pins; governance has `form_export.py` but not the #1233 history change.
* Issues #440, #96 and #93 are OPEN. No duplicate checkpoint issue is needed.

Admission facts (heavy resource released, #188 handoff finished, 5.9GB RAM) are coordinator-supplied and not re-verified. Observed locally: disk 99% used with 3.8G free; nothing deleted.

## Source read (local observed, static, from git objects)

Diff `4642b55fd^..4642b55fd` is 10 files, +280/-1: seven original RPI artifacts for #96 (r15, r16), `src/core/README.md` (+7/-1), `form_export.py` (+2), `tests/test_form_export.py` (+54).

* `form_export.BODY_KEYS` gains `"history"`, and `draft_export` passes `history=report["history"]`. The content hash is computed over `BODY_KEYS`, so history is integrity covered.
* `export_freshness` rebuilds the body from `BODY_KEYS`; a saved copy missing `history` raises `KeyError`, caught, and returns `Invalid` with action "Create a new held export from the working review." No backfill path exists.
* Status stays `Held`, `reviewed` false; actor is checked by `forms._actor`.
* Preflight evidence visibility is in `form_review._visible` (not changed by #1233, already in parent `0472fd5d5`): it checks prior and new evidence of every history event, cited documents, digests and attachments against the case, so unreadable historical evidence yields `Unavailable`. This is attributed to the earlier integrated parent, not to #1233.
* Tests added: `test_export_carries_ordered_detached_review_history` (empty history, ordered decisions accept, correct, reject, accept; equality to the stored history; detached copy; deterministic digest; digest changes on newer review; stale after a newer review) and `test_history_is_integrity_covered_and_legacy_copy_is_invalid` (legacy without history, reordered and truncated history all `Invalid`; intact copy `Current`). Both loop over the JSON and SQLite stores.

## Document identities (local observed, equal on governance and main)

| Document | Version and status | Blob |
| --- | --- | --- |
| BRD | 0.21.0 draft | `34d88395de861e9799eb9e24121a21c92c7a5adc` |
| PRD | 0.21.0 in-review | `c788b917bafaede215f326f0efc71e071a687f1c` |
| ADR 0003 | accepted with owner amendment | `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| ADR 0006 | accepted | `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review are not approval. Requirement joins use document-qualified IDs: PRD FR-040, FR-042, FR-043, AC-048, AC-050, AC-054 as in the earlier finance records (read in the eleventh pack; re-check wording at write time), and BRD NFR-002 (immutable versions, retained prior versions) as related context. Earlier #1225 scoped finance checkpoint is historical and unchanged.

## Remaining criteria (from live issue bodies)

#96 unchecked: approved versioned schema per form; reviewed export never submits or implies eligibility; source, schema or rule change marks only dependent proposals and approvals stale. Checked: candidate values with provenance; accept, correct or reject preserving prior values and reviewer; field-specific validation. #93 unchecked: stabilization checkpoint before epic closure, child features closed or deferred, no automated path submits or approves. Checked boxes are the owner's records, not re-adjudicated here.

## Evidence not observed here

Child `abeb022ba` FULL receipt, 205-row ledger, SQL 285 tests with one JSON-only skip, browser observations, vulnerability reports (zero fixable; 39 unfixed, 37 High and 2 Critical, retained per image) and hosted checks are coordinator-supplied or issue-comment evidence, source qualified to the child, and not accessible by path in this cycle. The FULL receipt is not an exact-head receipt for `4642b55`; tree equality with the reviewed child is an equality observation only. No tests are run in this cycle.

## Findings

No new defect or necessary refactor confirmed by static reading. Known limits: history evidence is synthetic-data only; history is field review, not Finance pack approval; the hash is not a signature; unsupported real-data, named schema, DPO, Legal, assistive-technology and Azure evidence are absent. Open issue search for form export history found only #96 and #80 (existing owners).

## Planning readiness

Ready: one pack section, README paragraph and log entry, with a classification table, document-qualified traceability and gate effects.
