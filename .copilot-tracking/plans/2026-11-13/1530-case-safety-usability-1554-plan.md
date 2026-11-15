<!-- markdownlint-disable-file -->
# Plan: Issue 1530 case safety usability

Task: `1530-case-safety-usability-1554`. Tier: Focused. Details: [details](../../details/2026-11-13/1530-case-safety-usability-1554-details.md). Research: [research](../../research/2026-11-13/1530-case-safety-usability-1554-research.md).

## Phases

* [ ] P1 Rework `safetyPanel` in `app.js` (Option A1): per-action forms, labels, hints, next-step callout, key facts, details disclosures, raise form guidance, `Significant` default.
* [ ] P2 Add CSS classes in `style.css` and `.field-hint`/safety classes to `design-system.md`; regenerate `docs/architecture/cutover-reference-inventory.tsv` if it shifts.
* [ ] P3 Add `src/api/tests/test_safety_panel_ux.py` (static source and node DOM render) covering each acceptance criterion.
* [ ] P4 Run the targeted unit tests, three browser checks, ruff, mypy.
* [ ] P5 Independent code-review and accessibility review, fix findings, commit locally.

## Success

All acceptance criteria in the UX spec hold; no backend change; banned-word, aria-invalid (8) and table (13) counts unchanged.
