---
title: Issue 154 representative expiry research
ms.date: 2026-11-01
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged)

* #501: designs J1-J6 and R1 in `residents.md`, shared non-digital and adjustment frame, validation scripts (all Not run).
* #664: regression tests pinning design text (criteria 1, 2 wording, 4).
* #652 and the #444 preview (`resident_preview.py`): synthetic read-only preview with default-deny grants and representative task limits.

No open PR references #154.

## Remaining slice

Criterion 3 (task-limited, expiring representative views) is specified in R1 and implemented in the synthetic preview, but R1's boundary statements are only partly pinned by tests:

* R1: authority is unavailable from the review date (`authority_date <= today < review_date` in `resident_decisions.authority_for`). Existing test uses a past review date only, so the exclusive boundary is untested.
* R1: only a Confirmed status grants authority; denied response must reveal no case details.
* R1: a representative briefing is not the household timeline (no `home`).

## Out of scope and still unproven

Usability programme (#155) validation, assistive-technology acceptance, OD-41 and OD-42, live contact. Azure-live work is not authorised.

## Correction cycle (PR 712, 2026-11-01)

Evidence: `AUTHORITY_STATUSES` in `resident_decisions.py` lists Confirmed, Unclear, Disputed, Revoked; the fixture builds addresses as `{case id suffix} Synthetic Row`, so SYN-C2 is `2 Synthetic Row`. No plan change.
