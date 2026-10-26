<!-- markdownlint-disable-file -->

# Plan Critique: issue444-resident-feedback-preview

| Field | Value |
|-------|-------|
| Date | 2026-10-24 |
| Executed | yes, once, on the final candidate plan and details before any implementation |
| Reviewer | independent `rubber-duck` agent (separate context), read-only, given the issue, artifacts and real code |
| Verdict | Proceed with changes |
| Subject | [plan](../../../plans/2026-10-24/issue444-resident-feedback-preview-plan.md), [details](../../../details/2026-10-24/issue444-resident-feedback-preview-details.md) |

## Findings and direct dispositions

No finding conflicts with a confirmed owner decision, so none needed a user decision. All were applied directly to the details file; the critique is not repeated for this task.

| ID | Severity | Finding | Disposition |
|----|----------|---------|-------------|
| C1 | Blocking | Environment refusal list incomplete: `Ai` reads `AI_ENDPOINT`, `IDENTITY_*`, `AZURE_CLIENT_ID`; document store reads `ZF_DOC_*`; `ZF_DIGEST_DIR` (`store.py:61-66`, `ai.py:23-43`, `documents.py:202-209`) | Accepted. Prefix deny rule over the whole environment (`ZF_`, `AI_`, `IDENTITY_`, `MSI_`, `AZURE_`, etc.) plus one test per family |
| C2 | Blocking | `authority_for` dereferences `context["revision"]`; `current_context` can return `None`; malformed authority records can raise (`resident_decisions.py:468-499`) | Accepted. Shape pre-validation, all domain exceptions mean task denied (generic 403), tests for missing scope, design mismatch and malformed records |
| C3 | Significant | `_proc()` uses `setdefault` (mutates store); `appointment_status` can append to `_proc_context` (`procurement.py:77`, `appointments.py:164-174`) | Accepted. Read `store.data.get("procurement")`, run without a procurement context, whole-store before/after equality tests incl. absent procurement block |
| C4 | Significant | Lexical path containment can be evaded by symlinks or `ZF_DATA` | Accepted. Reject any `ZF_` variable (covers `ZF_DATA`), `resolve(strict=True)`, reject symlinks/non-regular files, tests |

## Verdict handling

Proceed with changes: all four findings applied. Remaining uncertainty is recorded in the review phase rather than a second critique.
