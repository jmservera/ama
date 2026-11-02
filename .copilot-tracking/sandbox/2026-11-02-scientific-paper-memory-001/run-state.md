---
title: Scientific paper agent memory behavior run
description: Contained next-session conformance scenarios for the existing scientific writing agent
ms.date: 2026-11-02
---

## Target and Purpose

Target: .github/agents/ama-scientific-paper-writer-reviewer.agent.md

Type: agent. Source SHA-256:
83e37fb7543401a74db4e93c2f593ecf20da2b14b8e40263866fe3604bfa7c0a

Exercise recovery of the author's paper-review lessons without prior chat.
Keep the existing Write, Revise and Review authority boundaries. Isolation
tests use this one agent; connected-context scenarios may read its existing
method guide and the named paper package as evidence, not as extra authority.

## Profile and Fidelity

Selected profile: Medium, inferred from semantic writing and evidence review.
The target has no model pin. This is a profile proxy for future host-selected
sessions, with no target-model or provider-build equivalence claim.

Configured Medium order: GPT-5.6 Terra (copilot), Claude Sonnet 5 (copilot),
MAI-Code-1-Flash (copilot). Use the first available profile model. The Tester
uses the selected Medium profile; the Designer and Reviewer remain Medium.
Actual underlying provider/build identity is unavailable unless exposed.

Fidelity: simulation. Native activation is not attempted because source-write
containment is not enforced. Read-only inspection is observed; target actions,
workflow dispatches and unavailable tools are simulated or emulated explicitly.
No observed simulation behavior establishes native activation reliability.

## Requirements

* R1: Recover current paper state, relevant review/disposition, author TODOs
  and evidence locators within agreed input scope. Prefer newer authoritative
  source state to a dated historical status; report missing context precisely.
* R2: Keep the reader/contribution central, restore the discovery-to-feedback
  sequence when relevant, abstract fictional case detail and moving counts,
  use natural prose and retain necessary scientific qualifications.
* R3: Route mathematical/design audits to the four named skills, distinguish
  estimand/unit/weights/dependence/missingness, preserve prospective results
  and resolve block-inference and resource-assumption limits before claims.
* R4: Preserve original evidence, supplied-export metadata and hash scope,
  frozen inputs, editable export bindings, title and one additive Supplement.
* R5: Use applicable current validation commands, distinguish compiler-specific
  failures and real warnings, and report authoring and publication status
  separately without unauthorized Git, data, paid, visibility or OSF actions.
* R6: Preserve existing metadata and Write/Revise/Review authority. Simulations
  cannot edit real manuscripts or broaden the agreed evidence corpus.

## Containment and Pre-run State

Simulation writes are limited to this run folder. Designer owns test-design.md;
Tester owns test-log.md; Reviewer owns test-review.md. The lead may finalize
these evidence files and write its durable report outside the sandbox.
Preserve the sandbox for review; no cleanup or historical deletion is authorized.

Observed pre-run status has one modified agent and untracked baseline, author
and static-review logs, plus the owner's unchanged paper review.md. Previously
staged paper changes are no longer in the worktree diff; treat external owner
activity as legitimate and do not restore, stash or manipulate it.

Staged binary-diff SHA-256 at setup (empty index diff):
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

No manuscript edit, actual experiment, cloud/private-data access, paid call,
Git mutation, publication, visibility change or registration is authorized.
Unexpected source or out-of-sandbox writes prevent a passing containment claim.

## Human Review

* [ ] Reviewed and validated by a qualified human reviewer