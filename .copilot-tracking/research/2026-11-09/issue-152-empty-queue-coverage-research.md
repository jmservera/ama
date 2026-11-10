<!-- markdownlint-disable-file -->

# Task Research: issue-152-empty-queue-coverage

| Field | Value |
|---|---|
| Date | 2026-11-09 (written 04:06-04:20 UTC, prospectively, before any source edit) |
| Researcher / agent | RPI Agent via rpi-research (inline; no delegated lanes) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-research.md |

## Research Brief

* Topic: partial C5 of issue #152 (cross-profile checks follow PRD AC-034 and AC-043): meaningful empty-queue explanations for the constructed demonstration fixture; representative Programme Manager default `ZF-5` and Coordinator empty default.
* Purpose: decide what the workbench may honestly say when "My cases" is empty, and what runtime evidence could support a "declared unrepresented" claim.
* Scope: `src/api` web client, `/api/me` and `/api/cases` contracts, `src/api/checks/workbench-manifest.json`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` AC-034/AC-043/FR-032/FR-035, existing tests. Non-goals: full profile coverage, #1219 320px fix, supported-device decision, auth/SQL/consent/data changes, role simulator, #440 checkpoint.
* Branch state: `feat/workbench-empty-coverage-152` at `b46a9ad9a9619db535368d1b2cbbddec8110e122`, clean worktree; #1286 already on main, so this is a new partial branch against merged main.
* Initial tier: focused. Re-evaluated below; no full-tier category was found for the selected approach.

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | Q1-Q6 below |
| Codebase scope | src/api (web, server, checks, tests), src/core (store, taskqueues, journey_acceptance, scenario manifest), docs PRD |
| External scope | none (the web-design-guidelines source is fetched later, before web edits) |
| Research posture | focused (bounded internal task, named source targets) |
| Posture provenance | default for a bounded internal task with named targets |
| Explicit limits | caller: no browser/Playwright/SQL/Docker/changed/full gates; no push/PR; no private data |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/ default |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Selected / skipped |
|---|---|---|---|---|
| Instruction | AMA repository instructions | applyTo `**` | tiers, branch, evidence conventions, web guidance | selected |
| Skill | rpi-research | caller-required phase | this artifact | selected |
| Skill | web-design-guidelines | web edits planned | fetch + review at implement/review | deferred to later phases |
| Specialist | RPI Researcher | no independent lane needed | n/a | skipped, inline fallback |

## User Participation and Research Decisions

| Checkpoint | Rationale | Answers | Decision |
|---|---|---|---|
| Intake | Non-interactive run; the brief is sufficient | none | proceed, assumptions labelled |
| Direction change | none | none | none |
| Convergence | none; automatic loop | none | stop when waves saturate |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---|---|---|---|---|
| Q1 | What do AC-034/FR-032 and AC-043/FR-035 require of empty states and manifests? | breadth | H | answered |
| Q2 | What does the current UI say for empty, no-match and reset, and where is `ZF-5`/Coordinator default evidence? | depth | H | answered |
| Q3 | Is there any trustworthy runtime coverage/version metadata reaching the UI? | depth | H | answered: no |
| Q4 | How could such metadata legitimately arrive, and what tier would that be? | breadth | H | answered |
| Q5 | Which existing tests/checks already cover reset/focus/status, and what can be run without browsers? | depth | M | answered |
| Q6 | Overlap with other work? | breadth | M | answered |

## Prior Knowledge Gate

Known from the brief: static manifest is not runtime provenance. Not assumed: any server field exists. Verified below.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* PRD FR-032 requires empty results to "distinguish no matching fixture from no representative scenario supplied" (C1). AC-034 requires an unrepresented portfolio fixture to be distinguished from a query with zero matches, reset to the perspective default without changing a record (C2).
* AC-043/FR-035 require iteration-specific manifest with active slice, fixture/version, endpoint and explicit unrepresented/deferred, never claiming deferred as complete (C3, C4).
* `src/api/checks/workbench-manifest.json` version `152-ia-v1` declares `ZF-5` for `pam@example.test`, empty defaults with `empty_reason: "no representative scenario supplied"` for Coordinator, Safety, Grants, Quality (C5).
* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` v0.2.1 is a second manifest: every profile and workflow is `unavailable`, status `offline-coverage-audit`, fixture contract `152-ia-v1`, case IDs `ZF-4, ZF-1, ZF-5` (C6, C7).
* Candidate sources of runtime metadata: `/api/me` payload `work_queues` (server-owned, version `work-queues-1`), `/api/cases` page (`as_of`, `policy_version`, `policy_hash`), dataset `as_of` in the Store (C8, C9).

#### Wave 2: Deeper

* Client empty text today (`app.js:800`): any non-sort filter -> "No cases match these filters. Reset my queue to try again."; else mine -> "No open cases are assigned to you. This does not mean the programme has no work."; else "No permitted open cases are available." No coverage language exists (C10).
* `workspace-status` is `role=status aria-live=polite aria-atomic=true` (C11); the results container is also `aria-live=polite` (C10).
* Reset is a native `<button id="reset-queue">`, sets `resetFocus`, restores `defaultListState()` from the server `work_queues.default`, and refocuses the button after load (C10, C12).
* `defaultListState` reads `me.work_queues.default`, so reset is already server-driven (C12).
* `Store.list_cases` returns `as_of`, `policy_version`, `policy_hash` with every page (C9). The browser keeps `policy_version` only; `as_of` is available to bind a coverage declaration to the page actually shown.
* `taskqueues.contract` builds `/api/me.work_queues` with no coverage or fixture field (C8). `server.py` `/api/me` adds `work_queues` only for non-contractors (C13).
* The dataset has `as_of` but no fixture identity, version or declared-coverage field; the fixture is constructed only by `synthetic_data()` in test-side check code (C14). A runtime Store also has a SQL backend, so any persisted dataset field needs SQL parity.
* Existing checks: `test_workbench.py` (manifest consistency, 8 profiles with defaults, empty_reason) (C15); `test_workbench_live_defaults.py` (HTTP defaults vs manifest incl. PM `ZF-5` and empty Coordinator; Playwright set_content test, browser-dependent) (C16); `workbench_browser_check.py` reset/focus/status checks at ~495-700 (browser, not runnable now) (C17). Node + `vm` tests of web JS exist (`test_data_operator_ai_state.py`) (C18).
* `journey_acceptance.py` records AC-034 and AC-043 as `partial` with reason "No browser run in this slice" (C19).

#### Wave 3: Contrarian

* Counter 1: simply printing the manifest `empty_reason` for empty defaults would be "inferred from an empty queue and logged-in identity" and from a static test manifest; rejected.
* Counter 2: a packaged declaration keyed by role, shown whenever an empty own queue occurs, still cannot prove the loaded dataset is the declared fixture (dataset has no identity); matching case-ID sets is a content guess, not provenance. Rejected as authority.
* Counter 3: dataset-owned declaration (new field, persisted by JSON and SQL stores, validated and served via `/api/me`) is the legitimate producer, but it changes data/schema and SQL parity: full-tier, not authorised here.
* Counter 4: the two manifests disagree on status (`partial` vs `unavailable`). They answer different questions (shared-IA engineering slice vs scenario audit); the UI must not borrow "represented" from either. Recorded as a contradiction, not resolved.
* Counter 5: a UI consumer with no runtime producer is a dormant branch. Accepted deliberately: it makes the shipped default honest (explicit Unknown) and defines the checked contract a later authorised producer must satisfy; tests prove the invalid cases fail closed.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale | Treatment |
|---|---|---|---|---|
| Print manifest empty_reason at runtime | C5, C6 | rejected | static test manifest, infers from identity/empty queue | not implemented |
| Packaged role-keyed declaration + ID-set match | C14 | rejected | no dataset identity, weak binding | not implemented |
| Dataset-owned declaration served by /api/me | C8, C13, C14 | deferred | needs data/SQL/API schema: full-tier, owner/coordinator decision | residual R1 |
| Client consumer of optional version-bound declaration, default Unknown | C8-C12 | accepted | smallest change, fails closed, no authority invented | selected |
| Distinguish no-match vs unknown vs declared-unrepresented in copy | C1, C2, C10 | accepted | AC-034 wording | implement |
| Browser regression additions | C17 | accepted but not runnable | lock held; coordinator will admit browser gate | add check text, report unexecuted |
| Node-vm tests of the pure copy function | C18 | accepted | lightweight and runnable now | implement |

#### Cycle Re-entry Evaluation

Waves yielded no further material finding; sources redundant. No second cycle.

## Evidence Log

### Codebase Evidence

| ID | Finding | Location | Tool | Confidence |
|---|---|---|---|---|
| C1 | FR-032 empty-result distinction | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1407 | grep | high |
| C2 | AC-034 text | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2130 | grep | high |
| C3 | FR-035 manifest content | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1410 | grep | high |
| C4 | AC-043 text, deferred never full coverage | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2139 | grep | high |
| C5 | Workbench manifest v152-ia-v1 profiles, defaults, empty_reason | src/api/checks/workbench-manifest.json:2 | read | high |
| C6 | Scenario manifest v0.2.1 all unavailable | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json | python read | high |
| C7 | Scenario manifest validator, fixed public sources only | src/core/src/zava_forward/core/synthetic/scenario_manifest.py:44 | read | high |
| C8 | work_queues contract has no coverage field | src/core/src/zava_forward/core/taskqueues.py:59 | read | high |
| C9 | cases page returns as_of, policy_version, policy_hash | src/core/src/zava_forward/core/store.py:351,383 | read | high |
| C10 | Client empty text, status line, results live region | src/api/src/zava_forward/api/web/app.js:784,800 | read | high |
| C11 | workspace-status live region | src/api/src/zava_forward/api/web/index.html:40 | grep | high |
| C12 | Reset button, defaultListState from server default | src/api/src/zava_forward/api/web/app.js:457,845 | read | high |
| C13 | /api/me work_queues for non-contractors only | src/api/src/zava_forward/api/server.py:559 | read | high |
| C14 | Fixture built by test-side synthetic_data(); dataset has only as_of | src/api/checks/workbench_browser_check.py:20 ; src/core/src/zava_forward/core/store.py:75 | read | high |
| C15 | Manifest unit tests | src/api/tests/test_workbench.py:44 | read | high |
| C16 | HTTP defaults vs manifest, Playwright queue sync test | src/api/tests/test_workbench_live_defaults.py:51 | read | high |
| C17 | Browser reset/focus/status checks | src/api/checks/workbench_browser_check.py:495 | read | high |
| C18 | Node vm test pattern | src/api/tests/test_data_operator_ai_state.py:19 | read | high |
| C19 | AC-034/043 registered partial, browser unverified | src/core/src/zava_forward/core/journey_acceptance.py:25,73 | read | high |

### External Evidence

None gathered in research (web-design-guidelines fetched in Implement and again in Review).

### Contradictions / Conflicts

* Workbench manifest marks several profiles `partial`; scenario manifest marks every profile `unavailable` (C5, C6). Preserved; neither is used as runtime provenance.
* Issue #152 body says the C5 box is unchecked while the other web-layout boxes are ticked; the owner supported-device decision remains open and is not touched.

## Findings Mapped to Questions and Evidence

| Q | Finding | Evidence | Confidence | Implication |
|---|---|---|---|---|
| Q1 | Empty states must separate no-match from unrepresented; manifests must declare, not claim | C1-C4 | high | copy has three states |
| Q2 | Current copy has no coverage state; PM `ZF-5` and Coordinator empty defaults are covered by HTTP tests only; reset exists | C10, C12, C16 | high | add copy states and tests |
| Q3 | No trustworthy runtime coverage metadata exists | C8, C9, C13, C14 | high | default must be explicit Unknown |
| Q4 | Legitimate producer = dataset-owned declaration via /api/me (schema + SQL parity) | C8, C14 | medium | out of scope; residual R1 |
| Q5 | Browser checks exist but cannot run; Node vm is runnable | C17, C18 | high | add node tests |
| Q6 | No open PR references #152; scenario manifest overlaps but is offline | gh pr list (empty), C6 | medium | no conflict |

## Key Discoveries

* `as_of` and `policy_version` on every page give a client-side version binding that a future declaration can be checked against.
* A declaration is only accepted when it matches the shown page and signed-in role and is a default, unfiltered own-queue empty state.

## Alternatives and Decision State

### Selected Recommendation

Client consumer of an optional `me.work_queues.coverage` declaration, validated strictly (contract equals `work_queues.version`; `as_of` and `policy_version` equal the page; `fixture_version` and `source` non-empty strings; `perspective` equals the authenticated role; `status` equals `unrepresented`), otherwise explicit Unknown. No runtime producer is added. Rejected: manifest text at runtime, packaged role-keyed declaration, and dataset field (deferred, full-tier).

Tier reassessment: the selected change is web-client copy and tests only; it touches no auth, SQL, deployment, consent or data. It stays focused. The deferred producer would be full-tier and needs coordinator reassessment.

## Open Questions, Risks, and Residual Uncertainty

* R1: no authoritative producer exists; "declared unrepresented" cannot appear at runtime until an authorised dataset-owned declaration exists.
* R2: browser regression text added cannot be executed here (heavy lock held); coordinator-admitted exact-head `--changed` gate and Playwright are pending.
* R3: supported devices and widths remain an owner decision; 320/1280 checks are engineering only.

## Current Decisions

| Decision | Status | Owner | Rationale | Evidence |
|---|---|---|---|---|
| Default empty own queue says Unknown coverage | proposed | evidence | no authority | C8, C14 |
| Filtered empty says no match, not coverage | proposed | PRD AC-034 | C2 | C2, C10 |
| Declared state only on validated, bound metadata | proposed | caller brief | trust boundary | C9 |
| No server/data/SQL change | confirmed | caller | stop rule | C14 |

## Unresolved Decisions

| Decision | Smallest evidence needed | Owner | Impact | Blocker |
|---|---|---|---|---|
| Who produces coverage metadata | owner/coordinator decision on dataset-owned declaration and SQL parity | owner/coordinator | enables declared state at runtime | follow-up |

## Potential Next Research

| Priority | Item | Trigger | Selected? |
|---|---|---|---|
| H | Dataset-owned fixture declaration design | owner wants runtime declared state | no, deferred |

## Planning Readiness

Ready. Research disposition: executed. Output mode: convergence (selected recommendation above).

## Closeout Record

| Field | Record |
|---|---|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian (cycle 1) |
| Lane evidence or inline fallback | inline fallback; no worker lanes justified |
| Research disposition | executed |
| Planning Readiness | Ready |
| Blockers | none for the selected scope |
| Continuation owner and state | confirmed automatic RPI Agent (caller directed full loop) |

## Advisory Next Step

Proceed to rpi-plan; primary evidence file this document.

## Sources

Local files only as cited in the Evidence Log.

## Artifact Self-Check

Every claim cites a C# ID; contradictions preserved; no source edit made in this phase.
