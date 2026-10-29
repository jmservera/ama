<!-- markdownlint-disable-file -->

# Task Research: iot-consumer-110-refresh

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md |

## Research Brief

* Target: refresh draft PR #508 on feat/iot-consumer-110 against origin/main, preserving bounded IoT behavior and current CI contracts.
* Purpose and audience: give the coordinator a locally validated, committed, unpushed candidate and original dated RPI evidence.
* Scope: branch divergence, conflicts, src/core and src/api, external tests, scenario manifest, rubric ownership, local validation and read-only IoT pricing.
* Non-goals: push, merge, issue closure, Azure changes, paid resource creation, live IoT acceptance or rewriting previous review outcomes.
* Criteria: preserve both sides' intent; main owns rubric and scenario manifest; verify hashes and affected tests; report unavailable gates honestly.
* Output mode: convergence, preparing planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What changed on main? Which conflict and validation contracts apply? What is the smallest paid Hub estimate? |
| Codebase scope | Existing PR branch and current main |
| External scope | GitHub PR/check metadata and Microsoft public retail pricing only |
| Initial internal candidate areas | src/, .github/workflows/, .github/rubric/, tools/, prior IoT evidence |
| Initial external candidate areas | Azure Retail Prices API |
| Research posture | focused |
| Provenance | Bounded caller task with explicit branch and validation instructions |
| Limits | No push, no cloud writes, full API suite only with nonblocking heavy-lock admission |
| Completion basis | All material in-scope questions evidence-backed |
| Edits allowed | Research evidence and required workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | Provided project guidance; src-only, preserve original evidence, local publication gate | Selected |
| Skill | rpi-research | Three sequential research waves and evidence IDs | Selected |
| Skills | rpi-plan, rpi-implement, rpi-review | User explicitly requests full lifecycle | Deferred to owning phase |
| Specialist | Independent critique and review | Required by repository/RPI protocols | Deferred to owning phases |
| Skills | Web design/accessibility | No web surface intended to change | Not applicable |

## User Participation and Research Decisions

User explicitly requests the full loop and rebase, authorizes local commits and forbids pushing. Execute the requested phases without an interactive mode change; record manual mode with explicit advance authority for each of the four phases. No automatic follow-up session is inferred.

## Scope and Success Criteria

Refs #110 #184 #185 #187 #188 #189. Source stays in src/, tests outside packages; no legacy application code. Git worktree was clean and branch matches the open draft PR. Existing commits and original 2026-10-27 findings must survive the rebase.

## Direction Controls

* Rebase onto fetched origin/main; preserve both sides except main owns rubric and scenario manifest.
* Use /tmp/mv; affected lint, format, typing and unittest coverage.
* Do not create/modify Azure resources or expose credentials.
* Price estimate belongs only in PR notes, not source or knowledge-base economics.
* Commit with required co-author trailer; coordinator owns push and hosted CI.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What branch/main changes require reconciliation? | depth | Answered |
| Q2 | Which manifest, validation and publication contracts apply? | depth | Answered |
| Q3 | What is the smallest paid IoT Hub monthly estimate? | straightforward | Answered; estimate restricted to PR notes |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Prior PR metadata reports successful source CI but a failed rubric conclusion with pending rubric/score; those are historical, not current-head acceptance. Cross-session lookup found no additional matching recent session.

## Research Cycle Log

### Cycle 1

Focused scope; all waves inline because the branch/contracts form one coupled trace.

#### Wave 1: Wider

Opening branch inspection found four topic commits and an open draft PR targeting main. Fetched main is b0364e4b. Next inspect changed source contracts, current workflow and manifest.

Reflection: main changes overlap README/index/log, typing configurations and the synthetic model used by replay, while topic-only SDK adapter files have no upstream counterpart. Prior passing counts cannot establish new-main compatibility.

#### Wave 2: Deeper

Inspected the replay implementation, sensor-stream tests, generator changes, current project configs, workflow selectors and manifest tests. Main changes the generator version and bounds noise; replay derives descriptor model version dynamically and compares observations against the actual generator, so preserve main model semantics rather than freezing old outputs. Main updates two scenario source hashes. Existing /tmp/mv lacks the two IoT SDK distributions; installation is justified by observed missing dependencies.

Reflection: tests must cover replay/backfill/fault/privacy/manifest behavior as well as receiver/ingestion, not merely conflict-marker removal. Preserve both main's typing overrides and the topic's narrow SDK/stream overrides.

#### Wave 3: Contrarian

Challenged the assumption that all failed CI is source-related. The historical rubric run failed while trying to post a missing-verdict comment, with HTTP 403 "Resource not accessible by integration"; the scorer itself produced no verdict. Main owns rubric, and local success cannot prove this hosted permission/inference path works. Challenged manifest ownership against source drift: main's manifest pins main's changed workbench/recipe bytes; verify after rebase and change hashes only if actual pins differ. The nonblocking heavy-lock probe succeeded at research time but must be reacquired and held during any full API suite.

Reflection: no evidence supports widening to workflow-permission changes or live IoT activation. Preserve those boundaries and report hosted CI as pending coordinator publication.

### Parent synthesis and re-entry decision

Accept caller-selected rebase, main-owned rubric/manifest, dynamic model compatibility and affected local validation. Reject merge, old generator freezing, whole-issue acceptance, and workflow/protection changes. Defer hosted verdict and publication gate to coordinator if blocked; do not fabricate completion. One complete focused cycle covers the material questions; another cycle would duplicate established contracts.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | docs/reference/README.md:20 | Existing synthesis distinguishes bounded local evidence from live Hub/SQL/approval acceptance. |
| C2 | src/api/src/zava_forward/api/iot_stream.py:1 | Topic source resides under src/; test_iot_stream.py is outside the package. |
| C3 | src/core/src/zava_forward/core/synthetic/sensor_stream.py:198 | Descriptor reads the shared generator version dynamically. |
| C4 | src/core/tests/test_sensor_stream.py:126 | Exact replay is compared with the current generator, including deterministic suffixes. |
| C5 | src/core/tests/test_scenario_manifest.py:21 | Validates current manifest and all pinned source hashes. |
| C6 | .github/workflows/src-ci.yml:80 | CI uses package discovery, Ruff and mypy; retain workflow/check identities. |
| C7 | src/README.md: local RPI gate on origin/main | Commit original Review before external gate; clean exact-head/base receipt remains distinct from hosted/human approval. |
| W1 | https://github.com/jmservera/ama/actions/runs/40584245914 ; retrieved 2026-10-29 | Missing verdict plus failed 403 comment explains historical rubric failure; no fresh verdict inferred. |
| W2 | https://prices.azure.com/api/retail/prices?%24filter=serviceName%20eq%20%27IoT%20Hub%27%20and%20armRegionName%20eq%20%27uksouth%27%20and%20priceType%20eq%20%27Consumption%27&currencyCode=USD ; retrieved 2026-10-29 | Official regional retail meters returned without pagination; estimate reserved for PR notes only. |

## Findings, Alternatives and Decision State

Selected: rebase onto fetched main, resolve documentation and config conflicts by integration, take main's rubric/manifest, verify pins, install observed missing SDKs and run affected package checks. No cloud writes or remote publication.

## Open Questions, Risks and Residual Uncertainty

Exact conflicts will be observed during implementation. Hosted CI cannot validate an unpushed commit. Full local receipt depends on shared lock and tool/SQL/browser/scanner prerequisites; no skip or cloud fallback is authorized.

## Planning Readiness

Ready. Research disposition: executed. Brief, three waves, evidence, alternatives, constraints and handoff self-check complete. Parent is explicitly authorized to advance to Plan.
