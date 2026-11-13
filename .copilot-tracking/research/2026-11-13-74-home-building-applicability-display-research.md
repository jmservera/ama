---
title: Research for #74 home view building applicability display (initial increment)
ms.date: 2026-11-13
---

Base: `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626` (current main). Research disposition: executed (bounded, current head). Planning Readiness: Ready, subject to independent critique.

## Classification (coordinator admission)

One INITIAL additive read-only display increment for optional G5. Not a correction of a rejected head, not a bug repair, no review-correction cycle admitted, not a claim that G5 is required by literal #74 criterion 2. Historical #74 correction-pool count remains UNKNOWN.

## Prior evidence reused (frozen, not edited)

Source: `/home/azureuser/source/ama-demo-wt/issue-74-source-authority-0430` at `ccc786b0357daa31194cf2a4f3b36b9c1348399e`. G5 is defined in its `2026-11-10-issue-74-main-acceptance-audit-review.md` finding 2 ("whether building items must display their case/package applicability (G5)") and routed again in `2026-11-10-issue-74-qualified-audit-review.md`. The original adverse review (self-review, not independent, no Pass claim) and the qualified follow-up stay as recorded there; this task does not rebrand them. The superseded "no bespoke #74 grant means no standing default" claim is not copied.

## Current-head findings

* `core/buildings.py` `view()` returns the building record by deep copy. Rows in `dependencies`, `holds` and `works` carry `status`, `owner`, `case_ids` and `package_ids`; each scope is validated by `_scope` as `null` (unknown) or a list (empty list = explicitly none). `systems` and `costs` rows carry no scope fields.
* `core/home_case.py` embeds that same `buildings.view` result as `building` in the home-case API response (`home_case.py:131-166`), so the values already reach the browser. Contract unchanged.
* `web/app.js` `buildingView` (full building screen) already renders `Affected homes: ... Packages: ...` with `Unknown` for `null` and `None` for `[]`, guarded by `case_ids !== undefined`.
* `web/app.js` home-case screen `shared()` helper renders only `id: label`, `Recorded status` and `Source`. It drops the applicability the API already supplies. This is the G5 gap.
* Existing semantics (`buildings.blockers`): `null` = unknown; `[]` = explicitly none; a list = explicit scope. The notice states "Shared identity does not establish package applicability."

## Narrow write surface

* `src/api/src/zava_forward/api/web/app.js`: `shared()` row renderer in the home-case view only.
* `src/api/tests/test_home_case_api.py`: behavior regression (existing file).
* `src/api/checks/home_case_browser_check.py`: one assertion on existing synthetic data (existing file).
* No API, core, domain, schema, persistence, logic or fixture-semantics change.

## Constraints and open limits

* Display only; no eligibility computation, filtering or "this home is covered" derivation; no colour-only signal (text labels).
* Unknown (`null`) stays distinct from none (`[]`). Absent fields (systems) are not synthesised.
* Engineering evidence only; no WCAG, AT or human acceptance, no approval claim, no AC tick or closure. Linkage is `Refs #74`.
* Web guidelines source fetched 2026-11-13 from the skill URL (first 8000 characters, which contain all rules and the output format; remainder was not retrieved).
