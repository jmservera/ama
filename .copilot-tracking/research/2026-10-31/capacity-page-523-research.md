<!-- markdownlint-disable-file -->

# Task Research: capacity-page-523

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/capacity-page-523-research.md |

## Research Brief

* What to research: whether merged work already resolves #523, then reproduce the manager capacity page on a constructed local SQL/demo server using the existing Playwright checks.
* Why it matters: avoid reimplementing a delivered repair while preserving a regression and honest live-acceptance status.
* Audience or intended use: implementation planner and independent reviewer.
* Scope: issue/history, src/api/checks, capacity read endpoints, owning tests outside packages.
* Non-goals: deployment, live authentication, credentials, private data, other worktrees, main changes and unrelated UX changes.
* Criteria: real local page exercise, failure/retry coverage, adjacent manager-page checks and exact requested validation.
* Requested outputs: dated research, plan, changes and independent Review; local commit and gated publication with Refs #523 only.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1: already fixed? Q2: current SQL/browser behavior? Q3: smallest missing regression? |
| Codebase scope | src/api, relevant src/core storage, existing tracking evidence |
| External scope | jmservera/ama issue #523 and merged PR history |
| Initial internal candidate areas | capacity_browser_check.py, ops.js, test_procurement_api.py |
| Initial external candidate areas | issue #523, PR #528 |
| Research posture | focused |
| Posture provenance | bounded caller request |
| Explicit limits / deadline | pip only; no secrets/credential files; only current topic worktree |
| Posture-specific completion basis | all material task questions answered or explicitly blocked |
| Edits allowed during research? | no source edits |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints / excluded sources | no cloud fallback, live sign-in or default private dataset |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | supplied AMA repository instructions | all paths | evidence, branch and complete publication gate | selected |
| Skill | rpi-research | current phase | three-wave research | selected |
| Skill | web-design-guidelines | changed web review only | current interface rules | activate only if web edits required |
| Specialist | hve-core-all:rpi-researcher | available internal research lane | independent research evidence | skipped: one tightly coupled trace |

## User Participation and Research Decisions

Caller explicitly requests all four phases and publication. Non-interactive execution
continues through those phases without questions. This is a bounded automatic task,
not authorization to start further follow-up tasks.

## Scope and Success Criteria

Preserve original evidence and approval boundaries. Verify merged claims before
selecting regression-only work. Required live owner acceptance remains separate.

## Task Research Requests and Direction Controls

* Check merged work first, including local SQL and Playwright.
* If fixed, change no runtime source; add only regression coverage.
* Use branch fix/capacity-page-523, main PR target, Refs #523 with no closing keyword.
* Run the caller's API discovery and both Ruff commands; complete publication gate also applies.

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Did earlier merged work fix the root cause? | straightforward | H | answered |
| Q2 | Does current SQL-backed capacity and retry behavior work locally? | depth | H | answered |
| Q3 | What regression should this task add without duplicate runtime changes? | depth | H | answered |

## Prior Knowledge Gate

Issue #523 and PR #528 retrieved. Owner comment records merged repair with live
acceptance pending. Historical evidence is a lead, not current verification.

## Research Cycle Log

### Cycle 1

Focused, inline investigation; no independent research lane warrants delegation.

#### Wave 1: Wider

Issue/history and existing browser-check inventory inspected. PR #528 already
repaired legacy packages and read retry/session handling; later PR #577 also
references #523. Prioritize current code and current execution over stale status.

#### Wave 2: Deeper

Confirmed null-preserving appointment binding and legacy HTTP test. Ran current
`checks.capacity_browser_check --mssql` with the caller's exact PYTHONPATH from
src/api. The harness generated 980 fictional cases (443 open), started an owned
loopback SQL Server and local HTTP server, then exercised Chromium. Capacity
rendered one package and all 601 work orders. All twelve actual manager navigation
destinations passed. Both endpoint failures, keyboard retries, draft retention,
delayed sibling 401 orderings, cancellation, session expiry and empty states passed.
Reflection: merged runtime repairs hold on this current local configuration.

#### Wave 3: Contrarian

Challenged the repair with actual injected 503/403/transport failures and delayed
401s, rather than happy-path-only requests. All assertions passed, exit 0.
Several BrokenPipeError diagnostics occurred during deliberately aborted requests;
the harness still rejected unexpected browser failures and completed successfully.
Axe was not supplied and all four scans explicitly reported NOT RUN; this is not
accessibility acceptance. SQL restart/read preservation is not directly covered
by the existing legacy HTTP regression: it deletes metadata and reads in the
same fixture instance. Add a restart regression instead of duplicate UI/runtime
changes. Live state remains unknown. AI configuration correlation is not proven
causation. No further research cycle could change the bounded implementation choice.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Missing legacy contract version projects null rather than raising KeyError | src/core/src/zava_forward/core/appointments.py:97-114 | read | High |
| C2 | Existing legacy HTTP regression verifies 200/Unknown reads and unchanged 403 write denial | src/api/tests/test_procurement_api.py:127-153 | read, unittest (one passed, 0.915s) | High |
| C3 | Capacity wraps endpoint failures with named plain-language errors and guards aborted/expired sessions | src/api/src/zava_forward/api/web/ops.js:187-233 | read | High |
| C4 | Owned SQL/HTTP/Chromium check exercises full manager navigation and capacity recovery | src/api/checks/capacity_browser_check.py:94-177, 311-844 | actual --mssql execution, exit 0 | High |
| C5 | Reopening SqlStore and assigning app.store is existing HTTP-test prior art | src/api/tests/test_resident_api.py:944-947 | read | High |
| C6 | Caller validation needs installed distribution metadata; system Python lacks zava-forward-api metadata | src/api/pyproject.toml:6-25 | metadata probe, PackageNotFoundError | High |
| C7 | Current HEAD equals fetched origin/main | src/README.md:64-89 | git rev-parse, both 5666bd33e1827670e5c07e3e3063bbbe989b59d3 | High |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- | --- |
| W1 | Root cause and five local criteria marked complete; live verification remains unchecked | issue #523 | https://github.com/jmservera/ama/issues/523 | 2026-10-31 | High |
| W2 | Legacy package and capacity retry/session repairs merged | PR #528, merge 1dde6a908c20358dbb3067dcdd674e5ad0bd246d | https://github.com/jmservera/ama/pull/528 | 2026-10-31 | High |
| W3 | Later capacity acceptance and browser-import regression work merged | PR #577, commit a02984e8 in current ancestry | https://github.com/jmservera/ama/pull/577 | 2026-10-31 | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | Historical missing contract_version lookup already repaired; no current runtime failure found | W1-W3, C1-C3 | No runtime changes |
| Q2 | Current owned real SQL Server / Chromium and twelve manager destinations pass | C4 | Local reproduction complete, live owner verification still pending |
| Q3 | Add SQL reopen coverage preserving legacy Unknown reads and write denial | C2, C5 | Regression-only implementation |

## Alternatives and Decision State

Select one SQL-reopen HTTP regression in the existing owning test file. Preserve
legacy resident bindings so missing contract_version is isolated. Assert complete
package/order response identity and repeated read invariance; confirm writes stay
denied and unchanged. Reject runtime edits because C1-C4 already demonstrate the
repair. Reject live login/deployment and unrelated redesign as excluded.

## Open Questions, Risks, and Residual Uncertainty

Live owner acceptance cannot be inferred from merged code or local checks.

## Planning Readiness

Ready. All questions answered, one complete focused three-wave cycle executed.
Missing project metadata justifies pip restoration in a fresh external venv;
no manifest change or uv is needed. Complete final gate and live owner acceptance
remain separate requirements.

## Research Disposition and Self-check

Executed, complete. Source remained unchanged during Research. Evidence IDs
resolve, alternatives and residuals recorded. An initial unittest selector used
ProcurementAPI instead of ProcurementApi and failed before execution; corrected
selector passed. No credential files or private/default datasets were read.
