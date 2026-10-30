<!-- markdownlint-disable-file -->

# Task Research: pr507-evidence-corrections

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/pr507-evidence-corrections-research.md |

## Research Brief

Correct two PR #507 review findings without restoring discarded implementation.
Audience: owner applying the replacement PR body and reviewers of Refs #198.
Scope: cutover evidence pack, registered B6 evidence, current integrated diff,
prior frozen boundary, relevant tests and local links. Output mode: convergence.
Non-goals: score edits, issue completion, remote writes, unrelated test repairs.

## Research Parameters

Focused posture, selected for the caller's two named documentation findings.
Internal candidates: docs/architecture/cutover-evidence-pack.md,
.github/rubric/artifacts.json, latest synchronization RPI evidence and Git diff.
External scope: read-only PR #507 metadata/review evidence.
Resolved evidence root: .copilot-tracking/.
Research writes only evidence and required session state.
Completion requires all three waves and evidence for each requested correction.

## Extension Registry and Provenance

Repository instructions apply to all inputs: preserve history, use the existing
branch, dated RPI evidence, independent critique/Review, local-only commit.
rpi-research selected; remaining RPI skills activate at phase boundaries.
No domain specialist selected: this is one coupled documentation trace.
No web/UI skill applies. No delegation for the bounded research lane.

## User Participation and Research Decisions

The explicit full-loop request authorizes all four phases in this invocation.
No interactive mode transition or follow-up work is inferred. Non-interactive
execution; no clarification needed for the supplied bounded scope.

## Scope and Success Criteria

* Separate original candidate tests/guide delivery from integrated documentation.
* Verify the current frozen diff and 355/18/7 results rather than reuse old claims.
* Prove the recovery artifact is registered for B6; name a later PR without
  inventing an existing PR number.
* Produce /tmp/pr507-body.md, retain Refs #198, no closing-keyword references.
* Validate using /tmp/mv; preserve scores and original evidence; commit, no push.

## Task Research Requests and Direction Controls

Only the two review findings are in scope. Never hand-edit scores/latest.json.
No source/fixture/guide changes; no issue closure, push, PR update or merge.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What did the original and current candidates actually contain? | depth | Open |
| Q2 | What registered artifact can genuinely reopen B6 in later work? | straightforward | Open |
| Q3 | Which relevant local checks establish the correction's boundary? | straightforward | Open |

## Prior Knowledge Gate

Clean worktree at 254d2274 on feat/rubric-src-198; PR #507 open against main.
The current PR body still claims 374/1/7 and delivered fixtures/guide edits.
Prior synchronization artifacts must be checked before accepting these claims.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial index/registry inspection identifies solution-code (src/**/*) as B6
evidence; .github/rubric/README.md has no registry include. The pack contains
new synchronization notes alongside unreconciled original delivery claims.
Reflection: inspect the frozen synchronization record and affected pack section,
then verify matching/gate behavior before selecting corrected wording.

#### Wave 2: Deeper

The integrated branch differs from main only in three documentation files and
dated tracking artifacts. Protected inputs have no delta. Independently
recomputed the previous integrated three-document hash: 8059b4aa91f469ff735c33c620bd23cc1b529d108a5737a08d862b53f0061883.
This belongs to HEAD 254d2274 and base ffd8f35e63b24905b9aeb937dbf2a7fe9968747f,
not the original candidate's de87d9e0 hash against 09099ecd.
Reflection: the corrected body must identify both historical review boundaries
and cannot call either the final corrected candidate's hash (self-reference).

#### Wave 3: Contrarian

Read actual prepare/gate behavior instead of inferring that all documentation
is scored. solution-code includes src/**/* and B6; no registry artifact includes
the rubric guide or evidence pack. The incremental gate requires a changed
registered path citation for an increase; a README's mere presence is not
sufficient. Existing src tests omit a README-specific case but real matcher
assertions can cover src/README.md without editing fixtures.
Reflection: name a proposed later PR by title, not a fictional PR number.
Do not actually change a scored README to force scoring. Preserve original
results as history, qualify acceptance rows in place, and append KB history.
One completed cycle covers the bounded questions; further sources are redundant.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | docs/architecture/cutover-evidence-pack.md:2120-2162 | Integrated inputs/results already qualified, but downstream claims conflict |
| C2 | docs/architecture/cutover-evidence-pack.md:2236-2264 | Unregistered B6 guide, discarded fixtures and guide repairs still credited |
| C3 | .github/rubric/artifacts.json:26-32 | solution-code includes src/**/* and B6, excludes vendor/data/build outputs |
| C4 | .github/rubric/scripts/prepare.py:278-305; .github/rubric/scripts/gate.py:181-198 | Changed registered artifacts open criteria; increases require changed present evidence |
| C5 | .copilot-tracking/reviews/logs/2026-10-27/rubric-src-198-review.md:25-34 | Original frozen de87d9e0 boundary against 09099ecd; historical only |
| C6 | .copilot-tracking/changes/2026-10-30/rubric-src-198-sync-changes.md:155-164 | Integrated frozen 8059b4aa boundary; independently recomputed |
| C7 | .copilot-tracking/changes/2026-10-30/rubric-src-198-sync-changes.md:99-112 | Integrated 355 passed, 18 failed, 7 runtime skips; prepare false |
| C8 | .github/rubric/scripts/test_prepare.py:263-348 | Existing registered/src/exclusion tests are relevant selectors |
| W1 | https://github.com/jmservera/ama/pull/507, retrieved 2026-10-30 via gh | Open matching branch; body/title stale; both exact review comments retrieved |

## Findings Mapped to Questions and Evidence

Q1 answered by C1/C2/C5/C6/C7: original test/guide work is discarded,
not a current deliverable. Integrated suite remains adverse.
Q2 answered by C3/C4: use src/README.md in proposed later PR
"docs(src): strengthen B6 navigation and evidence", only once it actually changes.
Q3 answered by C8: run focused rubric selectors, migration regressions,
actual prepare/matcher assertions, local links/anchors, diff and unchanged-input
checks. /tmp/mv lacks pytest (observed missing-module failure); installing only
that missing test dependency in isolated external storage avoids shared-venv
mutation. No application code changes require full API/browser/SQL work here.

## Alternatives and Decision State

Accepted: qualify original/current claims in place; preserve original tracking
and append-only log; write body including suggested documentation-only title.
Rejected: restore discarded fixtures/guide, edit scores, or cite an unregistered
guide for recovery. All conflict with supplied scope or C3/C4.
Deferred: later real B6 README improvement, inherited suite/runtime repairs,
historical acceptance and publication gates.

## Open Questions, Risks, and Residual Uncertainty

The rubric suite may retain baseline failures; do not repair unrelated code.
The complete publication gate remains separate from this local-only correction.

## Planning Readiness

Ready. Research disposition: executed, Complete. Parent advances to Plan under
the explicit full-loop request; no additional research or user decision needed.
Self-check: three ordered inline waves, Q1-Q3 answered, stable evidence IDs,
scope and alternatives recorded; no implementation performed during Research.
