---
title: AMA Scientific Paper Memory Review 001
description: Fresh static review of the AMA scientific paper writer and reviewer agent
ms.date: 2026-11-02
human_review: unchecked
---

## Review Scope

Purpose assessed: preserve the learned author-review details for a subsequent
session without placing volatile facts in permanent instructions. The source
artifact was reviewed read-only at
.github/agents/ama-scientific-paper-writer-reviewer.agent.md. The author log,
author reasoning, manuscript, and author-review records were not read. No
native manuscript workflow was run.

Applicable host extensions were limited to Markdown, writing-style, and prompt
artifact conventions. They informed the review but did not change its bounded,
read-only workflow. The package README was read only to verify the agent's
current validation-routing claims.

## Findings

No Critical, High, Medium, or Low findings.

## Dimension Coverage

| Dimension | Assessment | Evidence |
| --- | --- | --- |
| Architecture fit | Pass | A direct, single-purpose scholarly writing and review agent is appropriate; no orchestration is required for the stated scope. |
| Workflow contract | Pass | Modes, authority, phase routing, stop rules, and the final execution versus assessment statuses agree across .github/agents/ama-scientific-paper-writer-reviewer.agent.md:24-59, :61-236, and :236-247. |
| Outcome and structure | Pass | Outcome, success criteria, and stop rules precede the phase protocol at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:9-37. |
| Emphasis calibration | Pass | Invariants protect authority, evidence integrity, and scope; conditional scholarly judgment is expressed as decision rules. |
| Load-timing placement | Pass | Volatile paper facts are recovered conditionally from the named current sources rather than embedded as fixed facts at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:87-168. |
| Reference discipline | Pass | The agent links canonical package sources and instructs the reader to reuse records rather than copy case narratives or make a parallel ledger at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:87-128 and :147-156. |
| Model fit | Pass | The unchanged, unpinned direct-agent model selection appropriately uses the current session selection. |
| Tool-contract executability | Pass | The unchanged, unpinned tool surface does not claim unavailable destructive capability; all writes remain subject to explicit authorization at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:38-59. |
| Reviewer bounding | Pass | Review work is limited to named evidence and manuscript scope, with real locators, evidence states, and no unrelated experiments at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:170-198 and :219-235. |
| Context handling | Pass | Retrieval is just in time and limited to the agreed input scope. The conditional recovery identifies README, disposition, evidence locators, active TeX inputs, protocol, and TODOs without treating historical counts or dates as durable instructions at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:87-168. |
| Evaluation hooks | Pass | Validation is selected from the current package README; checks, compiler diagnostics, publication gates, and actual blockers are distinguished at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:157-168. |
| Evidence fidelity | Pass | Evidence states, claim locators, inspected-material limits, and prospective-result limits are explicit at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:129-198. |
| Safety and enforcement | Pass | The agent prohibits unapproved research, paid calls, data collection, Git mutation, publication, visibility, and OSF actions while preserving human authority at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:38-59 and :164-168. |
| Extension precedence | Pass | Host conventions are treated as scoped review criteria and do not widen authority or the read-only review scope. |
| Portability and maintenance | Pass | Recovery routes to current canonical records, abstracts fictional domain details and moving facts, and retains existing evidence instead of duplicating it at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:114-128 and :147-156. |
| Stale-pattern absence | Pass | The agent avoids persona-only prompting, broad persistence instructions, fabricated results, and assertion-only validation. |
| Convention conformance | Pass | Existing name, frontmatter, unpinned tools/model behavior, and Write/Revise/Review authority remain intact. The source is structured, ASCII-compatible Markdown. |
| Skill packaging | Not Applicable | The target is an agent, not a skill package. |
| Subagent design | Not Applicable | The target defines no subagent. |
| Low-reasoning tool guidance | Not Applicable | No lower-reasoning subagent is declared. |
| Tool and output schemas | Not Applicable | The target registers no custom tool or structured-output schema. |

## Requirement-Specific Checks

* Conditional recovery is correctly limited to the Everything but the Software
  package when it is a named input within the agreed scope. It routes to the
  current README, owner disposition, current author review, active protocol,
  TODOs, source pins, and evidence locators at
  .github/agents/ama-scientific-paper-writer-reviewer.agent.md:87-113.
* The contribution-led account includes research discovery, Design Thinking,
  personas and journeys, disposable prototypes, BRD/PRD/ADR revisions, backlog
  handoff, coordinator work, human feedback, and deployment/migration rivals
  when relevant at .github/agents/ama-scientific-paper-writer-reviewer.agent.md:114-128.
* Prospective results, the false-results switch, quantitative audit conditions,
  experimental-unit and dependence requirements, conditional power,
  block-aligned bootstrap concerns, and cost/control limits are preserved at
  .github/agents/ama-scientific-paper-writer-reviewer.agent.md:123-146.
* Original adverse evidence, hash and export scope, literal prompt, editable
  export bindings, and the single additive Supplement are preserved at
  .github/agents/ama-scientific-paper-writer-reviewer.agent.md:104-113 and :147-156.
* Current README-scoped validation correctly distinguishes structural, test,
  PDF, scientific, human, hosted, and publication checks, including Tectonic
  versus pdfLaTeX-marker diagnostics and honest repository-gate blockers at
  .github/agents/ama-scientific-paper-writer-reviewer.agent.md:157-168.
* The current package README supports the routing claim: its current status at
  docs/capstone/thought-leadership/everything-but-the-software/README.md:11-44
  identifies the single additive Supplement, prospective limits, Tectonic
  warning and optional pdfLaTeX-marker distinction, and blocked gate without
  treating prior records as current approval.

## Verdict

Pass. The agent meets the stated memory-preservation purpose without embedding
transient case facts as permanent instructions. No Critical or High finding
remains. Human review remains unchecked.
