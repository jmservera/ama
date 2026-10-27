<!-- markdownlint-disable-file -->
# Task Research: resident-sensors

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | Native RPI Agent / rpi-research |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-27/resident-sensors-research.md |

## Research Brief

* What: locate generated sensor data, resident authority and UI conventions for #468.
* Why: show a resident only their own home's synthetic readings and history.
* Audience: implementer and independent reviewer.
* Scope: resident showcase core, resident API/demo, generator and affected tests.
* Non-goals: header markup, Azure, private data, verifier, MAX_MAPPINGS, deployments.
* Criteria: source-backed values, isolation, native gauges, accessible history and table.
* Requested outputs: evidence and implementation handoff.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Where are readings generated; how does home authority work; how to render accessibly? |
| Codebase scope | src/core, src/api, synthetic generator |
| External scope | Current Web Interface Guidelines |
| Initial internal candidate areas | resident_showcase.py, resident_demo, generator, UX standards |
| Initial external candidate areas | vercel-labs/web-interface-guidelines |
| Research posture | focused |
| Posture provenance | Bounded caller task |
| Explicit limits | No two-hour gate; affected unit tests, ruff, mypy, focused browser validation |
| Completion basis | Material questions covered with source evidence |
| Edits allowed during research | Evidence and state only |
| Resolved evidence root | .copilot-tracking/ |
| Excluded sources | Private datasets, secrets, .env, verifier |

## Extension Registry and Provenance

| Kind | Candidate | Match/provenance | Authority | Selection |
| --- | --- | --- | --- | --- |
| Instruction | Repository guidance | All files | Branch, evidence, data boundaries | Selected; owner explicitly replaces full gate |
| Skill | web-design-guidelines | Resident UI | Current fetched rules | Selected |
| Specialist | RPI Researcher | Registered | Independent evidence lane | Skipped: single coupled trace handled inline |
| Skill | design-taste-frontend | Public marketing pages | Art direction | Skipped: existing resident app, no redesign |

## User Participation and Research Decisions

| Checkpoint | Rationale | Answer | Decision |
| --- | --- | --- | --- |
| Intake | Explicit full ordered loop and publication instructions | Supplied request | Automatic session; no routine prompts |

## Scope and Success Criteria

Own-home sensor projection, synthetic labelling, semantic gauges and history table,
cross-home regression tests, local browser exercise; no unrelated UI overhaul.

## Task Research Requests

Find existing synthetic stock values rather than invent a live stream or read private data.

## Direction Controls

| Control | Boundary | Source | Effect |
| --- | --- | --- | --- |
| Exclude | Azure, private data, secrets, verifier, header markup, mapping cap | Owner request | Local synthetic sources only |
| Change | Target PR base feat/resident-interactive; Refs only; no force/merge | Owner request | Stacked publication |
| Change | Targeted checks instead of complete local gate | Owner request | Record exact tests, not full-gate claim |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What sensor fields and history exist in generated stock? | depth | High | Open |
| Q2 | What principal projection prevents cross-home access? | depth | High | Open |
| Q3 | What native patterns support accessible readings? | straightforward | High | Open |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index/memory, sector primer and UX standards.
Branch is clean feat/resident-sensors at parent 55c239d9; no existing PR.
Supplied issue criteria verified through gh. Code claims remain to be verified.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline trace found temperature/humidity backfill separate from case JSON. Stock
home IDs are not case IDs. The resident SQL view currently exposes neither stock
IDs nor sensor rows. Reflection: do not infer a device or read private snapshots.

#### Wave 2: Deeper

The generator writes sensor_register/sensor_reading, marks SYNTHETIC and uses
UTC timestamps. Case home.stock_id anchors the generated stock. The HTTP server
selects its case from a signed session and freshly authorises before projection.
Reflection: project bounded history through that same view, never grant table
access or accept a home ID from the browser.

#### Wave 3: Contrarian

Absent sensor tables are valid today; mandatory joins would break existing
deployments. Generated OUTLIER/STUCK and missing values must not look normal.
Historical timestamps must not be presented as live readings. A dual-axis
mixed-unit chart risks confusion; use two labelled SVG plots plus one data table.
Reflection: use a source-only optional SQL view projection, default empty when
sensor tables are absent; no SQL execution/deployment in this task.

#### Parent Synthesis and Disposition

Accept existing generator fields and stock-home join (C1-C4); reject fabricated
live readings, re-generation in requests and direct sensor-table permissions.
Accept native meters for valid latest values and text for unavailable values.

#### Cycle Re-entry Evaluation

No further cycle required: source contracts and important counterexamples covered.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | UTC temperature/humidity readings, synthetic provenance, injected faults | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:30 | read | High |
| C2 | Stock sensor mapping, granted-only generation | src/core/src/zava_forward/core/synthetic/sensor_stock.py:68 | read | High |
| C3 | Generated case home.stock_id | support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:132 | search/read | High |
| C4 | Single SQL view, fixed parameterised case query | src/core/src/zava_forward/core/resident_showcase_sql.py:18 | read | High |
| C5 | Fresh authorisation before positive projection | src/api/src/zava_forward/api/resident_demo/app.py:127 | read | High |
| C6 | Native UI, Fluent tokens, no chart dependency | src/api/src/zava_forward/api/resident_demo/web/demo.js:21 | read | High |
| C7 | View has no sensor columns currently | infra/sql/resident-showcase.sql:26 | read | High |

### External Evidence

| ID | Finding | Source | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Native semantics, chart text alternatives, visible focus, reduced motion and Intl formatting | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-27 | High |

## Planning Readiness

Ready. Research disposition: executed. Q1-Q3 answered (C1-C7, W1).

## Alternatives and Decision State

Selected: bounded stored readings through an optional source SQL projection,
strict Python shaping, semantic meters, separate static history plots and table.
Reject request-time invented data and direct sensor-table grants.
No heavy dependency; no operational safety thresholds or health judgement.

## Risks and Residual Uncertainty

No private generated snapshot was inspected, so populated live sensor history is
unknown. Source view updates need a later separately authorised operator apply.
No Azure or SQL changes will be executed. SQL opt-in checks may remain unrun;
local fake-reader browser validation must be explicitly distinguished.

## Self-check and Handoff

Three waves performed in order inline; claims have source pointers; no production
writes. Native parent continues to Plan with C1-C7/W1 and no research blocker.
