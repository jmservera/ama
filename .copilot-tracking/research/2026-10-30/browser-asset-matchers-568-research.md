---
title: Browser asset matcher correction research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: correct PR #594 browser harness assumptions after release-versioned assets, Refs #568.
* Purpose and audience: evidence for a local-only correction and independent RPI assessment.
* Scope: asset routes, response/request waits, DOM selectors and coverage comparisons in `src/api/checks`; related tests and API guide.
* Non-goals: application asset redesign, Azure, private data, secrets, push, issue closure or live acceptance.
* Criteria: reproduce the workflow browser failure with the heavy lock; demonstrate versioned/unversioned matching and negative cases; pass existing browser checks, relevant unit tests and Ruff.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Status | Complete |
| Researcher | RPI Agent / rpi-research |
| Questions | Q1: Which asset assumptions bypass versions? Q2: What normalization preserves matching precision? Q3: Which local commands reproduce and validate CI? |
| Posture / provenance | Focused / named caller targets and failure |
| Initial internal areas | `src/api/checks`, static asset handler, tests, `.github/workflows/src-ci.yml` |
| External scope | None required for code research |
| Explicit limits | pip, src only, heavy lock, no Azure/secrets/push |
| Completion basis | All in-scope matching surfaces and counterexamples covered |
| Edits during Research | Evidence and session state only |
| Evidence root | `.copilot-tracking/` |

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | Selected: branch, pip, synthetic data, local evidence and publication boundaries |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian cycle |
| Skill | UI design skills | Skipped: harness-only correction, no UI edits/design |
| Specialist | Research worker | Skipped: one continuous local trace, investigate inline |

## User Participation and Research Decisions

Explicit request authorizes the full ordered loop and local commit. Non-interactive execution needs no routine phase confirmation. Existing clean `fix/employee-chat-cache-568` branch matches open PR #594 targeting main.

## Scope and Success Criteria

Verify the supplied failure against executable source and CI; preserve strict asset identity, fault injection, retry counts, genuine coverage, and cache assertions.

## Task Research Requests and Direction Controls

Only Refs #568; no closing keyword. Run all four phases and preserve dated original evidence. No remote writes. Publication gates and human approval cannot be claimed from these focused checks.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Locate every version-sensitive browser asset assumption | depth | answered |
| Q2 | Select precise query/segment-independent matching and tests | depth | answered |
| Q3 | Reproduce the exact workflow browser command locally | straightforward | answered |

## Prior Knowledge Gate

Read original/addendum, reference index/memory and customer primer. Memory is context, not evidence. Caller finding is a hypothesis to verify; PR lifecycle and branch were verified read-only. No existing correction evidence reused.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline survey finds static asset assumptions in workspace, loading, employee workspace, chat widget, case journey and case-view checks. CI invokes the design-system harness, regulatory check and case journey. Reflection: named files are not the complete correction surface; inspect all asset instrumentation before selecting a fix.

#### Wave 2: Deeper

`StaticAssets.url` emits `?v=<sha256>`. Seven checks contain asset instrumentation: workspace scripts, loading briefing, employee workspace, chat widget, case journey, case-view UX and asset cache. Bare direct GETs and legacy-cache priming deliberately exercise bare-URL behavior, not matcher bugs. Workspace also retains an obsolete Leaflet `no-store` assertion. Inline investigation avoids splitting a continuous trace.

Baseline ran the three CI browser commands in their original order with `flock -w 600 /tmp/ama-rpi-heavy.lock`, installed src packages in a task-owned pip environment, and the workflow-pinned axe download. Design-system/workbench and regulatory checks passed; case journey timed out at the exact CI fallback assertion (`:1489`). External raw log: `/home/azureuser/.copilot/session-state/7dc0069c-bd97-46db-8804-627147673f47/files/baseline-ci.log`. Chromium already ran successfully, so no browser/system package installation was necessary. Reflection: versioned enhancement bypasses fault injection; this is a real reproduced regression, not merely a reported hypothesis.

#### Wave 3: Contrarian

Challenge: broad `**/app.js*` matches similarly named assets and query-spoofed paths. Query-only URL parsing addresses current versions but not the caller's requested version path segments. Choose a shared anchored regex matching the complete canonical asset suffix, optional leading version-directory segments, and optional query/fragment. Reuse its exact pattern in JavaScript DOM instrumentation and preserve origin filtering for CDP coverage. Test filename suffixes, missing vendor path, query spoofing and trailing paths as negatives. Keep cache release identity, exact retry URLs and actual coverage counts asserted; update Leaflet to the actual revalidation/ETag contract rather than removing its assertion.

Reflection: current application only emits query versions; segment variants can be proven with synthetic matching tests, not claimed as served by the app. New helper is justified across seven checks; unrelated API matching remains untouched.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Match all asset instrumentation using one anchored canonical suffix pattern | C2-C5 | Accepted | Handles both requested version forms without filename/query false positives |
| Change application asset generation | C3 | Rejected | Handler already works; harness assumptions are faulty |
| Relax coverage/cache assertions | C2, C6 | Rejected | Would hide duplicate execution or cache regressions |
| Run complete publication gate | C1 and caller scope | Deferred | Local correction only, no publication requested; no release/hosted/human acceptance claim |

#### Cycle Re-entry Evaluation

No further cycle: all named and adjacent matching surfaces inspected, same CI failure reproduced, alternatives and negatives identified. Focused scope is covered; remaining live/publication evidence cannot change this local harness correction.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | CI step invokes design-system, regulatory and case-journey checks | `.github/workflows/src-ci.yml:93` | High; read source |
| C2 | Recovery route/wait and coverage expect bare asset URLs | `src/api/checks/workspace_scripts_browser_check.py:91`, `:106`, `:192`, `:234` | High; read source |
| C3 | Handler emits query versions and revalidation/ETags | `src/api/src/zava_forward/api/static_assets.py:21`, `:53` | High; read source |
| C4 | Loading shell, helper/law failures and other checks use bare routes | `src/api/checks/loading_briefing_browser_check.py:63`, `:110`, `:279`; `src/api/checks/chat_widget_browser_check.py:919`; `src/api/checks/employee_workspace_browser_check.py:95` | High; read source |
| C5 | CI enhancement fault injection and focused UX fallback routes bypass versions | `src/api/checks/case_journey_browser_check.py:1483`; `src/api/checks/case_view_ux_browser_check.py:156` | High; read source and baseline |
| C6 | Bare/cache requests are deliberate; Leaflet cache assertion is stale | `src/api/checks/asset_cache_browser_check.py:119`, `:145`; `src/api/checks/workspace_scripts_browser_check.py:349`; `src/api/tests/test_static_assets.py:60` | High; read source |
| C7 | Baseline CI reproduces original case-journey timeout | `src/api/checks/case_journey_browser_check.py:1489` | High; observed local baseline and GitHub run 41144371712 |

## Findings Mapped to Questions and Evidence

Q1: seven asset-instrumenting checks, C2/C4/C5/C6. Q2: anchored shared pattern with exact vendor suffix and origin-preserving coverage, C2/C3/C6. Q3: original CI command sequence reproduced the same case-journey timeout, C1/C7.

## Key Discoveries

Do not weaken assertions merely to hide versioned asset execution; real fault injection and coverage must be preserved.

## Alternatives and Decision State

Selected: shared anchored regex reused by Playwright and JavaScript DOM matching. Optional prefix directory segments support version paths without relaxing the required asset suffix. Reject suffix glob (filename/query overmatch); reject query-only parsing (does not meet segment scope). Confidence high for current query versions; synthetic tests must demonstrate segment variants.

## Open Questions, Risks and Residual Uncertainty

No research blockers. Current app serves query versions only. Synthetic segment matching will not establish segment-based HTTP serving or live employee-site acceptance. Full publication gate, hosted rerun and human approval remain outside this local-only deliverable.

## Current Decisions

Keep existing topic branch; local-only commit; synthetic data.

## Unresolved Decisions and Potential Next Research

None requiring user input. Inspect normalization prior art.

## Planning Readiness

Ready, based on C1-C7. Research disposition: executed. Original failure reproduced and root cause located. All ordered waves complete; no source edits in Research. Automatic RPI parent may proceed to Plan after state persistence.

## Sources and Self-check

Internal source and GitHub CI log only; no external research sources used. Public pinned axe asset was fetched solely as CI runtime input. Artifact self-check: brief, controls, extension provenance, questions, ordered waves, evidence, alternatives, dispositions and readiness complete.

## Closeout Record and Advisory Next Step

Research Complete / executed / Planning Readiness Ready. Inline investigation completed Wider, Deeper and Contrarian with no delegation. Automatic parent continues to Plan; no user action required. Stable identity is `pr-594-browser-asset-matchers-568`.
