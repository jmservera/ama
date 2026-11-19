---
title: Issue 107 release-invariant classifier correction research
description: Original dated research for the single remaining High classifier finding on the old-image SQL probe at candidate 0b90a5d
ms.date: 2026-11-17
---

## Status

Opening artifact written before research-open and before any substantive source search. Validation against actual code is appended after that boundary.

## Scope

* Child branch `test/assistant-old-image-sql-107`, declared target `feat/assistant-107-integration` pinned 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4, opening candidate 0b90a5d667aea3df45a7f6536c027188602ba04e (tree 438a999102c873982625d3025ff62015698412f7).
* Diagnostic judge, directly coupled focused tests and README only. No application, store, policy, schema, dependency or gate change.
* Input: independent review of 0b90a5d, one High finding at `src/api/checks/old_image_sql_probe.py` 657-661 plus the missing later-snapshot revocation check (own evidence `c1-functional-findings.json`).

## Finding under validation

The refusal judge ignores an active release row whose `prompt_version` is the injected mutation, and audits the revoked capability for restoration only in `after_mismatched_restart`.

## Evidence boundary

No Docker socket and no SQL here. Only fake-driven unit tests, the labelled current-source SQLite self-test and static checks can run; none is actual old-image evidence. The immutable older image stays sha256:ad99bbb99df321f8d874b0df52ead4b3e24f4fb02c21a2245b278ea1a1e2cf78 with unknown Git provenance.

## Validation against actual code (after research-open, seq 2)

Read: probe `judge` and helpers (lines 445-760), tests `Judge` and `good()` (58-215), README judging paragraph (5979-5985).

* Confirmed: `refused` (probe 657-661) flags an active release only when `prompt_version != MUTATED`, so an active MUTATED row after the supported mismatch restart yields ACCEPTED. `MUTATED` proves the trigger only.
* Confirmed: the later revoked-release audit (679-681) reads only `after_mismatched_restart`; `after_remaining` and `after_larger` never inspect any release row.
* Confirmed: `release_rows` returns `None` for an unreadable snapshot but an empty list passes silently because of the `rows and` guard, so a lost row is not INSUFFICIENT.
* Fixture note: `good()` already holds the mutated row non-active in every snapshot except the pre-worker `after_provision` row; `after_mutation` carries a revoked status in the fixture, so only the real run exercises the active-after-mutation precondition (not a violation, not audited).
* Post-worker snapshots: `after_revoked_restart`, `after_mismatched_restart`, `after_remaining`, `after_larger`. Revoked capability audited in all four; mismatched capability audited in the last three, gated on the mismatch step having completed `ok`.
* Release identities are available from `after_provision` rows (`id` column); a new active row for a capability is also a violation, so the audit scans all rows of the capability and additionally requires the bound IDs to remain readable.

## Planning Readiness

Ready. Research disposition: executed. Fidelity: fake-driven judge tests and the labelled current-source SQLite self-test only; no actual old-image evidence.
