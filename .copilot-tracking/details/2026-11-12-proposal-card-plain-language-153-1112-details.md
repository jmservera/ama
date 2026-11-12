---
title: Issue 153 proposal card plain-language default details
ms.date: 2026-11-12
task_id: 153-proposal-card-1112
---

## Phase 1: card structure (`assistants.js`)

* Replace the two sibling `details` with one `details[data-proposal-technical]`, summary "Suggestion details (technical, for audit and support)" (glossary term "Suggestion details").
* Inside: one muted note, `h4` "Permitted sources, versions and hashes" with the unchanged `JSON.stringify(p.snapshot, null, 2)` in a `pre` with `tabindex="0"` and an accessible name, `h4` "AI usage and changes to this suggestion" with the unchanged history `pre` (same `tabindex` and name) and the existing "Earlier changes to this suggestion" button.
* Edit field: label and `aria-label` "Edited proposal (technical JSON format)", with a note above it that this is the full proposal in a technical format. `JSON.parse` submission path unchanged.

## Phase 2: tests

* `assistants_browser_check.py`: replace label strings; add `plain_default_card` (constructed fixture, desktop and 360 px): technical content hidden by default, safety text and unknowns visible, keyboard Enter and Space toggle, snapshot and history JSON equal the fixture, no horizontal overflow, edit field holds the full output JSON, axe scan.
* `test_content_standard.py`: static test that the disclosure contains both records and the old label is gone and that safety text is not inside it.
* `test_case_journey.py`: label string only.

## Phase 3: documentation

* `docs/reference/research/ux/content-standard.md`: card row note, `ms.date`.
* `docs/reference/log.md`: appended entry.

## Validation

Focused: `test_content_standard`, `test_case_journey`, `test_assistants`, `test_browser_asset_urls`, `assistants_browser_check.py`, ruff check, mypy on the changed test module, diff review.
