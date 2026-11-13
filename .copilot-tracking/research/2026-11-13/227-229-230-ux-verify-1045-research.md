# Research: UX verification #227 #229 #230 (2026-11-13)

Disposition: executed (static read). Planning Readiness: Ready.

## Sources and disclosure

* docs/case_study_48_original.md, the addendum, docs/reference/README.md and memory.md were NOT re-read in this bounded 7-minute run (disclosed gap).
* web-design-guidelines SKILL.md read; rules fetched live from the vercel-labs source, first 6000 characters only (Locale/i18n and later sections not retrieved; partial retrieval).
* UX docs (design-system.md, wcag-conformance-baseline.md, content-standard.md): section headings and content-standard front matter read; bodies not read. Fluent, WCAG and plain-language judgement is therefore from the guideline rules and visible renderer copy, not the full baseline text.
* Prior inputs 499e6428a (1 file) and fc68e7c60 (2 files) are tracking-only; neither read renderer bodies nor ran tests.
* Read: src/api/src/zava_forward/api/web/role-screens.js lines 18-35, 296-560 (programme), 760-1064 (hazard, data operator); src/api/checks/data_operator_ai_state.py.

## Findings (file:line, role-screens.js unless stated)

Passes (static only):

* :26-33 screenTable uses caption, th scope=col, a keyboard-focusable labelled scroll region, an explicit empty state and a role=status truncation notice.
* :18-19 screenPanel gives h2 sections; :976,979,986 h3 nests under h2.
* #227: :799-826 sent, received, accepted and release are separate textual cells; state is words, not colour. :817 routes emergencies to the human procedure. :811,815 use limit Infinity so no hazard is hidden.
* #229: :901 role=alert for access denied and unavailable; :931-955 CSV download is a native button with aria-describedby, role=status result and a fail-closed path; empty and partial states say "not an all clear".
* #230: :311-312,:323 paging and filter outcomes in role=status text; :341-345 native buttons in a role=group labelled "Queue pages"; scope filter is a labelled native select in a form; gate rows say "not a pass; a named person decides readiness".
* Reduced motion and focus: style.css:23,30 (prefers-reduced-motion), style.css:48 (:focus-visible).
* Each screen states it changes nothing and names the human owner.

Observations (minor, follow-ups, not proven defects):

* O1 (withdrawn after critique) :931 class "alt" is styled by style.css:46 (button.alt); no defect.
* O2 :341-345 Previous/Next stay enabled at range ends and the click is silently ignored; only the range text at :321 signals the end.
* O3 :323 "Loading page." has no trailing ellipsis (guideline); plain-language standard may prefer current wording.
* O4 :811,815,849,984 render unlimited rows without virtualisation (guideline: lists over 50); per-home volumes are small and the programme page is capped at 50.
* O5 :313 select has name but no autocomplete="off" (non-auth field guideline only).

Not established: manual assistive-technology testing, WCAG AC4 and AC5 acceptance, browser rendering, resident or staff validation. No conformance claim is made.
