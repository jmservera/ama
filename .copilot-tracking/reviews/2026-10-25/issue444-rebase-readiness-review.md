# Issue 444 rebase and PR boundary review

Date: 2026-10-25. Executed once by an independent read-only code-review agent over `git diff origin/main...HEAD` (rebased onto 0245944a). Earlier reviews (2026-10-24 Conformant with follow-ups; lineage Conformant) are preserved unchanged.

## Outcome

Conformant with one Low follow-up. No defects. Review execution: yes.

## Finding

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Low | Only the grants file is re-read per request; the dataset copy (case and representative-authority data) is loaded once at start-up, so changing authority in the dataset needs a restart. Grant revocation is immediate. | Documented limitation for the synthetic disposable preview; routed as a later follow-up. No source change in this run. |

## Verified by the reviewer

Staff files unchanged vs main; one additive pyproject line; log.md adds only the #444 entry; resident source identical to the pre-rebase backup; reviewer ran the 45 resident tests (pass); identity, default-deny grants, allowlist projection, offers vs confirmed, write denial, host check, XSS and CSP; accessibility read from source only.

## Not verified by the reviewer

Browser check not run by the reviewer; fixture builder not read in full; resident_decisions and full appointment_status mutation path not traced; no full suite, lint or mypy by the reviewer (author ran them). No human screen-reader audit; Fluent 2 partial; no conformance claim.
