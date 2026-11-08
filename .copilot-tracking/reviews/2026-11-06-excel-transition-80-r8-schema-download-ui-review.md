# Issue 80 r8 final review (author review, not independent)

Executed once, after the final checks recorded in the r8 changes record. Reviewed head c12014f0f1c2e6b719f7e6d59d3564e51a2947c3 (ignored-inclusive status 0 entries). Earlier records, including the r8 state file written before this review, are preserved; this review covers only the committed r8 source and tests, not later edits.

## Web guidelines

Source fetched in full at the start of r8 and refreshed before this review: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (both retrievals complete, no failure). Skill `web-design-guidelines` loaded. Repository ASCII, Fluent 2 and plain-language standards override generic style advice.

## src/api/src/zava_forward/api/web/role-screens.js

src/api/src/zava_forward/api/web/role-screens.js:1234 - heading "Form schema catalogue" is sentence case, the guideline says Title Case; kept to match every other screen heading and the owner content standard (overridden, not a defect)
src/api/src/zava_forward/api/web/role-screens.js:1236 - `<a>` with `download` for same-origin navigation: correct element, no click handler, link text specific and identical to the existing "Download for Excel" links; visible focus comes from the global `:focus-visible` rule (style.css:48); hover state of `.btn.alt` not re-inspected
src/api/src/zava_forward/api/web/role-screens.js:1234 - `readable &&` yields `false` when unreadable; the shared `h` helper already accepts `cond && h(...)` children (same file lines 97-98), and the vm test confirms the panel is absent
src/api/src/zava_forward/api/web/role-screens.js:1235-1236 - no `...`, no inline style, no animation, no icon, no image, no gesture-only path; text wraps in the existing `screen-record` card (long-line wrapping not browser-checked)

Qualified result: no rule violations found in the changed lines by static reading. This is not an accessibility-conformance claim; no browser, keyboard, screen reader, responsive or download run was performed.

## Behaviour and boundaries

* The link appears only after a successful `form-review` read, which uses the same `forms._actor` intersection as the catalogue; role names are not used. Unreadable or nonconforming reviews show no link (tests with `null`, `{}` and a partly unreadable review). The server re-authorises every click.
* No API, core, CSS, dependency, quality.py, other list, threshold or role change. Existing no-control assertion still rejects buttons, inputs, selects, textareas, role=button and onclick; it permits exactly one href.
* Test-before-fix was recorded (1 failure before the source change). One mypy annotation correction in my own test is recorded in the changes file.
* Limits: the link is shown on a per-case screen although the catalogue is portfolio-wide (text says so); a revoked right after load yields a refused download that was not browser-tested.

## Completed light checks versus deferred gates

Completed: node --check, nine API unit modules (120 tests, rc 0, no skips reported), Ruff check and format, mypy (186 files, after correction).

Deferred and unproven: requirement-specific browser/keyboard/download check (future selector `a[href="/api/form-schemas.csv"]` on `#/screens/finance-funding/<case>`, as a reason-view-enabled Retrofit Programme Manager and as Grants and Evidence Officer; not run), FULL receipt on the final head and fresh main (#79 owns the heavy lane), independent exact-head review, hosted CI, owner acceptance. Every-list export and owner-threshold criteria remain unticked; other list families are not exported.
