<!-- markdownlint-disable-file -->
---
title: Issue 86 historical recorder identity changes and evidence
ms.date: 2026-10-18
---

## Task and Scope

Task 86 / issue-86-recorder-identity. Full plan scope P01-P03.
Exact base: 6c1e376ff1241316272df22a5a3a6853aae9f87b.
Branch: fix/review-recorder-identity-86. No pre-existing working changes.
Plan/details/research use this slug/date in their canonical directories.
P01/P02 complete; locally verified delivery is ready for its one original Review.
P03 Review/publication remain pending below.

## Decisions and Amendments

One original independent critique executed: Revise, PC-001 High. Directly resolved
in plan/details: never reconstruct an unbound legacy review's identity from
measure/version ordinals, which can recycle after retention. Original untouched.
This is an immediately relevant correction within confirmed user direction,
not approval invention or a retention change.

## P01: Implementation

Complete P01-T01/T02. New decision snapshots use existing `_identity` and atomic
resident `_operation`, including SQL actor replay and explicit existing recorder
role gate. Shared normalized same-person comparison protects both assignment
paths and retains handler/reviewer separation. New requests retain the exact
selected version's snapshot, even after decisions are deleted/recreated.
Unbound legacy review stays Unknown with no lookup/backfill. Views derive
Known/Unknown on detached copies; projection strips the new snapshot for
nonresident roles. Core/API contracts explain the bounded change.

Tests: five new inherited core methods plus one SQL-only method, two API methods.
No removals. JSON fixture helper now persists registry changes in its canonical
staff list, not only lookup cache, to make restart probes meaningful.
No post-Review corrective source cycles used.

## Validation Commands and Results

Research failing-first: sanitized environment, PYTHONPATH=src/core/tests,
/tmp/issue86-recorder-identity-venv/bin/python
.copilot-tracking/research/2026-10-18/issue-86-recorder-identity-probe.py.
Exact base: eight changed-email code/oid open/reassign bypasses on JSON/SQLite,
all modified case and successful audit. Expected exit 1 retained in research.

System python import first failed ModuleNotFoundError zava_forward. Created
/tmp/issue86-recorder-identity-venv and installed editable src/core[dev], src/agents,
src/api[dev] with pip. Driver import succeeded. odbcinst executable absent;
mssql-python imports successfully; actual SQL parity subsequently passed below.

### Executed focused and coupled checks

All commands below use /tmp/issue86-recorder-identity-venv/bin tools. Runtime
commands use `env -i PATH=/tmp/issue86-recorder-identity-venv/bin:/usr/bin:/bin
HOME=/tmp` with only the listed PYTHONPATH/owned SQL variables. No configured
ZF_DATA, law data or inference credentials are inherited.

* Root: unchanged research probe command, output `issue-86-recorder-identity-after.txt`:
  eight of eight code/oid changed-email JSON/SQLite open/reassignment probes now
  refuse, case unchanged, successful audit unchanged, snapshots present; exit 0.
* From src/core: `PYTHONPATH=tests python -m unittest
  test_resident_decisions.JsonResidentDecisions
  test_resident_decisions.SqlResidentDecisions -q`: 78 ran, 77 pass, one existing
  JSON-only skip. Output `issue-86-recorder-identity-core.txt`.
* From src/core: `PYTHONPATH=tests python -m unittest
  test_resident_decisions.JsonResidentDecisions
  test_resident_decisions.SqlResidentDecisions test_change_provenance
  test_quality_procurement test_hazard_referral -q`: 232 ran, 230 pass, two
  existing JSON-only skips. Output `issue-86-recorder-identity-core-coupled.txt`.
* From src/api: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest
  test_resident_api -q`: nine ran, eight pass, one explicit browser opt-in skip.
  Output `issue-86-recorder-identity-api.txt`.
* From src/api: same environment, `python -m unittest test_resident_api
  test_role_matrix test_hazard_api -q`: 26 ran, 25 pass, one browser opt-in skip.
  Output `issue-86-recorder-identity-api-coupled.txt`.
* Root: `python .copilot-tracking/changes/2026-10-18/issue-86-recorder-identity-local-sql.py`:
  actual SQL Server 2022, existing MssqlResidentControls, 44 ran in 201.546s,
  43 pass/one JSON-only skip. Unique task-owned loopback container and UUID fixture
  databases; readiness confirmed by SELECT 1. All fixture databases and container
  removed. Runtime-generated secret never printed/stored. Output
  `issue-86-recorder-identity-mssql.txt`.
  Repeated after final typed/format-only test refinements: 44 ran in 212.049s,
  43 pass/one existing skip, same actual engine/cleanup; output
  `issue-86-recorder-identity-mssql-final.txt`. Final JSON/SQLite rerun:
  78 ran, 77 pass/one existing skip in 21.084s, output
  `issue-86-recorder-identity-core-final.txt`.
* From src/core: `ruff check . && ruff format --check . && mypy`: pass;
  71 formatted files/124 type-checked files. Output
  `issue-86-recorder-identity-core-quality.txt`.
* From src/api: identical configured command: pass; 24 formatted files/56
  type-checked files. Output `issue-86-recorder-identity-api-quality.txt`.

### Initial errors and disposition

`issue-86-recorder-identity-core-initial.txt`: initial 78-test run had three
JSON fixture errors because current staff cache changes were not persisted for
restart; corrected fixture canonical-list update, not production fallback.
`issue-86-recorder-identity-api-initial.txt`: two fixture failures, stale auth
staff cache after direct SQL oid injection and incorrect literal fixture code.
Fixed explicit fixture cache and source-derived expectation; no auth relaxation.
Initial Ruff detected unbound loop closures/long lines, formatter differences;
fixed with typed functools.partial and configured formatter. Initial mypy found
four lambda inference errors, missing Store db narrowing and API heterogeneous
dict typing; corrected types/narrowing/partial, not suppressions.
Expected rule-check unavailable logs in HTTP suites reflect the deliberately
unloaded synthetic law store; not legal validation. Coupled tests intentionally
inject post-commit errors and log them; passing assertions verify boundaries.

### Packaged local application

`docker build -q -f src/api/Dockerfile -t issue86-recorder-identity:local src`
passed. Image SHA-256:
8b4bed0cc1edc4b1d6d230f035920f6713a63947766494b910bd25a83dcbf2e6.
Output `issue-86-recorder-identity-image-build.txt`.

Actual runtime command, repository root replaced here by its exact path:

```bash
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,size=128m,mode=1777 \
  -e ZF_DATA=/tmp/no-configured-data.json -e ZF_STATE=/tmp/state \
  -e PYTHONPATH=/test-api:/test-api/tests:/coretests:/agenttests \
  --mount type=bind,src=/home/azureuser/source/ama-wt/issue-86-recorder/src/api/tests,dst=/test-api/tests,readonly \
  --mount type=bind,src=/home/azureuser/source/ama-wt/issue-86-recorder/src/core/tests,dst=/coretests,readonly \
  --mount type=bind,src=/home/azureuser/source/ama-wt/issue-86-recorder/src/agents/tests,dst=/agenttests,readonly \
  --entrypoint sh issue86-recorder-identity:local -c \
  'python -c "import os,hashlib,pathlib; from zava_forward.core import resident_decisions,projection; assert os.getuid()==10001; print(\"UID\",os.getuid()); print(\"CAPS\",[line.strip() for line in pathlib.Path(\"/proc/self/status\").read_text().splitlines() if line.startswith(\"CapEff:\")]); [print(pathlib.Path(m.__file__).name,hashlib.sha256(pathlib.Path(m.__file__).read_bytes()).hexdigest()) for m in (resident_decisions,projection)]" && python -m unittest test_resident_api -q'
```

Passed: UID10001, CapEff zero, read-only root, no-new-privileges and all capabilities
dropped. Installed resident/projection hashes match local source exactly.
All nine actual loopback authenticated resident HTTP tests ran, eight passed and
one visual-browser opt-in skipped. Output `issue-86-recorder-identity-container.txt`.
The ephemeral container exited/was removed. No live service or private data used.

## Review, Hashes and Publication

One original independent Review executed against frozen candidate
671ec03ac0e2e99478e9ae2c71537030d0541413, committed with all delivery and pre-Review
evidence. Execution Complete; outcome Conformant for the entire bounded candidate.
Zero implementation defects; RV-001 Low routes broader issue86 acceptance outside
the scoped fix. Reviewer assessed all 29 candidate paths plus current metadata,
ran independent write-free syntax/inventory/hash/whitespace checks and 12 helper
cases; it did not rerun filesystem-backed application suites. Those recorded
actual local runtime/engine suites remain implementer evidence, not reviewer
execution claims. No corrective source cycles or repeated original Review.

Original Review path:
.copilot-tracking/reviews/logs/2026-10-18/issue-86-recorder-identity-review.md.
SHA256: 9d55fbff9904feb9e1d303cfb13be1f5047c766ee038aa2275cb911749a78dcc.
Original critique hash remains unchanged; the original Revise/PC-001 finding is
not rewritten as Pass. Later handoff commits change evidence/state only; delivery
source/test/component contracts remain byte-identical to the reviewed candidate.

P03 original Review complete; authorized publication now in progress, not blocked
on an invented authorization. No push or PR yet.
`gh api user --jq '{id,login}'` returned id8036360/login
jmservera. Both author/committer will use repository-local
8036360+jmservera@users.noreply.github.com; no private/global email.
`git diff --check` passed. Remote main remains exact base at prefreeze check.

| Frozen input | SHA-256 |
| --- | --- |
| resident_decisions.py | 02a2f9e7fb44b95150a94f53f832f5ebe1283f250900250e6638ac7384ae1b1a |
| projection.py | 1b28e6080a675b4db9231e1f992a97184b5331b0496284be979701cf98a3c276 |
| test_resident_decisions.py | e543b1eb6e6b26f45eaf5fc3c3144ea4d76466828a97b92c4bedd63bd46cc7df |
| test_resident_api.py | 4f07cb91e44a7ca4ea767fbcc28aed4e4d0ca88a36d5d7d3fb10513e18dfa5e1 |
| Original plan critique | 5d39b3e712277f9441e8cb33396786b28d1620ea193ad5519b8599fdae1b48db |
| Original independent Review | 9d55fbff9904feb9e1d303cfb13be1f5047c766ee038aa2275cb911749a78dcc |

## Boundaries and Unmet Gates

No issue closure: formal complaints integration, historical erasure, contact
identity, human accessibility/without-detriment acceptance remain unmet.
No #130/#76 authorization. #122/#92 untouched. No private inputs, support/env,
Azure/IAM/Graph, real contacts, inference or spend. No web edits, so web skills,
visual browser/accessibility review are N/A; existing opt-in browser tests are
explicit skips, not Pass. Actual packaged/local HTTP checks passed. Full Azure,
model, human acceptance and hosted PR checks are not local engineering acceptance.
