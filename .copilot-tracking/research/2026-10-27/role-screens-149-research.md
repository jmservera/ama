<!-- markdownlint-disable-file -->

# Task Research: role-screens-149

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Blocked |
| Artifact path | .copilot-tracking/research/2026-10-27/role-screens-149-research.md |

## Research Brief

* What to research: existing role workbench, stories #225-#232 and #233, safe reusable screen contracts and stacked delivery constraints.
* Why it matters: deliver synthetic staff screens without granting operational authority or misrepresenting accessibility acceptance.
* Audience or intended use: implementation, independent critique and review, owner.
* Scope: src/api web and tests, existing core read contracts, UX evidence, GitHub story requirements.
* Non-goals: Azure deployment, live sending, real data, new legal authority, resident portal, framework replacement.
* Criteria: story-level traceability, native semantics, textual states, manual routes, separate human decisions.
* Requested outputs: dated research, plan, details, changes and original review; child draft PRs targeting feat/role-screens-149 and one parent PR targeting main.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which screens and read contracts already exist? Which missing fields can be represented honestly? Which delivery gates require an owner decision? |
| Codebase scope | src/, tools/rpi-checks.py, docs/reference/research/ux/, repository instructions |
| External scope | GitHub issues/PRs; current web-design-guidelines source |
| Initial internal candidate areas | src/api web, checks, tests; src/core existing scoped read contracts |
| Initial external candidate areas | jmservera/ama stories and merged dependencies; guideline upstream |
| Research posture | focused |
| Posture provenance | Default for named internal stories and explicit owner limits |
| Explicit limits / deadline | Local-first unit/browser work; one scoped parent gate, foreground lock timeout 0; no full gate, uv, Azure or secrets; #233 last; stop at owner decision and post one blocker comment |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints / excluded sources | Synthetic data only; preserve acceptance checkboxes without proof |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | All paths | Repository layout, identity, branches, publication gates | Selected |
| Skill | rpi-research | RPI wrapper | Evidence and three ordered waves | Selected |
| Skill | web-design-guidelines | Staff web edits/review | Current upstream interface rules | Selected before web edits |
| Skill | redesign-existing-projects | Existing app screens | Preserve Fluent-derived foundations and UX baseline | Deferred: blocked before implementation |
| Skill | design-taste-frontend | Public pages only | Public-page art direction | Skipped: staff app |
| Research specialist | hve-core-all:rpi-researcher | Available general research lane | Bounded independent uncertainty | Skipped: continuous repository trace handled directly |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit instruction to run full ordered loop and publish stacked drafts | Sufficient for automatic continuation without routine phase prompts | Treat request as explicit automatic-loop direction |
| Direction change | Owner forbids full gate, but applicable repository instructions require it before any final-candidate publication | Unresolved; stop requested at any owner decision | Stop Research before Plan, source edits, cleanup, gate or publication; post one blocker comment |

## Scope and Success Criteria

* Reuse the existing workbench IA and Fluent-derived components.
* Priority: #232, #227, #230, #225, then #226/#228/#229/#231; #233 last.
* No AI integration is required by the initial four story descriptions; economics design is not inference authorization.
* Record local engineering results separately from direct human, screen-reader and WCAG conformance acceptance.

## Task Research Requests

* Establish role-specific missing information and the safe endpoint of each view.
* Verify #150 and merged PRs #313/#317 rather than treating open #152 as wholly absent.
* Determine exact stacked branch and gate requirements before publication.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| add | One child branch and draft PR per story targeting parent; one parent PR to main | Owner request | No direct main push or merge |
| narrow | One --changed parent gate, no full gate | Owner request | Inspect selection and policy before gate execution |
| exclude | Secrets, private datasets, Azure, uv, live resident contact | Owner request | All investigation and validation synthetic/local |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What contracts and UI can be reused for each role? | depth | H | deferred after owner-decision blocker |
| Q2 | What does each story require and prohibit? | straightforward | H | answered by current GitHub bodies |
| Q3 | Can scoped-only publication satisfy repository gates? | depth | H | answered: not under current instructions |

## Prior Knowledge Gate

* Read original case study, addendum, knowledge-base index, owner memory, sector primer and src README.
* No matching session found in seven-day session history.
* Clean worktree, current parent branch feat/role-screens-149; no matching PR or remote branch.
* HEAD and fetched origin/main both 864a502126ee0dfedf13eaf54f08a10f2339279c.
* Verified #150 closed; #152 open; PRs #313/#317 merged. Issue status alone is not delivery evidence.

## Research Cycle Log

### Cycle 1

* Active posture: focused; local existing-contract trace.
* Wider: read all nine requested story bodies and dependency merge evidence.
* Wider reflection: initial four are constrained staff views, not new approval engines. Finance includes Unknown-first AI economics design.

#### Wave 2: Deeper

* Prioritized gate policy before web implementation because it determines whether the requested delivery can be published.
* Read the exact mandatory publication requirement in .github/copilot-instructions.md:71-83 and the newer small-versus-big feature policy in src/README.md:64-123.
* Inspected changed-path selection and locking in tools/rpi-checks.py:336-381 and :2175-2265. The requested lock is built in; --lock-timeout 0 is supported. A changed-path receipt is deliberately partial unless it selects the complete matrix.
* Read the three required UX standards and fetched the current web-interface guidelines successfully. No web files were edited or reviewed.
* Reflection: the command is implementable, but a scoped receipt cannot be represented as satisfying an unconditional complete-gate instruction.

#### Wave 3: Contrarian

* Tested the alternative interpretation that the newer src README authorizes this delivery as a small change.
* Counter-evidence: the README reserves complete gates for big features, and this request spans eight role stories plus a cross-role pass. More importantly, the applicable repository instruction still explicitly includes documentation-only final candidates and requires --all. No authorized reconciliation appears in that instruction.
* Checked the latest epic comments for an existing resolution; neither of the two comments addresses gate policy.
* Considered continuing source work without publication. Rejected for this run because the owner explicitly requests stopping at any owner decision, not merely withholding the final push.
* Reflection: this is an unresolved policy decision, not a missing tool or test failure. Do not execute either gate, alter policy, or fabricate an exemption.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Disposition | Rationale | Treatment |
| --- | --- | --- | --- | --- |
| Scoped-only gate satisfies publication | C2-C4 | Rejected | Explicit complete-gate instruction remains applicable | Blocker B1 |
| Existing Fluent foundations imply full adopted component library | C5 | Rejected | Design system explicitly distinguishes token/native foundations from full adoption | Preserve limited claim in later work |
| Continue implementation pending gate decision | W5, C3 | Deferred | Owner requested stop at any owner decision | No Plan/Implement/Review |

#### Cycle Re-entry Evaluation

* Another complete cycle needed: no additional discovery can authorize a policy exception.
* Stop basis: concrete owner-decision blocker B1.
* Revised brief required: reconcile scoped-only execution with the mandatory complete publication gate through authorized instruction changes, or authorize the required full gate.
* Readiness effect: Blocked. Screen contract research remains incomplete and must resume after resolution.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | WCAG baseline is an engineering target, not conformance acceptance | docs/case_study_48_addendum.md:207 | read | High | EXA-011 |
| C2 | Source projects own runtime/tests; changed-tier gate exists but full tier remains required for big features | src/README.md:64 | read | High | Reconcile with stricter repository instructions before publication |
| C3 | Every final RPI candidate, including documentation-only work, requires --all and immediate pre-push receipt verification | .github/copilot-instructions.md:71 | read | High | Unconditional applicable requirement |
| C4 | Changed selection retains transitive prerequisites; receipt verification defaults to full scope; heavy lock supports timeout 0 | tools/rpi-checks.py:336; tools/rpi-checks.py:2175; tools/rpi-checks.py:2192 | read | High | No gate invoked |
| C5 | Fluent 2 tokens and native foundations do not establish full Fluent library adoption | docs/reference/research/ux/design-system.md:17 | read | High | Document says #150 stays open, while current GitHub issue is closed; do not silently infer adoption acceptance |
| C6 | Local checks do not establish human/screen-reader/WCAG acceptance | docs/reference/research/ux/wcag-conformance-baseline.md:18 | read | High | No acceptance checkbox changed |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| W1 | Resident choices must be measure/version specific; no contact action | Story #232 | https://github.com/jmservera/ama/issues/232 | 2026-10-27 | Current body | High |
| W2 | Safety view cannot classify, set clocks, close or authorize | Story #227 | https://github.com/jmservera/ama/issues/227 | 2026-10-27 | Current body | High |
| W3 | Programme states and chase/update ownership must remain separate | Story #230 | https://github.com/jmservera/ama/issues/230 | 2026-10-27 | Current body | High |
| W4 | Finance safe endpoint is reviewed readiness/export; missing economics input is Unknown | Story #225 | https://github.com/jmservera/ama/issues/225 | 2026-10-27 | Current body | High |
| W5 | User explicitly requires one scoped gate, no full gate, and stop at any owner decision | Current task request | User conversation, 2026-10-27 | 2026-10-27 | Current request | High |
| W6 | Current interface guidelines successfully retrieved | Web Interface Guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-27 | Current main response | High |

### Contradictions / Conflicts

* C3 requires complete --all publication evidence; W5 excludes that execution. C2 documents partial-tier support but does not remove C3 and reserves complete gates for big features. No silent policy change made.
* C5 describes #150 as open and partial adoption; current GitHub #150 is closed. Preserve the documented foundation limit rather than claim full Fluent adoption from issue state.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Readiness implication |
| --- | --- | --- | --- | --- |
| Q2 | Read-only role surfaces with explicit evidence boundaries fit initial story scope | W1-W4 | High | Existing read contracts need investigation |
| Q3 | Requested scoped-only publication cannot meet applicable unconditional full-gate policy | C2-C4, W5 | High | Blocked before further phases |

## Key Discoveries

* Open #152 does not invalidate its merged IA contributions.
* No acceptance criterion is treated as proven by reading its requirement.

## Alternatives and Decision State

* Reuse existing scoped reads and native workbench; reject parallel role simulator.
* Selected current action: stop at B1 and preserve original evidence locally.
* No implementation recommendation selected because screen-contract investigation is incomplete.

## Open Questions, Risks, and Residual Uncertainty

* B1: scoped-only gate authorization versus mandatory full-tier publication policy.
* Availability of synthetic fields and authentic same-home continuity remains uninvestigated after the stop boundary.

## Current Decisions

* Preserve identity, role enforcement and existing human approval boundaries.

## Unresolved Decisions

* B1 needs an authorized reconciliation of the applicable instructions or authorization for the required complete gate. No gate waiver, policy edit or full execution is inferred.
* Posted exactly one blocker comment: https://github.com/jmservera/ama/issues/149#issuecomment-6444242587.

## Potential Next Research

* After B1 resolution, resume Research into existing browser harness, fixtures, role screens and same-home read contracts before Plan.

## Planning Readiness

* Blocked: B1 prevents the requested delivery under current instructions.
* Research disposition: executed, partial.
* Plan, critique, Implement and Review: Not run. No source changes, tests, browser exercise, cleanup, gate, push or PR creation.

## Artifact Self-check

* Ordered Wider, Deeper and Contrarian waves recorded; remaining screen investigation explicitly deferred.
* Claims cite stable internal/external IDs; no source acceptance or accessibility result invented.
* Artifacts remain local until publication policy permits push. Local commit is not publication.
* No paid inference, real datasets, secrets, Azure operations or destructive cleanup performed.

## Resumed cycle 2: owner-authorized continuation

The original blocked result above is preserved. On 2026-10-27 the owner
explicitly authorized one scoped --changed parent gate instead of --all for
this delivery. B1 is resolved, not waived by the delivery agent. Resolution
comment: https://github.com/jmservera/ama/issues/149#issuecomment-6444333817.

### Wider

Re-read all nine current GitHub story bodies (#225-#233), the existing
workbench manifest and navigation, API guide, and the three UX standards.
Eight existing authenticated roles serve eleven research perspectives.
There are no separate Asset Executive, Procurement or Data Steward logins.
Those perspectives must not become a role switcher or invented authority.
The original eleven-perspective manifest already permits explicit deferrals.

### Deeper

* C7: src/api/src/zava_forward/api/workbench.py:16 supplies navigation only;
  endpoint guards and core projection retain authority.
* C8: src/api/src/zava_forward/api/web/app.js:145 owns route cancellation,
  unsaved changes and status; api() rejects denied requests and ended sessions.
* C9: src/core/src/zava_forward/core/projection.py:145 preserves resident
  evidence only for existing authorized roles, redacts staff notes by need,
  and removes finance from non-finance roles. Reuse these exact responses.
* C10: src/api/src/zava_forward/api/web/panels.js:123 already renders scope
  revisions, measure decisions, service requests and update commitments;
  new specialist views can read those same fields without a new write path.
* C11: src/api/src/zava_forward/api/web/app.js:750 already distinguishes
  hazard sending, receipt, acceptance, repair and human restart evidence.
* C12: src/api/checks/design_system_browser_check.py:226 starts a loopback
  server with constructed fixtures and a scrubbed environment, waits for
  health and terminates its own process. Reuse this harness, not a deployed app.
* C13: src/api/checks/workbench-manifest.json:21 records eleven perspectives
  and nine workflows as partial/deferred, not delivered acceptance.
* C14: src/api/src/zava_forward/api/web/ops.js:23 keeps independent quality
  acceptance, defects and reinspection distinct from provider submission.
* C15: src/api/src/zava_forward/api/web/panels.js:87 retains both stock
  sources; authority and eligibility remain Unknown without human evidence.

### Contrarian

Rejected a new parallel backend or screen-only fixtures: existing scoped case
reads contain the evidence and unknowns. Rejected fabricated eligibility,
prices, hazard clocks and new staff roles. Missing source inputs remain
visible with a responsible role and manual next action; no request to invent
them is needed. No story authorizes new paid inference; AI economics is a
design section with Unknown inputs, not an AI invocation.

A parent containing all child commits would empty independently reviewable
child PRs targeting that same parent. Therefore the parent is a draft shared
foundation/integration anchor. Each independent child starts from its shared
foundation and is reviewed before owner-controlled integration. The parent
PR remains draft and explicitly does not claim integrated role delivery.
Local child tests cover their own exact source; the single scoped gate covers
the exact parent candidate only. Integration after review invalidates that
receipt and requires the next owner-authorized validation, not a fabricated
aggregate pass.

### Synthesis and readiness

Selected: a shared read-only specialist-screen host in the existing workbench,
with native links, URL case/page state, bounded lists, existing server-scoped
reads and separately reviewable role modules. Preserve normal workbench and
manual paths; the contractor module uses only its existing restricted reads.
Priority order remains #232, #227, #230, #225, then #226/#228/#229/#231,
and cross-role trace #233 last.

Research disposition: executed (resumed cycle complete).
Planning Readiness: Ready for bounded synthetic engineering delivery, not
whole-issue, integrated, human usability or WCAG acceptance.
No further research cycle is needed for the read-only design boundary.
