<!-- markdownlint-disable-file -->
# Task Research: affected-person-challenge-220

| Field | Value |
| --- | --- |
| Date | 2026-10-19 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md |

## Research Brief

* What to research: actual existing challenge, resident decision, complaint, versioned AI/source/policy and dependency invalidation paths for issue #220.
* Why it matters: deliver a bounded reusable engineering slice rather than duplicate delivered controls or invent human policy.
* Audience or intended use: implementation planner, independent critique/reviewer and coordinator.
* Scope: src core/API/agents contracts, component guides, PRD FR-052/FR-043/AC-071, current issue and comments.
* Non-goals: cloud writes, real inference, private data, tenant setup, automated redress decisions, consent/refusal/sanctions, hazard-clock changes, unrelated closure or publication.
* Criteria: both constructed channels, permitted explanation and version/human decision provenance, human owner, non-digital route, next update and resolution, exact dependency-only invalidation and negative boundaries.
* Requested outputs: evidence-backed overlap map and implementation-ready recommendation followed by the explicitly requested ordered Plan, Implement and original Review.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1 existing overlap; Q2 safe version/identity/dependency contracts; Q3 test and UI seams |
| Codebase scope | src, relevant docs, tools/rpi-checks.py |
| External scope | current GitHub issue; current web guidelines only if web edits |
| Initial internal candidate areas | resident_decisions, continuity, controls, AI registry, API server/web, existing tests |
| Initial external candidate areas | https://github.com/jmservera/ama/issues/220 |
| Research posture | focused |
| Posture provenance | explicit bounded caller scope and named sources |
| Explicit limits / deadline | no remote writes, real AI calls, private data or new framework/workflow; fixed base eeb6c3aba5d07244ae3cc0e53d839617fd928e3b |
| Completion basis | source-backed scope coverage and contrarian evidence |
| Edits allowed during research | research and required workflow tracking only |
| Resolved evidence root | .copilot-tracking/ |
| Excluded sources | private .env/data; fictional role responses as authority |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and authority | Disposition |
| --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | repository-wide supplied instructions; original/addendum/KB read at intake | selected |
| Skill | rpi-research | actual three-wave research and primary evidence | selected |
| Skills | rpi-plan, rpi-implement, rpi-review | requested later phases | deferred until actual phase transition |
| Skills | web-design-guidelines, accessibility | conditional web implementation/review scope | load before applicable work |
| Specialist | RPI Researcher | available hve-core-all:rpi-researcher; single continuous source trace | skipped: inline investigation avoids redundant delegation |

## User Participation and Research Decisions

Intake direction is explicit: run the entire ordered RPI cycle. This is direct
authorization of automatic progression, not an inferred manual-to-auto switch.
No routine phase question is needed. Interactive tenant setup is separate.
The clean supplied topic branch equals the supplied base; no matching PR exists.
Live issue has no comments or explicit blocking dependencies. Caller-provided
related issues remain context, not blocking gates. Owner human/legal/RAI and
publication approval are not inferred.

## Scope and Success Criteria

All five issue acceptance criteria require actual constructed engineering
evidence; local results do not establish live AI, Azure or human acceptance.
Preserve original critique and Review even if adverse. Commit source and dated
evidence before the clean exact-head 17-group gate; no commits after gate.

## Task Research Requests and Direction Controls

Reuse existing modules; preserve server recorder identity (#406), generated
stock lineage and resident/human decisions. Tests stay outside packages.
No push, PR, merge, issue/board/settings changes. All externally visible
publication awaits coordinator independent assessment.

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What does existing consent/complaint/challenge code already provide? | depth | H | open |
| Q2 | How can exact source/policy/proposal dependencies and human decisions be preserved? | depth | H | open |
| Q3 | What real core/HTTP/SQL/browser seams prove both routes and negative boundaries? | depth | H | open |

## Prior Knowledge Gate

Read original case study, addendum intake sections, KB index and owner memory.
Memory remains untouched and is context only. Verify supplied overlap claims
against current source rather than trust issue delivery labels.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Completed inline. Existing resident actions already supply staff identity,
independent measure-decision review, complaint owners and remedy separation.
Existing AI tasks supply retained source hashes, envelope and human review;
assistant tasks separately compute snapshot staleness. Form collection is
explicitly unapproved and has no accepted review dependency graph.
Reflection: extend existing case resident path and retained AI proposal contracts;
do not create a duplicate complaint workflow or pretend forms are approved.

#### Wave 2: Deeper

Completed inline. The retained priority path uniquely combines actual ranking
policy version, case IDs, human disposition and actionable/relied_on projection.
It lacks a source-version capture; capture that at creation, never reconstruct
old evidence. Resident `_operation` already replays validation under SQL's
writer and truthfully reports committed acknowledgement failures. Derived stale
state can depend on case-held challenge resolution without mutating original
recommendation or review evidence.
Reflection: choose the retained priority vertical slice, with explicit limits
for unrelated assistant/form paths and unknown historical source versions.

#### Wave 3: Contrarian

Completed after Deeper. Challenged the tempting generic graph/review rewrite:
forms have only unapproved candidates, the assistant queue has independent
transaction/release contracts, and legacy source labels are case-wide rather
than field/document-version dependencies. Inventing per-document dependencies,
source authority or live redress policy would overclaim. A challenge does not
prove a correction. Record a supplied human resolution separately; only an
explicit "Correction recorded" plus evidence invalidates its exact selected
proposal, case-source hash or policy version. Original decisions stay intact.
Reject automatic complaint closure, source edits, sanctions, hazard waits and
consent inference. Current registered owner/reason rights and writer replay are
required; client-supplied actors, dependencies and timestamps are rejected.
Reflection: coherent bounded engineering is ready; whole-system AC-071 and
human/live acceptance must remain partial, rather than duplicate frameworks.

#### Parent Synthesis and Disposition

Accept existing resident/identity/transaction controls (C1/C2/C5). Accept retained
priority slice (C3/C4). Reject invented global dependency engine and retroactive
source history (C3/C6). Defer other assistant/form challenge integration until a
separate scoped iteration. No absent owner policy blocks recording supplied
constructed evidence under the existing exercise baseline.

#### Cycle Re-entry Evaluation

No further cycle needed: the source trace answers Q1-Q3 with concrete seams;
remaining live/human authority is a declared non-goal, not a missing local design
decision. Ready for Plan. Research disposition: executed.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool / confidence |
| --- | --- | --- | --- |
| C1 | Resident actions already record independent measure review and separate response/remedy ownership | src/core/src/zava_forward/core/resident_decisions.py:423,527-665 | read, high |
| C2 | Current named actor/owner checks and SQL validation replay/committed outcomes are reusable | src/core/src/zava_forward/core/resident_decisions.py:49-239; src/core/src/zava_forward/core/sqlstore.py:554-618 | read, high |
| C3 | Retained priority captures actual policy version and human disposition; source hashes absent | src/core/src/zava_forward/core/store.py:753-818,846-892 | read, high |
| C4 | Real policy registry has verified content hashes; case-source hash helper already exists | src/core/src/zava_forward/core/ranking.py:22-64; src/core/src/zava_forward/core/ai_tasks.py:188-193 | read, high |
| C5 | Existing projection provides resident/reason/contractor boundaries and workbench native forms | src/core/src/zava_forward/core/projection.py:48-52,155-207; src/api/src/zava_forward/api/web/panels.js:108-237 | read, high |
| C6 | Forms explicitly unapproved; assistants have independent snapshot/release control | src/core/src/zava_forward/core/forms.py:1,115-129; src/core/src/zava_forward/core/assistants.py:667-695 | read, high |
| C7 | Actual loopback HTTP, SQLite and Chromium harnesses exist, outside packages | src/api/tests/test_resident_api.py:27-113; src/api/checks/provenance_browser_check.py:19-60 | read, high |
| C8 | Ordered clean exact-head gate requires actual SQL/browser/images/scans and external receipt | src/README.md:58-118; tools/rpi-checks.py:32-59 | read, high |
| C9 | Existing baseline permits staff workbench, synthetic digital/non-digital intake and prohibits agent redress decisions | docs/case_study_48_addendum.md:108-130,454-500; docs/prds/zava-forward-retrofit-programme-demonstrator.md (FR-052, AC-071) | read/search, high |

### External Evidence

| ID | Claim | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Open issue defines five ACs, related 130/86/88/154 and parent 218; no comments or blocking dependency text | https://github.com/jmservera/ama/issues/220 | 2026-10-19, gh issue view including comments | high |
| W2 | Current web guideline rules successfully retrieved before any implementation | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-19, web_fetch, complete | high |

## Findings Mapped to Questions and Evidence

Q1 answered C1/C6: overlap is real but no supplied challenge bound to priority
AI/source/policy versions exists. Q2 answered C2-C5: capture actual creation
source/policy references, freeze target+human disposition, derive dependency-only
staleness after supplied human correction, preserve original evidence. Q3 answered
C7/C8: real JSON/SQLite core and loopback HTTP with Chromium plus full gate;
no private dataset or real model needed for these local contracts.

## Alternatives and Decision State

Select existing priority/workbench slice with two resident actions and a
read-projected target catalog. Reuse existing writer, current staff/owner rights,
policy/source hash helpers and native forms. Alternative generic new service or
cross-assistant graph rejected (C1/C6) as duplication and unsupported authority.
Unknown old source versions remain unavailable; priority ID itself can still be
challenged. A digital route is staff recording an explicitly supplied digital
challenge, not a new resident portal or proof of resident authentication.

## Open Questions, Risks, and Residual Uncertainty

Live use and human/legal/RAI approvals remain outside local engineering.

## Planning Readiness

Ready for the bounded Plan. Research disposition: executed, complete.
Whole-system/live AC-071, legal/privacy/RAI authority and resident comprehension
remain explicitly unverified. Self-check: three ordered waves complete, evidence
IDs resolve, rejected alternatives and limits preserved, no source edited.
