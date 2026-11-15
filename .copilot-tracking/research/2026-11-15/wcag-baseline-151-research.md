<!-- markdownlint-disable-file -->

# Task Research: wcag-baseline-151

| Field                | Value                                                              |
|----------------------|--------------------------------------------------------------------|
| Date                 | 2026-11-15                                                         |
| Researcher / agent   | RPI Agent (`rpi-research`)                                         |
| Status               | Complete                                                           |
| Artifact path        | .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md |
| Research disposition | executed                                                           |
| Planning Readiness   | Ready                                                              |

## Research Brief

* What to research: Complete inventory of all workbench HTML, CSS, and JavaScript surfaces (`src/api/src/zava_forward/api/web/`), every visual map, chart, funnel, bar/progress distribution, heatmap, or table widget (`#119` / `#151`), the current state and gaps across all 8 required WCAG 2.2 AA audit dimensions in `docs/reference/research/ux/wcag-conformance-baseline.md` (keyboard operation, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, and error identification), and deterministic automated verification coverage in `src/api/tests/`.
* Why it matters: Issue `#151` requires proving two acceptance criteria with engineering and audit rigor: (1) an audit covering keyboard, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, and error identification; and (2) accessible equivalents for the workbench map, charts, and tables (`#119`), without falsely claiming human screen-reader or assistive-technology acceptance.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this automatic RPI loop, plus reviewers verifying `#151` against `feat/demo-233-same-home-tensions-0825`.
* Scope: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `src/core/tests/test_scenario_manifest.py`, `src/core/tests/test_needs_inventory.py`, `tools/rename-zava-tests.py`.
* Non-goals: Claiming manual human screen-reader / assistive-technology conformance (human rows stay `Not run`, commit uses `Refs #151`), modifying `main`, or performing unrelated visual redesigns outside Fluent 2 tokens and WCAG 2.2 AA semantics.
* Criteria: Every visual map, chart, or visual distribution widget in the workbench has a synchronized, keyboard-reachable, screen-reader-accessible tabular/list equivalent with explicit headings, captions/`aria-label`s, and textual state meaning; `wcag-conformance-baseline.md` records a complete structured 8-dimension WCAG 2.2 AA workbench audit across all workbench HTML/CSS/JS files; deterministic automated tests in `src/api/tests/` assert both the 8-dimension audit coverage and map/chart/table accessible equivalents while preserving counted guards and `scenario-manifest.json` SHA checks.
* Requested outputs: Converged implementation recommendation for `rpi-plan` with exact `path:line` evidence and guard impact inventory.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q6 covering visual widgets/tables inventory, 8-dimension WCAG 2.2 audit gaps in code & docs, counted static/SHA guards, and test design |
| Codebase scope                       | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `src/core/tests/`, `docs/reference/`                      |
| External scope                       | Vercel Web Interface Guidelines (`command.md`) and W3C WCAG 2.2 specification via `accessibility` skill                              |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/*.html`, `*.css`, `*.js`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `src/api/tests/test_accessibility_baseline.py` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`, `https://www.w3.org/TR/WCAG22/`            |
| Research posture                     | balanced                                                                                                                            |
| Posture provenance                   | default (bounded internal audit and engineering hardening across workbench web assets, UX documentation, and automated unit tests)  |
| Explicit limits / deadline           | Focused validation tier (`ruff`, `mypy`, `node --check`, `src/core` + `src/api` focused tests, `tools/rename-zava-tests.py`)        |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence across all workbench web assets, 8 WCAG dimensions, and counted test/manifest guards  |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, plain-language content standard (#153), counted guards in `test_accessibility_baseline.py`, and `scenario-manifest.json` SHA bindings |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                 | Scoped authority or output contract                                   | Selected / skipped reason                                                       |
|---------------------|-----------------------------------|------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence paths | Enforces Fluent 2, WCAG 2.2 baseline, content standard, KB log, tiers | Selected: mandatory repository contract                                         |
| Skill               | `rpi-research`                    | Active phase skill for Research                      | Three-wave research artifact and readiness contract                   | Selected: active RPI phase                                                      |
| Skill               | `accessibility`                   | Domain match on WCAG 2.2 AA criteria and heuristics  | WCAG 2.2 SC roll-up and assessment heuristics                         | Selected: loaded at intake for 8-dimension WCAG 2.2 mapping                     |
| Skill               | `web-design-guidelines`           | Repository Web Development Guidance mandatory skill  | Fetched `command.md` rules for web edits and `file:line` review       | Selected: loaded and fetched via `web_fetch` at intake                          |
| Skill               | `redesign-existing-projects`      | Repository Web Development Guidance existing-app skill | Scan-diagnose-fix discipline subordinated to Fluent 2 and WCAG 2.2  | Selected: loaded per repo web guidance; aesthetic swaps subordinated to Fluent 2 |
| Research specialist | `hve-core-all:rpi-researcher`     | Host-registered specialist for independent lanes     | Delegated subagent lane markdown                                      | Skipped: tightly coupled workbench HTML/JS/CSS and Python guard trace is faster and exact inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                   | Answers / unanswered   | Resulting decision or selected further research                                 |
|------------------|---------------------------------------------------------------------------------------------------------|------------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller scope, branch, target base, acceptance criteria, and tests | N/A (non-interactive) | Proceed autonomously in confirmed automatic RPI mode with `balanced` posture and `convergence` output mode |
| Direction change | None; Cycle 1 findings stayed within caller scope (`web/`, `wcag-conformance-baseline.md`, KB index/log, `src/api/tests/`) | N/A | Retain active brief without expanding into unrelated files or SHA-pinned browser-manifest inputs |
| Convergence      | All 6 research questions answered with exact `path:line` evidence and contrarian guard verification | N/A | Converge on surgical workbench HTML/JS/CSS fixes, complete 8-dimension baseline audit, and deterministic static + Node VM DOM tests |

## Scope and Success Criteria

* Scope: All workbench HTML (`index.html`, `welcome.html`, `law.html`), CSS (`style.css`, `chat-widget.css`, `progress.css`), and JS (`app.js`, `role-screens.js`, `ops.js`, `panels.js`, `progress.js`, `aftercare.js`, `assistants.js`, `async-action.js`, `case-workspace.js`, `chat-widget.js`, `chat.js`, `law.js`, `simulator-control.js`, `staff-intake.js`, `timecapture.js`, `workspace-shell.js`) files under `src/api/src/zava_forward/api/web/`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, and `src/api/tests/`.
* Assumptions:
  * Some workbench visual widgets or tables (for example `progress.js` bars/charts, `ops.js` sensor tables, `app.js` funnel/heatmap/charts/map, `law.html`, or `role-screens.js` tables) may have gaps in captions, row/col headers, keyboard scroll regions, or synchronized accessible equivalents that Cycle 1 must verify line by line.
  * `wcag-conformance-baseline.md` currently leaves several rows partial/incomplete (e.g., `law.html` omitted from `lang`/zoom check, `ops.js` sensor table explicitly noted as unaudited without caption, reflow/zoom CSS rules and target-size primary 44px vs minimum 24px audit incomplete, focus order across modals/drawers/disclosures not systematically recorded).
* Success criteria:
  * Every research question Q1-Q6 is answered with exact `path:line` codebase evidence.
  * Every visual map, chart, distribution widget, and table across `src/api/src/zava_forward/api/web/` is inventoried and verified.
  * All 8 WCAG 2.2 AA audit dimensions are mapped to concrete code/CSS/HTML evidence and any engineering gaps are identified for remediation.
  * Counted guards and `scenario-manifest.json` SHA dependencies are verified so no regression is introduced.

## Task Research Requests

* Explicit requests:
  1. Verify and complete accessible equivalents for workbench map, charts, and tables (`#119` / `#151`), ensuring every visual map, chart, or visual distribution widget has a synchronized, keyboard-reachable, screen-reader-accessible tabular/list equivalent with explicit headings, captions/`aria-label`s, and textual state meaning.
  2. Complete and record the structured WCAG 2.2 AA workbench audit in `docs/reference/research/ux/wcag-conformance-baseline.md` (plus `docs/reference/README.md` and `docs/reference/log.md` if materially updated) covering all 8 required dimensions: keyboard operation, focus order and visibility, name/role/value, status messages, contrast, reflow and zoom, target size, and error identification.
  3. Add deterministic automated verification tests in `src/api/tests/` asserting both the 8-dimension WCAG 2.2 audit coverage and map/chart/table accessible equivalents across the workbench HTML/JS templates, updating `test_accessibility_baseline.py` and `scenario-manifest.json` if needed.
* Inferred research questions:
  * Which visual widgets (charts, map, progress bars, funnels, heatmaps, stage maps, gauges, SVG/canvas/bar elements) exist across every file in `src/api/src/zava_forward/api/web/`?
  * Which tables exist across every file in `src/api/src/zava_forward/api/web/` (including `innerHTML` or non-`h("table", {},` builders like `ops.js`, `progress.js`, `law.js`, `panels.js`, `role-screens.js`, `aftercare.js`, `app.js`), and do they all have captions/`aria-label`, `th scope="col"`, `th scope="row"` where appropriate, keyboard-scrollable `.table-scroll` wrappers, and textual state meaning?
  * Are there real WCAG 2.2 AA code defects across the 8 dimensions in `web/*.html`, `web/*.css`, and `web/*.js` that we should fix as part of `#151`?
  * Which existing tests in `src/api/tests/` guard exact counts, regexes, DOM structures, or file hashes?
* Caller constraints and non-goals: Focused validation tier; do not claim human screen-reader testing; do not push to `main`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint    | Effect on active brief, evidence, or revalidation                            |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier (`src/core` + `src/api` unit/focused tests, `ruff`, `mypy`, `node --check`, `rename-zava-tests.py`) | Caller prompt / Intake | Keep test design fast, deterministic (static + Node VM / ASGI), and focused |
| add                                                      | Audit all 8 WCAG 2.2 dimensions and all map/chart/distribution/table widgets across `web/`              | Caller prompt / Intake | Wave 1 must sweep all 22 HTML/CSS/JS files in `src/api/src/zava_forward/api/web/` |
| exclude                                                  | Do not claim human assistive-technology testing or push to `main`                                       | Caller prompt / Intake | Preserve `Not run` manual AT status and `we do not claim conformance` guard  |

## Research Questions

|  # | Sub-question                                                                                                                                          | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What HTML pages, CSS stylesheets, and JS modules make up the workbench in `src/api/src/zava_forward/api/web/`, and how are routes/views structured?   | breadth         | H        | answered |
| Q2 | What visual maps, charts, funnels, bar/meter distributions, stage maps, or SVG/canvas widgets exist across `web/`, and what accessible equivalents do they currently provide? | depth           | H        | answered |
| Q3 | What tables exist across `web/` (both `h("table"` and any other builders), and do all have captions/names, `scope="col"`/`scope="row"`, keyboard `.table-scroll` regions, and textual state meaning? | depth           | H        | answered |
| Q4 | Across the 8 WCAG 2.2 AA dimensions (keyboard, focus order/visibility, name/role/value, status messages, contrast, reflow/zoom, target size, error identification), what exact code/CSS evidence and engineering defects exist? | depth           | H        | answered |
| Q5 | What gaps or stale statements exist in `docs/reference/research/ux/wcag-conformance-baseline.md`, and how do `docs/reference/README.md` and `docs/reference/log.md` track UX KB updates? | straightforward | H        | answered |
| Q6 | What static counts, regex assertions, Node-VM harnesses, and `scenario-manifest.json` SHA bindings exist across `src/api/tests/` and `src/core/tests/` that constrain changes? | breadth         | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `src/api/tests/test_accessibility_baseline.py`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
* Reused (verified) findings:
  * `test_accessibility_baseline.py` currently checks `index.html` and `welcome.html` for `lang="en-GB"` and zoom, 10 text contrast pairs, 4 non-text contrast pairs, two-tone `:focus-visible`, basic strings in `app.js` for chart/map equivalents, 4 selector `min-height >= 24px` rules, `9` `aria-invalid` sites, `2` `position:fixed` rules, no drag handlers, `14` `h("table", {},` sites, and non-conformance wording in `wcag-conformance-baseline.md`.
  * `scenario-manifest.json` pins SHA-256 hashes of four specific files: `src/api/checks/workbench-manifest.json`, `src/api/checks/workbench_browser_check.py`, `src/core/tests/dataset.py`, and `src/api/tests/test_workbench.py`.
* Superseded / stale:
  * `wcag-conformance-baseline.md` has `Keyboard` marked `Not tested` even for engineering checks, omits `law.html` from page language/zoom, explicitly notes `ops.js` sensor table is excluded from the table regex and unaudited, leaves reflow/zoom CSS rules and primary 44x44px vs minimum 24x24px target-size engineering rules partially unrecorded, and has not consolidated recent role-screen/progress/aftercare/coordinator visual widgets into a complete workbench audit.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; sweep all 22 web assets and 8 WCAG 2.2 AA dimensions; preserve `Not run` human assistive-technology testing boundary (`Refs #151`, `Refs #119`).
* Active research posture and completion basis: `balanced`; scope coverage and adequate codebase + standards evidence across every workbench surface, WCAG dimension, and repository guard.
* Explicit limits or deadline effect: Keeps automated tests deterministic in `unittest` + Node `vm` without requiring external network or browser downloads at test time.

#### Wave 1: Wider

* Plan and independent lanes: Enumerate every HTML, CSS, JS, and vendor file under `src/api/src/zava_forward/api/web/`, map how routes and views render into `index.html` (`/app`, `/app?view=progress`), `welcome.html` (`/`), and `law.html` (`/law.html`), and catalogue all existing UX/accessibility tests in `src/api/tests/` and `src/core/tests/`.
* Worker evidence relationships or inline fallback: Inline investigation (tightly coupled file set; 22 non-vendor web files and 11 accessibility/UX test suites) establishing `C1`-`C6` and external references `W1`-`W2`.
* Reflection: All 19 HTML/JS files audited by `test_content_standard.py` (`AUDITED_FILES`) and all 3 custom stylesheets (`style.css`, `progress.css`, `chat-widget.css`) plus `vendor/leaflet.css` are accounted for. Identified 5 visual widget families and 15 script-built data tables requiring line-by-line Wave 2 inspection.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Line-by-line inspection of all visual widgets (Leaflet map, Overview SVG bar charts, Progress `<meter>` bar charts, 6-step case journey stepper, 8-stage role journey list, coordinator heatmap/funnel, KPI map-filter tiles), all 15 script-built `h("table"` tables, and all 8 WCAG 2.2 AA dimensions across HTML/CSS/JS.
* Plan and independent lanes: Inspect DOM construction, ARIA attributes, keyboard handlers, focus management, live regions, contrast pairs, 320 CSS px reflow/200% zoom rules, 24x24 / 40-44 CSS px target sizes, and form error associations across `app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, `aftercare.js`, `case-workspace.js`, `chat-widget.js`, `chat.js`, `assistants.js`, `staff-intake.js`, `simulator-control.js`, `timecapture.js`, `law.js`, `workspace-shell.js`, `async-action.js`, `index.html`, `welcome.html`, `law.html`, `style.css`, `progress.css`, `chat-widget.css`, and `vendor/leaflet.css`.
* Worker evidence relationships or inline fallback: Inline trace establishing `C7`-`C18`. Concrete engineering defects found:
  1. `ops.js:38` (`sensorTable`): only table in `web/` missing `<caption>` (uses `"aria-label": title` only) AND missing `.table-scroll` (`role="region"`, `tabindex="0"`) keyboard horizontal-scroll wrapper (`C10`).
  2. Five more multi-column tables lack `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) for 320 CSS px reflow AND use `<td>` instead of `<th scope="row">` for their row-identifying first column: `ops.js:475` (`packagesView` contractor capacity), `panels.js:143` (`technicalPanel` sign-offs), `panels.js:232` (`residentPanel` measure decisions), `panels.js:590` (`financeQueueView` invoices), and `app.js:2926` (`fundingView` applications); plus `app.js:2898` (`Contractors`) and `app.js:2902` (`Team workload`) have `.table-scroll` and `<caption>` but use `<td>` instead of `<th scope="row">` (`C10`, `C11`, `C12`).
  3. `app.js:2426` (`bars` SVG horizontal bar charts on `#/overview`): all 5 chart disclosures use identical `<summary>Show this chart as a table</summary>` without naming the chart, lack `.table-scroll` (`role="region"`, `tabindex="0"`) around the inner `<table>`, and render an empty `<tbody>` if `data.length === 0` (`C8`).
  4. `app.js:2565` (`mapPanel` `renderList`): when `d.items` is empty (0 mapped homes in current filter/bounds), `<details class="maplist">` contains an empty `<ul class="plainlist">` with no plain-language empty-state explanation (`C7`).
  5. `progress.js:58` (`chart` visual `<meter>` distribution on `/app?view=progress`): `<meter min="0" max="..." value="..." tabindex="-1">` has no accessible name (`aria-label` or `<label>`), failing WCAG 4.1.2 Name, Role, Value (`aria-meter-name`), and `tableWrap` has no explicit empty-row fallback when `rows.length === 0` (`C9`).
  6. Target Size (`style.css` & `vendor/leaflet.css`): bare `<details> > <summary>` disclosures (`panels.js`, `ops.js`, `assistants.js`, `staff-intake.js`, `.chart-data summary`) lack a baseline `min-height: 1.5rem` (`24px`) rule (dropping to `21.6px` inside `.case-summary` `line-height: 1.35` at `<=600px`), standalone checkboxes/radios outside `.regulatory-mode` lack `min-width/min-height: 1.5rem`, and desktop Leaflet `.leaflet-bar a` defaults to `26x26px` in `vendor/leaflet.css:291` instead of workbench `2.5rem` (`40x40px`) (`C14`, `C15`).
* Reflection: Every defect above is surgical, improves genuine WCAG 2.2 AA conformance across `#119` and `#151`, and preserves Fluent 2 visual tokens. Next, Wave 3 must challenge each proposed edit against counted repository tests, content-standard vocabulary bans, AST/slice harnesses, and Playwright browser checks.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether any proposed HTML/JS/CSS or documentation edit violates pinned counts, substring slices, forbidden jargon, browser acceptance contracts, or `scenario-manifest.json` SHA-256 hashes.
* Plan and independent lanes: Audit `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_*.py`, `test_finance_exposure_screen.py`, `test_scenario_manifest.py`, `employee_acceptance_check.py`, `map_fullscreen_browser_check.py`, and `design_system_browser_check.py`.
* Worker evidence relationships or inline fallback: Inline contrarian audit (`C19`-`C24`) uncovered 5 critical constraints that materially shaped the safe implementation design:
  1. **Critical Map List Contract (`employee_acceptance_check.py:276-280`, `C19`)**: `MAP_RENDERED` asserts `same([...panel.querySelectorAll('.maplist li')].map(e => e.textContent), expected.labels)`, where `expected.labels` is `[]` when `total == 0` and `${name}, ${MAP_LABELS[kind]}` for points! Adding an `<li>` inside `.maplist ul` when `d.items` is empty OR altering point `<li>` text would break `employee_acceptance_check.py`! Solution: keep `<ul class="plainlist">` `<li>` items byte-identical and render a sibling `<p class="muted maplist-empty">` inside `<details class="maplist">` (hidden when `d.items.length > 0`, shown when `d.items.length === 0`).
  2. **Pinned `aria-invalid` Count (`test_epic149_form_error_summary_associations.py:19-60`, `C20`)**: Both `test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py` pin `setAttribute("aria-invalid", "true")` to exact count `9` (and `test_epic149_form_error_summary_associations.py` literally asserts `"self.assertEqual(sites, 9,"` appears in `test_accessibility_baseline.py`!). Therefore, keep the exact 9 `setAttribute("aria-invalid", "true")` sites intact.
  3. **Substring Slice in `panels.js` (`test_finance_exposure_screen.py:15`, `C21`)**: Slices `panels.js` from `function exposureNotice` to `\n}\n` after `async function financeQueueView`. Keeping `financeQueueView`'s closing `\n}\n` at column 0 preserves this harness.
  4. **Pinned Substrings & Counts (`test_accessibility_baseline.py:67,108`, `test_content_standard.py:16-31`, `C22`, `C23`)**:
     * `"Show this chart as a table"` must remain an exact substring in `app.js` -> use `h("summary", {}, "Show this chart as a table", h("span", { class: "sr-only" }, `: ${title}`))` so visual text stays concise, substring check passes, and screen readers announce `"Show this chart as a table: Cases by stage"`.
     * `h("table", {},` count increases cleanly from `14` to `15` when `ops.js:38` `sensorTable` gains `h("table", {}, h("caption", { class: "sr-only" }, title), ...)` -> update `test_accessibility_baseline.py` from `14` to `15` and update `wcag-conformance-baseline.md` + `docs/reference/README.md` table inventory from `14` to `15` (0 unaudited script tables!).
     * `AUDITED_FILES` in `test_content_standard.py` pins the exact 19 `.html`/`.js` filenames in `web/` and forbids `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, `envelope(s)` anywhere in `web/*.html` and `web/*.js` (even comments!).
  5. **Guarded Phrases in `wcag-conformance-baseline.md` (`test_epic149_ux_evidence_results.py` & `test_epic149_ux_journey_requirement_traceability.py`, `C24`)**: Must preserve every required non-conformance phrase, existing requirement IDs, valid relative links, and existing `test_*.py` module references without `@unittest.skip`.
* Reflection: Contrarian wave prevented breaking `employee_acceptance_check.py`, `test_epic149_form_error_summary_associations.py`, `test_finance_exposure_screen.py`, and `test_content_standard.py`. No unresolved contradictions remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|--------------------|--------------------------|----------------------------|
| Upgrade `ops.js` `sensorTable` with `<caption>` + `.table-scroll` and update counted baseline `14 -> 15` | `C10, C22` | accepted | Eliminates the last uncaptioned table in `web/` and fixes 320px horizontal overflow | Core implementation item |
| Add `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) + `<th scope="row">` across remaining multi-column tables in `ops.js`, `panels.js`, `app.js` | `C10, C11, C12, W1` | accepted | Prevents WCAG 1.4.10 horizontal page scroll at 320 CSS px and provides WCAG 1.3.1 programmatic row headers | Core implementation item |
| Disambiguate Overview chart `<summary>` names with `.sr-only` chart title, wrap inner table in `.table-scroll`, and add empty-data fallback row | `C8, C22, W1` | accepted | Preserves `"Show this chart as a table"` substring while disambiguating all 5 chart disclosures and fixing empty/narrow states | Core implementation item |
| Add sibling `<p class="muted maplist-empty">` inside `<details class="maplist">` when `d.items.length === 0` without altering `.maplist li` | `C7, C19` | accepted | Closes blank screen-reader list state on 0-home map views while keeping `.maplist li` 100% compatible with `employee_acceptance_check.py` | Core implementation item |
| Add explicit `aria-label` on `<meter>` bars and empty-row fallback in `progress.js` | `C9, W1, W2` | accepted | Satisfies WCAG 4.1.2 Name, Role, Value on `<meter>` elements alongside synchronized `tableWrap` data tables | Core implementation item |
| Harden `style.css` target sizes (`details > summary`, standalone checkbox/radio, `.leafmap .leaflet-bar a` + `:focus-visible`) and include `law.html` in baseline tests | `C2, C14, C15, W1, W2` | accepted | Ensures >= 24x24 CSS px minimum across disclosures/inputs and 40x40 CSS px on Leaflet zoom controls | Core implementation item |
| Altering `.maplist li` text or adding a 10th `setAttribute("aria-invalid", "true")` site | `C19, C20` | rejected | Would break `employee_acceptance_check.py` `MAP_RENDERED` and `test_epic149_form_error_summary_associations.py` pinned 9-site assertion | Rejected via Contrarian Wave |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Scope saturation — all 22 web assets, all 8 WCAG 2.2 AA dimensions, `wcag-conformance-baseline.md`, and all guarding test suites have been inspected line by line with zero remaining codebase unknowns.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: `inline: tightly coupled 22-file web asset directory and counted Python guard suites inspected directly with deterministic grep/view sweeps`

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | Primary workbench shell declares `lang="en-GB"`, scalable viewport, `.skip-link` to `#app`, `<header>`, `<nav id="nav" aria-label="Primary">`, `#workspace-status` polite region, and `<main id="app" tabindex="-1">` | `src/api/src/zava_forward/api/web/index.html:2` | view | high | Core `/app` shell landmarks and focus target |
| C2 | Entry and law reference pages declare `lang="en-GB"` and scalable viewport (`width=device-width, initial-scale=1` with no `maximum-scale` or `user-scalable=no`); `law.html` was not yet asserted in `test_accessibility_baseline.py` | `src/api/src/zava_forward/api/web/law.html:2` | view | high | Single-purpose pages (`NO_SKIP_LINK = {"/", "/law.html"}` in `test_epic149_landmarks_skip_link_focus_order.py:21`) |
| C3 | Design tokens define Fluent 2 palette (`#242424`, `#424242`, `#0b5d6b`, `#08434d`, `#b42318`, `#1a6b3a`, `#7a858d`), two-tone focus ring (`outline: 3px solid #f2a900; box-shadow: 0 0 0 5px #1f2933`), reduced-motion zeroing, and `rem`-based typography | `src/api/src/zava_forward/api/web/style.css:1` | view | high | Verified contrast pairs >= 4.5:1 text and >= 3:1 UI/focus |
| C4 | Reflow rules collapse multi-column grids below `900px`/`700px`/`600px`, constrain media/dialogs (`max-width: 100%`), wrap `.table-scroll` with `overflow-x: auto`, and convert `.stepper` to vertical list at `<=900px` | `src/api/src/zava_forward/api/web/style.css:87` | view | high | Also `style.css:169,205,228` and `progress.css:20` |
| C5 | Floating assistant widget uses the only 2 `position:fixed` rules in `web/*.css`, supports keyboard Escape/Minimize/Dock/Resize (`Arrow*` keys on `role="separator"`), `role="log"`, and collapses within `320px` viewports at `@media(max-width:599px)` | `src/api/src/zava_forward/api/web/chat-widget.css:1` | view | high | Paired with `chat-widget.js:42-182` |
| C6 | Route focus order moves focus cleanly to `#main-heading` (`tabindex="-1"`) or preserved reset target on navigation, announces busy/ready states via `#workspace-status`, and cancels stale route loads | `src/api/src/zava_forward/api/web/app.js:338` | view | high | Paired with `workspace-shell.js:76` |
| C7 | `mapPanel` provides keyboard pan/zoom (`Arrow*`, `+`/`=`/`-`), shape+letter markers (`O`, `W`, `!`), modal `<dialog>` with focus return, live `info`/`tileNote` status, `"Show these as a list"`, and `<details class="maplist">`, but `renderList` leaves `<details class="maplist">` silent when `d.items` is empty | `src/api/src/zava_forward/api/web/app.js:2470` | view | high | `renderList` at `app.js:2565` |
| C8 | `bars(title, data, link)` renders 5 Overview SVG bar charts (`role="img"`, `aria-label`) paired with `<details class="chart-data"><summary>Show this chart as a table</summary><table>...`, missing per-chart summary disambiguation, `.table-scroll` region wrapper, and empty-data fallback row | `src/api/src/zava_forward/api/web/app.js:2426` | view | high | Used on `#/overview` (`app.js:2889-2895`) |
| C9 | `progress.js` `chart(title, columns, rows)` renders 6 `<ul class="bars">` widgets with `<meter min="0" max="..." value="..." tabindex="-1">` lacking an accessible name (`aria-label`), paired with `tableWrap` (`role="region"`, `tabindex="0"`, `<caption>`, `<th scope="col">`, `<th scope="row">`) | `src/api/src/zava_forward/api/web/progress.js:52` | view | high | `/app?view=progress` dashboard |
| C10 | `ops.js` `sensorTable` uses `h("table", { "aria-label": title }, ...)` without `<caption>` and without `.table-scroll`; `ops.js:475` (`packagesView`) also lacks `.table-scroll` and `<th scope="row">` | `src/api/src/zava_forward/api/web/ops.js:38` | view | high | Explicitly listed as unaudited in `wcag-conformance-baseline.md:78` |
| C11 | `panels.js` has 3 multi-column tables (`technicalPanel` at `143`, `residentPanel` at `232`, `financeQueueView` at `590`) missing `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) and `<th scope="row">` on row-identifying first cells | `src/api/src/zava_forward/api/web/panels.js:143` | view | high | Causes horizontal overflow at 320 CSS px |
| C12 | `app.js` `fundingView` (`2926`) lacks `.table-scroll` and `<th scope="row">`; `overviewView` `Contractors` (`2898`) and `Team workload` (`2902`) have `.table-scroll` and `<caption>` but use `<td>` instead of `<th scope="row">` | `src/api/src/zava_forward/api/web/app.js:2898` | view | high | Coordinator heatmap (`2805`), funnel (`2819`), aftercare (`93`), and role-screens (`511, 525, 1621`) already have both |
| C13 | Case 6-step retrofit stepper (`case-workspace.js:97`), 8-stage role journey list (`role-screens.js:647`), and Overview KPI filter tiles (`app.js:2872`) expose semantic lists/groups, `aria-current="step"` / `aria-pressed`, and visible plain-text state labels | `src/api/src/zava_forward/api/web/case-workspace.js:97` | view | high | Non-colour status signals verified |
| C14 | Bare `<details> > <summary>` elements lack a global `min-height: 1.5rem` (`24px`) rule in `style.css` (shrinking to `21.6px` inside `.case-summary` at `<=600px`), and standalone checkboxes/radios outside `.regulatory-mode` lack `1.5rem` box sizing | `src/api/src/zava_forward/api/web/style.css:228` | view | high | WCAG 2.5.8 Target Size (Minimum) hardening |
| C15 | Non-touch Leaflet zoom links `.leaflet-bar a` default to `26x26px` without workbench `:focus-visible` ring override unless scoped in `style.css` | `src/api/src/zava_forward/api/web/vendor/leaflet.css:291` | view | high | `.leafmap .leaflet-bar a` can be upgraded to `2.5rem` (`40x40px`) |
| C16 | All 9 `setAttribute("aria-invalid", "true")` sites pair `aria-describedby` with plain-language inline error elements (`role="status"` / `role="alert"`) and clear `aria-invalid` on valid input/reset | `src/api/tests/test_epic149_form_error_summary_associations.py:19` | view | high | Verified across `assistants.js`, `ops.js`, `progress.js`, `app.js`, `panels.js`, `role-screens.js`, plus `aftercare.js:129` |
| C17 | Live status regions (`role="status"` / `role="log"` / `role="alert"` with `aria-live="polite"`) cover route loading, filter/page counts, async button actions (`async-action.js:10`), map counts, held-case checks, AI draft counts, and chat messages | `src/api/src/zava_forward/api/web/async-action.js:1` | grep/view | high | 30+ polite status/log regions inventoried across 12 JS modules |
| C18 | `wcag-conformance-baseline.md` currently records partial initial-audit rows (`Keyboard: Not tested`, 14 of 15 tables, partial reflow/target-size coverage) while establishing strict non-conformance wording | `docs/reference/research/ux/wcag-conformance-baseline.md:27` | view | high | Needs structured 8-dimension workbench audit + complete widget/table register |
| C19 | `employee_acceptance_check.py` `MAP_RENDERED` asserts `.maplist li` `textContent` array equals `expected.labels` (`[]` when 0 homes, `${name}, ${MAP_LABELS[kind]}` on points) | `src/api/checks/employee_acceptance_check.py:274` | view | high | Empty-state copy in `.maplist` must use `<p>` outside `<ul>`, never an extra `<li>` |
| C20 | `test_epic149_form_error_summary_associations.py` pins exact 9 `SITES` and asserts `"self.assertEqual(sites, 9,"` literally appears in `test_accessibility_baseline.py` | `src/api/tests/test_epic149_form_error_summary_associations.py:57` | view | high | Keep `self.assertEqual(sites, 9, ...)` unchanged |
| C21 | `test_finance_exposure_screen.py` slices `panels.js` from `function exposureNotice` to `\n}\n` at the end of `async function financeQueueView` | `src/api/tests/test_finance_exposure_screen.py:14` | view | high | Preserve column-0 closing `}` of `financeQueueView` |
| C22 | `test_accessibility_baseline.py` pins `"Show this chart as a table"` in `app.js`, `2` `position:fixed` rules, `0` `outline:none/0`, reduced-motion guard, and counted `h("table", {},` (`14 -> 15`) | `src/api/tests/test_accessibility_baseline.py:67` | view | high | Update table count `14 -> 15` when `ops.js` `sensorTable` gains `<caption>` |
| C23 | `test_content_standard.py` pins the exact 19 `.html`/`.js` filenames in `web/` and bans `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, `envelope(s)` across all lines | `src/api/tests/test_content_standard.py:16` | view | high | Do not add new files in `web/` or use banned jargon |
| C24 | `test_epic149_ux_evidence_results.py`, `test_epic149_ux_journey_requirement_traceability.py`, and `test_scenario_manifest.py` guard required disclaimers, cited test modules, requirement IDs, relative links, and 4 SHA-256 manifest files | `src/api/tests/test_epic149_ux_evidence_results.py:35` | view | high | Do not claim conformance; keep all cited tests real and unskipped |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Web Interface Guidelines require visible `:focus-visible`, accessible names on all controls/landmarks/meters, polite status announcements, tabular numerals, explicit labels/error bindings, safe reflow, and `prefers-reduced-motion` | Vercel Web Interface Guidelines (`command.md`) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main (live fetch) | high |
| W2 | WCAG 2.2 Level AA normative success criteria for non-text equivalents (`1.1.1`, `1.3.1`), contrast (`1.4.3`, `1.4.11`), resize/reflow (`1.4.4`, `1.4.10`), keyboard & focus (`2.1.1`, `2.1.2`, `2.4.3`, `2.4.7`, `2.4.11`), target size (`2.5.8` >= 24x24 CSS px), error identification (`3.3.1`, `3.3.2`), and name/role/value + status messages (`4.1.2`, `4.1.3`) | W3C Web Content Accessibility Guidelines (WCAG) 2.2 | https://www.w3.org/TR/WCAG22/ | 2026-11-15 | W3C Recommendation | high |

### Contradictions / Conflicts

* `redesign-existing-projects` generic typography/aesthetic advice (replacing system/Fluent fonts or reworking dashboard layouts) vs repository custom instructions (`Preserve the owner-selected Fluent 2 design system, WCAG baseline and plain-language content standard over generic aesthetics`): resolved by extension precedence rule 3 > 5 -> keep Fluent 2 tokens and existing stack intact, applying only WCAG 2.2 AA semantic, reflow, target-size, and accessible-equivalent improvements.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | The workbench comprises 3 HTML entrypoints (`index.html`, `welcome.html`, `law.html`), 3 stylesheets (`style.css`, `progress.css`, `chat-widget.css`), 16 JS modules, and vendored Leaflet (`vendor/leaflet.js`, `vendor/leaflet.css`). | `C1, C2, C3, C5, C23` | high | Complete 22-file audit scope locked; no new files in `web/` so `AUDITED_FILES` stays 19. |
| Q2 | Five visual widget families exist: (a) Leaflet map (`app.js:2470`), (b) 5 Overview SVG horizontal bar charts (`app.js:2426`), (c) 6 Progress `<meter>` bar charts (`progress.js:52`), (d) 6-step case stepper & 8-stage role journey list (`case-workspace.js:97`, `role-screens.js:647`), and (e) Overview KPI map-filter tiles & Coordinator heatmap/funnel (`app.js:2797-2872`, `role-screens.js:525`). Three targeted gaps exist: silent empty `.maplist` when 0 homes (`C7`), undifferentiated chart `<summary>` labels + missing `.table-scroll`/empty row in `bars()` (`C8`), and unnamed `<meter>` elements + empty row handling in `progress.js` (`C9`). | `C7, C8, C9, C13, C19, W2` | high | Remediate all 3 widget gaps in `app.js` and `progress.js` and verify in Node VM DOM tests. |
| Q3 | Fifteen script-built tables exist across `web/*.js` (`1` in `ops.js` `sensorTable` without `<caption>`, plus `14` `h("table", {}, h("caption", ...)`). Six multi-column tables lack `.table-scroll` (`role="region"`, `tabindex="0"`, `aria-label`) and eight tables use `<td>` instead of `<th scope="row">` for row-identifying first cells. | `C10, C11, C12, C21, C22` | high | Upgrade all 15 script-built tables to have `<caption>`, `<th scope="col">`, `<th scope="row">` on row headers, and `.table-scroll` (`role="region"`, `tabindex="0"`) wrappers; update baseline count `14 -> 15`. |
| Q4 | Across the 8 WCAG 2.2 AA dimensions: keyboard, focus order/visibility, status messages, contrast, and error identification have strong implementations (`C1, C3, C5, C6, C16, C17`), while name/role/value (`progress.js` `<meter>` name, `ops.js` `sensorTable` caption, `<th scope="row">`), reflow/zoom (6 unwrapped tables, `law.html` zoom test gap), and target size (`details > summary`, standalone checkboxes/radios, `.leafmap .leaflet-bar a`) have concrete, fixable gaps. | `C1-C17, W1, W2` | high | Fix code/CSS gaps and record all 8 dimensions with file/line evidence + honest manual boundaries in `wcag-conformance-baseline.md`. |
| Q5 | `wcag-conformance-baseline.md` lacks a complete structured 8-dimension workbench audit table/sections covering all 22 web files and all visual widgets/tables, still lists `ops.js` sensor table as unaudited, and omits `law.html`; `docs/reference/README.md` (line 1076) and `docs/reference/log.md` track material updates. | `C18, C24` | high | Update `wcag-conformance-baseline.md`, `docs/reference/README.md`, and append to `docs/reference/log.md` while keeping all guarded non-conformance phrases intact. |
| Q6 | Guard checks constrain `.maplist li` (`C19`), `sites == 9` `aria-invalid` count (`C20`), `financeQueueView` closing brace (`C21`), `"Show this chart as a table"` substring (`C22`), 19 `AUDITED_FILES` & plain-language vocabulary (`C23`), UX evidence traceability (`C24`), and 4 SHA-pinned manifest files. | `C19-C24` | high | Design implementation and `test_wcag_workbench_baseline_151.py` to satisfy every guard cleanly. |

## Key Discoveries

* Upgrading `ops.js:38` `sensorTable` to include `<caption class="sr-only">` and `.table-scroll` closes the explicit unaudited table gap in `wcag-conformance-baseline.md` and brings script-built captioned tables to 15 of 15 across `web/*.js` (`C10`, `C22`).
* `employee_acceptance_check.py` compares `.maplist li` text directly against `expected.labels` (`[]` on zero-home filters), so the zero-home accessible explanation inside `<details class="maplist">` must be rendered as a `<p class="muted maplist-empty">` sibling rather than an `<li>` (`C7`, `C19`).
* `progress.js` `<meter>` elements (`C9`), six unwrapped multi-column tables (`C10`-`C12`), and disclosure `<summary>` / Leaflet zoom control target sizes (`C14`, `C15`) can all be fixed deterministically in vanilla JS/CSS and verified via both static AST/regex tests and Node `vm` DOM execution in `src/api/tests/test_wcag_workbench_baseline_151.py`.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Execute a four-part surgical engineering + audit update:
  1. Complete map, chart, and table accessible equivalents and WCAG 2.2 AA fixes in `app.js`, `progress.js`, `ops.js`, `panels.js`, and `style.css` without adding new files in `web/` or touching SHA-pinned manifest inputs.
  2. Expand `docs/reference/research/ux/wcag-conformance-baseline.md` with a structured 8-dimension WCAG 2.2 AA workbench audit and complete visual-widget/table accessible-equivalents inventory across all workbench routes, updating `docs/reference/README.md` and appending to `docs/reference/log.md` while preserving all non-conformance boundaries (`Not run` for human assistive-technology sign-off).
  3. Update `src/api/tests/test_accessibility_baseline.py` (`law.html` `lang`/zoom check, table count `14 -> 15`, target-size selector coverage) while keeping `self.assertEqual(sites, 9, ...)` intact.
  4. Add `src/api/tests/test_wcag_workbench_baseline_151.py` testing both the 8-dimension WCAG 2.2 audit documentation/code invariants and Node `vm` DOM rendering of `bars()`, `mapPanel()`/`renderList()` (clusters, points, and empty states), `progress.js` `chart()`/`tableWrap()` (`<meter aria-label>` and synchronized tables), and all 15 script-built tables' `.table-scroll` / `<caption>` / `<th scope="col">` / `<th scope="row">` contracts.
* Rationale: Proves both `#151` acceptance criteria end to end with runtime-executed Node DOM assertions and static CSS/HTML/JS/Markdown invariants while respecting every repository guard (`C19`-`C24`).
* Evidence refs: `C1`-`C24`, `W1`, `W2`
* Implementation impact: Modifies 5 web files (`app.js`, `progress.js`, `ops.js`, `panels.js`, `style.css`), 3 documentation files (`wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`), and 2 test files (`test_accessibility_baseline.py` edit + new `test_wcag_workbench_baseline_151.py`).
* Confidence: `high`: Every affected line and repository guard has been verified directly in source.

File tree:

```text
docs/reference/
  README.md                                      (modify)
  log.md                                         (modify - append entry)
  research/ux/wcag-conformance-baseline.md       (modify)
src/api/
  src/zava_forward/api/web/
    app.js                                       (modify)
    ops.js                                       (modify)
    panels.js                                    (modify)
    progress.js                                  (modify)
    style.css                                    (modify)
  tests/
    test_accessibility_baseline.py               (modify)
    test_wcag_workbench_baseline_151.py          (create)
```

### Alternative: Documentation-Only Audit Without Fixing Workbench Table/Meter/Target-Size Gaps

* Approach: Record the missing `ops.js` table caption, unwrapped tables, unnamed `<meter>` elements, and silent empty `.maplist` as open defects in `wcag-conformance-baseline.md` without modifying `web/`.
* Trade-offs: Zero JS/CSS edit risk, but leaves real WCAG 2.2 AA / `#119` accessible-equivalent defects unfixed when the prompt explicitly instructs us to "Verify and complete the accessible equivalents for the workbench map, charts, and tables (`#119` / `#151`)".
* Evidence refs: `C7`-`C15`
* Rejection rationale: Fails caller requirement 1 to complete accessible equivalents across map, charts, and tables.

### Alternative: Full Playwright Chromium Harness Inside Unit Tests

* Approach: Launch headless Chromium in `test_wcag_workbench_baseline_151.py`.
* Trade-offs: Measures browser layout boxes directly, but browser tests are skipped or environment-gated in focused `unittest` runs and slower/fragile in shared environments.
* Evidence refs: `C19`, `C24`
* Rejection rationale: Focused validation tier requires deterministic `unittest` tests that always run (`0` `@unittest.skip`, required by `test_epic149_ux_journey_requirement_traceability.py` if cited in UX docs!). Combining Node `vm` DOM execution + CSS token/geometry parser + HTML/JS static checks runs fast and deterministically with zero skips.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Human assistive-technology walkthroughs (NVDA, JAWS, VoiceOver, TalkBack, Dragon/Voice Control, real browser 200%/400% zoom) and owner confirmation of `O-1` (WCAG 2.2 AA target and third-party map tile boundary) remain human gates outside automated checks (`Refs #151`, `Refs #119`).
* Follow-up: Extending automated runtime axe-core scans in hosted CI (`#155` / accessibility coverage matrix) and closing remaining `NO_SKIP_LINK` / `NO_FIELD_FOCUS` shrink-only items in separate focused slices.
* Residual uncertainty: Computed pixel dimensions of subpixel font metrics depend on the user's OS font rasterizer; CSS `min-height` / `min-width` in `rem` guarantees minimum box dimensions independent of glyph metrics, while real browser rendering remains honestly marked for human/browser verification.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Remediate all identified map, chart, `<meter>`, table, reflow, and target-size engineering gaps across `app.js`, `progress.js`, `ops.js`, `panels.js`, and `style.css` | confirmed | Evidence / caller scope | Fulfils `#151` / `#119` accessible equivalents and 8-dimension WCAG 2.2 AA audit criteria cleanly | `C7-C15, W1, W2` | Updates `h("table", {},` baseline count from `14` to `15` |
| Preserve `.maplist li` DOM contract and `sites == 9` `aria-invalid` count | confirmed | Repository test guards | Required by `employee_acceptance_check.py` and `test_epic149_form_error_summary_associations.py` | `C19, C20` | Render `.maplist` empty notice as `<p class="muted maplist-empty">` outside `<ul>` |
| Preserve `Not run` human assistive-technology status and `Refs #151` commit linkage | confirmed | Repository instructions & UX test guards | Automated static/Node DOM checks are engineering evidence, not WCAG 2.2 conformance or human AT sign-off | `C18, C24` | Retains all guarded phrases in `wcag-conformance-baseline.md` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Owner confirmation `O-1` of WCAG 2.2 AA target and third-party map tile boundary | Explicit owner sign-off on issue `#151` | Repository owner | Governs formal conformance target ratification; does not block engineering audit or tests | follow-up |
| Manual assistive-technology and browser zoom sign-off across roles | Named human tester session with NVDA/VoiceOver/keyboard at 200%/400% zoom | Human tester / owner | Required before closing `#151` or claiming WCAG 2.2 AA conformance | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Runtime Playwright axe-core coverage matrix config (`a11y-runtime.config.json`) | Automates live-browser contrast/target-size probes in hosted CI | Follow-up work after `#151` baseline lands | deferred | `Q4, Q6; C22, C24` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on surgical 5-file web remediation, structured 8-dimension WCAG 2.2 AA audit in `wcag-conformance-baseline.md` (+ KB index/log), updated `test_accessibility_baseline.py`, and new unskipped deterministic suite `test_wcag_workbench_baseline_151.py`.
* Evidence basis: `C1`-`C24`, `W1`, `W2`
* Preconditions met: Complete 22-file codebase inventory, 3-wave cycle completed, contrarian guard compatibility verified, focused validation commands known.
* Blockers: none
* Smallest action to change readiness: none (ready to transition to `Plan`).

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Cycle 1: Wider, Deeper, and Contrarian |
| Lane evidence or inline fallback | Inline across all 22 workbench files and 11 test/check suites (tightly coupled invariants) |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C24`, `W1`, `W2`) |
| Blockers | none |
| Continuation owner and state | Confirmed automatic RPI Agent; automatic continuation to `Plan` |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C24`, `W1`, `W2`) |
| Output mode and planning support | `convergence`; yes — concrete file/line targets and guard constraints established |
| Acting owner | Confirmed automatic RPI Agent |
| Required gates or confirmations | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), 3 waves complete (`passed`), pre-transition state write (`passed`) |
| Continuation result | Automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md |
| Notes for planning or re-entry | Plan phases should separate web accessible-equivalent/WCAG fixes, KB baseline audit documentation, and deterministic automated tests + focused validation, followed by one-pass `rpi-plan-critique`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All 22 workbench files, 8 WCAG 2.2 dimensions, and repository guard suites are completely mapped; further research would be redundant.

## Sources

* Codebase: `src/api/src/zava_forward/api/web/*`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_*.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_finance_exposure_screen.py`, `src/api/checks/employee_acceptance_check.py`, `src/core/tests/test_scenario_manifest.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* External: Vercel Web Interface Guidelines (`W1`, retrieved 2026-11-15), W3C WCAG 2.2 Recommendation (`W2`, retrieved 2026-11-15).

## Self-Check

* [x] Research Brief, Parameters, Extension Registry, Direction Controls, and Prior Knowledge Gate completed.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order with explicit reflection and parent disposition.
* [x] Every codebase finding cites a workspace-relative `path:line` (`C1`-`C24`) and external sources cite URL + retrieval date (`W1`-`W2`).
* [x] Zero production/source files were edited during Research.
* [x] Planning Readiness (`Ready`) and Research disposition (`executed`) are recorded consistently.

