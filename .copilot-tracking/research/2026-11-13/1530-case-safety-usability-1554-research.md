<!-- markdownlint-disable-file -->
# Research: Issue 1530 case safety usability (safetyPanel)

Task: `1530-case-safety-usability-1554`. Disposition: executed (code inspection) plus reuse of the supplied UX specification. Planning Readiness: Ready.

## Evidence

* UX specification: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/ux-spec-1530.md` (7 defects, Option A1 chosen by owner brief, acceptance criteria).
* `src/api/src/zava_forward/api/web/app.js` `safetyPanel` (about line 1568): three controls rely on `aria-label` only, one shared `evidence` input feeds six actions, `hazardState` shows "Repair evidenced" for unverified legacy rows, the release button shows whenever `x.repaired`.
* `src/core/src/zava_forward/core/workflows.py` `release_hazard`: refuses with HTTP 400 unless `repair_evidence` and `accepted_at` exist; role check via `SAFETY_ROLES`, `gates.safety_release_gate` for non-legacy holds, `hazard.require_independent` for raiser and repair recorder (matches on email, code, oid, else name).
* `hazard_view` returns the full hazard record, so `raised_identity`, `repaired_identity`, `raised_by(_email)` and `repaired_by(_email)` reach the client.
* Existing guards: `test_hazard_api.py` (three `app.js` substrings), `test_content_standard.py` (banned words), `test_accessibility_baseline.py` (8 `aria-invalid`, 13 `h("table"`), `test_case_journey.py` (`safetyPanel(` once), browser checks need `#case-safety`, `#hz-source` visible and the h2 text.

## Determination

Option A1: no backend change. Client-only rework of `safetyPanel`, CSS classes and the design-system doc. No test requires the `Emergency` default.

## Risks

* Cutover reference inventory TSV tracks line numbers in `docs/reference/`; regenerate if the design-system doc shifts them.
* Banned words must not appear in app.js or style.css (only `x.hold`).
