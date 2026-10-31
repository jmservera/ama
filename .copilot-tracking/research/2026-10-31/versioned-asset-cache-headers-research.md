<!-- markdownlint-disable-file -->
---
title: Versioned asset cache headers research
description: Focused RV-001 source investigation for both demo apps
ms.date: 2026-10-31
---

## Research Metadata

| Field | Value |
| --- | --- |
| Date | 2026-10-31 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md |

## Research Brief

* What to research: RV-001 from the original PR #596 redeploy Review, static asset response policy and both app serving paths.
* Why it matters: release-versioned dependencies should be reusable without allowing stale unversioned libraries to persist across releases.
* Audience or intended use: implementation and independent Review of a local source correction.
* Scope: `src/api/src/zava_forward/api/static_assets.py`, its employee/resident callers, focused unit tests and existing browser checks.
* Non-goals: deployment, Azure, secrets, remote writes, workflow changes, live authentication or issue closure.
* Criteria: current content-version assets use `public, max-age=31536000, immutable`; HTML remains no-store; unversioned or obsolete version requests retain revalidation; both apps and conditional responses remain consistent.
* Requested outputs: dated research, plan, critique, details, changes and Review, focused regressions and local commit with Refs #568 and required trailer.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Where is request version available, how are headers selected, and how do we prevent stale-version responses becoming immutable? |
| Codebase scope | API source, tests, checks and API README |
| External scope | None; supplied requirement defines the exact HTTP policy |
| Initial internal candidate areas | Original remote Review; StaticAssets; employee and both resident handlers; test_static_assets; asset_cache_browser_check |
| Initial external candidate areas | None |
| Research posture | focused |
| Posture provenance | Default for bounded source task with named failure |
| Explicit limits / deadline | No Azure, secrets, push, workflow edits or closing keyword |
| Posture-specific completion basis | Scope coverage and evidence for every material question |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints / excluded sources | No private datasets or live services |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository AMA guidance | Supplied applyTo ** | Component tests, topic workflow, original evidence retention | Selected |
| Skill | rpi-research | Explicit full RPI loop | Three-wave evidence and readiness | Selected |
| Skill | web-design-guidelines / design skills | Backend HTTP cache policy only | Visual/UI scope | Skipped; no web UI edits |
| Research specialist | hve-core-all:rpi-researcher | Registered internal lane specialist | Read-only independent lane | Skipped; single tightly coupled trace handled inline |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Caller supplies exact source, finding, output policy and validation | Explicit full loop; non-interactive host | Proceed automatically through requested phases; no routine prompts |

## Scope and Success Criteria

* Verify supplied prior finding against current source; do not amend original Review.
* Confirm shared policy across employee, resident preview and resident demo.
* Preserve HTML freshness, auth/API no-store and conditional GET/HEAD behavior.
* Complete all three waves before Planning Readiness.

## Task Research Requests

* Exact requested commands run from `src/api`: supplied unittest discovery, `ruff check`, `ruff format --check`.
* Keep relevant `checks/*_browser_check.py` behavior passing, without live endpoints.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| narrow | RV-001 asset cache source fix | Owner | No authentication/deployment fixes |
| exclude | Azure, secrets, push, .github/workflows | Owner | Local constructed data and commit only |
| change | Versioned static responses become long-lived | Owner | Investigate exact-current-version guard |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How are versioned URLs produced and request paths/queries parsed? | depth | High | answered |
| Q2 | Which handlers and response paths must use the shared policy? | depth | High | answered |
| Q3 | Which tests/checks need updated expectations, including stale-version and 304 behavior? | depth | High | answered |

## Prior Knowledge Gate

* Read original Review via `git show origin/chore/ops-redeploy-1031:.copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-1031-review.md`.
* Current shared asset headers still use no-cache without max-age.
* Read case study, addendum, knowledge index and owner memory; no business, legal or UI scope change.

## Research Cycle Log

### Cycle 1

* Active controls: owner bounded local correction.
* Posture: focused; inline investigation because one continuous code trace.
### Wave 1: Wider

* Inline trace identified employee server, resident demo and resident preview as all StaticAssets consumers (C3-C5).
* Reflection: fix the shared policy and pass request queries through all consumers, not just the employee app.

### Wave 2: Deeper

* Prioritized version identity, header generation and conditional HTTP.
* Release SHA-256 covers sorted packaged paths and bytes; handlers snapshot it once (C6). Existing GET/HEAD/304 paths reuse asset headers (C3-C5).
* Existing test_static_assets spans all three handlers, real loopback requests and release turnover (C7). Baseline: 4 tests passed.
* Reflection: the asset can retain its snapshot version and classify a parsed query inside headers; HTML must short-circuit before version classification.

### Wave 3: Contrarian

* Challenged treating any `v` parameter as immutable. Old URLs currently return current snapshot bytes, not historical content (C6-C7); arbitrary/stale/blank/duplicate versions must continue revalidating.
* Challenged relying on reload to prove ETag revalidation. With immutable responses Chromium should reuse fresh cache without an origin request; existing check assumes a reload creates a 304 (C8).
* Workspace browser check asserts the existing policy on a bare Leaflet URL (C9); preserve it and add its versioned counterpart.
* Reflection: use exact single current version, prove actual browser reuse, then explicitly send a conditional request to test 304 independently.

### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Shared request-aware Asset.headers | C3-C7 | accepted | Single policy for all consumers and statuses |
| Any present version is immutable | C6-C7 | rejected | Stale URL does not identify current bytes |
| Retain bare/obsolete ETag behavior | C1, C7 | accepted | Preserves freshness and compatibility |
| Browser reuse and explicit revalidation | C8-C9 | accepted | Tests exact new contract rather than weakening checks |
| Live redeployment and authenticated acceptance | C2 | deferred | Outside owner local-only task |

### Cycle Re-entry Evaluation

* Another cycle needed: no. All material source and regression questions answered; further source sweeps are redundant.
* Readiness: Ready; no blocking research gaps.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Non-HTML shared assets currently only revalidate | src/api/src/zava_forward/api/static_assets.py:19 | view | High | Confirms supplied RV-001 |
| C2 | Original redeploy Review routes cache source repair as distinct work | origin/chore/ops-redeploy-1031:.copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-1031-review.md:169 | git show | High | Read-only original evidence; not local completion |
| C3 | Employee parses query already and shares headers for 200/304 and HEAD | src/api/src/zava_forward/api/server.py:238 | rg/view | High | Auth guard precedes static response |
| C4 | Resident demo discards query before static selection | src/api/src/zava_forward/api/resident_demo/app.py:305 | view | High | Host/expiry/method guards remain |
| C5 | Preview also discards query before selection | src/api/src/zava_forward/api/resident_preview/app.py:112 | view | High | Loopback/read-only guards remain |
| C6 | Stable release snapshot and rewritten URLs are centralized | src/api/src/zava_forward/api/static_assets.py:35 | view | High | Previous versions are not stored |
| C7 | Actual handler cache contract and snapshot turnover tests exist | src/api/tests/test_static_assets.py:41 | view/unittest | High | Baseline 4 tests passed |
| C8 | Warm-cache check assumes reload must trigger a 304 | src/api/checks/asset_cache_browser_check.py:161 | view | High | Needs browser reuse plus explicit conditional request |
| C9 | Workspace check expects revalidation header on bare Leaflet | src/api/checks/workspace_scripts_browser_check.py:351 | view | High | Keep bare assertion and add versioned counterpart |

### External Evidence

No external sources used.

## Planning Readiness

* Status: Ready.
* Disposition: executed.
* Evidence basis: C1-C9; all three waves complete.
* Preconditions: source consumers, snapshot semantics and affected checks identified; focused baseline passed.
* Blockers: none for Plan/Implement. No publication gate or live acceptance established.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Confidence | Implication |
| --- | --- | --- | --- | --- |
| Q1 | Shared Asset must know release version; headers parse query with blank values preserved | C3-C6 | High | Current single version only |
| Q2 | All three handlers must pass queries to both 200 and 304 headers | C3-C5 | High | Preserve GET/HEAD consistency |
| Q3 | Extend existing tests and update two browser expectations | C7-C9 | High | Avoid unrelated UI/check edits |

## Key Discoveries

* Content versions identify an entire handler snapshot, not individual file hashes (C6).
* HTML stays no-store even with a correct version query (C1, C7).
* Immutable fresh-cache reuse and conditional validation are separate measurable behaviors (C8).

## Alternatives and Decision State

### Selected Recommendation

* Retain release version on each immutable Asset, pass raw query to its shared headers method and parse a single matching `v` with `parse_qs(..., keep_blank_values=True)`.
* HTML always no-store; other query shapes keep existing no-cache and ETag semantics.
* Scope: shared module, three callers, focused tests, two browser checks and directly related README.
* Evidence: C1, C3-C9; High confidence within local source contract.

### Alternatives

* Any `v` presence: rejected because old URLs serve new bytes (C6-C7).
* Per-handler flags/parsing: rejected because it duplicates policy and allows drift (C3-C5).
* Reject stale URLs: rejected because it changes compatibility beyond cache policy (C7).

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence | Implication |
| --- | --- | --- | --- | --- | --- |
| Single current version grants immutable policy | confirmed | Owner exact content-version requirement and source evidence | Safe content identity | C6-C7 | Blank/old/duplicate versions revalidate |
| Keep ETags on versioned responses | confirmed | Existing contract | Explicit validators remain useful | C7-C8 | 304 carries same cache policy |
| Preserve original Review | confirmed | Repository retention policy | Historical acceptance does not change | C2 | Local source repair only |

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none.
* Live deployment caches and signed-in acceptance remain unverified and unauthorized (C2).
* Snapshot file changes require process restart; already-open pages are not hot-reloaded (C6).

## Unresolved Decisions

None within requested source correction.

## Potential Next Research

| Priority | Item | Value | Trigger | Selected? | Evidence |
| --- | --- | --- | --- | --- | --- |
| Medium | Owner-authorized live cache acceptance | Validate deployed headers | Separate deployment authorization | deferred | C2 |

## Closeout Record

* Research execution: Complete; disposition executed.
* Completed waves: Wider, Deeper, Contrarian, inline; no workers needed.
* Planning Readiness: Ready; C1-C9.
* Continuation owner: automatic RPI Agent, explicitly directed full loop.

## Advisory Next Step

* Automatic parent transitions to Plan after persisting state.
* No research skill initiated a peer phase; parent owns continuation.
* No additional research needed within current bounded scope.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Questions, three waves, posture, controls, provenance and decisions recorded.
* [x] Every codebase finding has stable C-ID and path:line.
* [x] Alternatives, synthesis dispositions, residual uncertainty and readiness cite evidence.
* [x] No external sources, secrets, source edits or worker execution implied.
* [x] All applicable template sections populated; illustrative code/config/diagrams omitted as unnecessary.
