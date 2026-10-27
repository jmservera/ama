---
title: Faster Gate 470 Coordinator Author Evidence
description: Bounded HVE Builder improve-mode authoring evidence for the coordinator gate policy
ms.date: 2026-10-27
---

## Stage and boundary

* Mode: improve; authoring status: Complete.
* Source: .github/agents/ama-backlog-delivery-coordinator.agent.md.
* Evidence: .copilot-tracking/changes/2026-10-27/faster-gate-470-agent-author.md.
* Classification: Major. The owner explicitly changes stage-gate selection
  and parent/child branch and PR decisions, not merely wording.
* Existing branch: feat/faster-gate-470. The matching open-PR query returned
  no PR. Existing runner/test changes and other tracking artifacts belong to
  the parent workstream and were left untouched.
* All frontmatter was preserved as opaque bytes, without field inspection
  or tool-configuration assessment. No new capability surface was authored.
* No agents, workflows, full gate, Azure operations, commits or pushes ran.

## Inputs and baseline findings

Bounded reads covered the supplied target body, installed HVE Builder
workflow-contract.md, requirements-catalog.md and stage-dispatch.md references,
plus introductory project specification, knowledge-base index and owner-memory
context. No open-ended repository exploration was performed.

The original target required complete local receipts for all issues, including
documentation work, repeated that requirement in the brief, candidate output,
publication, merge and rebase instructions, and generally based dependent work
on merged main. It did not encode the requested parent-topic integration stack
or the verification-image retention boundary.

## Authored policy and requirement mapping

| Change | Exact policy | HVE requirement |
| --- | --- | --- |
| Tier selection | Full tier for big features, releases, infrastructure, deployment, SQL and security-sensitive changes; focused tier for small issues, tooling and documentation outside those categories; mixed scope escalates and changed scope is reassessed | Outcome and structure: explicit success criteria; no conflicting layers |
| Focused evidence | Relevant unit and focused checks with recorded commands, results and justified non-applicability; no unconditional full receipt or heavy-service dependency | Evaluation and validation: runnable checks; evidence, not assertions |
| Full evidence | Complete local gate and external full receipt; full-scope verification remains the default; partial receipts cannot satisfy full tier | Agent architecture: define stage gates and terminal outcomes |
| Receipt lifecycle | Fresh final-head evidence after commit, correction, rebase or base change; changed source/tool/image inputs invalidate receipts; retain verification images until --verify-receipt succeeds; preserve adverse receipts | Outcome and structure: stop rules and missing-evidence behavior |
| Runner options | --changed --jobs N for focused affected-project runs; --required-scope partial only for focused partial receipts whose coverage matches planned checks; --resume FAILED_RECEIPT uses a new --out and preserves the immutable parent receipt | Outcome and structure: explain non-obvious reasons; evaluation and validation: evidence, not assertions |
| Parent and child PRs | Parent topic is the integration branch; child branches base on it, child PRs target it and declare dependency; integration parent targets main; hierarchy does not serialize independent siblings or require parent main merge before child work | Outcome and structure: explicit success criteria; no conflicting layers |
| Stack lifecycle | Fetch and validate the actual target base; apply stack-aware wave, merge and rebase conditions; retain parent topic while needed; independently validate integrated parent; do not silently retarget children | Agent architecture: own the control flow and context |
| Publication and review | Candidate brief, output, independent exact-head assessment, publication, merge and correction/rebase all use selected-tier evidence; full receipts remain required when full tier applies | Outcome and structure: no conflicting layers |
| Open issues | Use Refs #{number} for kept-open/unmet issues, including pending integration; preserve the existing fully satisfied issue-closure policy | Safety and enforcement: confirm risky actions |

Both tiers retain the complete original RPI evidence requirement, independent
review and exact-head assessment, required hosted CI, current review verdict,
failure handling and human approval boundaries. The selected tier cannot waive
its own failing or missing checks. The existing execution route, model,
correction-cycle limit, board synchronization, merge commands, publication
authority and prohibition on bypassing protection were not otherwise changed.
Pre-existing execution examples outside the policy surface were left intact.

## Available author checks

| Check | Owner | Status | Evidence and limits |
| --- | --- | --- | --- |
| git diff --check | local | Passed | No whitespace errors in current worktree diff |
| Opaque frontmatter preservation | local | Passed | Original HEAD and edited file frontmatter bytes match; no fields inspected |
| Body policy assertions | local | Passed | Ten requested markers present and four stale blanket-full-gate phrases absent after Markdown whitespace normalization |
| Fenced-code delimiter balance | local | Passed | Body fence count is balanced; not a Markdown parser or native host loader |
| Independent static review | local | Deferred | Parent owns fresh-context review; author checks are not an independent verdict |
| HVE behavior gate | local | Deferred | Major mutation requires parent invocation of hve-builder-tester on the final candidate |
| Native host validation | local | Unavailable | No supplied native agent validator was executed; frontmatter was not parsed or graded |
| Required hosted checks | CI | Pending CI | No publication or CI dispatch performed in this authoring-only stage |

The first literal policy-marker check stopped on a line-wrapped phrase.
Normalizing Markdown whitespace corrected the check without changing the
candidate; the final bounded assertion run passed. These checks do not claim
native execution, behavior conformance or CI success.

## Handoff

Authoring is complete within the two-file write boundary. Independent static
verdict is pending. Behavior execution is Deferred, behavior verdict is Not
available, and fidelity is not selected because the parent will invoke the
tester. Overall lifecycle outcome remains Deferred, not Pass.

Next action: parent obtains independent final-state static review, invokes
hve-builder-tester for this Major policy mutation, and records applicable host
validation and hosted evidence before claiming lifecycle completion.
