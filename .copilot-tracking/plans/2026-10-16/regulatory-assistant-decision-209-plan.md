---
title: Regulatory Assistant Decision Plan
description: Bounded documentation plan for issue 209
ms.date: 2026-10-16
---

Task ID: issue-209. Task slug: regulatory-assistant-decision-209.
Status: documentation complete; single Review Conformant; publication pending.

## Executive Summary

Record the owner's synthetic-only acceptance in ADR 0005, preserve human
authority and operational gaps, compare all three options and accept the
deterministic-card comparator as the chat ship test. Update the index and
append-only log. No implementation or paid service work is authorized here.

## User Decisions and Requirements

* Owner decision dated 2026-10-16: ACCEPT for synthetic development only.
* Juan Manuel Servera is the exercise Legal, Compliance and DPO owner, not a
  verified real company delegate.
* Keep real owners, grant awards, contracts and leases unverified.
* Compare no assistant, cards/store without chat, and full assistant with chat.
* Chat must demonstrate value over deterministic cards with provision links.
* Mark Search and monitoring costs unknown rather than invent estimates.
* Docs only; preserve prohibited paths, issue body and existing approvals.
* Publish a topic-branch PR with Refs #209, the required identity and trailer.

## Goals

Make the dated decision, approval capacity, non-authority, reversal condition
and remaining evidence needs discoverable without claiming completed delivery.

## Scope and Non-Goals

Canonical targets: docs/adrs/0005-regulatory-compliance-assistant.md,
docs/reference/README.md, docs/reference/log.md.
Tracking evidence: research, plan, details, critique, changes, review and state.
No generated targets, source changes, other requirement approvals, deployment,
new pricing or legal currentness research. Historical proposal wording in the
dated addendum remains unchanged; the index points to the later ADR decision.

## Functional Requirements

ADR status must distinguish accepted synthetic development from unapproved
operational reliance. Explicitly list never-permitted assistant actions,
exercise ownership and retained separation of authors and approvers. Present
trade-offs and a fallback for chat failing or lacking benefit evidence.

## Non-Functional Requirements

Use existing Markdown/frontmatter conventions and relative links. Preserve all
prior log content, the 2026-10-15 fixture safeguards and existing architecture.
No secrets, private datasets, identifiers or fabricated evidence.

## Acceptance Criteria

Audit each issue criterion separately: three-option comparison; authority
boundary and prohibitions; named owners/capacity or gap; unverified binding
sources; accepted chat value gate; Search/monitoring cost estimated or unknown.
Distinguish passing documentation criteria from unmet implementation,
operational approval, actual benefit measurement and actual cost verification.
Leave issue checkboxes unchanged for the coordinator.

## Phase Checklist

<!-- P01 -->
### P01: Record the decision

* [x] P01-T01: Update ADR status, owner decision, options, gate and open items.
* [x] P01-T02: Add index routing and append the knowledge-base log.

<!-- P02 -->
### P02: Validate and publish

* [x] P02-T01: Review links, append-only log, scoped diff and six criteria;
  execute one post-implementation RPI Review and record remaining gaps.
* [ ] P02-T02: Commit, push branch and create PR against main with Refs #209.

## Validation Contract

Test ownership: documentation review owned by this task; no executable behavior
changes. Exact removals: none. Maximum additions: the named tracking artifacts,
one ADR decision/ownership/options/cost treatment, one index route and one log
entry; no new application files or tooling. Semantic coverage: each of six
issue criteria. Regression coverage: prior safeguards, unchanged log prefix,
relative links and protected-path exclusion. Evidence: git diff --check,
local relative-link/path review, diff review and a criterion-by-criterion matrix.
Ruff, mypy, unit suites, app run and Azure are not applicable to docs-only work.
Hosted checks remain Pending CI until observed.

## Critique Disposition

One independent final-candidate critique executed, verdict Revise; both
findings dispositioned without another critique:

* PC-001: Apply the completion-integrity requirement. Resolve introduced
  documentation defects during validation before Review; any material open
  Review finding prevents a passing completion claim. Retain accepted future
  ownership/source/value/cost gaps. Do not apply advice to reopen implementation
  after Review: the one-pass lifecycle routes those findings to later work.
* PC-002: Applied. Resolve gh identity again at the commit boundary and derive
  the repository-local noreply address, checking it against the owner's required
  identity. Verify both author and committer before publication.

## Follow-Up Items

Operational ownership/source verification, measured chat value and actual
service sizing/pricing remain out of scope and explicitly unproved.

## Handoff

Research: .copilot-tracking/research/2026-10-16/regulatory-assistant-decision-209-research.md.
Details: .copilot-tracking/details/2026-10-16/regulatory-assistant-decision-209-phase-details.md.
Implementation changes: .copilot-tracking/changes/2026-10-16/regulatory-assistant-decision-209-changes.md.
