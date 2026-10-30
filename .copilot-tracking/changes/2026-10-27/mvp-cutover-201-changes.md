<!-- markdownlint-disable-file -->
# RPI Changes: Retire legacy MVP directories

## Metadata

* Task ID: issue-201
* Task slug: mvp-cutover-201
* Date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md
* Details: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md

## Execution Status

Complete full plan: P01/P02/P03 and every task marker complete.
Implementation/source scope independently reviewed and published in PR #499.
Approved write boundary: named pointer deletion, existing live documentation,
dated RPI artifacts. No workflow/runtime/test changes or generated snapshots.

## Execution Summary

Research and one independent critique completed before implementation.
Original critique Revise retained; parent disposed all three findings directly.
Owner-authorized source retirement does not establish hosted/live acceptance.

## Completed Work

### Local archive and pointer retirement (P01-T01)

Fresh gh account-derived identity configured repository-locally before tag.
Created absent annotated refs/tags/v0.21.0:
tag object0096b11301236c6eef85fd3cdefc657582109b8a, target
65a514ed20e97816dbf47e9fb981ab4cfe40597d (BRD0.21.0).
Readback confirmed target and privacy-safe tagger. No tag push.
Deleted only mvp/README.md via apply_patch; rmdir removed its empty directory.
prototype was already absent. No private data inspected.

### Live guidance reconciliation (P01-T02)

Updated the approved existing docs/README/instructions, archive command,
prospective sign-off note and intentional-reference policy.
The discovered regulatory UX source path is an immediately relevant target,
not new requirements work; fixed it to existing core assistants.py.
PRD's 2026-10-08 baseline is explicitly retained as historical with current
source navigation added; no requirements or version changed.
Semantic verification confirms exact original log prefix, unchanged workflows,
absent tracked/filesystem legacy paths, archive target and zero new/changed
local-link failures. Historical log links have an additive valid repair map.
Existing baseline link debt remains: architecture index1, KB index1, log7
distinct failures; none is silently reported as newly repaired.

## Implementation-Time Plan and Detail Updates

### Critique dispositions before execution

PC-001: allowlisted test process environment with task-owned external scratch,
no inherited application/SQL/cloud settings. No applicable external-temp ban.
PC-002: freshly derive privacy-safe account identity before tag and commit.
PC-003: all five issues use Refs in this PR due to incomplete broader evidence;
the user permits closure only when every criterion is proven.
No new user decision, second critique or scope widening required.
P01-T02 target list/old-anchor destination corrected in details: regulatory UX
source path and agents README hold the actual relevant current content.

### Final reference sweep: coordinator source-layout fact

The public tracked-reference sweep exposed the same transitional status in
the coordinator agent. Added that known, directly related factual target to
P01-T02/details and changed only its cut-over status/archive wording.
HVE Builder activated for this Minor improve: no architecture, capability,
workflow decision, tool configuration or write-authority change.
Behavior gate Satisfied-and-skipped: execution Not run, verdict Not applicable,
fidelity Not applicable, because only a historical/current source-location
fact is clarified. Distribution wiring is Not applicable for existing
repository-specific artifacts. Existing file/frontmatter and local-link
checks apply; independent RPI Review will include bounded static delta
assessment. Parent performs the tiny editorial batch directly under the
host's no-trivial-delegation rule, rather than spawn separate author/validator
workers. No standalone comprehensive HVE conformance claim is made.

## Validation Record

No full gate; optional --changed not needed for this prose/pointer change.

Initial requested API command under sanitized env failed:69 tests attempted,
53 import errors, missing installed zava_forward distributions. Full output:
/home/azureuser/.copilot/session-state/064745c5-eb4a-4eda-a5d3-e54696e0c15f/files/cutover-201/api-initial.log.
This missing-package failure justifies isolated pip installation.

After editable install of all five src distributions without deps, API
discovery ran1058 tests in400.136s, failed6 import/prerequisite errors with310
skips. Four modules need the manifest's Azure runtime dependencies; two
Node-based tests failed because the sanitized PATH omitted existing Node.
Full output remains api.log beside the initial log. Installed only existing
hashed src/api/requirements.txt; added the existing Node directory explicitly
to allowlisted PATH. Final API rerun passed1121 tests in423.800s,
314 skipped, zero failures/errors (api-final.log).

Initial rename run attempted25 tests, failed7 missing PIL/pptx errors.
Installed existing tools/rename-zava-requirements.txt into a separate owned
venv; rerun passed25 tests, zero skips (rename.log).
Existing parity/registry selectors passed17 tests, zero skips
(parity-registry.log).

Task-owned scratch root:
/home/azureuser/.copilot/session-state/064745c5-eb4a-4eda-a5d3-e54696e0c15f/files/cutover-201.
All test launches use env -i with PATH, LANG=C.UTF-8, HOME and TMPDIR under
that root; API/rename also set TMP/TEMP/XDG_CACHE_HOME/ZF_DATA explicitly
there. The two venvs are isolated; no dependency manifests or pins changed.
Semantic verifier at that root checks only current changed docs and baseline
Git objects; it never opens private datasets.

### Final validation summary (P02-T01)

| Check | Result | Boundary |
| --- | --- | --- |
| Required API discovery | Passed;1121 discovered,807 executed,314 skipped | Exact requested command after existing pinned prerequisites restored |
| Required rename regressions | Passed25, zero skips | Exact requested root command |
| Existing parity/registry regressions | Passed17, zero skips | test_cutover_audit and test_eval_registry |
| Directory/tag/workflow/log/link assertions | Passed | semantic-final.json and verifier under external scratch |
| Legacy imports in src/infra/tools | None | Anchored Python import search, not historical fixture-token absence |
| Diff whitespace | Passed | git diff --check and cached equivalent |
| Full/scoped rpi-checks runner | Not run | Owner explicitly forbids full; optional changed tier unnecessary |
| Hosted/deployment/SQL/browser integration | Not run | Remain distinct owner/CI acceptance |

Static skip inspection without executing tests discovered313 decorator skips:
308 SQL opt-ins and5 browser opt-ins. The remaining one runtime skip is the
JSON store's inapplicable SQL COMMIT acknowledgement test
(src/api/tests/test_progress_report_api.py). Exact reason counts are in
skip-reasons.json; no claim of SQL/browser execution. The initial missing
package/Node failures remain above rather than being overwritten.

Exact successful command environment (SCRATCH is the task-owned root above):

```bash
# API, from src/api; no inherited application or credential environment
env -i PATH="$SCRATCH/venv/bin:/home/azureuser/.nvm/versions/node/v24.21.0/bin:/usr/local/bin:/usr/bin:/bin" \
  LANG=C.UTF-8 HOME="$SCRATCH/home" TMPDIR="$SCRATCH/tmp" TMP="$SCRATCH/tmp" TEMP="$SCRATCH/tmp" \
  XDG_CACHE_HOME="$SCRATCH/cache" ZF_DATA="$SCRATCH/data/zavaforward.json" \
  PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
# Rename, from root, same environment with rename-venv/bin and no PYTHONPATH
python3 tools/rename-zava-tests.py
# Parity/registry, from root, same sanitized source venv
PYTHONPATH=src/core/tests:src/agents/tests python3 -m unittest test_cutover_audit test_eval_registry -q
```

Final public reference sweep excludes private support/data/environment paths
and classifies remaining references as dated history, pinned evidence,
intentional cut-over notices, legacy check identities or defensive fixtures/
guards. The paper's repo_history_metrics.py intentionally classifies historical
Git paths, not current executable inputs. Existing audit TSVs remain unchanged.
No remaining live legacy Python import or local mutable old-guide link was
found outside the preserved append-only log.

## Pre-Review Reconciliation

Ready for one independent Review. Plan P01/P02 and task markers, phase details,
completed source changes, validation failures/final results, historical
exceptions and remaining work agree. Original critique unchanged. No source
change after this validation boundary is planned; Review findings route later.

## Blockers

None.

## Remaining Work

None within the bounded task. Retained hosted checks, owner merge, tag/release
publication and wider issue acceptance are distinct follow-ups.

## Independent Review Result

Exactly one Review executed Complete / Conformant for completed source and
validation P01/P02, no substantive RV findings or publication blocker.
Canonical record:
.copilot-tracking/reviews/logs/2026-10-27/mvp-cutover-201-review.md.
Original Review is immutable and explicitly leaves later publication pending.
Independent source-diff SHA256:
c06d4a24ea2c37e8166fa7c3d05fbaf4fdaff675a335f170e777e6ffef165404.
Parent independently reproduced this unchanged hash after fresh main fetch;
source remained at reviewed base65a514ed. No second Review or in-task fixes.

## Publication (P03-T02)

Fresh gh account-derived privacy-safe identity configured repository-locally
for author and committer. Conventional source/evidence commit:
0e4271ece29de72c2fa4e2be48bb420c3724539f,
chore: retire legacy MVP directories after owner sign-off.
Required Copilot co-author trailer is present. No private identity was used.

Independent exact-head publication identity assessment passed, external
exact-head-initial.json beside scoped logs. This checks committed source hash,
original Review/critique identity, clean branch, local tag, no legacy tracked
paths and unchanged workflows; it is not another RPI Review or full gate.

Fetched main unchanged at65a514ed immediately before branch publication.
Pushed only HEAD:refs/heads/chore/mvp-cutover-201 with --no-follow-tags and
push.followTags=false. Opened main-target PR #499:
https://github.com/jmservera/ama/pull/499.
The PR explicitly records owner SIGNED OFF #201 on2026-10-27, archive target/
exact owner push command, local validation/skip boundaries, original Review,
and Refs for all five issues with their unmet acceptance. No issue was closed,
tag pushed, release published, protection changed or main merged.

PR-template discovery found none. Shared public-output policy was read and
applied; no content concern was found. Existing independent RPI assessment
and complete source diff were reused rather than rerunning redundant parallel
PR reviews under the host's no-duplicate-review/no-trivial-delegation rule.
PR helper instructions were located under installed rules/ after their
documented instructions/ path proved absent. The generic staged-change MCP
tool was unavailable; permitted Git CLI staging/diff review was used.

Read-only hosted inventory additionally confirms Source projects CI is active;
legacy MVP workflows are disabled_manually, unchanged by this task.
Latest observed Source CI main run39130862637 succeeded at older
612cbed78a35a4ab426571aa7d2aeb0ae6d691dd, not current main or this PR.
Do not treat that historical green as current-candidate evidence.

This final bookkeeping commit changes tracking records only. Original
critique/Review bytes and all non-tracking source are preserved. External
final exact-head identity/readback records bind the eventual publication head
without self-referential committed receipt hashes.

## Follow-Up Items

Owner/coordinator retains hosted CI, deployed health, full baseline parity,
post-merge rubric comparison and archive tag publication/release.

## Return-to-Caller State

Bounded task complete, PR #499 open. Automatic session remains running at
Follow-up, awaiting owner-selected action; no new child work starts.
Ranked follow-ups: owner archive tag publication (exact command above), retained
hosted checks and owner merge, then broader #199-#203 acceptance evidence.
No blockers within delivered scope; no human/hosted approval is inferred.
