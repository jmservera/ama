<!-- markdownlint-disable-file -->
# RPI Phase Details: Retire legacy MVP directories

## Metadata

* Task ID: issue-201
* Task slug: mvp-cutover-201
* Plan: .copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md
* Research: .copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Preserve and retire | Complete | P01-T01, P01-T02 |
| P02 | Validate | Complete | P02-T01 |
| P03 | Review and publish | Review Complete / Conformant; publication pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Preserve and retire

Context: executable migration already present at main65a514ed; only pointer
remains. Owner sign-off 2026-10-27 is new prospective authority, not a rewrite
of the old evidence pack or automatic proof of its remaining acceptance.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Archive then delete

Verify BRD version0.21.0 at cut-over, absent local tag, expected archive commit
65a514ed20e97816dbf47e9fb981ab4cfe40597d containing mvp/README.md.
Use annotated v0.21.0 only if absent, never force/move; conflicting tag blocks.
Before tag creation derive the privacy-safe identity from fresh gh api user
id/login fields, repository-local configuration, with author/committer/tagger
overrides removed so a different inherited identity cannot replace it.
Tag records current main tree, not legacy executable contents that predate M6.
Git history retains those modules. Record exact owner command
git push origin refs/tags/v0.21.0:refs/tags/v0.21.0, but never execute it.
Delete only named pointer and its empty directory. Do not inspect datasets.
Completion: tag object/target readback and empty git/path queries.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Live source guidance and durable record

Likely targets: README.md, .github/copilot-instructions.md, src/README.md,
src/core/README.md, .github/rubric/README.md, docs/capstone/README.md,
docs/prds/zava-forward-retrofit-programme-demonstrator.md,
docs/architecture/mvp-to-src-parity-matrix.md,
docs/architecture/cutover-evidence-pack.md, docs/architecture/README.md,
docs/adrs/0006-src-layout-and-cutover.md, docs/reference/README.md,
docs/reference/log.md and the live source path in
docs/reference/research/ux/regulatory-literacy-for-journeys.md.
No workflow/runtime/test edits.
The final public-reference sweep also identified the same stale retirement
status in .github/agents/ama-backlog-delivery-coordinator.agent.md.
Update only that factual source-layout note; preserve workflow decisions,
frontmatter/capability surfaces and all other instructions.

Fix current PRD location only, without modifying requirements/version or
historical dated baselines. Preserve all dated snapshots/ADRs and pinned URLs.
Add explicit classification: historical source paths, negative test/guard
strings and legacy workflow identities are intentional; no live build input.
Guard references to mvp/data remain, since refusing accidental committed data
is safe after retirement. Do not regenerate old audit TSVs merely for token
count. Clarify old evidence pack unsigned statement applies to original date,
then append current owner sign-off/archive and bounded verification section.

The append-only log repair map routes old README anchors to src/api/README.md
for entra-id-on-container-apps, honest-limits and five-retrofit-assistants
implementation (now in src/agents/README.md); inspect actual target anchors.
Never edit earlier entries.
Archive linkage supplements rather than falsifies historical paths.
Completion: readable source guidance, current mutable local links, exact log
prefix, no changes to memory/original case study/workflows.

<!-- rpi:phase id=P02 -->
## P02: Validate bounded retirement

<!-- rpi:task id=P02-T01 -->
### P02-T01: Existing tests and semantic assertions

Run from src/api:
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q.
From root: python3 tools/rename-zava-tests.py.
Additional narrow selectors: src/core test_cutover_audit and src/agents
test_eval_registry. Missing distributions/dependencies justify isolated venv
pip setup, not uv, no source path import workaround.

Preserve full output externally; record test totals/skips/reasons truthfully.
All tests use env -i with only PATH, safe locale, and newly owned external
HOME/TMPDIR/TMP/TEMP/XDG_CACHE_HOME/ZF_DATA under this session's files/cutover
scratch root. Set these before Python starts. Never inherit ZF_TEST_*,
ZF_SQL_*, Azure credentials, connection strings or private data locations.
Keep fixture-only PYTHONPATH explicitly on the API command. The exact
scratch root and sanitized commands are recorded in changes; no values from
the original application/credential environment are read or printed.
Use a task-owned external virtual environment if package imports fail.
External scratch is permitted by repository policy; the critique's claimed
system-temp prohibition is not an applicable requirement. Keep bounded
evidence logs, and remove only exactly owned disposable files if needed.
API general discovery does not prove opted-in SQL/Azure/browser contracts.
Use parity function via existing unit tests, not stale report --write.
Verify filesystem absence, no tracked paths, same workflow blobs as base,
log original prefix and changed-document relative links. Review any baseline
broken links separately rather than fix unrelated debt.
No --all. No optional --changed unless it adds necessary scoped evidence.

<!-- rpi:phase id=P03 -->
## P03: Review and publish

<!-- rpi:task id=P03-T01 -->
### P03-T01: Original independent Review

Activate rpi-review once, assess implemented source plus canonical research,
plan, details, critique, changes and recorded validation. Independent worker
writes only its review artifact. Source correctness and acceptance boundaries
matter more than unchanged historical token count.
Preserve Complete/Partial/Blocked and Accepted/Not accepted truthfully.
Route findings to later work; no second Review or in-task closure repair.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Commit and PR

Authenticate gh user, derive repository-local email
{id}+{login}@users.noreply.github.com from fresh returned fields.
Use privacy-safe author/committer, Conventional Commit and mandatory
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
Explicit branch ref only with --no-follow-tags. PR includes sign-off date,
main/archive SHA, local-only tag/owner push command, findings/validation and
per-issue remaining criteria. All five use Refs unconditionally in this PR;
no deployment/run/approval invented.
Do not merge or modify branch protection. Hosted checks are retained, not
replaced by scoped testing.
