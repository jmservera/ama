---
title: PR 429 main refresh plan critique
description: Independent one-pass assessment of preservation and publication readiness
ms.date: 2026-10-27
---

## Metadata

* Task ID: pr-429-main-refresh-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/pr-429-main-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/pr-429-main-refresh-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate pass.

## Inputs and Criterion Boundary

* Caller requirements: isolated rebase of remote topic
  docs/cutover-soak-review-201 from
  ad79455a3ec2c47d935fbc3cd055555ff188bc35 onto
  49c942b33b89100c084d48a91215989e22de5887; preserve both sides, original
  RPI evidence and append-only history; explicit topic-only lease; no main
  write, merge, closing keywords, secrets, cloud calls, Azure operations or uv.
* Inputs: supplied plan, phase details and research; their cited prior changes
  report, src/README.md and tools/rpi-checks.py at reviewed main; bounded
  inspection of cited local infrastructure test contracts and Git inventories.
  Repository context documents and the critique template were also read.
* Decisions and acceptance: five substantive commits replayed, sole obsolete
  score-only commit excluded, main score retained; four production Markdown
  paths plus original/new tracking evidence; zero production tests, tools or
  dependencies added; at most one external standard-library audit helper.
* Boundary: assess plan credibility and publication policy, not execute a
  rebase, validation gate, remote update or implementation Review. This
  artifact is the only file written by this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01, authoritative base and topic | Covered | Supplied SHAs and local topic inventory identify five substantive commits and one score-only commit. |
| P01-T01, untracked evidence and identity | Partial | PC-003 and PC-004. |
| P01-T01, original RPI evidence and both sides | Covered | Exact tracking-blob comparisons, full main-log prefix, one original entry and both index rows are explicit. |
| P02-T01, documentation validation | Covered | Link/anchor comparisons to main and old topic, allowlist, markers and whole/staged whitespace checks address the requested regression boundary. |
| P02-T02, original Review and final evidence | Covered | One independent Review, immutable outcome and separate final exact-head admission preserve distinct controls. |
| C2, P03-T01, publication policy and offline tooling | Partial | PC-001 and PC-002. |
| P03-T01, explicit lease and remote movement | Covered | Original full SHA is bound to the named remote ref; movement requires reevaluation, not blind retry. |
| No source changes, removals or scope expansion | Covered | Rubric-only exclusion is verified separately; no other removal or tool addition is authorized. |

## Verdict

* Verdict: Revise
* Severity summary: Two High and two Medium findings.
* Rationale: preservation and lease design are credible, but the publication
  path rests on an incorrect offline-tool inference, leaves the governing gate
  unresolved and misses a concrete execution-policy conflict. Planner-owned
  corrections can make the implementation plan credible; publication remains
  blocked by PC-002 under the current environment constraints.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve the gate policy without treating offline Bicep as cloud execution

* Related IDs: C2; P03-T01; plan Executive Summary and Dependencies; research
  Cycle 1 Contrarian and Risks and Readiness.
* Evidence: src/README.md:48-91 at reviewed main documents a changed-path tier
  and separately retains the full gate. The supplied repository instructions
  explicitly require --all even for documentation. tools/rpi-checks.py:335
  selects preflight/static for documentation; :1319-1338 still invokes
  az bicep version in preflight. Its infrastructure commands at :1435-1460
  are local build/lint and tests. The runner sets a fresh AZURE_CONFIG_DIR,
  binary-from-PATH and disabled telemetry at :1072-1074.
* Concern: the plan calls offline Azure CLI categorically incompatible and
  proposes a non-Azure documentation tier, although that tier also invokes
  the local CLI. An executable named az does not establish an Azure service
  call. Conversely, selecting the changed tier does not resolve the stricter
  applicable instruction requiring the complete gate.
* Impact: implementation could manufacture an Azure blocker, or publish with
  a partial receipt that does not satisfy the governing instruction.
* Smallest useful change: state that local Bicep version/build/lint are not
  login, deployment, what-if or Azure resource operations. Keep all actual
  cloud calls forbidden and require local binaries/modules without cloud
  fallback. Apply the stricter --all requirement for this run; classify a
  changed-tier result only as supplementary partial evidence unless an
  authoritative applicable instruction explicitly supersedes that requirement.
  Remove the unsupported claim that the full gate is blocked merely by the
  Azure executable name.
* Action owner: Planning parent.
* Exact resolving evidence: synchronized plan/details and a research
  qualification recording the two policy sources, selected governing rule,
  exact full-gate/verification contract, and the distinction between local
  compilation and prohibited cloud operations. Preserve the original research
  conclusion as dated evidence rather than silently erasing it.
* Decision route: Direct planner correction. No user decision is necessary
  to enforce the stricter existing rule; no waiver is implied.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The current runner writes a forbidden temporary-directory lock

* Related IDs: P03-T01; no source/tool changes; supplied environment limits.
* Evidence: tools/rpi-checks.py:2173-2177 at reviewed main hardcodes
  /tmp/ama-rpi-heavy.lock and opens it with O_CREAT and O_RDWR.
  Both execution tiers enter heavy_lock at :2245. No lock-path option is
  exposed by the adjacent argument parser. The task environment prohibits
  all file operations in temporary directories, not just receipt output.
* Concern: choosing a safe external output directory or setting TMPDIR does
  not relocate this literal lock. The plan leaves execution conditional on
  inspection but does not identify this already observable incompatibility.
* Impact: either tier would violate an explicit execution restriction before
  checks start. This is a genuine gate blocker, unlike the mere presence of
  offline Bicep.
* Smallest useful change: explicitly mark gate execution and publication
  blocked in the current environment. Continue only the authorized rebase,
  documentation checks and original Review that can comply. Do not execute
  the runner, patch its lock, bypass serialization, change protections or
  fabricate a receipt within this documentation-only task.
* Action owner: Planning parent for disposition; repository tooling owner for
  any separately authorized prerequisite remediation.
* Exact resolving evidence: plan/details identify the hardcoded lock and
  stop-before-gate/publication boundary. Clearing publication subsequently
  requires a separately approved compliant runner/environment, fresh exact-head
  full receipt and verification against freshly fetched main, and independent
  admission; any tool/base/head change invalidates earlier gate evidence.
* Decision route: Direct planner correction to record and honor the blocker.
  Remediation is out of this task's source-change scope, not an invitation to
  weaken the environment restriction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Make preservation of the live untracked RPI evidence executable

* Related IDs: P01-T01; P02-T02; no ignored/untracked source input.
* Evidence: initial worktree status lists the new plan, phase details,
  research and pr-429-main-refresh-state.json as untracked. This critique
  adds another new evidence path. Phase details:31-33 prohibit staging new
  evidence into replayed commits but do not specify collision checks,
  recovery or post-rebase verification.
* Concern: Git can retain non-colliding untracked files during rebase, so
  their presence alone is not a blocker. However, the current plan cannot
  demonstrate that all live evidence survived, or that broad conflict staging
  did not fold it into an original replay commit.
* Impact: task evidence could be lost or mixed into historical commits,
  undermining the requested original-evidence separation and later clean gate.
* Smallest useful change: inventory and hash all task-owned untracked evidence
  after critique disposition; compare its paths against replay/base paths.
  Retain a recoverable task-owned copy in a permitted persistent location
  outside the worktree without moving existing files. Leave originals in
  place if non-colliding, stage only named conflict paths, and compare the
  inventory/hashes immediately after rebase before intentional later edits.
  Stop on a collision rather than clean, stash or overwrite. Commit new
  evidence separately after the original Review and require clean status
  before any exact-head gate.
* Action owner: Planning parent / implementing parent.
* Exact resolving evidence: P01 records the path inventory, collision result,
  recoverable-copy location and pre/post hash comparison; staged-path and
  replayed-commit inventories show no new evidence in original replay commits.
  Later intended state/plan updates are identified separately.
* Decision route: Direct planner correction; no new user authorization to move
  or discard existing evidence is assumed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Derive commit identity from the authenticated account

* Related IDs: P01-T01; repository-local noreply identity requirement.
* Evidence: phase details:29-30 say to resolve gh api user but then prescribe
  a literal account-specific noreply address. Repository instructions require
  construction from the returned id and login and prohibit hardcoding it.
* Concern: the stated lookup does not control the subsequent configured value.
  Authentication can differ from the account assumed in the plan.
* Impact: new evidence commits could have the wrong attribution or fail privacy
  checks. Repository-local configuration is also shared by linked worktrees.
* Smallest useful change: derive id+login@users.noreply.github.com from the live
  response, configure repository-local email as required, and use that value
  for author and committer of new commits with the required Copilot trailer.
  Preserve historical authorship on replayed substantive commits.
* Action owner: Planning parent / implementing parent.
* Exact resolving evidence: corrected instructions without a literal user
  address; authenticated id/login-derived email, local configuration and new
  commit author/committer/trailer inspection agree.
* Decision route: Direct planner correction; no user response required.

## Strengths and Residual Risk

* The original remote SHA and exact destination ref support a safe lease:
  force-with-lease=refs/heads/docs/cutover-soak-review-201:ad79455a3ec2c47d935fbc3cd055555ff188bc35,
  with HEAD explicitly mapped to that same ref. No generic force or main
  update is authorized.
* Full main-log prefix and exact original entry bytes provide stronger
  preservation evidence than resolving either file wholesale. Both index
  additions and immutable historical Review outcomes are explicitly retained.
* Existing historical broken links are disclosed rather than used to justify
  unrelated fixes. Link/anchor checks plus preservation and whitespace checks
  are proportionate documentation validation, but not publication admission.
* The score-only exclusion was verified as affecting only
  .github/rubric/scores/latest.json. Historical objects are retained; all other
  substantive topic content and original tracking files remain in scope.
* Base or remote-topic movement requires reevaluation and new exact evidence.
  Observed mergeability and hosted check status must not be presented as merge
  authorization or operational acceptance.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required for these corrections.
  Publication is blocked by the known execution-policy conflict in PC-002;
  no missing prerequisite, gate pass or cloud activity has been inferred.

## Limitations

* No gates, tests, rebase or remote operations were executed. Installed tool
  availability and actual implementation preservation remain unverified.
* Local Bicep inspection establishes that the listed commands are compilation
  and tooling operations, not a proof that every possible binary/module or
  test execution is network-free. Real cloud calls, automatic remote restore
  and credential use remain prohibited; stop if required for execution.
* This is the single complete finding set for the supplied boundary. Correct
  findings directly and preserve this original assessment; do not request a
  second plan critique.

## Recommended Next Action

* Highest-impact finding: PC-002, the concrete gate execution restriction.
* Action owner: Planning parent.
* Smallest next action: record the publication blocker, resolve PC-001 through
  PC-004 in the plan/details with a separate disposition, then perform only
  the compliant implementation and original Review stages.
* User response required: No for planner corrections or preserving the
  blocked publication boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/pr-429-main-refresh-plan.md](../../../plans/2026-10-27/pr-429-main-refresh-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-27/pr-429-main-refresh-phase-details.md](../../../details/2026-10-27/pr-429-main-refresh-phase-details.md) | Assessed implementation details |
| [.copilot-tracking/research/2026-10-27/pr-429-main-refresh-research.md](../../../research/2026-10-27/pr-429-main-refresh-research.md) | Supplied research |
| [.copilot-tracking/reviews/plans/2026-10-27/pr-429-main-refresh-plan-critique.md](./pr-429-main-refresh-plan-critique.md) | Original one-pass critique |

## Next Steps

The active planning parent disposes all four findings directly, without another
critique, and records the exact publication stop condition. No user action is
required to make these revisions. Do not execute the incompatible gate or push
without compliant governing-gate evidence and independent exact-head admission.
