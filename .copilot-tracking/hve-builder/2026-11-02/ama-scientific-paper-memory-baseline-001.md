---
title: AMA Scientific Paper Memory Baseline Review
description: "Static baseline review for the scientific paper writer and reviewer improve request."
ms.date: 2026-11-02
---

## Purpose and Scope

Baseline static review of .github/agents/ama-scientific-paper-writer-reviewer.agent.md for an improve request. The intended improvement is durable recovery of the reusable nine-point author-review lessons and the current Everything but the Software paper context after a new session, while preserving the existing Write, Revise and Review authority boundaries.

Reviewed criteria: HVE requirements catalog and review rubric, workflow contract, repository Markdown and writing conventions, docs/reference/method/scientific-paper-writing-and-review.md, and the named paper-package evidence. This review is limited to instruction-contract gaps, duplication risk and conflicts. It does not assess the manuscript, venue fit, model migration, new agents, skills or enforcement controls.

## Findings

### High: Context handling and outcome and structure

Location: Phase Protocol, Intake and Write or Revise.

The agent directs a generic intake and one generic method-guide read, but contains no conditional recovery procedure for the active Everything but the Software package. A fresh session is not told to recover the latest review/disposition, package state, unresolved TODOs and source locators, nor to treat dated counts, page totals, protocol status and validation summaries as refreshable rather than premise facts. This blocks the stated memory-restoration purpose.

Smallest resolving change: add a compact, conditional capstone-paper recovery subsection that reads the package README, anc/revision-report.md section "Author Review Disposition 1 November", anc/case-evidence-matrix.json and review.md; recovers the current manuscript/source state, unresolved TODOs and locators; and requires refresh of volatile counts/status before use. Reference these sources rather than copying their contents.

### High: Context handling and reference discipline

Location: Evidence and Integrity; Write or Revise.

The agent does not preserve the author-review's concrete scientific contract: contribution-led prose, the discovery through renewed-feedback sequence when relevant, abstract fictional domain context and non-premise treatment of moving counts/dates. It also lacks the required package-specific guard that pending experiment results remain author TODOs with the results switch false and the actual prospective protocol unchanged.

Smallest resolving change: add conditional guidance for this paper that directs prose toward the supported contribution and workflow sequence, abstracts fictional case detail, treats counts/dates as refreshable context, and preserves pending results as TODOs while retaining the false switch and source-bound prospective protocol.

### High: Context handling and evaluation hooks

Location: Evidence and Integrity; Write or Revise.

The generic requirements for units, sample size and uncertainty do not require the four named skills or the audited definitions and claim limits. The agent therefore does not reliably recover the equation/design audit's units, estimand, experimental unit, dependence and missingness rules, or reject unsupported causal, precision and affordability claims.

Smallest resolving change: name sympy, statistical-analysis, scientific-critical-thinking and experimental-design as conditional audit skills for this package, and require the listed quantitative definitions and claim-boundary checks before presenting equations, power, causal, precision or affordability conclusions.

### High: Context handling and evidence fidelity

Location: Evidence and Integrity.

The existing claim-record rules do not capture package provenance requirements: exact source/export hash scope, original evidence retention, and preservation of one additive Supplement rather than reintroducing duplicated standalone material. A later session could make a correct-looking revision while weakening the paper's evidence chain.

Smallest resolving change: add a conditional provenance paragraph that identifies source authority, exact hash scope, native-to-export bindings, original evidence retention and the single additive Supplement rule, with changed or unavailable provenance reported rather than inferred.

### High: Evaluation hooks and workflow contract

Location: Write or Revise; Output.

The agent requests generic cross-checking but does not identify the package's current focused authoring tests, structural checks and compiler-specific diagnostics. It consequently does not distinguish an inherited inputenc warning or a pdfLaTeX-specific optional-log failure from publication-gate blockers, and does not state that it must not auto-commit, stash, publish, change visibility or collect data.

Smallest resolving change: add a conditional focused-validation note that points to the package README commands, distinguishes direct Tectonic/PDF evidence from compiler-specific optional checks, labels publication-gate status separately, and repeats the existing no-commit/stash/publish/visibility-change/data-collection boundary for this workflow.

## Passing Dimensions

* Architecture fit: Pass. A single scientific writing and review agent remains appropriate; the request does not require a new agent or architecture.
* Workflow contract: Pass for existing Write, Revise and Review authority boundaries. The mode table, switch-to-editing authorization and human ownership are clear. The package-specific recovery and validation gaps above are additions, not conflicts.
* Outcome and structure: Pass at the generic level. Outcome, success criteria and stop rules precede the protocol; the recovery gap is recorded above.
* Emphasis calibration: Pass. Strong prohibitions are reserved for integrity and authority invariants.
* Reference discipline: Pass at the generic level. The canonical scientific-paper method guide is referenced rather than duplicated. The missing package references are recorded above.
* Reviewer bounding: Pass. Review scope and output are bounded to supplied material and evidence.
* Context handling: Revise. The five High findings identify missing durable, conditional state recovery.
* Evaluation hooks: Revise. Package-specific focused checks and diagnostic interpretation are missing.
* Evidence fidelity: Revise. Package-specific provenance and Supplement preservation are missing.
* Safety and enforcement: Pass. The source agent denies unauthorized external, remote and publication actions; this review adds no enforcement-control proposal.
* Portability and maintenance: Pass. The agent uses action-oriented, inspectable Markdown and a canonical method reference.
* Stale-pattern absence: Pass. No persona-only, copied-style-guide or universal iteration-count pattern was found.
* Convention conformance: Pass. The agent has valid frontmatter and uses clear Markdown sections. The review log follows the repository requirement to retain human approval unchecked.

## Not Applicable

* Load-timing placement, skill packaging, subagent design, model fit, tool-contract executability, low-reasoning tool guidance, tool and output schemas, and extension precedence: the target has no scoped instruction layers, declared skills, subagents, model pin, tools or schema.

## Evidence Limits

This was a static, read-only review. No source artifact, manuscript, index entry, Git state, staged change or untracked review.md was modified. No native manuscript commands, remote queries, paid research, data collection, visibility change, commit, stash or publication action ran. Dated package counts and statuses were assessed only as documented context and must be refreshed by a future authoring session.

## Verdict

Revise.

The current agent preserves its Write, Revise and Review authority boundaries, but five High gaps prevent it from fulfilling the requested durable recovery of the nine-point author-review lessons and current paper context. The smallest suitable change is one compact, conditional package-memory subsection with references to the named canonical and package sources, plus narrowly scoped scientific-audit, provenance and focused-validation rules.
