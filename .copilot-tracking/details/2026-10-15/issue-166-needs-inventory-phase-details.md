---
title: Issue 166 needs inventory phase details
description: Task context, targets and evidence boundaries
ms.date: 2026-10-15
---

## Metadata

Task ID: issue-166. Slug: issue-166-needs-inventory.
Plan: .copilot-tracking/plans/2026-10-15/issue-166-needs-inventory-plan.md.
Research: .copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Reconcile canonical metadata and tests | Complete |
| P02 | Validate, review and publish | Validation complete; Review/publication remaining |

<!-- rpi:phase id=P01 -->
## P01: Inventory and scenario integration

C2-C8 show a sound existing schema, missing scenario link and stale fixture
claims. Preserve the thirteen identities and every existing open human gate.
Canonical targets are the pack JSON/README, reference index/log, core README
and `src/core/tests/test_needs_inventory.py`. Generated targets: none.
Test ownership: core. Exact removals: none. Maximum additions: one manifest
JSON and eight test methods, plus requested RPI artifacts. Do not modify the
published `manifest.json` pack receipt or private data.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Metadata and gate

Use relative reciprocal filenames within the pack. New scenario manifest is
an inventory-review integration seed for #103, not full AC-043 compliance.
Its review binds inventory version/date and all thirteen reviewed row IDs;
reviewer is explicitly the automated engineering pass and owner status stays
pending. Preserve future iteration review/versioning instructions and the
pre-start row citation rule. Add no approval assertions or legal claims.

Correct directly contradicted SN-01/02/03/08/09/12 notes from public
repository sources, distinguishing small fixtures, projected full-stock
volumes, actual runs and live acceptance. Sensor remains partial (generator
exists; full-stock/climate decisions not evidenced). Add chat fixture dataset
reference and correct sensor provenance to the migrated generator/output.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Regression tooling

Keep old structural tests except the stale mandatory missing-sensor assertion.
Use typed helpers for new review checks if useful, no runtime gate abstraction.
Test actual canonical JSON plus independently mutated stale version/date,
missing/duplicate row IDs, reciprocal path and owner approval boundaries.
Semantic coverage means these exact invariants, not merely JSON parses.
Do not assert all thirteen needs are covered or that CI proves human approval.

<!-- rpi:phase id=P02 -->
## P02: Evidence and delivery

All new code remains src/core tests. Existing application and deployment
behaviour must remain unchanged.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local validation

Use `.validation-166/` under this worktree for environment, logs and scratch.
Export TMPDIR, TMP and TEMP to its absolute `tmp/` path and preflight
`tempfile.gettempdir()` before execution. Smoke data/state also stay there.
Keep all scratch paths unstaged and remove owned scratch after validation.
Use pip only. Install after
recorded `ModuleNotFoundError` for packages/ruff/mypy. Run five suites using
the documented fixture PYTHONPATH for API/orchestrator and agents if needed.
Run configured linters/type checkers per project and explicitly check changed
test code outside the migration exemptions. Temporary app data comes from
`src/core/tests/dataset.py`, never the real/private stock; local smoke is
non-delivery development evidence and cannot pass real AI/SQL/Azure acceptance.
Before executing core discovery, exclude
`test_synthetic_provenance.ProvenanceRegisterTests.test_private_register_is_labelled_and_has_no_person_fields`
and `test_synthetic_provenance.ProvenanceRegisterTests.test_private_and_public_outputs_are_separated`.
They read private files; list both as Not run and qualify the core count.
Other generator tests patch register loading with constructed inputs; do not
run unpatched private generators. Sensor provenance retains `not-generated`
for the unmaterialized canonical dataset, with the generator described.
Record every shell command, exit outcome/count and skips in changes and PR.
Stop only owned processes and remove only named temporary smoke data.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and PR

One RPI Review compares plan, details, critique, diff and command evidence.
Required human checkboxes stay open. Review findings route later work.
Check staged paths for prohibited/private changes. Commit using account
returned by a fresh `gh api user`, derive `{id}+{login}@users.noreply.github.com`
and configure repository-local email for both author and committer. Verify
it matches the requested 8036360/jmservera identity; mismatch blocks publication.
Keep the requested coauthor trailer and inspect resulting commit identities. Push only
feat/src-needs-inventory-166; PR base main, Refs #166, never Closes.
Report review result separately from issue acceptance and CI status.

## Completion evidence before Review

P01 metadata and eleven canonical/mutation tests pass. P02-T01: selected core
264 tests passed (two private readers excluded), agents 70, API 459 (92
skipped), orchestrator 17, importer 39; five-project quality checks and isolated
changed-file checks pass. Synthetic local HTTP/SQLite smoke and link/diff
checks pass. Docker socket permission denied; SQL Server/image rely on CI.
No runtime change, live AI, Azure deployment or owner approval is claimed.
P02-T02 is ready for the one Review, then publication.
