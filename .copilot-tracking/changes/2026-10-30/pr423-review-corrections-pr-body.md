---
title: PR 423 proposed description replacement
description: Local coordinator handoff, not applied to GitHub
ms.date: 2026-10-30
---

## Private Blob result transport - Refs #360

Offline implementation and review corrections. Whole-issue acceptance remains
unproven; no Azure, deployment, actual sign-in or live transport was performed.

### Owner decisions retained

* DN1: private Blob and managed identity; no result tags, public Blob, SAS
  or shared keys.
* DN2: complete bounded paging, 48 KiB plaintext/page and at most 64 pages;
  explicit refusal rather than truncation.
* DN3: three earlier failures remain unknown historical transport failures;
  no resource retirement or deletion authority follows.
* DN4: production app roles remain manually assigned through Entra Enterprise
  App; no directory-admin grant or roster contents are included.
* DN5: controlled-worker image/run/integrity/completeness checks remain;
  independent signed attestation is deferred and unverified.

### Review corrections

| Thread | Correction |
| --- | --- |
| 4392465810 | Request offset 0 and length MAX_BLOB + 1 before buffering; reject overflow/changed length; replacement-race test confirms bounded bytes and temporary-job/secret cleanup |
| 4392465888 | Validate complete serialized head and every items wrapper; exact-bound, intermediate-page, escaping, max-count and round-trip regressions |
| 4392465933 | Current runbook uses includeResultBlob default false, separately approved container writer, private operator Entra list/read and routing; ciphertext remains under lifecycle/soft delete, not tag cleanup |
| 4426748172 | Historical run9 provenance below is not current-head gate evidence; current status and coordinator responsibilities are explicit |

### Integration and rubric

The local fix branch preserves remote score-only commit `32cc1f81` and main
`d986c4c4a1010b6a5c7ba6b00d2c452c4db8f089` without rewriting history.
Both KB append sequences, current-main source and trusted recorded score
are retained. No retired source, result-tag permission or old relay is restored.
The hosted PR comment reports **77/100 PASS**, baseline 77, at
https://github.com/jmservera/ama/actions/runs/41101368098.
This is not a fresh score for unpublished corrections. No scorer, scoring
rules, rubric floors or recorded grade is modified by the corrections.
The strict D1 extra-key rejection remains, not an invitation to alter grades.
Main advanced to `f168d079` during local validation. A read-only local
merge-tree is clean, but the candidate retains the explicitly requested
`d986c4c4` baseline. Current-main ancestry and a fresh complete receipt require
coordinator reconciliation; conflict-free mergeability is not gate approval.

### Provenance and gate status: committed pre-gate snapshot

Historical only: run9 at source `f30d958313e6bff051e300f290e7853203bb8067`
and base `b4d467cad84535ed106cffa1ae9aa303db7bfed2`, receipt SHA-256
`2a4ac82d97da0df9abfe356258694c96d645c8f86c64205f1d4bb090602897b9`.
It does not cover subsequent integrated heads or this correction.
The prior integrated candidate `f74b270d` had no successful full-gate receipt:
the first attempt refused ignored generated inputs and the clean retry hit
the shared-lock timeout. Those adverse outcomes remain preserved.

This committed description is prepared before the final clean committed-head
gate. The final gate is **pending at this snapshot**, not verified. The
coordinator must supplement it with the task's external final handoff, which
records full HEAD/tree/base, actual gate/verification exits, receipt or failure
logs and remaining publication gates. Never label this pre-gate document or
an earlier receipt as current-head verification.

### Remaining acceptance

Fresh full local receipt verification, independent exact-head publication
assessment, hosted checks/rubric and human review remain distinct. Live private
routing, real result sizes, managed-identity write/operator Entra read,
real jobs/roles, browser/assistive-technology acceptance and signed attestation
are not proven by offline tests.

No push or remote description/thread update was made by the local worker.
Coordinator owns publication, this description update and remote review-thread
disposition. No pull request is merged.
