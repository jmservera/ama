---
title: Role 231 Technical and Quality renderer static web-guideline findings (REVIEW-EVIDENCE)
description: Static findings against the Web Interface Guidelines fetched 2026-11-13, owner Fluent 2 and WCAG baseline; no execution
ms.date: 2026-11-13
---

Labels: DEFECT (high confidence from source alone), RECOMMENDATION (optional pattern, no mandatory action), UNKNOWN (needs runtime or AT).
Paths are under `src/api/src/zava_forward/api/web/`.

## role-screens.js

role-screens.js:576 - Low - DEFECT vs design-system.md:111 (status line `.ok` = glyph plus words) - `h("p", { class: "ok", role: "status" })` is a bare `p.ok`. The only `.ok` rules are `.status-line.ok` (style.css:289-290), so the positive state has words but no glyph or border. Noncolour text is present ("Recorded evidence is complete ... does not approve the stage"), so the colour-alone rule is met. Same at role-screens.js:648. The negative state `.blocked` does get a glyph (style.css:302), so positive and negative are visually asymmetric.
role-screens.js:576,648 - Low - UNKNOWN (WCAG 4.1.3) - `role="status"` is on a paragraph rendered with its content already present. Whether a screen reader announces it on route render is not established statically; baseline line 47 already records announcement as untested.
role-screens.js:20-22 - Low - RECOMMENDATION (guidelines: headings hierarchical; owner design-system.md:131) - `.blocked-title` is a `p`, not a heading, so the blocked state is not reachable by heading navigation. The enclosing `h2` (line 19) keeps the hierarchy intact. The CSS glyph is generated content (style.css:302); the words "Cannot confirm readiness" are real text.
role-screens.js:575,647 - Low - RECOMMENDATION (plain language, content handling) - blockers are joined into one `dd` string with `join(" ")`, which makes a long run of sentences. A list would scan better. Long-text wrapping of that `dd` was not verified (no `overflow-wrap` rule located for `dd`): UNKNOWN.
role-screens.js:29 - Info - PASS - the table wrapper is a named `role=region` with `tabindex=0` (`h()` sets `tabindex="0"` because only `false`/null are skipped, app.js:27), matching design-system.md:109. Focus indicator is the global `:focus-visible` rule (style.css:48); no `outline:none` was found in the reached styles. Static focusability only, not observed keyboard use.
role-screens.js:29-30 - Low - RECOMMENDATION - the region `aria-label` and the `caption` carry the same text, so the name may be announced twice. Semantics are otherwise native (`table`, `caption`, `th scope="col"` at line 31), consistent with WCAG baseline line 54.
role-screens.js:32 - Low - RECOMMENDATION (WCAG 1.3.1 technique, not an AA failure) - first-column identifiers (Query, Sign-off, Check, Missing item) are `td`, not row headers (`th scope="row"`).
role-screens.js:28 - Info - PASS - truncation to 50 rows is disclosed in text with `role="status"` and "not a complete readiness check"; line 33 gives a plain empty state ("No records supplied. This does not establish readiness."). Guidelines: handle empty states; large lists.
role-screens.js:15-17 - Info - PASS - label/value pairs use native `dl/dt/dd` (grid CSS style.css:134-135).
role-screens.js:25,589,653 - Info - PASS - the withheld list is a native `ul`. State is text ("Needs reassessment", "Nobody yet", "Evidence noted" / "No evidence"), not colour or glyph alone.
role-screens.js:124-127 (via 580-581) - Low - RECOMMENDATION (locale rule: Intl formatting) - "N days old" is a hand-built string. `screenStamp` (lines 9-14) uses `Intl.DateTimeFormat`. Whether a relative-age formatter is wanted is a product choice; no mandatory action is inferred.
role-screens.js:530-601 and 642-661 - Info - N/A - the renderers emit no `a`, `button`, form control, image, media, animation or `onclick` handler, so the link, button, forms, images, motion and gesture rules have nothing to assess. Line 600 mentions "resident-choice" as plain text, not a link.
role-screens.js:569,642 - Info - UNKNOWN - the page `h1`, skip link and landmark are created by the host view (outside scope) and were not read. Heading level continuity across the whole page is therefore not assessed.

## style.css (reached rules only)

style.css:330 - Low - UNKNOWN - `.screen-record` uses `content-visibility:auto`; behaviour of off-screen focusable table regions, find-in-page and AT with skipped content needs a runtime check.
style.css:224-225 - Info - RECOMMENDATION - table cells set no `font-variant-numeric: tabular-nums`; the reached tables are mainly text, so this is optional.
style.css:23,30 - Info - the reached rules use no transitions on these screens; `prefers-reduced-motion` rules exist globally. No `transition: all` was found in reached rules.
Contrast, target size, reflow at 320 px, forced-colors, and focus-not-obscured by the chat launcher: UNKNOWN (CSS tokens not computed).

## Rule-by-range matrix (amendment from critique)

| Guideline area | Helpers 1-48 | Technical 553-603 | Quality 605-663 |
| --- | --- | --- | --- |
| Semantics, tables, regions | finding line 29-32 | via helpers | via helpers |
| Headings | note line 20 | h2 per panel, pass | h2 per record, pass |
| Noncolour state | note lines 20-22 | findings 576 | findings 648 |
| Focus | pass line 29 | via helper | via helper |
| Links, forms, images, motion | none present | none present | none present |
| Content and locale | none | recommendation 580 | none |
| Runtime and AT | unknown | unknown | unknown |

## Declared constructed states (static requirement context only)

Selectors 231 and 231q require refusal wording ("Cannot confirm readiness", "No evidence", "Awaiting independent reinspection"); 231p and 231qp require positive boundary wording ("does not approve the stage", "does not record the handover"). Source text matches those literals statically. None of these states was executed or observed here.

## Coverage limits

* Static review only. No WCAG 2.2 AA conformance, production readiness, human acceptance, keyboard, browser or screen reader result is claimed. Static focusability is not observed keyboard usability.
* The full guideline text was retrieved (one fetch, complete). The skills were loaded; `.agents/skills` was absent, so no design-taste skill was loaded.
* Owner standards: design-system.md and the baseline were read in targeted ranges; content-standard.md was only grepped, so plain-language findings are labelled recommendations.
* Title Case guidance in the fetched rules was not applied against the owner's content standard, which was not fully read.
* Host page, other roles, other screens and #232 were not reviewed. Prior 231 read-model findings are unchanged inputs.

## Review reconciliation addendum (appended after the independent Review; original findings above are preserved unedited)

The independent Review (see the review record) found these errors in the text above. Each was checked against source by the author. The addendum supersedes the earlier lines.

* role-screens.js:575,647 wrapping: UNKNOWN is withdrawn. `dd` has `overflow-wrap:anywhere` (style.css:319), and the renderer output is placed inside `section.screen-evidence` (role-screens.js:100-104, style.css:328). Only the optional list recommendation remains.
* Tabular numerals: `.screen-evidence td { font-variant-numeric: tabular-nums }` exists (style.css:331), so the optional recommendation at style.css:224-225 becomes PASS, given the host wrapper above.
* `assetAgeDays` is role-screens.js:126-128. `h()` sets attributes at app.js:29. The withheld list is defined at role-screens.js:23-25 and used at 600-601 and 660-661.
* New low-severity DEFECT, role-screens.js:128: the template gives "1 days old" for a one-day age (wrong plural in a plain-language string).
* New UNKNOWN, role-screens.js:20-22: `div.blocked` has no role, so whether its appearance is announced is not established. `p.ok` styling conclusion rests on a grep of the reached stylesheet, not a computed cascade (high confidence, not proven).
* `text-wrap: balance` applies to `.screen-evidence h2` (style.css:329): PASS for the heading typography rule.
* The `role="status"` at role-screens.js:28 carries the same announcement UNKNOWN as lines 576 and 648.
* Host: the h1 and the exact `section.screen-evidence` named region are in role-screens.js:100,108 (host, outside renderer scope, noted only as context).
