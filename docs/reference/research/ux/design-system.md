---
title: Zava Forward Workbench Design System Foundations
description: Design tokens, component inventory with states, non-colour signal rules and the extend-versus-adopt decision for the workbench UI (issue #150)
ms.date: 2026-10-15
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
| Focus | `--focus`, `--focus-ink`, `--focus-w`, `--focus-off` (3px dark outline with a 2px amber ring on `:focus-visible`, so the indicator shows on light and brand backgrounds; issue #151) |
| Motion | `--motion` (0s under `prefers-reduced-motion: reduce`) |

Legacy rules that still use literal lengths or white are migrated as they are
touched; new rules must use tokens.

## Layout rules

* Page content sits in `main` (max 1320px, 1rem side padding).
* List and detail screens use `.layout` (15rem filter side column plus `.main`);
  it collapses to one column under 900px.
* Groups of summary values use `.tiles`; independent panels use `.grid`.
* Overview data tables sit in `.table-scroll`, a named `role=region` with
  `tabindex=0`, so wide rows scroll with a keyboard without widening the page.
* One primary action per card; a case list shows one plain status and one next
  action per item (SA-001).

## Component inventory

States: default, focus, disabled, error, loading, empty, blocked.

| Component | Class or element | States and usage |
| --- | --- | --- |
| Button | `button`, `.btn`, `.alt` | Default; hover; focus ring; `disabled` or `aria-disabled=true` greyed with not-allowed cursor; `aria-busy=true` appends "(loading)" text. |
| Form field | `input`, `select`, `textarea`, `label` | Default; focus ring; `aria-invalid=true` gets a thick red border and must be paired with a `.field-error` message. |
| Field error | `.field-error`, `.err` | Warning glyph plus text; never colour alone. |
| Card and list item | `.card`, `.item` | Default; hover border; one name, one status, one meta. |
| Data table | `.table-scroll`, native `table` | Named focusable horizontal-scroll region for wide tables; native column headers retain `scope=col`. Empty/error/loading states belong to the enclosing request. |
| Status flag | `.flag`, `.flag.danger` | Text label always present; danger adds a warning glyph. |
| Status line | `.status-line`, `.danger`, `.ok`, `.wait` | Border colour plus a leading glyph (warning, tick, hourglass) and the status words. |
| Tile | `.tile`, `.tile.danger` | Number plus explicit label; `aria-pressed` and visible "Selected"/"Select filter" words distinguish active filters without colour. |
| Empty state | `.empty` | Dashed border, plain sentence saying what is absent and what to do next. |
| Loading state | `.loading` or `aria-busy` | "(loading)" text is appended; no spinner-only signal. |
| Blocked step | `.blocked` | See below. |
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
* Current `aiNotes()` actions are "Accept as is", "I changed it" and "Reject",
  with a reason required for edit/reject. Priority suggestions use
  "Accept", "Edit" and "Reject". The `.reviewed` style is a foundation pattern,
  not evidence that all existing outputs use it.
* Human-reviewed output says it was reviewed as a draft and explicitly states
  it is not an approval, consent or safety decision. AI output never changes
  ranking, owners, stages or queues. The server still enforces authority.
* The label is text, so it is not colour- or border-style-only.

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

## Verification

`src/api/tests/test_design_system.py` checks mapping values, token consumption,
state components, decision and signal structure. Contrast tests resolve alias
chains before evaluating thresholds. The synthetic local app check is
`src/api/checks/design_system_browser_check.py`; run it with Playwright/Chromium
installed, using the installed src projects. It constructs only fictional data
and serves the real API on loopback. It does not call a live model, SQL Server
or Azure and does not replace human accessibility acceptance.
