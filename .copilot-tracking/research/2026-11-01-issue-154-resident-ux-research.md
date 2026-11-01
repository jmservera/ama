---
title: Issue 154 resident and representative UX research
ms.date: 2026-11-01
---

## Disposition

Research disposition: reused. Planning Readiness: Ready.

## Evidence

* `docs/reference/research/ux/customer-journeys/residents.md` (section "Resident and representative task designs (2026-10-27, #154)") already holds J1-J6 and R1 task flows, text wireframes, non-digital equivalents, the shared accessibility frame and the #155 validation scripts (all Not run). Delivered by PR #501.
* The 2026-10-31 closure audit left all five criteria unticked. Unmet reasons: no tests assert complete topic coverage, the offered/waiting/confirmed distinction, or R1 task-limits and expiry; usability and AT validation is Not run; resident-session enforcement is not implemented by the design.
* `src/core/tests/test_resident_preview.py` already covers grant expiry and revocation for the synthetic preview.

## Conclusion

The smallest valuable slice is a design-regression test in `src/core` that pins the required content. Usability validation, OD-41/42 and wording review need humans and cannot be delivered here.
