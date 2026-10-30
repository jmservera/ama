<!-- markdownlint-disable-file -->
# Task Research: iot-pr557-main-refresh

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md |

## Research Brief

* Target: reconcile PR #557, branch `feat/iot-hub-live-140`, with current `origin/main`.
* Purpose and audience: give the coordinator a locally committed, validated candidate without pushing.
* Scope: branch divergence, conflict intent, source layout, pinned scenario inputs and affected CI.
* Non-goals: Azure operations, deployment, remote publication, issue acceptance or historical evidence rewriting.
* Criteria: preserve both sides, use main's rubric/scenario manifest, source only in `src/`, tests outside packages; run requested static/types/targeted tests using `/tmp/mv`.
* Output mode: convergence, preparing planning.

## Research Parameters

* Posture: focused, selected for the caller's bounded maintenance request.
* Internal candidates: Git ancestry, prior IoT RPI evidence, infrastructure tests, core/API simulator, project and CI commands.
* External candidates: GitHub PR metadata only; no web or Azure discovery.
* Explicit limits: no push, no cloud changes, no issue-closing keywords; full API suite requires successful nonblocking shared-lock admission.
* Evidence root: `.copilot-tracking/`.
* Research edits: evidence and workflow state only.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository AMA and applicable tracking instructions | Selected: branch, evidence, validation and privacy-safe identity rules |
| Skill | rpi-research, rpi-plan, rpi-implement, rpi-review | Selected sequential phase protocols |
| Specialist | Independent critique and final reviewer | Selected for required independent gates, not research discovery |
| Skill | Web/design skills | Skipped: no web implementation is planned |

## User Participation and Research Decisions

The explicit full-loop request authorizes all four phases for this task, with no routine phase questions. Noninteractive execution precludes questions. This is a bounded requested loop, not authorization to start follow-up work. Rebase is explicitly requested; push and cloud operations are prohibited.

## Direction Controls

Caller instructions control conflict selection, validation admission, commit format and no-push scope. Original evidence must remain intact.

## Research Questions

| ID | Question | Type | State |
| --- | --- | --- | --- |
| Q1 | What branch and main changes overlap? | depth | Answered C3, C4 |
| Q2 | Which source/test and scenario contracts need reconciliation? | depth | Answered C5, C6 |
| Q3 | What local checks can be run safely without shared heavy work? | straightforward | Answered C2, C7 |

## Prior Knowledge Gate

Read both case studies, knowledge-base index/memory, sector primer and `src/README.md`. Clean starting worktree; matching topic branch and open PR. PR metadata reports `isDraft=false`, contrary to the request's historical draft label; no PR state change is necessary.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspect ancestry, changed paths and prior bounded IoT evidence; source and validation are tightly coupled and remain inline.

Results: ten local commits, remote topic tip equals local starting HEAD
`7bd71d37866671899ef11fa653d9eace9687069b`. Fetched main is
`8ee1b77f8983ddf39216da07ae60c63ef66431d6`. Main adds monitoring and UX
documentation; overlapping index/log/infra README are additive (C3).
Reflection: prioritize append-only resolution and generated-score precedence.

#### Wave 2: Deeper

Read runtime diff, compiled infrastructure tests, previous test-contract and
fix-cycle changes evidence, project Ruff/mypy configs and source CI selectors.
Runtime adds publisher-only activation while receiver still requires routed
activation. Prior tests assert live Bicep parameter map, full consumer group
name and actual region/SKU/units, so preserve all those checks (C5).
Reflection: use package Ruff/mypy and selected IoT/sensor modules, plus offline
infrastructure compilation; no new dependencies are indicated (C7).

#### Wave 3: Contrarian

Compared all four pinned manifest inputs and the manifest against main:
no differences. Checked main's README frontmatter: a single date versus the
topic's duplicated date. Preserve main's metadata and both content additions.
Checked prior adverse gate evidence: prior local integration successes are not
a full-gate or live acceptance pass. Initial nonblocking heavy admission
succeeded, but focused selectors suffice and do not require a full API suite.
Reflection: recheck pins after rebase anyway, keep main's exact rubric/manifest,
and report hosted/publication gates separately (C4, C6, C8).

### Parent Synthesis and Disposition

Accept additive documentation preservation and main-authoritative generated
files. Reject merge or global "ours/theirs" resolution because they violate
caller direction or lose intent. Defer cloud/live/full-publication acceptance.
No further research cycle is needed: all three questions are covered by
repository evidence within the bounded maintenance scope.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Namespace packages and external project tests are required | src/README.md:10 | High |
| C2 | Targeted checks precede heavier gates, shared heavy work requires nonqueued admission | src/README.md:174 | High |
| C3 | Branch adds existing-hub model and bounded publisher activation; upstream adds monitoring/runbooks and UX research | infra/iot-hub-live.bicep:1; Git ancestry/diff against main | High |
| C4 | Main has one index date; branch adds bounded IoT index entry and append-only log entry | docs/reference/README.md:4,56; docs/reference/log.md:8142 at intake | High |
| C5 | Receiver remains routed-only; compiled tests preserve scope, SKU, units, parameter and group-name contracts | src/api/src/zava_forward/api/iot_stream.py:204; infra/tests/test_iothub_module.py:1 | High |
| C6 | Four fixed public inputs must hash exactly; all match main at intake | src/core/src/zava_forward/core/synthetic/scenario_manifest.py:33,100; src/core/tests/test_scenario_manifest.py:21 | High |
| C7 | Ruff 0.17.1, mypy 2.4.0, Python 3.12.3 available in /tmp/mv; project CI runs package lint/types | src/core/pyproject.toml:19; src/api/pyproject.toml:23; .github/workflows/src-ci.yml:80 | High |
| C8 | Earlier gate failed integration-skip admission and does not establish publication eligibility | .copilot-tracking/changes/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-changes.md:100 | High |

No external research sources used. PR lifecycle/identity were retrieved read-only
with `gh`; cross-session branch lookup returned no prior session rows.

## Alternatives and Decision State

Requested rebase is the selected approach; merge/cherry-pick is excluded by caller direction. Main's rubric and manifest win while additive documentation keeps both sides.

## Open Questions, Risks and Residual Uncertainty

Exact per-commit conflicts will be resolved during implementation. Hosted CI
and remote mergeability cannot change until the coordinator pushes. Existing
live approval and historical gate blockers remain outside this task.

## Planning Readiness

Ready (C1-C8). Research disposition: executed, complete. Handoff: rebase onto
the recorded main SHA, preserve additive docs and branch runtime/test intent,
restore exact main rubric/manifest and validate the reconciled result.
Self-check: all questions mapped, three waves completed inline, alternatives
and residual gates explicit; no source changes during Research.
