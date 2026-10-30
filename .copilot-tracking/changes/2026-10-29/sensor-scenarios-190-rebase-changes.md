---
title: Sensor scenarios PR 505 rebase changes
description: Commands, conflict decisions, local validation and unpushed handoff
ms.date: 2026-10-29
---

## Context and Execution Scope

Task 505 / sensor-scenarios-190-rebase; parent 190.
Full plan: .copilot-tracking/plans/2026-10-29/sensor-scenarios-190-rebase-plan.md.
Details: .copilot-tracking/details/2026-10-29/sensor-scenarios-190-rebase-phase-details.md.
Original branch HEAD: 2fdf08bba5f3c30969645191aafee8bf8e087036.
Fetched main: b0364e4b326936715d69ab1d75040c4528282af7.
Implementation status: Complete for P01-P03; ready for independent Review.

Caller authorizes local rebase and commit, not push. All issue references use
Refs #190 #192 #193 #194. Source stays in src/ and tests outside packages.
Original 2026-10-27 records and adverse outcomes remain unchanged.

## Planning and Critique

Research executed / Ready. One independent critique executed Complete /
Revise. PC-001 asserts a temporary-path restriction absent from the parent
execution context and conflicts with the exact caller-selected environment.
Parent rejected it with evidence in the plan; original critique unchanged.
Do not treat that disposition as closure of historical original RV-001.

## Intake Commands and Results

| Command | Result |
| --- | --- |
| git status --short; git branch --show-current | Initially clean; feat/sensor-scenarios-190 |
| git fetch origin | Exit 0; fetched base above |
| gh pr view 505 --json state,isDraft,headRefName,baseRefName,title,statusCheckRollup | Open draft, correct branch/base; existing rubric success refers to old head |
| gh pr view 505 --json body,mergeable,mergeStateStatus | CONFLICTING / DIRTY before rebase |
| gh api user --jq '{id,login}' | Exit 0; id 8036360, login jmservera, privacy-safe email derived |
| git log --oneline origin/main..HEAD | Two existing branch commits ff899bb4 and 2fdf08bb |
| git merge-base HEAD origin/main | 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4 |
| /tmp/mv/bin/python -c "import sys, zava_forward.core; ..." | Exit 1: ModuleNotFoundError for zava_forward; local installs required |
| /tmp/mv/bin/python --version | Python 3.12.3 |
| flock -n /tmp/ama-rpi-heavy.lock true | Exit 0; probe only, not a held reservation |

## P01: Rebase and Conflict Decisions

| Command | Result |
| --- | --- |
| git config --local user.email '8036360+jmservera@users.noreply.github.com' | Exit 0; repository-local author/committer privacy-safe identity |
| GIT_EDITOR=true git rebase origin/main | Exit 1, expected conflict stop on first commit |
| git add docs/reference/README.md docs/reference/log.md docs/reference/research/retrofit-synthetic-data/data-dictionary.md; GIT_EDITOR=true git rebase --continue | Exit 0; both commits replayed, no skip or merge commit |
| git merge-base --is-ancestor origin/main HEAD | Exit 0 |
| git diff --exit-code origin/main -- .github/rubric docs/reference/research/retrofit-synthetic-data/scenario-manifest.json | Exit 0; exact main-owned copies retained |

Conflict decisions:

* Reference index: retain main's #179 indoor-envelope/snapshot-versioning
  account and the branch's #190 scenario pack as separate paragraphs.
* Append-only log: retain every incoming entry and append the original
  scenario entry; historical bytes are not rewritten.
* Dictionary frontmatter: retain the feature's later date, 2026-10-27,
  alongside auto-merged content from both sides.
* IoT synthesis and core README merged automatically; source/test additions
  did not conflict. No legacy application files or web edits introduced.

Replayed commits: b0cc7ccf (original ff899bb4) and df760b84 (original 2fdf08bb).
The new dated artifacts are task-owned untracked files; no pre-existing
uncommitted owner work was moved/stashed/committed.

## P02: Validation Commands and Results

Setup: `/tmp/mv/bin/python -m pip install --quiet -e 'src/core[dev]'
-e src/agents -e 'src/api[dev]'` exited 0 after the reproduced missing import.
No dependency manifest changes or pin loosening.
Full API discovery is deliberately excluded. Logs:
/tmp/ama-505-rebase-20261029-db103830/. These are external scratch,
not a committed receipt or hosted CI result. Test/static results follow.

Commands from `src/core`, using /tmp/mv tools:

```bash
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests \
  /tmp/mv/bin/python -m unittest -q \
  test_sensor_scenarios test_scenario_manifest test_sensor_backfill \
  test_sensor_plausibility test_sensor_faults test_sensor_stock \
  test_sensor_privacy test_indoor_projection test_historical_backfill \
  test_synthetic_provenance test_synthetic_determinism \
  test_synthetic_output_dir test_dependency_rule
```

Commands from `src/api`:

```bash
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests \
  /tmp/mv/bin/python -m unittest -q \
  test_sensor_ingestion test_workbench test_dependency_rule
```

| Check | Result | External log |
| --- | --- | --- |
| Core Ruff | Exit 0, all checks passed | core-static.log |
| Core format | Exit 0, 106 files already formatted | core-static.log |
| Core mypy | Exit 0, 159 source files | core-static.log |
| API Ruff | Exit 0, all checks passed | api-static.log |
| API format | Exit 0, 56 files already formatted | api-static.log |
| API mypy | Exit 0, 107 source files | api-static.log |
| Core 13 selected modules | Exit 0, 124 tests / 32.629s, one opt-in SQL skip | core-tests.log |
| API three selected modules | Exit 0, 50 tests / 18.464s, zero skips | api-tests.log |
| git diff --check; git diff --check origin/main | Exit 0 | Tool output |
| Original seven 2026-10-27 evidence files compared against 2fdf08bb | Exit 0, byte-identical | git diff --exit-code on explicit paths |
| Scenario source/test compared against 2fdf08bb | Exit 0, byte-identical | git diff --exit-code on explicit paths |
| git ls-files 'mvp/*' | Exit 0, empty | No legacy files introduced |

Core tests emitted existing ResourceWarnings for unclosed CSV files in
test_sensor_backfill.py, not failures or new changes. The single skip is
the existing opt-in SQL test; no actual SQL integration is claimed.
Ruff 0.17.1 and mypy 2.4.0 match current project pins.

### Shared Environment and CLI Evidence

The no-PYTHONPATH CLI initially failed with
`No module named zava_forward.core.synthetic.sensor_scenarios`.
Read-only import/distribution inspection showed all three editable mappings
had been replaced by another worktree at
/home/azureuser/source/ama-wt/iot110. This is a shared-venv mapping race, not
missing source in this candidate. Do not overwrite another worker's mapping
again. The requested explicit source/test PYTHONPATH selects this checkout;
all unit commands already used it, including their subprocess CLI checks.

From repository root:

```bash
PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests \
  /tmp/mv/bin/python -m zava_forward.core.synthetic.sensor_scenarios \
  --seed 190 --out /tmp/ama-505-rebase-20261029-db103830/scenario-snapshot
```

Exit 0. Snapshot: eleven cases, 6,888 rows, fifteen independently matched
checks. All fourteen payload hashes verified by SHA-256 against the retained
truth manifest; source fingerprint now binds incoming main's model.

* Generator revision:
  sha256:bbb63c44098d2292a1e1e3b2f0cd712f7a69e9c66f605eba358ddc0a4c50dff1.
* Manifest SHA-256:
  1b7080a6297e00c87cd338ea3a693c5e996c0b2d66fd25fc0c07b7ede25cdf19.
* Report SHA-256:
  826f099cb4f7b5f01dfbc4e5b5c1f933c64c2db1ebc331dfedfc6c1b92952d70.
* Actual retained CLI stdout: scenario-cli.json in the external log directory.

### Main-owned Scenario Manifest

`test_scenario_manifest` passed within the core selection, including actual
source hash validation. Independent byte hashing confirmed all four pins:

| Source | SHA-256 |
| --- | --- |
| src/api/checks/workbench-manifest.json | 1569339177bc54b659cecd9bd9cb556ecbb5ac66819ae77a752abd2e471788fb |
| src/api/checks/workbench_browser_check.py | dea58169392471861486ccb9d5ef4f263a4208d34c920847615bfc1a944fe6f0 |
| src/core/tests/dataset.py | a54612aa549cd5d048281a875b4c80a3a26b22e6d59c9c83d080eebbc8760dc5 |
| src/api/tests/test_workbench.py | 62b3be27e69d32f39ef0cc52b91f44dceae31579edf9fd1c08bb25e36649ba96 |

No stale pins remain after taking main's copy; no recomputation/edit is needed.
Rubric files and manifest remain exactly equal to fetched main.

## P03: Review, Commit and Gate

One independent Review executed Complete / Conformant at the bounded
precommit rebase scope, zero new findings. Commit follows that original
Review and includes its dated evidence. Do not push. Full gate,
hosted checks and human acceptance are separate from targeted test success.

Review:
.copilot-tracking/reviews/logs/2026-10-29/sensor-scenarios-190-rebase-review.md.
Reviewer independently verified ancestry, exact source/historical evidence
preservation, main-owned inputs, all four pins, append-only log and twelve
links. It assessed, but did not rerun, the parent's test commands.
The Review is not an exact-final-head publication assessment or original
feature acceptance.

### Additional Checks and Setup Recovery

| Command | Result |
| --- | --- |
| /tmp/mv/bin/python tools/rename-zava-tests.py | Exit 1; 25 tests, seven missing-package errors (pptx/PIL) |
| /tmp/mv/bin/python -m pip install --quiet -r tools/rename-zava-requirements.txt | Exit 0; existing tooling requirements restored after actual failure |
| /tmp/mv/bin/python tools/rename-zava-tests.py | Exit 0; 25 tests / 0.513s, zero skips; migration-tests-restored.log |
| Read-only added-link/anchor validator over git diff origin/main | Exit 0; twelve added local links/anchors verified |
| Main log prefix byte comparison (git show origin/main:docs/reference/log.md) | Exit 0; all main historical bytes preserved as exact prefix |
| git fetch origin main; git rev-parse origin/main HEAD; git merge-base --is-ancestor origin/main HEAD | Exit 0; main unchanged b0364e4b, rebased HEAD df760b84 |
| Fresh flock -n /tmp/ama-rpi-heavy.lock true | Exit 1; heavy resource remains held elsewhere; no full API discovery/gate |
| gh api user --jq '{id,login}' before final commit | Exit 0; same authenticated identity |
| git log -5 --oneline origin/feat/sensor-scenarios-190; git rev-list --left-right --count 2fdf08bb...origin/feat/sensor-scenarios-190 | Exit 0; remote has one extra rubric-score-only commit e2c9f0eb |
| git diff --stat 2fdf08bb..origin/feat/sensor-scenarios-190 | Only .github/rubric/scores/latest.json differs; caller's main-owned rubric policy intentionally supersedes that old score |
| gh pr view 505 --json headRefOid,mergeable,mergeStateStatus,statusCheckRollup | Remote remains e2c9f0eb / CONFLICTING / DIRTY; no push, existing score success is old-head evidence |

The migration suite's `Cannot migrate broken.pptx` output is its expected
malformed-fixture test, not a remaining failure. First failed log retained
as migration-tests.log; successful recovery is separate and not overwritten.

## Plan Amendments and Divergences

No source compatibility correction required. P03 wording reconciled to
prepare Review rather than include Review inside its own prerequisite;
the wrapper still runs exactly one separate Review and owns commit/gate.
Explicit PYTHONPATH avoids a reproduced shared editable-mapping race and
matches caller direction; no tool/runner behavior or source exemption changed.
Minor post-rebase log correction removes an inserted blank line so main's
historical log prefix remains byte-identical. Unrelated work stays follow-up-only.

## Remaining Work and Follow-ups

Independent Review Complete / Conformant; P01-P03 implementation complete.
Local commit is the final wrapper action. A fresh
`flock -n /tmp/ama-rpi-heavy.lock true` returned 1; full gate is blocked on
shared heavy capacity, not treated as passing. Docker server version 29.9.0
is reachable; tools python3/node/docker/az/actionlint/shellcheck/trivy exist.
No full API discovery run. Original RV-001-RV-004 remain owned by their original
planning/consumer/live/parent follow-ups; this branch update does not close
or defer their issues.

### Commit and Coordinator Boundary

The final wrapper commit uses repository-local privacy-safe identity and:

```bash
git commit -m "chore(sensors): reconcile PR 505 with current main" \
  -m "Preserve both documentation narratives and main-owned rubric and scenario manifest. Record dated RPI evidence and scoped validation; leave publication and hosted checks to the coordinator." \
  -m "Refs #190 #192 #193 #194" \
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Its own SHA is intentionally not embedded in its tracked evidence. The final
handoff verifies the resulting commit, clean status, ancestry and exact
main-owned files through Git. Rebase necessarily rewrites ancestry. Remote
tip e2c9f0eb is retained as the coordinator's lease/reference boundary;
its only additional change is the superseded rubric score, not missing
implementation work. No push, merge, draft promotion, CI dispatch or remote
metadata write occurred.

All requested local static and selected-unit validation is complete; full
publication gate remains unrun because repeated final capacity probes fail.
No receipt exists to verify. Coordinator must complete the gate and verify
against then-current main before independently assessing/publishing the exact
candidate, then observe new hosted CI. This handoff is not a green remote PR
claim. Automatic task is completed at Follow-up with session running; no child
work item has been selected.

## Pre-Review Reconciliation

Plan markers P01/P01-T01, P02/P02-T01 and P03/P03-T01 are complete.
Details and this record agree on conflict resolutions, unchanged source,
static/test counts, genuine setup failures/recovery, shared mapping race and
unrun full publication gate. No implementation blocker or source correction
remains. Review readiness is Ready for the bounded local rebase; whole-PR
hosted green/merge approval is not claimed.
