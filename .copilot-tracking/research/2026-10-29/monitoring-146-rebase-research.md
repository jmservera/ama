---
title: Monitoring 146 rebase research
description: Focused evidence for reconciling draft PR 512 with main
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Research Brief

Bring draft PR #512, `feat/monitoring-146`, up to date with `origin/main`,
preserving monitoring intent and upstream changes. Refs #146. Audience:
coordinator performing later publication. Output mode: convergence, preparing
planning. Research posture: focused, selected for a named branch and conflict.
Research root: `.copilot-tracking/research/2026-10-29/`.

## Research Parameters and Direction Controls

* Execute the explicitly requested Research, Plan, Implement and Review sequence.
  Remain in manual mode; the request authorizes each named phase, not an
  ongoing automatic follow-up session.
* Rebase is explicitly authorized. Do not push, change Azure resources, close
  issues, weaken hosted gates, or introduce legacy application paths.
* Preserve append-only log/index contributions; upstream rubric and scenario
  manifest are authoritative. Recheck pinned scenario sources if changed.
* Use `/tmp/mv`, scoped Ruff/mypy/unittest checks, and lock-gate any full API
  discovery. Record actual commands/results and distinguish local evidence
  from hosted checks and human acceptance.

## Extension Registry and Provenance

* Repository instructions: selected for branch, evidence, namespace, retention
  and validation constraints.
* RPI skills: selected sequentially for the four requested phases. Independent
  critique and post-implementation review will use bounded delegates.
* Web/design and Azure deployment skills: skipped; no web edits or deployment.
* Research specialists: skipped; this is one coupled, low-volume git trace.
* Interaction unavailable and unnecessary: branch/base and side-selection
  rules were supplied explicitly.

## Prior Knowledge and Questions

Original case study, addendum, reference index and owner memory read.
Memory is context, not evidence. Prior monitoring RPI evidence is historical
and will not be rewritten. No matching prior session was returned by the
seven-day history query.

1. What conflicts and upstream changes affect the monitoring source?
2. Which current checks exercise the rebased change and pinned scenarios?
3. Does existing CI failure represent a source defect or an approval boundary?

## Research Cycle Log

### Cycle 1, Wider

Initial inspection found a clean active topic branch with two commits, no
in-progress rebase, and an open draft PR targeting main. Fetch succeeded.
The branch delta is infrastructure and documentation only, not application
Python. Existing source CI jobs passed; rubric conclusion failed and scoring
remains pending. Next: inspect actual logs and upstream conflict surfaces.

### Cycle 1, Deeper

Read-only `git merge-tree --write-tree --name-only origin/main HEAD`
identifies real content conflicts only in `docs/reference/README.md` and
`docs/reference/log.md`; infrastructure merges automatically. Upstream changes
the default employee model and derived model outputs, independent of monitoring.
The branch has two original commits and no branch-owned rubric or scenario
manifest changes. Only upstream rubric scores differ since the common ancestor.
The scenario validator binds four public source files by SHA-256, so run its
test module even if the manifest merges without conflict. `/tmp/mv` has Python
3.12.3, Ruff 0.17.1 and mypy 2.4.0. Account resolved as id 8036360/login jmservera;
repository-local privacy email configured before any rewritten/new commit.

Reflection: choose concatenation/insertion at the index/log conflict sites,
not either complete side. Retain all latest-main source outside the monitoring
delta. Validate actual resulting infrastructure, not just conflict-marker absence.

### Cycle 1, Contrarian

Challenged the assumption that rebase alone establishes CI success. The failed
rubric run reports `HttpError: Resource not accessible by integration`, whereas
the existing source CI jobs passed. This is hosted integration evidence, not a
local application defect; do not modify rubric protection or claim a rerun.
Challenged silently trusting automatic Bicep merges: focused Bicep policy,
IoT/container/governance/secret regressions and offline compile are required.
Challenged one-sided append-only conflict resolution: compare pre-rebase and
upstream log/index additions explicitly after resolution. Upstream index
frontmatter itself has duplicate dates; normalize only the conflicted date
field when resolving to the latest date rather than propagating invalid YAML.

Reflection: no new domain research or Azure operation would improve this
bounded reconciliation. Stop after one complete inline cycle.

## Evidence Log

* C1: `src/README.md:24` describes completed src-only cut-over.
* C2: `src/README.md:75` describes local gate scope and evidence limitations.
* W1: https://github.com/jmservera/ama/pull/512 retrieved 2026-10-29.
  Open draft, head `feat/monitoring-146`, base `main`.
* W2: https://github.com/jmservera/ama/actions/runs/40586304604
  retrieved 2026-10-29. Conclusion fails with integration access error.
* C3: `infra/main.bicep:104` and upstream diff: new employee-model inputs and
  Foundry outputs must coexist with the monitoring module.
* C4: `src/core/src/zava_forward/core/synthetic/scenario_manifest.py:38`
  defines four pinned public sources; `src/core/tests/test_scenario_manifest.py:22`
  validates current iteration, hashes and honest unavailable statuses.
* C5: `.github/workflows/src-ci.yml:80` runs per-project units, Ruff and mypy;
  `:202` requires offline Bicep and infrastructure controls.
* C6: `.copilot-tracking/changes/2026-10-27/monitoring-146-changes.md:49`
  records 87 historical focused infra tests; this is prior evidence, not
  current validation.
* C7: `docs/reference/README.md:20` and `docs/reference/log.md` are actual
  merge-conflict surfaces as confirmed by merge-tree on the fetched refs.

## Findings, Alternatives and Decision State

Accept rebase onto fetched main `356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7`,
preserving all log entries, both index contributions, upstream rubric/scenario
files and both independent Bicep intents. Original branch head:
`3faac99513fff0e73ebd8a2bcef4e91a0ae4946f`.
Reject whole-file ours/theirs for append-only surfaces: loses unrelated work.
Reject merge instead of rebase: conflicts with caller direction.
Defer hosted integration/approval investigation beyond the observed failure:
coordinator owns publication; do not alter permissions to manufacture success.
No independent research delegates ran.

## Open Questions, Risks and Further Research

Hosted CI cannot run on an unpublished new head; coordinator must publish and
retain hosted evidence later. No local pass will be labelled a hosted pass.
The mandatory complete local publication gate is separate from the requested
bounded local checks. This task does not publish; missing gate prerequisites
must remain explicit, with no cloud fallback. Actual monitoring activation
and original human/operational residuals remain outside scope.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Questions 1-3 are answered by C3-C7 and W1-W2. No unresolved implementation
decision remains. Parent proceeds to the explicitly requested Plan phase.
Artifact self-check: focused scope, all three waves, evidence, alternatives,
limitations and continuation recorded.
