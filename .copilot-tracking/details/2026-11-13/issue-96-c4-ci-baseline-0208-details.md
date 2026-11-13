---
title: Issue 96 C4 details, accessibility baseline eighth invalid-field site
description: Phase details for the bounded baseline test and record update
ms.date: 2026-11-13
---

## Phase 3 edits

1. `src/api/tests/test_accessibility_baseline.py`, `test_every_invalid_field_is_tied_to_a_message`:
   * Change the expected count from 7 to 8 and keep the generic window check for all other sites unchanged.
   * Add one specific association check for the saved-copy site, scoped to the `fundingSavedCopyCheck` body in `role-screens.js` (up to `fundingDraftPanel`), after critique CR-1: the file input's `aria-describedby` equals `${id}-error`; an element with `id: \`${id}-error\`` and class `field-error` exists; `show()` sets the error text, clears `hidden` and sets `aria-invalid`; a `label` has `for: id`; and the label, input and error sit in one returned paragraph. Each is mutation-checked in scratch text.
   * Update the failing message to say the saved Held copy site is audited. No weakening of any prior assertion.
2. `docs/reference/research/ux/wcag-conformance-baseline.md`, Error identification row: keep the 2026-11-04 text, append a dated 2026-11-13 (96 C4) entry that the inventory is now eight sites, naming `role-screens.js` `fundingSavedCopyCheck`: the file input, its visible label, the `field-error` message with glyph and next-step text, `aria-describedby`, the live status sibling, read from source; existing browser check observes `aria-invalid` and message text; not tested: screen reader output, assistive technology. No conformance claim; preserve "pending owner confirmation" and "we do not claim conformance".
3. `docs/reference/log.md`: append one new entry; no earlier entry edited.

## Validation

* `cd src/api && python3 -m unittest tests.test_accessibility_baseline -v` (expect 12 OK, reads the edited record).
* RoleScreens and RoleScreenConformance classes (21 tests), same invocation style as C3.
* ruff and mypy as configured for `src/api` on the changed test file.
