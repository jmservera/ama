---
title: Resident retention restart implementation evidence
ms.date: 2026-10-16
---

## Scope and state

Task ID: issue-86-retention-restart. Slug: retention-restart-86.
Declared scope: full P01 plan, including implementation, validation,
documentation and PR publication. Execution: complete and published.
One Review completed, outcome Conformant. Blockers: none.
Plan and details use matching task slug under their 2026-10-16 directories.
One critique completed; PC-001/002 applied and unsupported PC-003 rejected.

## P01-T01: Contact boundary

Completed: first_contact excludes the contact prefix recorded by the content-free
resident_retention_tombstone.contacts_before_deletion count. Deletion clears the
cached first-contact marker and preserves separately purposed general contacts.
Fresh general or safe contact establishes the new origin; subsequent contacts
cannot extend it until the next deletion. Date-only legacy records filter
general contacts/cached dates conservatively while fresh safe history remains
eligible. No SQL/schema, permission or consent change.

## P01-T02: Validation

Completed targeted/full unit suites, Ruff/mypy and coherent original-module
mutation. Missing Ruff detected before installing core dev dependencies in
an isolated pip venv under the session files directory. Installed editable
core, agents and API distributions; no manifest changes.

Venv: /home/azureuser/.copilot/session-state/7096f887-1e10-4612-b1e1-773b3cb1ed9f/files/venv.
Commands use that venv's python/ruff/mypy:

* src/core: `python -m unittest discover -s tests -p test_resident_decisions.py -q`:
  40 tests, one explicit isolated-Azure-SQL opt-in skip; 39 executed tests pass.
* src/core: `python -m unittest discover -s tests -q`:
  482 tests, same one skip; 481 executed tests pass. Existing sensor fixture
  ResourceWarnings are unrelated and unchanged.
* src/api: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover
  -s tests -p test_resident_api.py -q`: 3 passed. Existing synthetic fixture
  logs explicitly report unavailable law-store evaluation; no live checks claimed.
* src/core: `ruff check .`, `ruff format --check .`, `mypy`: all pass
  (36 formatter-selected files; mypy 89 files). Existing migrated-module
  exclusions remain; these checks are not full static verification of that module.
* `git diff --check`: passed.

Mutation in a fresh process imports resident_decisions before Store, reads the
entire original module via `git show HEAD:src/core/src/zava_forward/core/resident_decisions.py`,
executes it in that module namespace, then imports Store/tests. Assertions verify
Store's helper alias and ResidentDecisionMixin MRO are the original definitions.
Selected methods, each in JsonResidentDecisions and SqlResidentDecisions:
test_returning_resident_general_contact_restarts_after_deletion,
test_returning_resident_safe_contact_starts_once_not_at_deletion,
test_renewed_period_expires_and_contact_cannot_reset_before_next_deletion,
test_legacy_deletion_ignores_old_contacts_and_allows_later_contact,
test_deletion_tombstone_contains_only_boundary_metadata.
All 10 fail intended assertions (old origin/due or missing metadata), zero
import/setup errors/skips. No package files are mutated. A fresh normal installed
code run afterwards passes the 40-test resident suite with the same opt-in skip.

## P01-T03: Documentation and publication

Core README limit replaced with approved restart rule and legacy boundary;
reference index updated and dated log appended. One Review completed:
.copilot-tracking/reviews/logs/2026-10-16/retention-restart-86-review.md.
Execution Complete, outcome Conformant for local P01 evidence; no findings.
Published implementation commit 2cc3e3d to
feat/retention-restart-after-deletion-86 and opened
https://github.com/jmservera/ama/pull/338 targeting main. Author and committer use
8036360+jmservera@users.noreply.github.com; required Copilot trailer included.
Normal push only. PR body has Refs #86 as its only issue linkage;
closingIssuesReferences is empty and issue #86 remains open. Hosted checks
started; no hosted success or owner merge is claimed.

Structured PR reference XML was generated in the session workspace (1161 lines),
not committed as another source artifact. No PR template was found.
No private datasets, excluded files, uv, Docker or Azure used.

## Amendments and divergences

No user-decision divergence. Count metadata handles same-day ordering without
new SQL/schema; conservative legacy recovery is an immediately relevant
current-state refinement recorded in research/plan.
Initial repeated-expiry test wrongly expected direct-answer recording to fail.
Inspection confirmed existing behavior permits recording but holds work release.
Corrected the test to assert require_resident_clear raises GateError; production
behavior is preserved. This is a local test correction, not a product divergence.
Publication is a post-Review handoff, avoiding a circular Review prerequisite.

## Follow-up

Existing issue #86 human/live-platform acceptance and historical erasure remain
separate owner work, not this slice's acceptance.
