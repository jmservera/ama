<!-- markdownlint-disable-file -->

# Task Research: map-filters-551

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/map-filters-551-research.md |

## Research Brief

* What to research: issue #551 expanded-map filters, shared header state, marker updates and existing browser coverage.
* Why: deliver compact, keyboard-operable controls without divergent filter state.
* Audience: implementer and independent reviewer.
* Scope: src/api web assets, tests/checks outside the package, component documentation.
* Non-goals: Azure, deployment, pushes, framework changes, unrelated design work.
* Criteria: all four issue criteria, Fluent 2 tokens, native controls, non-colour state, narrow reflow and reduced motion.
* Requested outputs: dated Research, Plan, Implement and Review artifacts and local commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Where do filters live, how does fullscreen map rendering work, and what tests prove synchronization? |
| Codebase scope | src/api/src/zava_forward/api/web; src/api/tests; src/api/checks |
| External scope | Required Web Interface Guidelines source only |
| Initial internal candidate areas | app.js, map code, style.css, API README and checks |
| Initial external candidate areas | vercel-labs/web-interface-guidelines command.md |
| Research posture | focused |
| Posture provenance | Default for bounded issue with named source targets |
| Explicit limits | No az, Azure changes, push or rubric score edits; use /tmp/mv; local real-browser verification |
| Completion basis | Material questions and acceptance criteria covered with source evidence |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository guidance | Supplied AMA instructions, all files | Selected: branch, evidence, local gate and privacy-safe commit rules |
| Skill | rpi-research | Loaded installed plugin | Selected: ordered three-wave research |
| Skill | web-design-guidelines | .github/skills/web-design-guidelines | Selected and source fetched 2026-10-29 |
| Skill | design-taste-frontend | Public pages only | Skipped: existing application, not public-page work or redesign |
| Specialist | RPI Researcher | Registered host agent | Skipped: one tightly coupled investigation, handled inline |

## User Participation and Research Decisions

User explicitly requests the full ordered RPI loop and no push. This is a bounded automatic task authorization, not authorization for follow-up work. Non-interactive execution requires reasonable decisions without routine questions.

## Scope and Success Criteria

Compact filters at the expanded map's top; consistent header/map state; keyboard operation and text state at narrow widths; durable automated behavior coverage and actual local browser exercise.

## Task Research Requests

Read #551 and the required project/UX documentation; investigate existing state ownership and local app/test entry points before choosing an implementation.

## Direction Controls

* Preserve selected Fluent 2 foundations, WCAG baseline and plain ASCII content.
* Source changes only in src/. Tests outside the package.
* Commit with the required trailer; never push or change rubric scores.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How can map controls reuse the header filters and update markers? | depth | Open |
| Q2 | How can focus, narrow layouts and repeat expand/collapse remain reliable? | depth | Open |
| Q3 | Which local commands and fixtures prove every criterion? | straightforward | Open |

## Prior Knowledge Gate

Read the original case study, addendum, knowledge-base index and owner memory. Inspected #551: four unchecked criteria, no comments. Clean worktree on the explicitly selected feat/map-filters-551 branch; no existing PR. Existing UX documents describe native Fluent-derived components, not complete library adoption or accessibility acceptance.

## Research Cycle Log

### Cycle 1

Focused, inline Wider -> Deeper -> Contrarian investigation; no independent delegated lane needed.

#### Wave 1: Wider

Inline inspection found one Overview tile group, one area selector and shared
`ovState`; mapPanel owns the native dialog and moves the map card into it.
Existing constructed-data browser harness starts a real loopback server and
blocks external requests. Reflection: reuse the existing controls, not a new
filter model.

#### Wave 2: Deeper

`draw(true)` requests the full selected population before fitting and then
redraws with viewport bounds. Latest-response sequence guards already prevent
stale draws. Expansion and collapse preserve the same panel and Leaflet map.
Reflection: reparent the original filter controls into the dialog above the
workspace, restoring their slot on collapse. This guarantees header state by
identity, includes area filtering and avoids duplicated controls.

#### Wave 3: Contrarian

Challenged a duplicated compact-toolbar design: it requires extra state sync,
duplicate IDs or separate area control handling, while reparenting needs none.
Existing `paint()` replaces all buttons and loses keyboard focus on activation;
change only state attributes and selection text in place. Completed is not a
filter, so keep its header tile but hide it in compact mode. Coordinator has
different cohort controls and must not acquire Overview flags.
Reflection: test node identity, focus persistence, bidirectional area/flag
changes, zero results, repeated collapse, route cleanup and narrow/enlarged
layout. The existing browser fixture supports all of these locally.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Reparent one control group | C1-C3 | Accepted | No parallel state, same native controls and handlers |
| Independent compact duplicate toolbar | C1-C3 | Rejected | Avoidable synchronization and ID/focus complexity |
| In-place selected-state updates | C1 | Accepted | Preserve focused control during requests |
| New framework or Coordinator flags | C2, C5 | Rejected | Outside the issue and different cohort semantics |

No further research cycle required: focused source contracts and concrete local
verification entry points cover the material questions.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/551 (retrieved with gh 2026-10-29) | Four acceptance criteria, compact expanded-map filters and synchronized state |
| W2 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (fetched 2026-10-29) | Native semantics, visible focus, live feedback, reduced motion and responsive controls |
| C1 | src/api/src/zava_forward/api/web/app.js:1952-1972 | Six OV_TILES flags, Completed static tile, area selector; paint currently replaces buttons |
| C2 | src/api/src/zava_forward/api/web/app.js:1606-1716 | Native dialog expansion, collapse, route disposal, focus restore |
| C3 | src/api/src/zava_forward/api/web/app.js:1726-1824 | Shared ovState API query, request sequence, empty/error handling and fitting |
| C4 | src/api/checks/design_system_browser_check.py:36-53,227-287 | Constructed 505-case fixture and isolated local server lifecycle |
| C5 | src/api/checks/map_fullscreen_browser_check.py:405-759 | Existing Playwright, integrity-pinned axe, keyboard, reduced-motion and narrow-width regressions |
| C6 | src/api/tests/test_map_fullscreen.py:9-121 | Static contracts for map lifecycle and source semantics |
| C7 | src/api/src/zava_forward/api/web/style.css:181-233 | Header tile styles, visible selection text and expanded flex/grid layout |
| C8 | src/README.md:61-159 | Local gate distinction; complete publication gate includes az, which caller prohibits |

## Alternatives and Decision State

Select the original-node reparenting approach with an optional filter-group
argument to mapPanel, an original header slot and expanded compact styles.
Preserve all route/request, safety, list and motion behavior. Keep the existing
page-session state model; do not expand this issue into URL-state migration.

## Open Questions, Risks and Residual Uncertainty

The complete publication gate requires az/offline Bicep (C8), prohibited by
the caller. Do not execute it or publish. Record focused checks and retain the
publication limitation. Local checks do not establish human acceptance, hosted
approval or full accessibility conformance. Direct screen-reader testing is
not part of the supplied local harness.

## Findings Mapped to Questions and Evidence

| Question | Answer | Evidence |
| --- | --- | --- |
| Q1 | Move existing flag/area controls into the dialog and restore their slot; continue using ovState and draw | C1-C3 |
| Q2 | Stable buttons, existing focus/modal lifecycle and token-based responsive compact layout | C2, C5, C7, W2 |
| Q3 | /tmp/mv unittest, node --check and extended real-server map browser harness | C4-C6 |

## Artifact Self-check

All three waves executed inline in order. Internal and external evidence cited.
Alternatives, caller boundaries and publication uncertainty recorded. No source
files edited in Research.

## Planning Readiness

Ready. Research disposition: executed. Parent continuation: Plan, then
implementation and one independent Review as explicitly requested.
