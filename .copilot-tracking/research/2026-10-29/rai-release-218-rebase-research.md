<!-- markdownlint-disable-file -->

# Task Research: rai-release-218-rebase

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md |

## Research Brief

* What to research: PR #504 divergence, integration conflicts, policy/scenario pins and relevant CI checks.
* Why it matters: prepare a locally validated rebase for the coordinator, without publishing.
* Audience or intended use: implementation, independent review and coordinator handoff.
* Scope: feat/rai-release-218 versus fetched origin/main; existing RAI implementation, tests, index/log and CI contracts.
* Non-goals: new RAI functionality, resolving human acceptance, Azure operations, push, merge or issue closure.
* Criteria: preserve both branch intents; main wins rubric/scenario conflicts; no legacy source; truthful local validation.
* Requested outputs: dated full RPI evidence and a committed, rebased candidate.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | What must be preserved, what conflicts, and which local checks cover integration? |
| Codebase scope | src/core, src/api, branch docs, CI and scenario manifest |
| External scope | GitHub PR #504 metadata only |
| Initial internal candidate areas | Original 2026-10-27 RPI evidence, project guides, CI, branch diff |
| Initial external candidate areas | https://github.com/jmservera/ama/pull/504 |
| Research posture | focused |
| Posture provenance | Default for explicit bounded integration task |
| Explicit limits / deadline | No push, no Azure; /tmp/mv; full API discovery requires shared-lock admission |
| Posture-specific completion basis | Scope coverage and materiality |
| Edits allowed during research? | No; evidence and required workflow state only |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No secrets/private data or cloud/real-model calls |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide | Layout, evidence, Git identity, acceptance boundaries | Selected |
| Skill | rpi-research | Full-loop caller | Three-wave research evidence | Selected |
| Skill | rpi-plan, rpi-implement, rpi-review | Full-loop caller | Later phase protocols | Selected at phase boundaries |
| Research specialist | hve-core-all:rpi-researcher | Registered internal researcher | Independent evidence lanes | Skipped: one tightly coupled integration trace |
| Skill | Web/design skills | No web change proposed | Web implementation/review | Not applicable |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit full-loop, rebase and no-push instructions are sufficient | Full-loop request authorizes automatic progression for this task | Reuse named clean active branch; no routine prompts |

## Scope and Success Criteria

* Keep original RPI evidence unchanged, preserve append-only entries and release-policy behavior.
* Verify the named branch is the open draft PR head.
* Test current source, not historical test counts. Distinguish local evidence from hosted success.

## Task Research Requests

* Rebase onto current main, preserve index/log intent and main rubric/scenario content.
* Run Ruff, formatting, applicable mypy and relevant unittest modules; record commands/results.
* Commit with Conventional Commit and required co-author; coordinator owns push.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| narrow | Integration only, source in src/, tests outside packages | User | No feature expansion |
| exclude | Azure, push, issue-closing keywords | User | Local-only delivery |
| change | Rebase explicitly authorized | User | History replay allowed; no force-push |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What branch changes and main changes intersect? | depth | H | answered |
| Q2 | Which relevant CI checks and scenario pins must be verified? | depth | H | answered |
| Q3 | Which risks invalidate a claim of mergeability/CI success? | straightforward | H | answered |

## Prior Knowledge Gate

* Clean worktree, branch feat/rai-release-218, open draft PR #504 targeting main verified before writes.
* git fetch origin succeeded; origin/main is 5653547507f3056f09a726a18516237728da5e5b.
* Existing branch has source/evidence commit 63e9074a and integration commit e9b5604d beyond its merge base.
* Prior PR validation is historical, not evidence for the rebased candidate.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inline inspection: PR metadata, divergence, project guide and knowledge-base index.
* Reflection: named branch matches the task and is clean; only two branch commits need replay. Existing policy-bound release work and documentation must survive newer main.

#### Wave 2: Deeper

* Inspected the three production deltas, original changes evidence, workflow,
  project tool configuration and manifest source allowlist (C3-C6).
* Reflection: main changes existing briefing-cache tests in the same API module,
  not the three production modules. Preserve both the added RAI regressions and
  main's dynamic cache-key assertions. Manifest recipe/workbench pins changed on
  main, so main's manifest must survive and test_scenario_manifest must run.

#### Wave 3: Contrarian

* Challenged the assumption that /tmp/mv imports this worktree: direct import
  resolves core/API/agents to another worktree (C7). Explicit local src paths
  must precede installed editable paths in every validation command.
* Challenged historical test/mergeability claims: main updated overlapping tests
  and scenario pins; old results cannot be promoted. Hosted CI remains unavailable
  for unpublished commits (W1, C2).
* Reflection: no production overlap requires an invented semantic rewrite.
  Source-identity assertions and relevant regressions are sufficient to test the
  scoped integration; a complete publication receipt remains separate.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Rebase and preserve both branches | C3, W1 | accepted | Explicit caller instruction; clean matching active branch |
| Main rubric/scenario wins | C5, C6 | accepted | Caller instruction plus changed public recipe pins |
| Trust default /tmp/mv imports | C7 | rejected | Would validate the wrong checkout |
| Claim hosted/full-gate success locally | C2, W1 | rejected | No push or final receipt requested/executed |

#### Cycle Re-entry Evaluation

No additional cycle needed: all bounded questions have direct evidence and
remaining publication/human acceptance does not change the local integration.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Packages and tests have separate src/project locations | src/README.md:11 | read | high | No mvp implementation |
| C2 | Prior broad results are not fresh publication evidence | src/README.md:77 | read | high | Exact-head gate and hosted approval remain distinct |
| C3 | Branch modifies three policy-binding modules and adds API regressions | src/core/src/zava_forward/core/assistants.py:297; src/core/src/zava_forward/core/ai_registry.py:70; src/core/src/zava_forward/core/quality.py:47 | git diff | high | Main has no overlapping production changes |
| C4 | CI runs project discovery, Ruff, formatting and mypy | .github/workflows/src-ci.yml:82 | read | high | Browser/images/SQL are separate contracts |
| C5 | Main briefing-cache assertions use dynamic keys | src/api/tests/test_assistant_release.py:532 (main revision) | git diff HEAD...origin/main | high | Retain alongside added RAI tests |
| C6 | Main updates hashes of recipe and workbench sources | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:46 | git diff | high | Run src/core/tests/test_scenario_manifest.py:17 |
| C7 | Default shared venv editable imports target another worktree | src/core/pyproject.toml:23; src/api/pyproject.toml:28 | /tmp/mv import probe | high | Use explicit local project/sibling src paths; no shared pip mutation |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- | --- |
| W1 | Open draft PR head is the named branch, target main, references only | GitHub PR API | https://github.com/jmservera/ama/pull/504 | 2026-10-29 | high |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | Docs need both entries; production delta remains independent; main test correction must survive | C3, C5, W1 | Rebase without wholesale ours/theirs on tests/docs |
| Q2 | Project statics, release/oversight/RAI/ranking/quality and manifest modules apply | C3-C6 | Focused validation, no full API discovery needed |
| Q3 | Wrong-checkout imports, unpublished CI and stale receipts undermine claims | C2, C7, W1 | Verify import origins; report local-only outcome |

## Key Discoveries

* Shared /tmp/mv is usable only with explicit local source precedence.
* Scenario pins changed; main's manifest already carries the updated hashes.

## Alternatives and Decision State

Selected: caller-authorized rebase, retaining three production deltas, both test
changes and all append-only entries. Rejected: merge (caller selected rebase),
blanket branch-file selection (would lose main intent), default venv imports
(wrong worktree). Confidence high for this integration boundary (C3-C7).

## Open Questions, Risks, and Residual Uncertainty

* Hosted checks cannot assess unpublished commits.
* Repository complete-gate publication requirement is distinct from scoped local checks; no publication is requested.

## Planning Readiness

Ready. C1-C7 and W1 cover branch identity, conflicts, validation and boundaries.
No research blocker. Automatic RPI parent may proceed to Plan.

## Research Disposition

Executed; Complete. Wider, Deeper and Contrarian completed inline because the
evidence is one tightly coupled integration trace, not independent research lanes.

## Current Decisions and Unresolved Decisions

Caller directions are confirmed; no unresolved local implementation decision.
Coordinator owns publication and hosted CI; human RAI acceptance remains outside
this task and is not inferred.

## Potential Next Research

None selected. Re-enter only for an actual conflict or failing regression that
exposes missing semantics.

## Closeout Record and Advisory Next Step

Research Complete; disposition executed; Planning Readiness Ready. Automatic RPI
parent continues to Plan. No source was changed in Research. No further user
action is needed for phase advancement.

## Sources

* W1 - GitHub PR #504 - https://github.com/jmservera/ama/pull/504 (retrieved 2026-10-29).

## Artifact Self-Check

Questions answered; three ordered waves and synthesis complete; posture, limits,
extensions and decisions recorded; evidence IDs resolve; speculation and
publication limits explicit; no delegated lane or external legal claims.
