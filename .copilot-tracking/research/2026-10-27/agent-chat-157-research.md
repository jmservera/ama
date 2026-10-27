<!-- markdownlint-disable-file -->

# Task Research: agent-chat-157

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/agent-chat-157-research.md |

## Research Brief

* Target: parent #157 and children #162, #159, #164, #163.
* Purpose/audience: establish evidence-backed independent engineering work and preserve owner/DPO/Legal/accessibility gates for one PR.
* Scope: existing src chat, assistant, memory, evaluation and workbench implementations and linked ADR/BRD/PRD.
* Non-goals: new agents, real personal data, private datasets, Azure operations, inference spend, invented approvals or retention periods.
* Criteria: each issue criterion must be independently evidenced; incomplete human criteria stay incomplete.
* Requested outputs: dated research, plan/details/critique, changes and Review artifacts, tested implementation and one PR.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What remains implemented vs unproven? Which gaps can be fixed without human decisions? |
| Codebase scope | src/, linked docs and tools' local validation contracts |
| External scope | Named GitHub issues and recorded decisions only |
| Initial internal candidate areas | Chat runtime, API routes, workbench, evaluation harness, privacy draft |
| Initial external candidate areas | jmservera/ama issues 157, 162, 159, 164, 163 and dependencies |
| Research posture / provenance | Focused / bounded caller task |
| Explicit limits | Local tests only; at most one locked scoped changed gate for large changes; no full gate, uv, secrets or private data |
| Completion basis | Named criteria covered with material gaps identified |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and disposition |
| --- | --- | --- |
| Instruction | Repository guidance | Selected: src layout, KB conventions, topic branch, privacy-safe commits |
| Skill | rpi-research | Selected: ordered three-wave evidence |
| Skill | rpi-plan, rpi-implement, rpi-review | Deferred to corresponding phases |
| Skill | web-design-guidelines, accessibility | Applicable if workbench edits selected |
| Specialist | Independent critique and Review | Reserved for those required gates; research performed inline |

## User Participation and Research Decisions

Caller explicitly requests the full ordered loop and supplied branch. No routine phase confirmation needed. Human approvals cannot be inferred. Clean worktree on feat/agent-chat-157; no existing PR found.

## Scope and Success Criteria

Reuse existing abstractions, default-deny isolation and proposal-only boundaries. Do not equate scripted tests with human or serving-model effectiveness.

## Direction Controls

User's no-full-gate instruction overrides the repository default for this task. Publication must disclose unperformed full validation. Do not close the parent while #440 or approval gates remain unproven.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What do the current requirements and recorded decisions actually authorize? | In progress |
| Q2 | Which remaining technical gaps can be independently delivered? | Open |
| Q3 | What validation and acceptance remain blocked by named humans? | Open |

## Prior Knowledge Gate

Issue bodies contain stale descriptions of no implementation. Owner comments record merged work in #281, #286, #305 and #307 and accepted ADR #279. Verify against current src rather than rebuilding.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Named issue bodies, acceptance criteria, comments, ADR 0004, KB index, memory and original/addendum read. ADR adoption is proven by #158 and local ADR, while remaining access/privacy/evaluation/assistive-technology decisions are not.

Reflection: prioritize current source and linked requirement sections; stale issue summaries are not a mandate to replace existing work.

#### Wave 2: Deeper

Inline trace: `ChatPanel.ask` reprojects current sources and excludes prior
assistant claims, but discards provider usage and silently truncates source
JSON through the generic 2,000-character `block` helper. Its server adapter
does not consult the existing AI release gate. The legacy `/messages` route
still calls a different uncited runtime. The panel omits the canonical
special-category warning and mislabels refusals as model unavailability.

Reflection: reuse the existing provider envelope, release admission and
metadata-only ledger, not a second store or governance service. Preserve an
explicit known grounding failure instead of claiming semantic accuracy.

#### Wave 3: Contrarian

Challenge: synthetic privacy references and successful scripted poisoning
cases are not permission to call a real model. Existing `Store.ai.gate`
denies unreleased tasks; chat must consume it. A registry entry or an owner
name string alone would not satisfy actual release. Do not invent a
retention period, per-role budget, threshold or break-glass policy.
Current development golden set already has passing poisoning/injection
scenarios and a known unsupported-claim/valid-citation failure.

Challenge: a provider callback can change permissions during its call;
recheck current user/case and the exact source projection before releasing
a reply. Thread questions remain untrusted context, not authority.

Reflection: choose fail-closed dispatch, bounded input with workflow fallback,
per-invocation metering, canonical warning and targeted adversarial regression.
Memory is not currently consumed by `ChatPanel`; do not activate it in this
slice. General memory-path tests are separate, not panel assurance.

### Parent synthesis and disposition

Accepted C2-C6 for independent engineering. Defer all human decisions in C1/W1,
and whole-parent #440 acceptance in W2. Reject a new memory/model runtime and
invented approvals. No further cycle needed: all bounded questions have
source-backed answers or explicit missing human evidence.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Option C accepted, live privacy/access/threshold gates remain open | docs/adrs/0004-per-user-agent-chat-and-memory.md:12 |
| W1 | Existing work covers many checked criteria; remaining human blockers explicitly named | gh issue view 159/162/163/164 --comments, retrieved 2026-10-27 |
| W2 | Parent additionally requires stabilization #440 and tokenomics | gh issue view 157, retrieved 2026-10-27 |
| C2 | Provider envelope contains validated tokens but adapter drops it | src/agents/src/zava_forward/agents/chat.py:32; src/core/src/zava_forward/core/ai.py:82 |
| C3 | Panel has lexical guards and excludes assistant history, but source block truncates | src/core/src/zava_forward/core/chat_panel.py:303; src/core/src/zava_forward/core/chat_isolation.py:49 |
| C4 | API /messages bypasses cited panel; /ask uses ChatModel without gate | src/api/src/zava_forward/api/server.py:680 |
| C5 | Canonical warning exists; general workbench textarea lacks it | src/core/src/zava_forward/core/chat_privacy.py:36; src/api/src/zava_forward/api/web/chat.js:34 |
| C6 | Golden report preserves actual-model/human/held-out gaps and known grounding failure | src/agents/src/zava_forward/agents/chat_eval.py:373; src/agents/evals/chat_golden.json:82 |
| C7 | Existing AI gate routes continuity and release checks | src/core/src/zava_forward/core/store.py:66 |
| W3 | Current web interface rules retrieved in full, repo ASCII/content standard takes precedence | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-27 |

## Alternatives and Decision State

Selected: bounded fail-closed provider admission and both HTTP turn routes,
non-content consumption receipts and offline reporting, source-complete prompt
bounds, post-call permission/source recheck and canonical warning. Rejected:
new store/agent, enablement based on synthetic refs, semantic grounding claims.

## Open Questions, Risks and Residual Uncertainty

Live provider terms, lawful basis, retention, access policy, approved thresholds, held-out human-labelled data and real accessibility exercise remain unavailable.

## Planning Readiness

Ready for independent engineering only (C2-C7); live activation and full issue
acceptance blocked by human decisions. Research disposition: executed.
Q1/Q2 answered; Q3 answered with explicit unavailable evidence above.
Self-check: three ordered inline waves, traced alternatives and open gates.
