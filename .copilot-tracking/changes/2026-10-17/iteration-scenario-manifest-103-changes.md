<!-- markdownlint-disable-file -->
# RPI Changes: iteration-scenario-manifest-103

Task #103, 2026-10-17. Full P01 scope from dated plan/details.

## P01-T01: Red contract tests

Complete. New contract suite first failed on missing helper. A separate
behavior assertion against the unchanged v0.1.0 manifest failed with
"Unsupported blanket deferrals in existing iteration manifest".
Missing installed core was observed before restoring only this
worktree's core[dev] editable distribution in .venv. No shared environment
modified. One final-candidate critique Complete/Pass.

## P01-T02: Implementation

Complete: one typed shared offline helper and one focused test file. Existing
scenario v0.2.0, inventory v1.3.0 reviewed 2026-10-17 and provenance display
name updated. All 20 full journeys unavailable, partial IA sources/defaults
retained and SHA-256 bound. No runtime/API/UI changes, new dataset or registry.
Current evidence contract deliberately rejects label-only represented/deferred
promotions; future evidence needs a reviewed/versioned contract update.

## P01-T03: Validation and documentation

Complete. From src/core with this worktree's .venv:

```bash
PYTHONPATH=tests ../../.venv/bin/python -m unittest \
  test_scenario_manifest test_needs_inventory test_generator_coverage \
  test_synthetic_provenance.ProvenanceRegisterTests.test_every_dataset_has_current_visibility_and_dictionary_entry \
  test_synthetic_provenance.ProvenanceRegisterTests.test_all_public_payloads_pass_production_checker -q
../../.venv/bin/ruff check src/zava_forward/core/synthetic/scenario_manifest.py \
  tests/test_scenario_manifest.py tests/test_needs_inventory.py
../../.venv/bin/ruff format --check src/zava_forward/core/synthetic/scenario_manifest.py \
  tests/test_scenario_manifest.py
../../.venv/bin/mypy src/zava_forward/core/synthetic/scenario_manifest.py \
  tests/test_scenario_manifest.py
```

29 tests pass, including mutation rejection and public-only provenance/pattern
checks. Ruff/format pass, mypy passes two changed typed files. Intermediate
static failures (one test-loop inferred type, one long line and inventory
narrowing) were corrected before final validation. Malformed-row mutations
first exposed 11 TypeError/KeyError cases; explicit ValueError guards resolved
them. Read interception proves unapproved source mutations fail before reading.
Validation does not mutate manifest inputs.

12 newly added production Markdown links/anchors verified against their actual
files/headings; `git diff --check` passes. Existing synthesis/index/provenance
display and append-only knowledge log updated; original/memory unchanged.
No full-suite, browser, real model, SQL or Azure check run: no such behavior
changed or acceptance claimed. Existing fixture files/registry unchanged.

## Amendments and Divergences

None. Operational owners and full journey acceptance remain unknown.

## Actual Phase Log

* 2026-10-17 Research: executed Wider -> Deeper -> Contrarian; one Programme
  Manager scope refinement, Ready. Exact issue/dependencies/prior art inspected.
* 2026-10-17 Plan: candidate finalized; one independent critique executed,
  Complete/Pass with zero findings.
* 2026-10-17 Implement: entered after persisted transition; P01-T01 starting.
* 2026-10-17 Implement: P01-T01 red evidence retained; P01-T02 helper/metadata
  complete; P01-T03 focused validation and documentation complete. All markers
  and handoff reconciled; ready for exactly one Review.
* 2026-10-17 Review: executed once over the full supplied offline boundary;
  Complete/Conformant, zero substantive findings. Full journeys and
  owner/human/application gates routed as distinct future work, not new tasks.
* 2026-10-17 Follow-up: parent proceeding only to authorized commit/push/main PR;
  no child delivery loop and no merge.

## Handoff

Full planned scope complete; single Review Complete/Conformant. No blocker or in-scope remainder.
Full FR-035 journeys and owner/human/application acceptance remain follow-up
boundaries, not silent approvals or new delivery work.

## Publication Preparation

GitHub account freshly resolved as jmservera/id 8036360; repository-local
author/committer email constructed as the account's users.noreply address.
Requested branch retained, no existing PR, base main bf98977.
Commit helper's referenced instruction resource and get_changed_files host
tool are unavailable; use explicit repository/user Conventional Commit rules
and directly inspected Git delta instead. No history rewrite or merge.

## Published Handoff and Stop

Implementation/evidence commit `6560d488aa6891080b34fc99dd886c42f1215ade`
was pushed to `feat/iteration-scenario-manifest-103`. Verified author and
committer both use the resolved account's users.noreply email.
PR https://github.com/jmservera/ama/pull/380 is OPEN against main, Refs #103,
with the exact two-row criterion audit and all seven RPI artifact pointers.
The initial GitHub check rollup was empty, not a CI pass.

2026-10-17 actual Follow-up closeout: task completed; automatic session stopped
at the caller's explicit pushed-PR boundary. No child task selected, nested
loop, merge, rebase or force-push. Full journeys/operational approval remain
distinct future owner-scoped work. Only this handoff and state are updated
after Review; no source behavior changed and no second Review is performed.

The PR helper's instruction/citation-policy resources were unavailable in
the installed/repository paths. The body uses the exact issue criteria and
already reviewed evidence; no extra parallel review or inferred approval.

## Authorized Same-PR Rebase Continuation (2026-10-17)

Caller explicitly authorized rebasing only the run-owned
`feat/iteration-scenario-manifest-103` for PR #380 onto latest `origin/main`,
then one final topic `--force-with-lease` push. Original remote head was
`7c3c6a7b69001adb0568bdf35ff95d6c8f3cd64d`; fetched main is `b15f2f0`
from merged #379. Worktree was clean. Both existing topic commits replayed,
producing implementation `7e2be79` and handoff `e26f776` before this single
continuation-evidence commit. No main rewrite or merge.

Exactly one conflict occurred: `docs/reference/log.md` at the shared append
point. Removed only conflict markers, retained the complete latest-main #360
tail first, then the complete original #103 append unchanged. The reference
index auto-merged: retained upstream's refined #375/#360 introduction and new
scoped initializer routing row, plus unchanged #103 routing row. No source,
manifest, inventory, fixture, test or unrelated upstream file was edited.

Byte comparisons verified all pre-existing topic files except the two shared
knowledge files unchanged from the old head, every upstream-only file unchanged,
latest-main log as an exact prefix with the original topic append as exact
suffix, and index exactly latest main plus the original #103 row once.
An initial overly strict check expected superseded old index prose to remain
verbatim; it failed because main deliberately refines that prose. Inspection
confirmed the upstream update, then the correct latest-main-plus-topic-row
assertion passed. No upstream wording was reverted.

Reran the exact combined focused command recorded under P01-T03 once after
rebase: 29 manifest/inventory/routing/public-provenance tests passed. Scoped
Ruff passed; format checked two files unchanged; mypy passed two source files.
`git diff --check origin/main` passed. No repeated full suite, generation,
private reads, cloud/model calls or browser check: application source and
fixture bytes are unchanged.

Caller identifies independent reviewer `fa457455` as assessing old head
`7c3c6a7`. That agent ID is not visible in this session; one direct read returned
"No agent found". No GitHub review/comment or Source CI run was present at
inspection. Do not transfer an old-head verdict or claim independent acceptance:
final exact-head follow-up remains required. Preserve the original Review as
historical; no new review loop or scope change.

The final push uses an explicit lease against the recorded original remote
head, topic ref only. Existing Source projects CI is ordinary unpaid engineering
CI; relevant src/metadata paths match its PR filter. After push, inspect runs;
if none exists for the exact final head, dispatch only existing `src-ci.yml`
on this branch. Do not dispatch paid rubric. Caller stop boundary is final
publication/CI handoff, with no extra receipt commit or head-chasing update.
