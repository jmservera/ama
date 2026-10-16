---
title: Environment parameter sets changes
description: Implementation and validation evidence for issue 137
ms.date: 2026-10-16
---

Task ID: issue-137. Task slug: environment-parameter-sets.
Declared scope: full plan. Candidate critique executed and disposed; ready.
Write boundary: infra/, reference README/log and requested RPI artifacts.
No Azure changes planned; pilot decisions remain open.

## Planning reconciliation

PC-001 through PC-004 applied directly: independent development opt-outs,
synthetic-only valid-check test baseline, README contradiction removal and
five-criterion mapping. PC-005 rejected because its scratch-path prohibition
is not a current user requirement. No second critique or new approval inferred.
Starting dependency-ready item: P01-T01.

## P01 Environment implementation

Updated the existing three parameter files, main/guard/SQL modules, deployment
wrapper and two test files. Preserved resource-name expressions and parameter
file paths. Dev explicitly relaxes only purge/quarantine; test/pilot retain
production settings. SQL is unconditionally private with no firewall/switch.
Recorded-check/location guards require explicit completed inputs; pilot
locations stay empty. Wrapper rejects invalid groups/workloads before Azure.
README reconciles current owner direction and single differences table;
reference index/log updated. Four test methods added, existing matrix and
mutations extended. No tests removed.

## Validation

Initial compiled-policy run: 30 tests, one mutation error caused by direct
dictionary access to an intentionally removed property. Changed assertion to
get() so the missing control yields AssertionError as required. Full rerun
pending. Missing ruff/mypy installed via pip in an isolated session venv;
source distributions installed editable without optional cloud dependencies.

Full infra run: 121 tests, two obsolete text assertions failed (SQL conditional
public switch and pilot uksouth/dev-test relaxations). Updated the existing
test_edge_module.py and test_governance.py assertions to the stronger contract,
without removing test coverage or adding methods. This is an immediately
relevant current-state plan update, not a new scope or user decision.

All 17 Bicep files built and linted successfully. Local synthetic App HTTP/
persistence smoke passed six tests, starting/stopping its own loopback server
over temporary fixtures. Ruff passed changed Python. Expanded mypy exposed
existing unannotated compiled-template class state and heterogeneous mapping
inference; added proper ClassVar/mapping annotations rather than suppressions.

Rerun: all 121 infrastructure tests passed with REQUIRE_AZ_BICEP=1 and
absolute source-project PYTHONPATH; no skips. Ruff lint/format and mypy passed
the wrapper and compiled/fake-az suites. Four new methods total; existing
security and resolver mutation tests retained. Added semantic tag-union
assertion proving required tags cannot be overridden while extras survive.

Final rerun after tag semantics: 121 tests passed, no skips, in 41.861 seconds;
ruff lint and mypy passed. All committed parameter files compile in this suite.
All-file build/lint and six local HTTP smoke tests passed before that test-only
addition. P01 and P02-T01 complete. Review-ready boundary is implementation and
offline acceptance; P02-T02/T03 remain review/delivery tasks. Deployment is not
planned; fresh checks and pilot decisions remain explicit external follow-ups.

## P02-T02 Single review

Review executed once at
.copilot-tracking/reviews/logs/2026-10-16/environment-parameter-sets-review.md.
Execution Complete; outcome Residual work. Four issue 137 criteria met offline;
region/quota criterion Partial because fresh live checks are intentionally
not run. All four issue 139 criteria have offline evidence, not live ARM
acceptance. RV-001 routes owner decisions/fresh checks to a distinct readiness
follow-up. No implementation defects identified; no new in-task review cycle.
Only P02-T03 delivery remains.
