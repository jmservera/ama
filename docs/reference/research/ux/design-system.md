---
title: Zava Forward Workbench Design System Foundations
description: Design tokens, component inventory with states, non-colour signal rules and the extend-versus-adopt decision for the workbench UI (issue #150)
ms.date: 2026-11-20
ms.topic: reference
---

## Scope and evidence

Partial delivery for issue #150 under epic #149. Sources: `src/api/src/zava_forward/api/web/style.css`,
`src/api/src/zava_forward/api/web/*.js`, PRD SA-001 to SA-004
([PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md)) and the
[prototype learnings review](./prototype-learnings-and-simplicity-review.md).
This is a design specification for a synthetic-data demonstrator. It is not
user-tested and not an accessibility conformance claim. Local token-pair contrast
checks do not establish full workflow contrast or screen-reader acceptance.

## Decision: adopt Fluent UI (Fluent 2)

Status: owner-selected on 2026-10-15. The
[adopt decision](https://github.com/jmservera/ama/issues/150#issuecomment-6194437555)
and [Fluent 2 selection](https://github.com/jmservera/ama/issues/150#issuecomment-6194477486)
supersede the earlier delivery-agent proposal to extend the MVP. The
[src pivot](https://github.com/jmservera/ama/issues/150#issuecomment-6196723580)
changes placement, not acceptance criteria.

The current slice establishes Fluent 2 token foundations and native HTML
component styling in the migrated API web assets. It does not import Fluent
React/Web Components and is not completion of the owner-selected Fluent UI
adoption. Delivery must still select/integrate an actual Fluent implementation
and evidence its rendered states, packaging, CSP and accessibility, or obtain
explicit owner acceptance of a native-only substitute. Issue #150 stays open.
This is not a renewed decision to retain the old bespoke system.

## Proposed resident task extension (2026-10-23, #441)

The [six proposed resident scripts](./customer-journeys/residents.md#proposed-optional-resident-increment-2026-10-23-441)
inherit owner-selected Fluent 2, native semantics, non-colour status, visible
focus, reduced motion and plain content. This is documentation only, not
resident UI implementation or completion of Fluent adoption.
Specify loading/empty/failed/unknown/stale/denied/session-expired/received/
scan-pending/reviewed/published/response-recorded/confirmed states distinctly.
Do not make receipt a verification, response a booking, or policy disposition
a human review. Safe recovery and revoked grants must have accessible routes
without disclosing another case. Keep person/urgent help and phone/email/visit
equivalents visible; non-use has no service detriment.

Resident components/states, keyboard and assistive-technology checks,
comprehension and real-user validation remain proposed/Not run under the
[WCAG extension](./wcag-conformance-baseline.md#proposed-resident-task-audit-2026-10-23-441).
No aesthetic overhaul, framework swap or native-only acceptance is inferred.

## Design tokens

Defined once in `:root` in `src/api/src/zava_forward/api/web/style.css` and used by components.
The [Fluent token model](https://fluent2.microsoft.design/design-tokens) separates
global values from semantic aliases. Values below were checked on 2026-10-15
against microsoft/fluentui at revision
`84abdb5fd25a10c627a08465ae82a96e17927270`, not a floating runtime dependency.

| Fluent foundation | Tokens and source mapping | Consumers |
| --- | --- | --- |
| Neutral colours | `--colorNeutralForeground1` #242424, `--colorNeutralForeground2` #424242 from [lightColor.ts](https://github.com/microsoft/fluentui/blob/84abdb5fd25a10c627a08465ae82a96e17927270/packages/tokens/src/alias/lightColor.ts) | `--ink`, `--muted`, body and secondary copy |
| Theme aliases | `--colorNeutralBackground1`, `--colorNeutralBackground2`, `--colorBrandBackground`, `--colorBrandBackgroundHover` | Existing surface/background and teal brand bridges; custom theme, not asserted Fluent default colours |
| Type | `--fontFamilyBase`, `--fontSizeBase400`, `--fontSizeBase500`, `--fontSizeBase600`, `--lineHeightBase500`, `--lineHeightBase600`; Segoe/system stack, 20/26px Subtitle 1 and 24/32px Title 3 from [typography](https://fluent2.microsoft.design/typography) | Body, headings and native controls; rem units preserve user font sizing |
| Spacing | `--spacingHorizontalXS`, `--spacingHorizontalS`, `--spacingHorizontalM`, `--spacingHorizontalL`, `--spacingHorizontalXXL`; 4/8/12/16/24px equivalents from [spacings.ts](https://github.com/microsoft/fluentui/blob/84abdb5fd25a10c627a08465ae82a96e17927270/packages/tokens/src/global/spacings.ts) | Legacy spacing bridges, card/control padding and row gaps |
| Shape | `--borderRadiusMedium`, `--borderRadiusXLarge`; 4/8px equivalents from [borderRadius.ts](https://github.com/microsoft/fluentui/blob/84abdb5fd25a10c627a08465ae82a96e17927270/packages/tokens/src/global/borderRadius.ts) | Buttons/fields and cards |
| Motion | `--durationFast`; 150ms from [durations.ts](https://github.com/microsoft/fluentui/blob/84abdb5fd25a10c627a08465ae82a96e17927270/packages/tokens/src/global/durations.ts) | `--motion` transition bridge; zero with reduced motion |

Explicit customizations: retain the existing teal/status palette pending brand
guidance, 16px body instead of Fluent's 14px Body 1, stronger field boundaries,
40px native buttons and the two-tone focus indicator. These are project choices,
not official Fluent component recipes or a library-conformance claim.

Legacy aliases keep existing screens connected to the new foundation:

| Group | Tokens |
| --- | --- |
| Colour | `--ink`, `--muted`, `--line`, `--bg`, `--surface`, `--brand`, `--brand-d`, `--soft`, `--soft-line`, `--warn`, `--warn-bg`, `--caution`, `--caution-bg`, `--caution-line`, `--ok`, `--ok-bg`, `--field-line`, `--disabled-bg`, `--disabled-ink` |
| Type | `--font`, `--fs-sm`, `--fs-base`, `--fs-lg`, `--fs-xl`, `--lh` |
| Spacing and shape | `--sp-1` to `--sp-5`, `--radius`, `--radius-lg` |
| Focus | `--focus`, `--focus-ink`, `--focus-w`, `--focus-off` (3px dark outline with a 2px amber ring on `:focus-visible`, so the indicator shows on light and brand backgrounds; issue #151). The main container is the one exception, by the owner's request of 2026-11-20: see [Focus on the main container](#focus-on-the-main-container) |
| Motion | `--motion` (0s under `prefers-reduced-motion: reduce`) |

Legacy rules that still use literal lengths or white are migrated as they are
touched; new rules must use tokens.

## Public welcome page palette (2026-11-20)

The public welcome page is the one surface that does not use the workbench
teal. At the owner's request it takes its look from the capstone deck: the
paper, forest, sage and amber values below, the deck's pictograms and four of
its pictures. The workbench, the resident sites and every signed-in screen keep
the teal and status palette above. The page still uses the workbench's focus
indicator, spacing and radius tokens, and its example case card reuses the
blocked-step, status and AI-suggestion patterns so a visitor sees what staff see.

| Token | Value | Use |
| --- | --- | --- |
| `--lp-paper` | `#faf9f6` | page ground |
| `--lp-ink` | `#1b2a24` | running text |
| `--lp-forest` | `#173f35` | main dark fields, buttons |
| `--lp-moss` | `#1f4b3f` | button hover |
| `--lp-green` | `#2e6b5e` | secondary dark fields |
| `--lp-sage` | `#e8f1ed` | light fields, pictogram discs |
| `--lp-amber` | `#e9b14c` | the one accent: sign-in action, stall markers, labels on forest |
| `--lp-amber-tint`, `--lp-amber-ink` | `#fff1d6`, `#7a4b00` | stall labels and the pilot caveat |

Paper, forest, green, sage, amber and the amber tint were sampled from the
rendered deck. Ink and moss are not deck values: ink is a near-black tinted
toward the forest for body text, and moss is a hover step between forest and
green. Amber marks where a case can stall, as it does in the deck's journey
line, and the same cue is repeated in words, so colour is never the only signal.

`src/api/tests/test_welcome.py` measures every text pair the page uses with the
same helper as the workbench token checks. The pictures are derived by
`tools/build-welcome-media.py` and carry the provenance gap recorded in the
[capstone asset catalog](../../../capstone/source/assets/catalog.json): original
address, prompt and licence are not established.

## Layout rules

* Page content sits in `main` (max 1320px, 1rem side padding).
* List and detail screens use `.layout` (15rem filter side column plus `.main`);
  it collapses to one column under 900px.
* Groups of summary values use `.tiles`; independent panels use `.grid`.
* Overview data tables sit in `.table-scroll`, a named `role=region` with
  `tabindex=0`, so wide rows scroll with a keyboard without widening the page.
* One primary action per card; a case list shows one plain status and one next
  action per item (SA-001).

## Supported devices and widths

The owner decided on 2026-11-13 (issue #152, Batch-2 Q1) which devices the
workbench supports. Source: `src/api/checks/workbench-manifest.json` and the
[decision record](supported-devices-proposal.md).

| Tier | CSS width | Layout rule |
| --- | --- | --- |
| Desktop | 1280px and wider | `.layout` keeps the filter side column beside `.main` |
| Tablet | 768px | `.layout` is one column under 900px; navigation wraps under 1100px |
| Mobile | 360px | One column; the under-600px rules stack lists, cards and definitions |

* The 320px reflow check from the PRD stays as a separate minimum; 390px and
  1024px remain checked widths but are not named tiers.
* Every tier shows the same role navigation, one next action per case and
  visible safety markers (SA-001, SA-007); only layout changes.
* These are CSS and DOM contract checks (`test_design_system.py`,
  `test_workbench.py`). Real-device and assistive-technology acceptance remain manual and open.
* 360px is not checked by a browser run in this change; the browser check reads
  the width from the manifest and runs it when Chromium is installed.
* PRD AC-034 and AC-043 stay partial; this decision does not tick them.

## Component inventory

States: default, focus, disabled, error, loading, empty, blocked.

| Component | Class or element | States and usage |
| --- | --- | --- |
| Button | `button`, `.btn`, `.alt` | Default; hover; focus ring; native `disabled` while pending; `aria-busy=true` and adjacent polite progress text, spinner after 200ms. |
| Form field | `input`, `select`, `textarea`, `label` | Default; focus ring; `aria-invalid=true` gets a thick red border and must be paired with a `.field-error` message. |
| Field error | `.field-error`, `.err` | Warning glyph plus text; never colour alone. |
| Labelled field | `.field`, `.field-hint`, `.field-row` | One visible label with "(required)" or "(optional)", an optional hint, the control and a hidden `.field-error`, built by `Fields.fieldBlock` in `fields.js`; `fail()` shows the error, marks the control invalid and moves focus to it. See [Labelled field and check row](#labelled-field-and-check-row). |
| Check row | `.check` | Checkbox before its label, hint or error on its own line indented under the label text, built by `Fields.checkRow`. The label carries the space beside the box, so the whole row is clickable. |
| Card and list item | `.card`, `.item` | Default; hover border; one name, one status, one meta. |
| Data table | `.table-scroll`, native `table` | Named focusable horizontal-scroll region for wide tables; native column headers retain `scope=col`. Empty/error/loading states belong to the enclosing request. |
| Status flag | `.flag`, `.flag.danger` | Text label always present; danger adds a warning glyph. |
| Status line | `.status-line`, `.danger`, `.ok`, `.wait` | Border colour plus a leading glyph (warning, tick, hourglass) and the status words. |
| Tile | `.tile`, `.tile.danger` | Number plus explicit label; `aria-pressed` and visible "Selected"/"Select filter" words distinguish active filters without colour. |
| Empty state | `.empty` | Dashed border, plain sentence saying what is absent and what to do next. |
| Safety issue card | `.safety-item`, `.safety-facts`, `.safety-next`, `.safety-step`, `.primary-step`, `.safety-optional`, `.safety-details`, `.field-hint` | One card per safety issue: plain heading, `.status-line`, a four-row facts list, a "What humans need to do next" callout, one `<form>` and `<fieldset>` per action with its own labelled evidence field, and a `.field-hint` linked by `aria-describedby`. Audit fields and optional external dates sit in native `<details>`. | Number plus explicit label; `aria-pressed` and visible "Selected"/"Select filter" words distinguish active filters without colour. || Empty state | `.empty` | Dashed border, plain sentence saying what is absent and what to do next. |
| Loading state | `.loading`, `.async-feedback` or `aria-busy` | Immediate progress text; decorative spinner after 200ms, static with reduced motion. No spinner-only signal. |
| Blocked step | `.blocked` | See below. |
| Journey strip and case tab list | `.stepper`, `.step`, `.case-tabs`, `.case-tabs-row` | Cards equal in height within a visual row; a blocked step shows "Why blocked" and opens the native popover; tabs wrap at 900px and wider and scroll in one row at 899px and below. See [Journey strip and case tab row](#journey-strip-and-case-tab-row). |
| Decision card | `.decision-item`, `.decision-facts`, `.decision-defect`, `.decision-grid`, `.decision-step`, `.decision-actions`, `.decision-feedback` | One quality record with the decision area for its state; client messages, server refusals and the recorded result show inside the record. |
| Handover card | `.handoff-result`, `.handoff-actions`, `.handoff-record`, `.handoff-candidates`, `.handoff-offer`, `.handoff-more` | Status list, the viewer's actions, one offer button per suggested person with an inline labelled form, and a notice with owner and next action when offering is not possible. |
| Sensor alert | `.sensor-alerts`, `.sensor-alert` | One item per alert with a warning glyph, a caution or warning tint and a definition list: What we see, Owner, Next action. |
| Layout and list helpers | `.layout`, `.side`, `.main`, `.list`, `.row` | Layout helpers only; they carry no state. `.layout` is a two-column grid that collapses to one column under 900px; `.side` holds the queue; `.row` groups buttons and links. |
| Specialist screen | `.screen-record`, `.screen-links`, `.screen-evidence` | Read-only role screens. `.screen-record` is a `.card` panel; `.screen-links` is the screen menu, with the current screen marked by `aria-current="page"` and bold text; `.screen-evidence` holds the selected home. State words stay in text. |
| AI suggestion | `.ai-suggestion` | See below (SA-004). |
| Map key and markers | `.key`, `.map-symbol`, `.map-marker`, `.cluster` | Circle/O = Normal; square/W = Waiting 60+ days; triangle/! = Safety issue open. Same symbols in key. Clusters show total homes and "Safety: N", including zero. Marker title/tooltip and list use status words. Explicit Enter/Space handlers activate Leaflet marker buttons; list links/buttons remain available. |

Native controls provide default/focus/disabled behavior; invalid fields must use
`aria-invalid` plus a linked text error, not just a red border. `aria-disabled`
alone never prevents activation: use native `disabled` for buttons and enforce
server authority for every action. Loading needs visible text and `aria-busy`;
an empty result must be distinguished from a failed request. Cards, map symbols
and status flags are not themselves form controls, so disabled/error/loading
states belong to the enclosing task or request, not a fictitious marker state.

### Blocked step (SA-003)

Markup: a `.blocked` container with a `.blocked-title` heading in plain words,
then a `dl` with exactly three rows: "Why it is blocked", "Owner" (a named
person or role, never "unassigned"), and "Next action" (one verb-led
sentence, with a link or button where possible). Avoid the internal terms gate,
hold, provenance and trace in the core flow. The title carries a no-entry glyph
so the state is readable without colour.

### AI suggestion label and review pattern (SA-004)

* The reusable `.ai-suggestion`/`.ai-label` pattern uses the exact text
  "AI suggestion, not approved". Current AI outputs also use `.ai`, `.aimeta`
  and task-specific sections with the same plain-language warning.
* Requesting assistance is optional; a case and the manual draft path never
  depend on it.
* Current `aiNotes()` actions are "Use this draft", "Edit this draft" and
  "Do not use this draft". Edit reveals a large editor and required reason;
  rejection reveals only a required reason. Accept needs no text field.
  Submission explicitly records a draft review, never approval of works.
  Priority suggestions use
  "Accept", "Edit" and "Reject". The `.reviewed` style is a foundation pattern,
  not evidence that all existing outputs use it.
* Human-reviewed output says it was reviewed as a draft and explicitly states
  it is not an approval, consent or safety decision. AI output never changes
  ranking, owners, stages or queues. The server still enforces authority.
* The label is text, so it is not colour- or border-style-only.

## Staff workbench UX update (2026-11-20)

Design record for the staff workbench UX review of 2026-11-20 (see the
[review record](./staff-workbench-ux-review-2026-11-20.md)). It adds one labelled-field
pattern, card classes for the case screen, a journey strip alignment rule and a few
global rules for links, targets and figures, and it removes the focus frame from the main
container. It is not user-tested, not a Fluent runtime adoption and not an accessibility
conformance claim.

### Labelled field and check row

`src/api/src/zava_forward/api/web/fields.js` (the `Fields` global, loaded right after
`async-action.js`; it calls `h()` from `app.js` at call time) builds one pattern for
form fields.

* `Fields.fieldBlock({ id, name, label, hint, required, optional, control })` returns
  `{ block, control, fail(message), clear() }`.
* `Fields.checkRow({ id, label, hint, control })` returns `{ block, control }`.
* An id and a visible label are mandatory; the helper throws without them.

```html
<div class="field">
  <label for="{id}">{label} (required)</label>
  <p class="field-hint" id="{id}-hint">{hint}</p>
  <input id="{id}" name="{name}" aria-describedby="{id}-hint">
  <p class="field-error" id="{id}-error" hidden></p>
</div>
```

Rules:

* The label is visible text. "(required)" or "(optional)" is appended to the label text,
  so it is read with the label. If both flags are set, required wins; with neither flag
  the label stays bare. The [content standard](./content-standard.md) carries the
  proposed marking rule, pending owner confirmation.
* The hint is optional, sits between the label and the control and is linked to the
  control through its description. It takes the muted colour and the small size.
* The error paragraph stays hidden until `fail(message)` runs. `fail` writes the text,
  shows it, adds its id to the control's description, marks the control invalid and
  moves focus to the control. `clear()` empties and hides the paragraph, drops its id
  from the description and removes the invalid mark. The paragraph is not a live
  message of its own: the person meets it as the description of the focused field. That
  design has not been checked with a screen reader.
* A validation error is one short sentence that says the reason and the fix, for
  example "Enter the case reference, for example ZF-1." or "Say why you are returning
  it."; the hint under the field stays as the guide. The three-part form (the reason,
  then "Owner: ..." and "Next action: ...") is for blocked or refused actions, and
  server refusals keep their own wording. The [content standard](./content-standard.md)
  already asks for this split. The first build used the three-part form on empty
  handover and time capture fields, and the final review found the two voices
  inconsistent.
* In a check row the checkbox comes first, then its label, then the hint, in one flex
  row. The label carries the space beside the box, so a click in the gap reaches the
  box, and the hint or error is indented by the box width plus that space so it lines
  up under the label text. The "resident told" tick in the quality card builds its own
  error line and links it by description, without marking the box invalid.

Classes in `style.css`:

* `.field`: block spacing. Inputs, selects and textareas inside it are block level and
  fill the width up to 36rem; checkboxes and radios are excluded.
* `.field-hint`: small size, muted colour.
* `.field-error`: the existing warning glyph and text, hidden through the `hidden`
  attribute so that the glyph never prints alone.
* `.field-row`: a wrapping flex row of fields aligned to the bottom, each field taking
  12rem or more; a button sits last.
* `.check`: a wrapping flex row for a checkbox and its label, with the hint or error on
  a line of its own, indented under the label text. The label has inline start padding
  of `--sp-2` and the row has a row gap of the same size.

### Decision, handover and sensor card classes

Colours come from existing tokens: borders from `--line`, `--warn`, `--caution` and
`--brand`, backgrounds from `--surface`, `--warn-bg` and `--caution-bg`.

* `.decision-item` is one quality record: bordered, rounded, on `--surface`, with a
  dashed border when it also has `.superseded`. Inside it sit `.status-line`,
  `.decision-facts` (a definition list with a 12rem label column, one column at 600px
  and below), `.decision-checks` (a native disclosure), `.decision-defect` (a left
  border in `--warn`) and `.decision-area` (hidden when empty).
* `.decision-grid` places two `.decision-cell` blocks side by side from 1200px and
  stacks them at 1199px and below. `.decision-step` is the fieldset with its legend,
  `.decision-actions` the button row (full-width buttons at 600px and below) and
  `.decision-feedback` the result area under it (hidden when empty). `.evidence-step`
  and `.evidence-checks` style the evidence form.
* `.handoff-result`, `.handoff-actions`, `.handoff-record`, `.handoff-candidates`,
  `.handoff-offer` and `.handoff-more` style the handover card: the result line with its
  undo button, button rows, the record fieldset, the candidate list with one button per
  person, the inline offer form and the closed disclosures.
* `.sensor-alerts` is the alert list. `.sensor-alert` has a caution border with a wide
  left edge and a tint, `.sensor-alert.danger` takes the `--warn` tokens, and its heading
  carries a warning glyph. Each alert is a definition list: What we see, Owner, Next
  action.
* `.case-links` lays the three case header links out as a wrapping list.

### Journey strip and case tab row

* Alignment rule: `.stepper` is a grid with `align-items:stretch` and `.step` is a flex
  column. The link takes the free height (`flex:1 1 auto`), so the blocker button sits
  at the foot of its card and the cards in one visual row have equal height. The strip
  has six columns at 1200px and wider, three columns by two rows from 900 to 1199px and
  one column at 899px and below.
* A blocked step shows the fixed words "Why blocked" on its blocker button. The full
  reason, owner and next action stay in the native popover, and the accessible name
  still starts "{Step}: why blocked". A closed case shows no blocker button.
* Tab list: `.case-tabs` wraps at 900px and wider. `.case-tabs-row`, the wrapper inside
  it, takes no box there (`display:contents`). At 899px and below the wrapper is a
  non-wrapping flex row with horizontal overflow and contained overscroll, and the tabs
  do not shrink. Script scrolls the selected tab into view along the row. The wrapper has
  no name and no focus stop, and its behaviour with assistive technology is not checked.

### Links, targets and figures

Appended to `style.css` under the `ux-batch:app-wide` comment:

```css
main a:where(:not(.btn,.item,.linkbtn)){color:var(--brand-d)}
main a:where(:not(.btn,.item,.linkbtn)):hover{color:var(--ink)}
:where(table a,.plainlist a,details li>a):where(:not(.leaflet-container a)){display:inline-block;min-height:1.5rem;padding-block:var(--sp-1)}
th,td{font-variant-numeric:tabular-nums}
@media(max-width:600px){main{padding-block-end:5rem}}
```

The coordinator screen has one rule of its own, in the coordinator block of the same file:

```css
.coordinator table a{display:inline-block;min-width:1.5rem;min-height:1.5rem;padding:var(--sp-1);text-align:center}
```

* One link colour: links in `main` take `--brand-d` (the hover step of the brand teal),
  and `--ink` on hover, except buttons, card links (`.item`) and link-styled buttons
  (`.linkbtn`). The exclusion list sits inside `:where()`, so it adds nothing to the
  weight of the rule, which is that of `main a` (two element selectors); the hover rule
  adds one pseudo-class. A component rule that names a class and sets its own link
  colour still wins, for example the stepper links, the jump links and the map controls.
* Compact target height: links in tables, map lists (`.plainlist`) and disclosure lists
  (`details li>a`), outside the Leaflet map container, are inline blocks with a minimum
  height of 1.5rem (the app's compact minimum, the same value `details>summary` and
  `.linkbtn` use) and block padding of `--sp-1`. The whole selector sits inside
  `:where()`, so this rule has zero specificity: a rule that sets its own display, height
  or padding wins, and buttons, the jump links and the map attribution keep their own
  sizes.
* Coordinator count links: the coordinator rule reaches links in tables only. It gives
  them the same minimum height, a minimum width of the same size and centred text, so a
  bare single-digit count stays a usable target. Count links inside a sentence stay
  inline. The specification's rule covered every link on the coordinator screen, and the
  final review found that it grew the lines of those sentences (application N7).
* The specification wrote the first and third rules with normal specificity. Measured on
  24 screens, that shrank the coordinator jump links from 40px to 34px, turned the map
  zoom controls teal and inline-block, shrank the Reset coordinator filters button and
  enlarged the map attribution (FB-8 measurement). The `:where()` form leaves those alone.
* The earlier specialist-screen rule that shrank a lone link now reads
  `.screen-evidence p>a:only-child:not(.btn)`, so Download for Excel keeps the button
  height. `test_design_system.py` pins the new selector.
* Figures: every table cell uses tabular numerals; earlier rules covered three tables
  only.
* Narrow screens: at 600px and below the page ends with 5rem of space so that the fixed
  chat launcher clears the last card. The space first applied at every width, and the
  final review found about 100px of empty space at the foot of every page, including at
  1440px, so it now sits in a media query (application N11). At the same width the
  employee chat panel's height setting is the full viewport height, where it is 70 or 80
  percent above 600px, and its composer may take up to 70 percent of the panel, where it
  takes up to 55 percent above 600px, so the Attach and Voice explanation shows at 390 by
  800. The clearance was measured on All cases at 390px; wider screens were not
  re-measured after the width change. The title row of a work list keeps a space of
  `--sp-4` below it.
* The `:where()` rules and the complex `:not()` need a current browser and were observed
  in Chromium only. Contrast of the link colour on each background it meets is routed to
  the accessibility skill; this update adds no contrast measurement.

### Focus on the main container

The two-tone focus frame applies to every focusable target except one. At the owner's
request of 2026-11-20, after a screenshot of a thick frame around the whole content
area, the main container (`main#app`) shows no frame however focus arrives there: mouse
navigation, keyboard navigation or the skip link.

```css
[tabindex="-1"]:where(:not(#app)):focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }
#app:focus-visible { outline-color: transparent; box-shadow: none; }
```

* The first rule is the frame for elements with tabindex -1. The exclusion of the main
  container sits inside `:where()`, so the rule keeps its weight and every other target
  keeps its frame. It stopped the frame after mouse navigation only: Chromium treats the
  container as keyboard-focused after Enter on a link or the skip link, so the global
  focus rule still drew it. The override is the second rule.
* Focus still moves to the main container after a route change and from the skip link;
  only the frame is gone. Links, buttons, fields and the case tab panel headings keep
  their frame from the global focus rule and the heading rules.
* No outline is switched off. The outline stays defined, only transparent, so
  forced-colours mode can still draw one. That rendering was not checked.
* The accessibility review of this choice is pending. It settles finding F36 and defer
  item D12 of the [review record](./staff-workbench-ux-review-2026-11-20.md) in the
  owner's favour. `test_polish_ux.py` pins the mechanism.

### Palette

The app palette is unchanged. The workbench keeps its Fluent 2 tokens and the teal brand,
and every rule added in this update uses existing tokens; tests check the field rules and
the app-wide block for raw colour values. The deck-derived palette stays on the public
welcome page only, as recorded above. The page declares the brand teal, `#0b5d6b`, as its
theme colour.

## Colour as a signal: delivered and evidence limits

* Danger, ok and wait statuses add a glyph and words, not only a colour.
* Disabled buttons expose native unavailable semantics, not just a visual style.
  Do not substitute `aria-disabled` styling for preventing activation.
* Errors use a thicker border, a glyph and message text.
* Map markers use outlined geometry plus O/W/!, not filled colour-only circles.
  Hover/focus names and the equivalent list include the same status words.
* Clusters show safety counts even when zero; hazard clusters also use a double
  border. Tile labels explicitly name safety status and selected words identify
  the current filter. No status is inferred from red text alone.
* Forced colours retain border geometry, symbols, safety counts and selected
  words. Decorative symbols are hidden from assistive technology; controls have
  human-readable names.
* Full screen-reader/user acceptance, all-workflow accessibility conformance and
  full Fluent runtime adoption remain open. Local checks do not prove these.

## Journey to requirement to design to test traceability

Added 2026-11-13 for the "design artefacts are traceable to journeys and
requirements" and "evidence recorded as test results" criteria of
[#149](https://github.com/jmservera/ama/issues/149). Each row links a journey
source to its requirement IDs, the UX design artefact, the implemented web
surface and the automated test that exercises it. Prefixes: `PRD:` and `BRD:`
mark an NFR in that document; `screen:` is a `registerRoleScreen` id in
`role-screens.js`; `panel:` is a function in `panels.js`; `route:` is an API
path in `server.py`; `web:` is a file in the served web folder. Tests are
`path::Class::method`.

These are source-level and local engineering checks on synthetic data. They do
not establish WCAG conformance, assistive-technology acceptance, plain-language
review by a named human, or usability with representative users. Every row
keeps the human evidence as `pending human test`: the manual assistive-technology
run and named-human reviews tracked in [#155](https://github.com/jmservera/ama/issues/155)
and [#151](https://github.com/jmservera/ama/issues/151), and live staff
usability sessions under the
[usability test programme](./usability-test-programme-plan.md), have not been
run. No acceptance criterion is ticked by this matrix.
`src/api/tests/test_ux_design_traceability.py` fails when a referenced file,
screen, panel, route, test class or method, or requirement ID no longer exists,
when a registered role screen is missing from the matrix, or when a row drops
its pending-human marker.

| Journey | Requirement IDs | UX design artefact | Web surface | Automated test evidence | Human evidence |
| --- | --- | --- | --- | --- | --- |
| Asset and investment: `docs/reference/research/ux/customer-journeys/asset.md` | `SA-001`, `SA-002`, `AC-040`, `AC-041`, `PRD:NFR-001` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:asset-board`, `panel:stockPanel`, `route:/api/asset/stock-queue` | `src/api/tests/test_asset_board_screen.py::AssetBoardScreen::test_unknowns_owner_age_and_no_controls` | pending human test: asset staff review and usability session |
| Programme coordination: `docs/reference/research/ux/customer-journeys/programme.md` | `SA-001`, `SA-002`, `AC-034`, `AC-036`, `AC-043` | `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/research/ux/program-manager-document-workspace-journey.md` | `screen:programme-queue` | `src/api/tests/test_programme_screen.py::ProgrammeScreen::test_queue_shows_return_sender_owner_receiver_and_separate_responsibilities`, `src/api/tests/test_queue_empty_state.py::EmptyQueueExplanation::test_empty_coordinator_default_without_declaration_is_unknown`, `src/api/tests/test_workspace_paging.py::WorkspacePaging::test_packages_are_paged` | pending human test: coordinator usability session |
| Technical and quality review: `docs/reference/research/ux/customer-journeys/reviewer.md` | `SA-003`, `AC-042`, `PRD:NFR-001` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:technical-queue`, `screen:quality-queue`, `panel:technicalPanel` | `src/api/tests/test_technical_quality_screens.py::TechnicalQueue::test_incomplete_signoff_record_cannot_show_readiness` | pending human test: reviewer usability session |
| Resident choice and service issues: `docs/reference/research/ux/customer-journeys/residents.md` | `SA-008`, `AC-035`, `AC-037`, `BRD:NFR-008` | `docs/reference/research/ux/resident-demo-redesign-2026-11-04.md`, `docs/reference/research/ux/equity-journey-test-plan.md` | `screen:resident-choice`, `screen:resident-service-issues`, `panel:residentPanel`, `route:/api/resident/choice-queue`, `route:/api/aftercare`, `web:aftercare.js` | `src/api/tests/test_resident_choice_screen.py::ResidentChoiceScreen::test_choice_pause_commitment_and_access_are_distinct`, `src/api/tests/test_resident_service_screen.py::ResidentServiceScreen::test_issue_owners_needs_and_commitment_are_visible`, `src/api/tests/test_aftercare_screen.py::AftercareScreens::test_errors_are_summarised_for_focus_and_shown_inline` | pending human test: representative resident sessions and assistive-technology run (#155) |
| Safety and hazard: `docs/reference/research/ux/customer-journeys/safety.md` | `SA-007`, `AC-038`, `PRD:NFR-001` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:safety-lead`, `screen:hazard-triage` | `src/api/tests/test_safety_screens.py::SafetyScreens::test_roles_are_scoped`, `src/api/tests/test_safety_panel_ux.py::SafetyPanelUx::test_next_step_callout_names_who_acts_and_explains_waiting` | pending human test: safety lead review and assistive-technology run (#155) |
| Suppliers and contractors: `docs/reference/research/ux/customer-journeys/suppliers.md` | `AC-039`, `BRD:NFR-009` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:procurement-packages`, `screen:contractor-job-pack`, `route:/api/workorders` | `src/api/tests/test_procurement_screens.py::PackageQueue::test_submission_is_separate_from_review_and_empty_is_unknown` | pending human test: contractor usability session |
| Finance and grants: `docs/reference/research/ux/customer-journeys/finance.md` | `AC-041`, `AC-042` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:finance-invoices`, `screen:finance-funding`, `panel:financePanel`, `route:/api/finance` | `src/api/tests/test_finance_grants_screens.py::FinanceGrantsScreens::test_roles_exclude_other_staff_and_no_controls` | pending human test: finance staff review |
| Data operator and auditor: `docs/reference/research/ux/customer-journeys/data.md` | `SA-005`, `AC-040` | `docs/reference/research/ux/atlas-screen-trace.md` | `screen:data-operator` | `src/api/tests/test_data_operator_screen.py::DataOperatorScreen::test_both_values_provenance_and_preserved_eligibility` | pending human test: data operator review |
| Plain-language content across journeys | `SA-003`, `SA-004`, `BRD:NFR-008` | `docs/reference/research/ux/content-standard.md` | `web:app.js`, `web:panels.js` | `src/api/tests/test_content_standard.py::CopyAudit::test_blocked_reasons_have_reason_owner_and_next_action`, `src/api/tests/test_content_standard.py::CopyAudit::test_ai_label_is_exact_and_never_implies_approval` | pending human test: named-human copy review |
| Accessibility baseline across journeys | `PRD:NFR-001`, `BRD:NFR-008`, `AC-093` | `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md` | `web:style.css`, `web:index.html` | `src/api/tests/test_accessibility_baseline.py::Wcag22Baseline::test_text_contrast_meets_aa`, `src/api/tests/test_accessibility_baseline.py::Wcag22Baseline::test_every_table_has_a_caption_and_column_headers`, `src/api/tests/test_design_system.py::DesignSystem::test_status_signals_have_non_colour_cue`, `src/api/checks/specialist_keyboard_browser_check.py` | pending human test: screen-reader and keyboard run by named testers (#155, #151) |
| Chat and AI suggestions | `SA-004`, `AC-093` | `docs/reference/research/ux/content-standard.md` | `web:chat-widget.js`, `route:/api/chat` | `src/api/tests/test_chat_panel.py::PanelTests::test_answer_is_cited_labelled_and_stored_with_evidence`, `src/api/tests/test_chat_widget_focus.py::ChatWidgetFocusTests::test_append_follows_only_bottom_readers_without_history_focus` | pending human test: screen-reader run of the chat panel |
| Scenario and needs coverage | `AC-043`, `SA-001` | `docs/reference/research/ux/atlas-screen-trace.md` | `web:role-screens.js` | `src/core/tests/test_scenario_manifest.py::ScenarioManifestTests::test_current_iteration_is_complete_and_honest`, `src/core/tests/test_needs_inventory.py::NeedsInventoryTests::test_rows_are_complete_and_unique`, `src/core/tests/test_atlas_screen_trace.py::AtlasScreenTraceTests::test_published_trace_is_complete` | pending human test: walkthrough with representative users |
| Usability programme and acceptance protocol | `SA-009`, `SA-010`, `PRD:NFR-001` | `docs/reference/research/ux/usability-test-programme-plan.md`, `docs/reference/research/ux/production-ux-acceptance-protocol.md` | `web:index.html` | `src/api/tests/test_production_ux_acceptance_protocol.py::ProductionUxAcceptanceProtocol::test_every_record_cell_is_not_run_or_names_tester_and_date`, `src/core/tests/test_usability_programme.py::UsabilityProgrammeTests::test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` | pending human test: live staff usability trials not run; results record blank |

## Verification

`src/api/tests/test_design_system.py` checks mapping values, token consumption,
state components, decision and signal structure. Contrast tests resolve alias
chains before evaluating thresholds. The synthetic local app check is
`src/api/checks/design_system_browser_check.py`; run it with Playwright/Chromium
installed, using the installed src projects. It constructs only fictional data
and serves the real API on loopback. It does not call a live model, SQL Server
or Azure and does not replace human accessibility acceptance.

The [loading and HAX briefing increment](../../../../src/api/README.md#loading-feedback-and-todays-briefing-531)
adds immediate/slow/retry shell feedback, shared native async states and
statement-source presentation. Fluent Storybook is a pattern reference only,
not new runtime adoption. Staff usability, assistive-technology and deployed
cold-start acceptance remain separate from synthetic engineering checks.
