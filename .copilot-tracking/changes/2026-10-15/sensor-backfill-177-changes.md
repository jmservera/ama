---
title: Sensor backfill 177 implementation evidence
description: Changes, commands, limitations and delivery for the register-backed slice
ms.date: 2026-10-15
---

## Scope and State

Full plan execution for task 177 / sensor-backfill-177.
Plan: .copilot-tracking/plans/2026-10-15/sensor-backfill-177-plan.md.
Details: .copilot-tracking/details/2026-10-15/sensor-backfill-177-phase-details.md.
P01 and P02-T01 complete; P02-T02 Review complete, publication remains.
No source changes before research and final-candidate critique.

## Intake Command Evidence

All commands run from the supplied checkout unless a project cwd is stated.
Read-only view/glob/rg operations inspected the explicitly listed source/docs.

| Command | Result |
| --- | --- |
| git status --short; git branch --show-current | Clean; feat/src-sensor-backfill-177 |
| gh issue view 177 --comments; gh issue view 177 --json title,body,comments | Three acceptance criteria and src migration comment read |
| gh pr list --head feat/src-sensor-backfill-177 --json number,state,baseRefName,url | No existing PR |
| gh api user --jq '{id,login}' | Verified id 8036360, login jmservera |
| gh pr view N --json number,title,state,mergedAt for 296-302 and 316 | All merged, including stock prerequisite |
| gh api repos/jmservera/ama/issues/177/sub_issues | Children 178-183 all open |
| gh issue view N --json number,title,body,comments for 178-183 | All child acceptance and owner synthetic-climate fallback read |
| gh issue view 110 --json state,body | Open; consumer contract implementation unavailable |
| git log -3 --oneline | HEAD 64f6b3c contains merged stock fabric #316 |
| command -v python3; python3 -m pip --version | Python 3.12, pip 26.2.1 available |
| command -v ruff; command -v mypy | ruff probe absent caused chained command exit 1; explicit module probes followed |
| python3 -m ruff --version; python3 -m mypy --version | Both modules missing |
| python3 -m pip show zava-forward-core zava-forward-api | Projects not installed |

## Plan Amendments and Decisions

One critique, no repeat. Add versioned stock SQL DDL and ID preflight, explicit
subset size and selection-before-consent semantics. Reject critique's claimed
/tmp ban: not present in parent scope; ephemeral fictional test output is needed
for user-requested local validation. No source/private dataset access elsewhere.
No user-owned policy or child deferral inferred.

## P01 Changes

Added typed sensor_stock adapter and 14 tests in src/core. Optional --register
reuses stock-fabric-v1 seed and construction assumptions, never a new stock.
Explicit sorted subset precedes synthetic consent filtering; unknown/declined
produce no readings. Complete allowlisted input validation precedes output,
private columns are dropped, hashes use canonical inputs and coverage includes
selected/excluded IDs and counts. Every generated reading/sensor is synthetic.

Writer and estimate use actual granted sensors, handle zero output, record
sanitized fabric and per-file hashes, retain historical fixture bytes and
reject repository/symlink/nonempty stock destinations. Additive stock-reading-v1
DDL accommodates full digest sensor IDs and bounded opaque home IDs without
changing legacy DDL or migrating databases. Core dependencies remain inward.
Existing v2 source fingerprints necessarily change; legacy CSV hashes do not.

Core README and existing synthesis/index/log document invocation, assumptions,
portable loading and remaining evidence. No mvp, workload image/dependency,
private data, .env, .vscode or github-issues files changed.

## Validation Commands and Results

VENV=/home/azureuser/.copilot/session-state/1d03ee17-d92c-40c5-b373-f2290e5f37f2/files/venv.
All python/ruff/mypy below use its bin directory. Temporary fictional outputs
are removed by their TemporaryDirectory contexts. No private inputs or billable
calls were used.

| Command (cwd where relevant) | Result |
| --- | --- |
| python3 -m venv VENV; VENV/bin/python -m pip install -q -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]' | Pass; restored missing local projects/dev tools, pip only |
| python -m unittest discover -s tests -p 'test_sensor*.py' -q from repository root | Failed: tests directory not importable; corrected cwd, not a code failure |
| cd src/core; python -m unittest discover -s tests -p 'test_sensor*.py' -q; python -m unittest discover -s tests -p 'test_synthetic_determinism.py' -q | Pass: 27 + 7 tests; includes 14 new tests, existing historical hashes and plausibility |
| cd src/core; ruff check .; mypy (initial) | Failed: two new long lines and three object-index typing errors; corrected without broad ignores |
| cd src/core; ruff format src/zava_forward/core/synthetic/sensor_stock.py tests/test_sensor_stock.py; ruff check .; ruff format --check .; mypy | Ruff passed; mypy found implicit imported provenance export; direct import corrected |
| cd src/core; python -m unittest discover -s tests -q | Pass: 353 tests, 106.887s; two pre-existing ResourceWarnings in test_sensor_backfill |
| cd src/core; ruff check . (after direct import) | Failed: new-test import ordering; fixed with ruff |
| cd src/core; ruff check --fix tests/test_sensor_stock.py; ruff format tests/test_sensor_stock.py; ruff check .; ruff format --check .; mypy | Pass: 25 formatted files, 78 typechecked source files |
| cd src/api; PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q; ruff check .; ruff format --check .; mypy | Pass: 495 tests, 98 skipped, 193.816s; 9 formatted files, 37 typechecked files |
| cd src/agents; python -m unittest discover -s tests -q; ruff check .; ruff format --check .; mypy | Pass: 70 tests, 6.840s; 11 formatted, 16 typechecked |
| cd src/orchestrator; PYTHONPATH=../core/tests python -m unittest discover -s tests -q; ruff check .; ruff format --check .; mypy | Pass: 17 tests, 0.124s; 5 formatted, 8 typechecked |
| cd src/importer; python -m unittest discover -s tests -q; ruff check .; ruff format --check .; mypy | Pass: 39 tests, 0.189s; 11 formatted, 10 typechecked |
| docker build -f src/api/Dockerfile -t zava-forward-sensor-177:local src | Blocked: permission denied connecting to /var/run/docker.sock; no image/runtime claim; rely on CI |
| python tools/rename-zava-tests.py (initial) | 25 tests, 7 missing pptx/PIL errors |
| python -m pip install -q python-pptx Pillow; python tools/rename-zava-tests.py | Restored tools; still 1 failure + 1 error from missing yaml |
| python -m pip install -q PyYAML; python tools/rename-zava-tests.py | Pass: 25 tests, 0.436s; broken.pptx diagnostic is an intentional negative test |
| cd src/api; PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistants.ApiTests.test_release_record_local_http -v | Pass: real local App/ephemeral listener, health/auth, SQLite release admission, denied inference, released scripted AI proposal, unchanged domain state and revocation; 1.098s |
| git diff --check; git status --short; git diff --numstat; git diff -- docs/reference/log.md | Pass; intended src/docs/artifacts only; log entry appended |
| tail -25 docs/reference/log.md; git diff --stat | Read-only append/scope inspection |
| git --no-pager diff -- src/core/src/zava_forward/core/synthetic/sensor_backfill.py src/core/tests/test_synthetic_determinism.py src/core/pyproject.toml; gh pr view N --json number,body for 296-302 | Read full current diff and all migration PR bodies; boundaries preserved |

The full API suite skipped 98 feature-gated tests under its default environment;
the separately selected release-record HTTP test ran and passed. This is not
live-model validation. Existing migrated lint/type exemptions remain; new helper
is strict, with only migrated untyped-call permission for the new test module.

### Two-year hourly executable CLI and SQLite experiment

Executed a python heredoc that creates a five-home, wholly fictional CSV with
three granted, one declined and one unknown choice in TemporaryDirectory.
It calls (via subprocess, installed module):

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register TEMP/register.csv --homes 5 --days 730 --cadence 60 \
  --as-of 2026-10-15 --estimate-only
python -m zava_forward.core.synthetic.sensor_backfill \
  --register TEMP/register.csv --homes 5 --days 730 --cadence 60 \
  --as-of 2026-10-15 --out TEMP/a
python -m zava_forward.core.synthetic.sensor_backfill \
  --register TEMP/register.csv --homes 5 --days 730 --cadence 60 \
  --as-of 2026-10-15 --out TEMP/b
```

It asserts all output bytes identical; estimate matches manifest; coverage is
5 selected / 3 monitored / 1 declined / 1 unknown. Result: 52,560 rows
(3 * 730 * 24), first in-memory SQLite load 52,560 inserted / no rejects,
second load zero inserted / no rejects. Temporary outputs cleaned automatically.

Payload SHA-256:

* estimate.json: ed7f03516ad2930afba1606568144ed9a432b7b0ef3fdb0d51ebd6f3f055bb13
* readings-0000.csv: 2a3b97b63673672111183bd9dcc7b29780b6368f31d9ac72aae44061a75ba4f6
* sensors.csv: 0f50daa0428c55ad621cc02cb5268ed038600bc5060eafaf1b78e27f1dbeb251
* stock-fabric.csv: 56b92be7481d4195fca3e85083e3d9047788ca520bfcc91042080574698aa9ce

These hashes describe disposable fictional payloads, not private-stock output,
historical climate, deployed devices or durable runtime records.

## P02-T02 Review and Publication

One post-implementation Review executed, Complete / Residual work. No material
implementation defect identified in the bounded slice. RV-001 routes existing
child evidence; RV-002 routes full-stock/activation owner decisions; RV-003
routes CI image/SQL evidence. No repeat review or unselected follow-up work.

Publication pending. Intended commit: feat(core): add register-backed sensor history.
Authenticated identity was verified before configuration; use the requested
privacy-safe repository-local email for author and committer. Explicitly stage
only intended src/docs/RPI artifacts; no private output belongs in the commit.

## Open Acceptance and Evidence

Parent children criterion stays unchecked: #178-#183 are open, not owner-deferred.
Historical outdoor records/licence approval, dated retrofit data, full occupancy/
ventilation/drying model, configurable full fault classes and separate truth,
#110 reusable consumer, full-stock storage/cost approval, real AI/SQL Server/
Azure and direct human/resident approval remain unproven. No CO2 or energy added.
