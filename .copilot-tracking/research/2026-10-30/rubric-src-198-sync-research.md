---
title: PR 507 current-main synchronization research
description: Focused evidence for the 2026-10-30 rebase
ms.date: 2026-10-30
---

## Research Brief

Bring draft PR #507, branch `feat/rubric-src-198`, up to date with
`origin/main`, preserving both sides' documentation intent and main's rubric
and scenario manifest. Refs #198. Audience: coordinator and independent reviewer.
Output mode: convergence, preparing planning. Research posture: focused,
selected for the caller's bounded branch-integration task.

## Research Parameters and Direction Controls

* Full Research, Plan, Implement and Review explicitly requested.
* Rebase explicitly authorized; no push, merge, issue closure or Azure changes.
* Application sources only under `src/`; tests outside packages; no legacy code.
* Use `/tmp/mv`; run Ruff, formatting, applicable core/API mypy and relevant tests.
* Full API tests require successful nonblocking shared-lock admission.
* Preserve original dated RPI outcomes and append-only history.
* Research root: `.copilot-tracking/research/2026-10-30/`.

## Extension Registry and Participation

Repository instructions and RPI phase skills selected. No visual, legal or
cloud research is needed. Research remains inline because this is one coupled
Git/validation trace. Independent planning critique and final Review will use
bounded agents under their respective phases. No clarification is needed:
the caller supplied branch, base, conflict policy and publication boundary.

## Questions and Candidate Areas

1. What differs from current main, and which original changes remain?
2. Which conflicts and pinned-source changes require reconciliation?
3. Which local commands exercise the retained delta and current CI contracts?

Starting areas: Git ancestry, PR checks, prior RPI evidence, project guides,
rubric/scenario tests and Source CI.

## Evidence Log

* C1: `docs/reference/README.md:62` records previous integration's main-owned
  rubric/manifest policy and warns that original counts are historical.
* C2: `src/README.md:15` requires tests outside packages.
* C3: `src/README.md:66` documents the focused/full local gate distinction;
  final publication remains separate from this no-push task.
* W1: https://github.com/jmservera/ama/pull/507, retrieved 2026-10-30:
  open draft, expected head and base, original acceptance gaps remain.

## Research Cycle Log

Cycle 1, Wider: clean worktree on the exact requested branch. Five branch-only
commits currently retain documentation and historical RPI evidence, with no
net rubric/application delta. Hosted checks on the old remote head passed or
skipped; they do not prove the rebased candidate.

Reflection: inspect current base changes, retained documentation and command
configuration before selecting the reconciliation and validation plan.

Deeper: `git merge-tree --write-tree --name-only HEAD origin/main` predicts
conflicts only in the index and log. Main is
`91e890e07af036263316c153cbc7ceff780cdaa2`; starting head is
`6517adf10c692cdfd1f1abad8431d7e6e4e43cca`. The retained source delta is three
documentation files and original artifacts. Only latest recorded score differs
in upstream-owned rubric inputs. Scenario manifest bytes are already equal.

Reflection: combine real textual conflicts rather than replacing entire files;
enforce main's complete rubric/manifest bytes after all five commits replay.

Contrarian: previous green focused checks do not prove this candidate or the
full rubric suite. Prior changes record eighteen inherited rubric failures
and seven missing-runtime skips. `/tmp/mv` has Python 3.12.3, Ruff 0.17.1 and
mypy 2.4.0, but not pytest. Use existing system pytest for the rubric suite,
and requested venv for application checks; no dependency mutation is necessary.
Current Source CI is path-filtered, so documentation-only changes do not
necessarily run its package matrix. A local rebase cannot refresh remote
mergeability or hosted checks without the prohibited push.

Parent synthesis: accept the explicit rebase/main-copy policy. Reject replacing
the whole index/log, modifying inherited rubric tests, or treating prior CI as
current. Run scenario validation even though the manifest is unchanged because
its pinned inputs may have evolved. Stop research: the bounded integration,
preservation and validation questions have evidence; additional discovery would
not change the plan.

## Additional Evidence and Prior Knowledge

* C4: `.github/workflows/src-ci.yml:4` filters the package matrix to source,
  infra, selected tools, scenario data and workflow changes.
* C5: `src/core/tests/test_scenario_manifest.py:21` validates current manifest
  and source bindings; no re-pinning is authorized.
* C6: `.copilot-tracking/changes/2026-10-29/rubric-src-198-rebase-changes.md`
  preserves earlier adverse outcomes, command patterns and original identities.
* W2: PR checks retrieved 2026-10-30: prior remote rubric score/preparation
  passed, score 77/100; this is not post-rebase evidence.
* Cross-session prior-knowledge query for PR 507 over seven days returned no
  rows; the local dated artifacts supplied the verified prior evidence.

## Risks and Decisions

Inherited rubric failures may prevent a full green local rubric suite while
main-copy policy prevents repairs here. Report exact results without disguising
failure or widening scope. Original issue acceptance gaps remain outside this
synchronization. No unresolved implementation decision.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Proceed to Plan under the caller's explicit full-loop request.
