<!-- markdownlint-disable-file -->
---
title: Rubric src cut-over research
description: Issue 198 evidence and planning readiness
ms.date: 2026-10-27
---

## Research Brief

* Target: #198, rubric registry cut-over and src evidence continuity.
* Purpose/audience: establish a truthful implementation and draft PR for the owner.
* Scope: registry, rubric workflow, tests, migration scoring history and cut-over documentation.
* Non-goals: deploy, paid/model scoring, private data, version bump, retrospective invented scores.
* Criteria: prove each acceptance criterion or explicitly retain its gap.
* Output mode: convergence; prepares planning.

## Research Parameters

* Posture: focused, selected for a bounded named issue.
* Evidence root: `.copilot-tracking/`.
* Starting internal areas: `.github/rubric/`, rubric workflow, ADR 0006,
  cut-over evidence pack and linked migration PRs.
* External areas: GitHub issue/PR/run metadata only.
* Limits: local tests only; no full gate; at most one locked scoped heavy gate
  for large changes; preserve workflow/check names and rubric_version.
* Research edits: evidence and workflow state only.

## Extension Registry and Provenance

| Candidate | Disposition | Authority |
| --- | --- | --- |
| Repository instructions | Selected | src layout, dated evidence, branch safety |
| rpi-research | Selected | Three-wave evidence and readiness |
| Research specialist | Skipped | Single tightly coupled trace, handled inline |
| Web/security skills | Skipped | No UI changes or vulnerability audit |

## User Participation and Research Decisions

The user explicitly requests the full ordered loop and draft PR. No routine
phase confirmation is needed. The existing clean topic branch
`feat/rubric-src-198` has no open PR and is reused. Owner comments explicitly
settle no rubric_version bump. No missing intake answer prevents research.

## Direction Controls

* Preserve historical scores; do not pretend local fixtures are model scores.
* Refs #198 unless all criteria are evidenced; do not tick unknown acceptance.
* No deployment, secrets, private datasets or retired-package changes.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What registry/workflow changes remain after migration? | depth | Open |
| Q2 | What score comparisons exist and what remains unavailable? | depth | Open |
| Q3 | What caused the recorded 19 failures, and what is current? | depth | Open |

## Prior Knowledge Gate

Read issue #198 and its owner comments, parent #195, knowledge-base index,
memory and original/addendum framing. Historical claims remain to be verified
against current code and hosted records. #292 reportedly added exclusions;
directory retirement is already on main. These are starting claims, not
assumed fresh rubric acceptance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inspection verified ADR 0006 layout and rubric counting, the linked
parity matrix, BRD demonstration/operational-authority distinction, PRD current
source baseline, registry, workflow and tests. The src glob covers package code,
external tests, project manifests, web assets and Dockerfiles. Reflection:
no new include glob or workflow production change is needed (C1-C3).

#### Wave 2: Deeper

Inspected registry commit history, migration PR bodies/comments and historical
score snapshots. #295 removed the dead infrastructure glob, #300 removed
executable legacy globs, #302 removed the README glob. All migration merge
snapshots retain the same 47-point assessment, not fresh per-PR scores.
#499 has a real 77 vs 77 hosted score. Ran existing rubric scripts locally:
18 failed, 355 passed, seven skipped. Reflection: repair migration-related
test assumptions and document actual sequencing, not replay removal edits (C4-C7).

#### Wave 3: Contrarian

Challenged the apparent 47-to-77 "migration gain": scored SHA and run metadata
show intervening work, so attribution is unsupported. Queried sticky score
comments for #292, #295 and #296-#302: none are available. The old 19-failure
claim is not the current failure count: seven seed-related, ten trigger/path
assumptions and one unrelated deck-selection mismatch fail today. Reflection:
retain the deck mismatch as unrelated, do not change production deck selection
or invent historical scores. Historical sequencing cannot now be satisfied
retroactively; keep Refs #198 and acceptance gaps.

### Parent Synthesis and Disposition

* Accepted: existing registry includes/excludes are correct; preserve them.
* Accepted: synthetic fixed gate fixture, baseline-relative prepare assertion,
  explicit current workflow trigger contracts and src/retired-path regressions.
* Rejected: rubric_version bump, redundant registry edits, any fake fresh score.
* Deferred: unrelated deck test mismatch and unavailable per-migration hosted
  comparisons. No owner/legal decision is required for independent repairs.
* Re-entry: unnecessary; focused scope covered, remaining gap cannot be
  reconstructed by more local searching.

## Evidence Log

| ID | Evidence | Location |
| --- | --- | --- |
| W1 | Issue and owner direction: exclusions delivered in #292; no version bump; score comparisons remain | https://github.com/jmservera/ama/issues/198 (retrieved 2026-10-27) |
| C1 | src includes and exclusions, seven solution criteria | `.github/rubric/artifacts.json:28-42` |
| C2 | Standard layout, tests outside packages, no additional include needed | `docs/adrs/0006-src-layout-and-cutover.md:53-124`, `:301-321` |
| C3 | Trusted base registry; retired historical narrative still reads as current | `.github/rubric/README.md:344-404`, `.github/rubric/scripts/test_prepare.py:292-349` |
| C4 | Live baseline drives fixed-66 gate expectations | `.github/rubric/scripts/test_gate.py:16-61`, `.github/rubric/scripts/test_prepare.py:411-433` |
| C5 | Stale mvp path and assumptions every workflow supports push/PR/manual | `.github/rubric/scripts/test_safe_output_runtime.py:156-174` |
| C6 | 77 current score, version 2, actual workflow provenance | `.github/rubric/scores/latest.json:1-30` |
| C7 | Historical sign-off row remains unmet; later retirement qualifies rubric | `docs/architecture/cutover-evidence-pack.md:1729`, `:1894-1896` |
| W2 | Exact removal timing: #295 infrastructure, #300 legacy code, #302 README | https://github.com/jmservera/ama/pull/295, https://github.com/jmservera/ama/pull/300, https://github.com/jmservera/ama/pull/302 (retrieved 2026-10-27) |
| W3 | Deletion PR hosted score 77/100 vs 77/100, no dip | https://github.com/jmservera/ama/actions/runs/40560161654 (PR #499 sticky comment, retrieved 2026-10-27) |
| C8 | BRD separates demo evidence from live authority; PRD names current src baseline | `docs/brds/agentic-retrofit-programme-brd.md:958-980`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md:474-480` |

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C3/W2: protect and test the delivered registry; correct live
documentation rather than add globs. Q2 answered with explicit gaps by C6-C7/W3:
47 then 77 observed, no attribution and no recovered fresh migration scores.
Q3 answered by C4-C5 and the local suite: 18 current failures; 17 tied to
seed/trigger assumptions, one unrelated deck fixture failure. Seven real MCP
runtime tests skip because GH_AW_RUNTIME_DIR is unavailable.

## Alternatives and Decision State

Leave failures and document only: rejected because migration-related coverage
would remain unusable. Repair production gate or scoring version: rejected,
no evidence of a production fault. Repair scoped tests and reconcile durable
evidence: selected. No approval or issue closure inferred.

## Risks and Potential Next Research

Fresh per-migration scorecards are unavailable from the checked PR comments and
merge snapshots. They remain an acceptance gap, not a local inference target.
Deck selection drift is unrelated and requires its own coherent task.

## Planning Readiness

Ready for scoped implementation, not whole-issue closure. Research disposition:
executed, complete. All three waves ran inline; no delegated lane was needed.
Self-check: cited questions answered or bounded as gaps; no secret/private data,
production writes or fabricated model judgement. Parent continues to Plan.
