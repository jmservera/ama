---
title: Issue 96 r12 research, malformed batch visibility
ms.date: 2026-11-05
---

Dated 2026-11-05. Refs #96, parent #93. Intake head `94c7218055809dd6a52d23a21a2946d05adf0701`, tree `dcbce30aee8f83f976273adaaed2ab173fc95efa`, main and local parent `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Earlier records, the passed r11b receipt (historical, invalidated for any new head) and the interrupted failed r11 receipt are preserved unchanged.

## Evidence

* Independent review `review-96-r11b/review.md` (Request changes, one Medium) and `96-malformed-proposal-reproduction.log`.
* Source `src/core/src/zava_forward/core/form_review.py` `_proposals` (lines 219-228): the binding test reads `batch["schema_digest"]` inside one `try`; a missing key raises `KeyError` and the batch is skipped, even when `case_id`, `schema_id` and `schema_version` identify this draft.

## Finding and feasibility

Confirmed by reading source: a staged batch attributable by case, schema id and version but lacking `schema_digest` vanishes from `proposal_freshness`, with status `Evaluated` and no Unknown entry. This contradicts the r6 fail-closed contract for malformed linkage. I will confirm by a failing regression before editing source.

## Smallest fix

Split attribution: a batch is attributable when `case_id`, `schema_id`, `schema_version` all equal this draft's. Among attributable batches, a missing `schema_digest` key reports the existing `proposal-record-malformed` Unknown entry (batch id only, no raw values); a present but different digest stays excluded as a distinct binding; missing or malformed attribution keys (cannot establish association) stay excluded. No new abstraction, write, policy or approval.
