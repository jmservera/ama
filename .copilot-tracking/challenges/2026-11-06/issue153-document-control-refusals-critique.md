---
title: Prospective critique and dispositions, issue 153 document-control refusals
ms.date: 2026-11-06
---

* Critique executed once, before implementation, by an independent read-only rubber-duck agent against the research, plan, details and the source/test files. Original findings are preserved verbatim below; dispositions are mine.

## Original findings (verbatim)

1. Blocking, impossible next step. The not-due copy says to check the due date in the retention list, but that list excludes documents with missing triggers or future due dates (`doc_controls.py` L265). Replace it with an actionable check that does not depend on that list.
2. Significant, hold authority is ambiguous. "A real hold needs the Legal delegate's decision" immediately follows release wording, implying a release decision that the evidence does not establish. Separate the existing synthetic placement label from release recording; do not imply release permission.
3. Significant, retention wording overclaims. "How long it must be kept" presents synthetic placeholder periods as authoritative, and "retention trigger" remains unexplained. Say the period is a demonstration value and explain the start date plainly. The recipient is already a programme manager, so "a programme manager can view it" adds no useful direction.
4. Significant, regression coverage is incomplete. The planned not-due test does not explicitly cover both missing and future trigger branches, blob preservation, audit-chain integrity or the due-date boundary. Test both branches and unchanged records, blobs and audits; verify due deletion still succeeds. Tie lexical assertions to the actual refusal literals and confirm restoring either old message fails.
5. Minor, documentation scope risks overclaiming. Removing `doc_controls.py` legal-hold wording wholesale from the unaudited list could imply all its hold wording was reviewed. Identify only the two refusal messages as covered; retain the resident-record path and other wording as outstanding.

Verdict: Revise; the proposed next action is incorrect and the authority wording needs clarification.

## Dispositions

| # | Disposition | Action |
| --- | --- | --- |
| 1 | Accepted. Verified against `retention_due` (lists only due records with a trigger). | Next action now points to the case closing date or recorded retention start date, not the list. |
| 2 | Accepted. | Hold copy says the system only records the hold and its release, quotes the existing "real hold needs the Legal delegate's decision" label as placement, and says a programme manager can record the release once the hold has ended. It does not say who decides the end. Missing decision stays reported. |
| 3 | Accepted. | Copy marks periods as demonstration values, explains the start date, and drops "a programme manager can view it". |
| 4 | Accepted. | Test covers no-trigger and future-trigger branches, document and blob retained, audit chain, exact due-day deletion still works; lexical guard checks both old literals fail. |
| 5 | Accepted. | Docs name only the two `approve_retention_deletion` refusals; resident-record path (`resident_decisions.py`) and other `doc_controls.py` messages stay listed as unaudited. |

No finding conflicts with a confirmed decision. No significant or divergent issue needs a user decision. Critique is not repeated for this task.
