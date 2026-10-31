<!-- markdownlint-disable-file -->

# Task Research: live-azure-verification

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/live-azure-verification-research.md |

## Research Brief

* What to research: existing employee/resident acceptance automation, deployed UI contracts and exact criteria for #523, #524, #570 and #432.
* Why it matters: distinguish deployed observations from source-only evidence.
* Audience or intended use: owner and delivery reviewers; audit prepares planning.
* Scope: named deployed employee/resident URLs, acceptance checks, evidence pack and issue records.
* Non-goals: Azure configuration, scaling, jobs, deployment, private datasets, unbounded inference, or fixing application bugs.
* Criteria: dated direct observations with exact commands and bounded sign-ins; checkbox changes only for proven criteria.
* Requested outputs: full RPI artifacts, evidence documentation, issue comments/bugs, main-targeted Refs PR.
* Output mode: audit (prepares planning).

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Safe automation, deployed/source boundaries, criteria and publication prerequisites |
| Codebase scope | src/api/checks, related UI/API contracts, docs/architecture, tools/rpi-checks.py |
| External scope | Supplied Azure app origins and jmservera/ama issues |
| Initial internal candidate areas | Employee check; resident checks/tests; cut-over evidence pack; project READMEs |
| Initial external candidate areas | Issues #523, #524, #570, #432 and deployed apps |
| Research posture | focused |
| Posture provenance | Default for bounded named targets |
| Explicit limits | Two sign-in attempts/account; credentials only inside automation; pip only; no Azure mutations |
| Completion basis | All material execution contracts identified and counter-evidence considered |
| Edits allowed during research | No source edits; evidence and workflow tracking only |
| Resolved evidence root | .copilot-tracking/research/ |
| Excluded sources | Private working data; credential contents in tools/logs |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Selection |
| --- | --- | --- | --- | --- |
| Instruction | Repository AMA guidance | Supplied applyTo ** | Branch, documentation, full gate, independent review | Selected |
| Skill | rpi-research | RPI lifecycle | Three ordered research waves | Selected |
| Skill | web-design-guidelines | No UI code review/edit requested | UI rules | Skipped; acceptance execution, not design audit |
| Research specialist | hve-core-all:rpi-researcher | Available | Independent evidence lane | Skipped; continuous small contract trace inline |

## User Participation and Research Decisions

| Checkpoint | Rationale | Answer | Decision |
| --- | --- | --- | --- |
| Intake | Explicit full-loop and live/publication authorization; non-interactive host | User request 2026-10-31 | Execute all phases without routine prompts |

## Scope and Success Criteria

* Preserve credentials and resident/case privacy; artifacts contain only synthetic/sanitized evidence.
* Existing source tests do not prove a deployed version or identity.
* Missing local/publication prerequisites remain blockers rather than invented passes.

## Task Research Requests

* Verify employee chat, first navigation/tabbed assets, resident chat dock/resize, capacity, identity and AI metering.
* Record each result, update proven issue criteria, file reproducible bugs, push non-forced and create Refs PR.

## Direction Controls

| Control | Boundary | Source | Effect |
| --- | --- | --- | --- |
| Exclude | Azure config, replicas, jobs, deploy | User | Read-only infrastructure boundary |
| Narrow | At most two sign-ins/account | User | Reuse authenticated browser contexts |
| Narrow | Credentials read only by automation | User | Never inspect credential files with output tools |

## Research Questions

| # | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What existing automation can execute safely? | depth | H | open |
| Q2 | Which issue criteria require live versus source/financial evidence? | straightforward | H | open |
| Q3 | What gates apply before publication? | straightforward | H | open |

## Prior Knowledge Gate

* Read original case study, addendum, knowledge-base index and owner memory.
* Clean existing topic branch docs/live-verification-2026-10-31 tracks origin/main at 45121932; no existing PR found.
* Index describes #570 constructed Chromium evidence and #432 source-only delivery, not live acceptance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inline investigation selected: existing checks, project guides and exact issue criteria.
* Reflection: #523/#524 each lack live verification; #570 requires actual chat/map/case; #432 has financial/quality/spend gates that a chat alone cannot prove.

#### Wave 2: Deeper

* `verify_employee` accepts an already-authenticated Page and independent tenant/object GUID expectations, re-admitting at each action. Its CLI runs local tests, not live sign-in.
* Resident checks operate synthetic loopback fixtures and some create/drop local SQL databases; do not point their mains at Azure. Reuse only capture-free UI assertions, with a dedicated live driver.
* Reflection: supplemental live automation is necessary. Directory lookup must precede employee sign-in; absent independent expectation blocks employee actions rather than weakening admission.

#### Wave 3: Contrarian

* Challenged HTTP200-only success: identity display email is diagnostic, map acceptance requires correlated actual rendering, and chat can return workflow-only text without AI.
* Challenged stale-assets claim: use a fresh non-persistent context and compare actually delivered script/style hashes with local source. A fresh browser cannot prove recovery for every historical cached browser or recreate a platform cold start without scaling.
* Challenged resident acceptance reuse: local fixture sign-ins, callback writes and fault injection are not live-safe acceptance entry points. Inspect selectors and reuse UI-only operations, never substitute fixture responses.
* Reflection: these boundaries remove false positives; no Azure mutation or financial batch is justified.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Use employee adapter after independently verified identity | C3 | accepted | Existing immutable admission contract |
| Run resident local main against live origin | C4 | rejected | Fixture/server/SQL side effects and different sign-in contract |
| Supplemental bounded live driver | C3, C4 | accepted | Necessary real sign-in, assets, geometry and report projections |
| Infer metering criteria from one chat | W2 | rejected | Billing, quality, price and authority gates are distinct |

#### Cycle Re-entry Evaluation

* Another cycle needed: no; focused execution contracts covered.
* Residual gaps are live outcomes to measure during implementation, not unresolved research design.
* Planning Readiness: Ready.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Full exact-HEAD gate and fresh receipt verification required | src/README.md:84 | view | High | Repository instruction explicitly requires --all for final RPI candidate |
| C2 | Source-only identity and metering boundaries | docs/reference/README.md:19 | view | High | Existing context, not live success |
| C3 | Immutable admission and capture-free actual chat/map/case observers | src/api/checks/employee_acceptance_check.py:444; src/api/README.md:81 | view | High | Existing CLI is local-only |
| C4 | Resident checks are local fixtures, not live drivers | src/api/checks/resident_account_check.py:1; src/api/checks/resident_demo_browser_check.py:1 | view | High | SQL fixture can create/drop its owned database |
| C5 | Named manager route/API/render contracts | src/api/checks/capacity_browser_check.py:41 | view | High | Reuse read-only route observations |

### External Evidence

| ID | Finding | Source | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- | --- |
| W1 | Target issue criteria retrieved | GitHub issue bodies | https://github.com/jmservera/ama/issues/570 | 2026-10-31 | High |
| W2 | Metering criteria need more than live chat | GitHub issue body | https://github.com/jmservera/ama/issues/432 | 2026-10-31 | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q2 | Keep financial and held-out batch criteria unproven without exact evidence | W2 | Do not infer cost/quality/spend from chat |
| Q3 | Full local gate required before push | C1 | Final receipt remains external |

## Alternatives and Decision State

* Prefer existing checks with supplemental bounded automation; do not redeploy to make tests pass.
* No operational approvals or spend batches inferred from test-user authorization.

## Open Questions, Risks and Residual Uncertainty

* Python Playwright is installed; namespace packages are missing and must be installed with pip before imports.
* Fresh directory attestation may be denied (existing source documents a prior denial); credentials themselves are not inspected during research.
* Fresh-context assets do not establish fleet-wide historical-cache recovery, minimum-replica state, or a controlled Azure cold start.

## Planning Readiness

* Research disposition: executed, complete.
* Planning Readiness: Ready for bounded live verification; use the existing employee adapter and a supplemental privacy-safe live driver.
* Self-check: three ordered inline waves complete; source findings cited; source/live boundaries and residual uncertainty preserved; no source/cloud changes.
