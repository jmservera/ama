<!-- markdownlint-disable-file -->

# Task Research: fabric-rebase-558

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/fabric-rebase-558-research.md |

## Research Brief

* What to research: safely reconcile PR #558 with current main and identify local CI-equivalent checks.
* Purpose and audience: provide the coordinator a mergeable local candidate with original dated RPI evidence.
* Scope: existing Fabric research, shared index/log, upstream rubric and scenario manifest, component validation.
* Non-goals: new product research, executable features, Azure changes, publication, merging or issue closure.
* Criteria: preserve both documentation intents and append-only history; upstream-owned rubric/manifest; no legacy source; explicit actual validation results.
* Requested outputs: research, plan, critique, details, changes, independent Review and local Conventional Commit.
* Output mode: convergence, preparing planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which branch/ancestry is authorized, what conflicts, and which checks apply? |
| Codebase scope | PR #558 and current origin/main |
| External scope | GitHub PR metadata only; no web/product re-research |
| Initial internal candidate areas | docs/reference/README.md, docs/reference/log.md, .github/rubric, scenario manifest, src component guides and CI |
| Initial external candidate areas | Existing PR #558 metadata/checks |
| Research posture | focused |
| Posture provenance | Default for explicit bounded reconciliation |
| Explicit limits | No push, no Azure, no closing keywords; full API discovery only after nonblocking shared-lock admission |
| Completion basis | Material questions covered with direct evidence, including contrarian validation |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | Provided project-wide guidance; source layout, preservation and publication gates | Selected |
| Skill | rpi-research | Installed RPI skill; three-wave evidence contract | Selected |
| Skill | rpi-plan, rpi-implement, rpi-review | Explicit requested lifecycle | Selected for subsequent phases |
| Specialist | Independent critique and Review | Installed task agents; bounded independent judgments | Reserved for required gates |
| Specialist | Research worker | Single coupled low-volume investigation | Skipped; direct inline investigation |
| Skill | Web/design and regulatory skills | No web edits or new regulatory claims | Not applicable |

## User Participation and Research Decisions

The explicit full-loop request supplies scope and action authority. No routine
question is needed or available in this non-interactive execution. The user
authorizes rebase/history replacement locally but explicitly withholds push.
The clean local topic branch is reused; no owner work is moved or discarded.

## Scope and Success Criteria

Preserve the eight original PR files' research intent. Bring current main into
the authorized local tracking branch. Prove ancestry, path ownership and relevant
checks; report hosted CI as unobserved until coordinator publication. Do not
confuse local mergeability with GitHub's unchanged remote mergeability.

## Task Research Requests and Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Rebase origin/main | Owner | No merge commit or unrelated branch creation |
| Keep both log/index entries | Owner | Resolve shared docs semantically |
| Upstream rubric and manifest | Owner | Retain exact origin/main content |
| /tmp/mv; component lint/types/tests | Owner | Use installed namespace and sibling test fixtures |
| Local commit only | Owner | No push, PR edits, merge or Azure |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is the exact authorized branch/base and PR lifecycle? | straightforward | Answered |
| Q2 | Which paths conflict and how can both intents survive? | depth | Answered |
| Q3 | What validation catches pinned-source and CI regressions? | depth | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index/memory, source gate and retention policy.
History search found no prior session on the two exact branch names in seven
days. Original Fabric research and its dated lane evidence are retained rather
than regenerated. Intake PR metadata contradicts the supplied draft description:
the PR is open and ready, not draft. Do not alter its lifecycle.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Intake inspected clean status, branch, remote, PR metadata, fetched origin and
enumerated branch-only commit/files. One commit f009d37 adds eight documentation/
research artifacts; main is 91e890e07af036263316c153cbc7ceff780cdaa2.
Reflection: shared index/log are likely conflict surfaces; no executable
feature implementation is justified.

#### Wave 2: Deeper

Inspected the original and upstream changes to the index and append-only log,
component pyproject configuration, scenario-manifest tests and hosted selectors.
Upstream removes duplicate index frontmatter and adds monitoring, finance, IoT
and resident-content entries. The branch adds Fabric navigation and an appended
research entry. The shared log tail needs union, not one-side replacement.
Rubric latest score changed upstream; the scenario manifest did not.
Reflection: preserve the entire upstream log as a prefix and append the
original Fabric block; retain upstream frontmatter and all navigation.

#### Wave 3: Contrarian

Challenged the assumption that an existing venv proves the correct checkout:
/tmp/mv imports core/API from another worktree by default. Explicit local
source and sibling source/test PYTHONPATH entries must precede those editable
paths. Do not reinstall into the shared venv unnecessarily. The scenario test
validates pinned public sources, so run it even though the manifest is unchanged.
The lock admission probe passed, but this task does not need full API discovery:
docs-only focused tests avoid expensive irrelevant work. CI paths exclude this
documentation-only diff from Source projects CI; hosted checks remain a future
observation, not a local success.
Reflection: require actual module-origin verification and focused tests, not
unqualified reuse of another worktree's environment. No new source or manifest
hash update is justified.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Authorized rebase with semantic doc union | C5, W1 | Accepted | Explicit direction, clean matching tracking branch |
| Upstream frontmatter/rubric/manifest ownership | C4, C5, C6 | Accepted | Main already repairs frontmatter; no PR override justified |
| Local PYTHONPATH override | C7 | Accepted | Existing editable installs point elsewhere |
| Full API discovery | C6, C7 | Deferred | No API changes; focused validation is sufficient for this slice |
| Fresh Fabric product re-research | C5 | Rejected | Would broaden a bounded branch reconciliation and rewrite dated evidence |

#### Cycle Re-entry Evaluation

No further cycle required: all material scope questions are answered. Actual
conflict resolution and command results belong to Implement, not more research.

## Evidence Log

| ID | Finding | Location / command | Confidence |
| --- | --- | --- | --- |
| C1 | Migrated projects and tests belong to separate src project source/test trees | src/README.md:10 | High |
| C2 | Local gate binds committed candidate/base and never substitutes for hosted/human approval | src/README.md:69 | High |
| C3 | Original tracking and adverse evidence must be preserved | docs/reference/method/tracking-retention-policy.md:10 | High |
| C4 | Index already has duplicate ms.date before this task | docs/reference/README.md:4 | High |
| C5 | Branch delta is one eight-file documentation/research commit; upstream shared-doc additions have distinct intent | docs/reference/README.md:23; docs/reference/log.md:8124; git diff base/main/HEAD | High |
| C6 | Scenario tests validate pinned source bytes; CI project checks use component lint/format/mypy | src/core/tests/test_scenario_manifest.py:21; .github/workflows/src-ci.yml:3,82 | High |
| C7 | /tmp/mv has Python 3.12 and dev tools but editable imports point to another worktree; nonblocking lock probe passed | src/core/pyproject.toml:35; src/api/pyproject.toml:46; interpreter origin/probe commands | High |
| W1 | PR open, not draft; head jmservera/fabric-research, base main; no checks reported | https://github.com/jmservera/ama/pull/558; gh pr view/checks, retrieved 2026-10-30 | High |

## Findings, Alternatives and Decision State

Selected: focused rebase with semantic doc preservation. Reject merge commit
because the owner explicitly requests rebase. Reject replacing whole shared
files because doing so loses one side's knowledge. Source changes are not
presumed necessary.

## Open Questions, Risks and Residual Uncertainty

Actual rebase conflicts and local validation outcomes remain implementation work. GitHub CI
cannot assess the new candidate until the coordinator pushes it. Full publication
gate is not permission to change Azure or interfere with a foreign lock holder.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready (C1-C7, W1).
Automatic parent continues to Plan; no required research blocker remains.
Preserve the complete original research and adverse evidence. A failed
focused check must be diagnosed, not hidden by changing upstream-owned inputs.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | Reuse docs/fabric-rebase-558 tracking the open owner branch; local-only history rewrite authorized | C5, W1 |
| Q2 | Union shared log/index; upstream rubric and manifest; no executable delta | C4-C6 |
| Q3 | Component static checks, local-origin guard, scenario and dependency tests, doc integrity | C1, C2, C6, C7 |

## Current and Unresolved Decisions

Owner confirms rebase, local commit/no push, no Azure and upstream ownership.
No unresolved implementation decision. Full publication receipt, independent
exact-head assessment, hosted CI and owner merge remain separate later gates;
this local-only task does not claim them.

## Potential Next Research

None required for this bounded reconciliation. Refresh Fabric claims only when
the owner requests a new assessment, not to make historical evidence look newer.

## Closeout Record and Advisory Next Step

Complete Wider, Deeper and Contrarian inline; focused scope made research
delegation unnecessary. Disposition executed; readiness Ready; automatic parent
owns Plan, independent critique, implementation and independent Review.

## Sources

* W1 - PR #558 - https://github.com/jmservera/ama/pull/558 (retrieved 2026-10-30).

## Artifact Self-Check

* [x] Questions answered, evidence IDs and sources resolved.
* [x] Three ordered waves, reflection and parent dispositions recorded.
* [x] Scope, posture, constraints, extension provenance and participation recorded.
* [x] Alternatives, residual risks, readiness and parent continuation recorded.
