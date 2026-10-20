---
title: Zava Forward Workbench WCAG 2.2 Conformance Baseline
description: Proposed target level and scope, first audit, automated check coverage, manual check record template and accessibility statement draft for the workbench (issue #151)
ms.date: 2026-10-20
ms.topic: reference
---

## Scope and evidence

Implements issue #151 under epic #149, after the design system (#150). Sources:
`src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/*.js`, `src/api/src/zava_forward/api/web/*.html`, `src/api/checks/browser_check.py`,
BRD NFR-008, PRD AC-034, SA-009 and the Accessibility engineering row of the
PRD test strategy, and the accessibility requirements in the
[document workspace journey](./program-manager-document-workspace-journey.md).
Standard: W3C WCAG 2.2 (Recommendation, 5 October 2023). The text was not
re-retrieved for this change; check the official W3C page before any external
statement.

This is a first-pass audit by the delivery agent of a synthetic-data
demonstrator. No screen reader, zoom or user test has been run. Nothing here is
a conformance claim.

## Decision: target level and scope

Status: proposed, pending owner confirmation (open item O-1).

| Item | Proposal |
| --- | --- |
| Target | WCAG 2.2 Level AA for every screen a signed-in user reaches, plus the welcome page |
| Beyond AA | Adopt 2.4.13 Focus Appearance (AAA) as a design goal only |
| In scope | Welcome, sign-in, work list, case view, overview (tiles, charts, map), funding, documents, assistants, operations and account panel, for all seven staff roles and the contractor view |
| Out of scope | Third-party map tiles and the vendored Leaflet library internals (recorded as a known gap); documents uploaded by users |
| Platforms | Current desktop Chromium, Firefox and Safari; one screen reader per desktop OS (NVDA with Firefox, VoiceOver with Safari) |
| Viewports | 320, 390 and 1280 CSS px, 200% text resize, 400% zoom where applicable (PRD test strategy) |

## Audit

Result key: Pass (automated or by inspection), Fixed (finding corrected in this
change), Gap (known, not fixed), Not tested.

| Area | WCAG 2.2 criteria | Result | Evidence and finding |
| --- | --- | --- | --- |
| Page language and zoom | 3.1.1, 1.4.4, 1.4.10 | Pass | `lang="en-GB"` and a viewport meta without `user-scalable=no` on both pages (`test_accessibility_baseline.py`). Reflow at 320 px not tested |
| Keyboard | 2.1.1, 2.1.2, 2.4.3 | Not tested | Controls are native buttons, links, inputs and `details`; the map has a list alternative. Full keyboard walk-through by role is a manual check |
| Focus visible | 2.4.7, 1.4.11 | Fixed | The amber outline had 2.01:1 against white. Focus is now a 3px dark outline (13.7:1 on white) with an amber ring, so it also shows on brand-coloured bars. Indicator on the brand header is not yet confirmed visually |
| Name, role, value | 4.1.2 | Pass, partial | Form fields built in `app.js` and `ops.js` carry `aria-label`; tiles use `aria-pressed`; the chart has `role="img"`. Static check only; accessible names of every generated control are not tested |
| Status messages | 4.1.3 | Pass, partial | `role="status"`, `role="alert"` and `aria-live="polite"` regions exist; announcement behaviour in a screen reader is not tested (AC-034) |
| Contrast, text | 1.4.3 | Pass | Computed for the token pairs in the table below. Disabled controls are exempt (1.4.3 inactive components) |
| Contrast, non-text | 1.4.11 | Fixed, gap | Form field border was 2.51:1 and is now 3.77:1. The caution marker colour is 2.61:1 on its tint and the map marker shapes remain colour-only differences (design-system open item); recorded as gap G-2 |
| Target size | 2.5.8 | Not tested | Buttons are padded about 2.5rem tall. Inline `linkbtn` rows and map controls are not measured |
| Error identification | 3.3.1, 3.3.3 | Pass, partial | `.field-error` and `aria-invalid` exist in CSS; every form error path is not audited |
| Charts | 1.1.1, 1.3.1 | Fixed | Charts were `role="img"` with a title only. Each now offers "Show this chart as a table" with the same values (#119) |
| Map | 1.1.1, 2.1.1 | Pass, partial | Region label plus "Show the map areas as a list" keyboard alternative (#119). Tile imagery is third-party |
| Tables | 1.3.1 | Pass, partial | Chart tables use `th scope`; other tables not audited |
| Redundant entry, consistent help, accessible authentication | 3.2.6, 3.3.7, 3.3.8 | Not tested | Sign-in uses Entra ID or a shared password in the demonstrator; not assessed |

### Contrast results

Computed with the WCAG relative luminance formula from the tokens in
`src/api/src/zava_forward/api/web/style.css`; reproduced by `test_accessibility_baseline.py`.

| Pair | Ratio | Needed |
| --- | --- | --- |
| Ink on page background | 13.7:1 | 4.5:1 |
| Muted text on white | 5.8:1 | 4.5:1 |
| White on brand | 7.5:1 | 4.5:1 |
| White on dark brand | 10.9:1 | 4.5:1 |
| Warning text on warning tint | 5.6:1 | 4.5:1 |
| OK text on OK tint | 5.8:1 | 4.5:1 |
| Field border on white | 3.8:1 | 3:1 |
| Focus outline on white | 13.7:1 | 3:1 |
| Caution marker on caution tint | 2.6:1 | 3:1 (gap G-2) |

## Automated checks

`src/api/tests/test_accessibility_baseline.py` runs with the existing unit test
discovery in `.github/workflows/mvp-ci.yml`. It checks page language and
viewport, the contrast ratios above, the focus indicator, the chart table
equivalent, the map list alternative and live regions, and that this record
exists. These are static checks, not a rendered-page scan.

Rendered-page scanning against key screens (axe-core through the existing
Playwright `src/api/checks/browser_check.py`) is not added: the browser check is a
manual script and the dependency choice needs the owner (O-2).

## Manual check record

Each cell holds Not run, or tester, date, tool and browser versions, criteria
checked, result and exceptions. Use one screen reader per OS, keyboard only,
at 320, 390 and 1280 px and 200% text size.

| Role workflow | Keyboard only | Screen reader | Zoom and reflow | Result |
| --- | --- | --- | --- | --- |
| Retrofit Coordinator | Not run | Not run | Not run | Not run |
| Resident Liaison Officer | Not run | Not run | Not run | Not run |
| Building Safety Liaison | Not run | Not run | Not run | Not run |
| Grants and Evidence Officer | Not run | Not run | Not run | Not run |
| Quality Inspector | Not run | Not run | Not run | Not run |
| Retrofit Programme Manager | Not run | Not run | Not run | Not run |
| Programme Support Officer | Not run | Not run | Not run | Not run |
| Contractor view | Not run | Not run | Not run | Not run |

Release rule (proposed, O-3): a release that changes a screen needs the
affected rows re-run and any new failure recorded or fixed.

### Map list alternative screen-reader check (#119)

Status at 2026-10-20: Not run. The unmet gate is a human or assistive-technology
run of the map list alternative; it stays open and is not met by any engineering
check below.

Tools found on the 2026-10-20 local host (Linux, no display, no audio device):
no screen reader is installed (no NVDA, Orca, VoiceOver, JAWS, eSpeak or
speech-dispatcher); `at-spi2-core` is present only as a library. Chromium is
available through Playwright for engineering checks. No axe-core package is
installed. Installing a desktop screen reader on the shared headless host was
judged outside scope, so no screen-reader run was attempted and none is claimed.

Existing engineering evidence is not a screen-reader run. In `src/api`,
`test_charts_and_map_have_accessible_equivalents` only checks that the text
"Show the map areas as a list" is in the script, and `test_status_regions_exist`
only checks that status and alert roles and `aria-live` appear in the page
source. The opt-in real-browser test documented in the API guide for the
coordinator map list exercises a keyboard route through the list. None of
these shows what a screen reader announces, and none establishes accessible
names, focus order after refresh or live-region behaviour.

Protocol for the human run (tester records name, date, tool and browser
versions, and result in the table above or an attached record):

* Use NVDA with Firefox on Windows or VoiceOver with Safari on macOS, with a
  synthetic-data session only, at 1280 px and 320 px and 200 percent text.
* Open Overview, find the map region, then the "Show the map areas as a list"
  disclosure. Check that it is discoverable by heading, landmark or form
  navigation, that its name is announced, and that it opens and closes with
  Enter or Space.
* At low zoom, check each cluster button announces count and safety count and
  "Zoom in to this area", that activating it moves the view, and that focus
  returns to the disclosure summary as designed.
* At high zoom, check each home link announces name and the non-colour signal
  label and opens the case.
* Check the polite status line announces results after a filter or pan, and
  the alert is announced when the map is unavailable, including with tiles
  blocked.
* Record anything unclear, such as focus loss after the list refreshes, as a
  finding, and do not treat a pass as WCAG conformance.

## Accessibility statement (draft)

Draft only. Not published and not approved; legal and owner review is needed
before use, and the public-sector accessibility regulations format should be
checked.

The Zava Forward workbench is an internal demonstrator that uses synthetic
data. We aim to meet WCAG 2.2 Level AA. We have not yet tested it with
assistive technology, so we do not claim conformance.

Known gaps at 2026-10-15:

* G-1: No screen reader, zoom, reflow or target size test has been completed.
* G-2: The caution map marker and the map marker shapes depend on colour; the
  key text and list alternative are the equivalent.
* G-3: Map tiles and the Leaflet library are third party and not assessed.
* G-4: Form errors, tables other than chart tables and sign-in were not fully
  audited.

To ask for another format or report a problem, contact: owner to supply (O-4).

## Open items

* O-1: Owner confirms the target level and scope.
* O-2: Owner chooses the rendered-page scanner for CI (axe-core suggested).
* O-3: Owner confirms the release rule and names manual testers, including
  people who use assistive technology.
* O-4: Contact route and enforcement or escalation wording for the statement.
* O-5: Re-retrieve WCAG 2.2 and any applicable accessibility regulation from
  the official source before external use.
