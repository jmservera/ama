---
title: Zava Forward Workbench Design System Foundations
description: Design tokens, component inventory with states, non-colour signal rules and the extend-versus-adopt decision for the workbench UI (issue #150)
ms.date: 2026-10-15
ms.topic: reference
---

## Scope and evidence

Implements issue #150 under epic #149. Sources: `src/api/src/zava_forward/api/web/style.css`,
`src/api/src/zava_forward/api/web/*.js`, PRD SA-001 to SA-004
([PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md)) and the
[prototype learnings review](./prototype-learnings-and-simplicity-review.md).
This is a design specification for a synthetic-data demonstrator. It is not
user-tested and not an accessibility conformance claim; contrast ratios and
screen reader behaviour still need the accessibility feature's checks.

## Decision: extend the current UI

Status: proposed by the delivery agent, pending owner confirmation.

* Decision: keep the single hand-written stylesheet and formalise it with CSS
  custom properties, rather than adopt an external design system now.
* Reasons: the workbench is a small static, no-build UI served by the Python
  server; an external system (for example GOV.UK Design System or Fluent UI)
  would add a build step, dependencies and restyling effort that the
  demonstrator does not need.
* Revisit when: a build pipeline is introduced, the accessibility feature finds
  gaps that a mature system would close, or the product moves toward a
  resident-facing public service where the GOV.UK pattern set is expected.
* Open item (owner): confirm the decision and whether Zava brand colours
  should replace the current teal tokens. No brand guideline is in the
  repository.

## Design tokens

Defined once in `:root` in `src/api/src/zava_forward/api/web/style.css` and used by components.

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
| Status flag | `.flag`, `.flag.danger` | Text label always present; danger adds a warning glyph. |
| Status line | `.status-line`, `.danger`, `.ok`, `.wait` | Border colour plus a leading glyph (warning, tick, hourglass) and the status words. |
| Tile | `.tile`, `.tile.danger` | Number plus label; `aria-pressed` shows a filter as active with border and shadow. |
| Empty state | `.empty` | Dashed border, plain sentence saying what is absent and what to do next. |
| Loading state | `.loading` or `aria-busy` | "(loading)" text is appended; no spinner-only signal. |
| Blocked step | `.blocked` | See below. |
| AI suggestion | `.ai-suggestion` | See below (SA-004). |
| Map key and markers | `.key`, `.dot`, `.cluster` | Colour is paired with the key text and the list alternative (`.maplist`). |

### Blocked step (SA-003)

Markup: a `.blocked` container with a `.blocked-title` heading in plain words,
then a `dl` with exactly three rows: "Why it is blocked", "Owner" (a named
person or role, never "unassigned"), and "Next action" (one verb-led
sentence, with a link or button where possible). Avoid the internal terms gate,
hold, provenance and trace in the core flow. The title carries a no-entry glyph
so the state is readable without colour.

### AI suggestion label and review pattern (SA-004)

* Unreviewed output sits in `.ai-suggestion` with a visible `.ai-label` reading
  exactly "AI suggestion, not approved".
* Requesting assistance is optional; a case and the manual draft path never
  depend on it.
* Review actions are plain buttons: "Use as draft" and "Dismiss". After a human
  reviews, add `.reviewed` (solid border) and change the label to "Reviewed
  draft". A reviewed draft never states or implies a controlled approval,
  consent or safety decision, and AI output never changes ranking, owners,
  stages or queues.
* The label is text, so it is not colour- or border-style-only.

## Colour as a signal: delivered and open

* Danger, ok and wait statuses add a glyph and words, not only a colour.
* Disabled controls change cursor and text colour; the disabled label wording is not yet distinct.
* Errors use a thicker border, a glyph and message text.
* Open items: `.cluster.hazard` and `.tile.danger strong` rely on colour (the tile has a label); map markers (`.dot.normal`, `.dot.long`, `.dot.hazard`) differ by
  colour only on the SVG; the list view is the non-colour alternative. Shape
  variants need the accessibility feature to confirm.

## Verification

`src/api/tests/test_design_system.py` checks the tokens exist, are referenced, that
the state components are defined and that the documented component classes
exist. It does not replace a browser or accessibility review.
