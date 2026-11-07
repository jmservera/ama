<!-- markdownlint-disable-file -->
# Research: parent topic integration preparation (#123, Refs #440 #128), 2026-11-05

Task slug `parent-integration-preparation-123`. Research disposition: executed (bounded git identity, scope and coupling inspection before any write other than this record). Planning Readiness: Ready.

## Scope and provenance

* Worktree `/home/azureuser/source/ama-wt/integration-123`, local branch `feat/discovery-assurance-integration-123` at HEAD `3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246`, clean (empty `git status --short` and empty ignored-inclusive status). The local ref is an old placeholder created from old main; it is not the remote integration head and is not discarded or reset.
* Fresh fetch on 2026-11-05 (read only): `origin/main` `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (tree `5c2988b71aec609b007b41f408685d54e2c28e0d`); `origin/feat/discovery-assurance-integration-123` `63dd5798ee474ea3137018749b604c1f78774801` (tree `73c8eda8f49891aea173623f79e1fd8f95c7ec1b`). Both match the coordinator's expected identities. No parent PR exists (open PRs: #1216, #1205, #1203, #1141, none from the parent topic).
* Merge base of local topic and remote parent is `3d7ad2fe` (the local ref is a strict ancestor of the remote parent). The remote parent is four commits ahead of that base and of main: #1211 `e546bf23e`, #1212 `ad1ee0264`, #1213 `23cdae38b`, #1221 `63dd5798e`. Local topic is five commits behind main in the main-only direction.
* Authenticated identity: `gh api user` gives id 8036360, login `jmservera`; repository-local `user.email` is already `8036360+jmservera@users.noreply.github.com`.
* Not touched: the primary checkout `/home/azureuser/source/ama` (dirty), the retained child #440 worktree, issue #144 heavy gate runner and its output, all other worktrees, caches and receipts. No push, PR, merge into main or issue mutation.

## Findings

* Remote-parent surface relative to the merge base is 39 files, 1711 additions, 2 deletions. It is not documentation only: it includes the constructed diagnostic `src/core/src/zava_forward/core/paired_equity.py` (67 line diff, blob `5aedcd7b`), 70 regression lines in `src/core/tests/test_paired_equity.py` (blob `f9b07cb6`), a `src/core/README.md` paragraph (blob `bb709453`), the original #128 RPI set and published functional assessment JSON, four #440 checkpoint families, the evidence pack (+518 lines), the KB index (+15) and the log (+20).
* Main relative to the merge base is 38 files (1357 additions, 12 deletions): gate tooling (`tools/rpi-checks.py`, `tools/test_rpi_checks.py`), `src/README.md`, an API `style.css` line, rubric score, log entries and RPI records for #1208, #1214, #1215. Main did not change `src/core`, the BRD, PRD, ADRs, the evidence pack or the KB index.
* Overlap of changed paths between the remote parent and main: only `docs/reference/log.md` (both append). Expected conflict is therefore append-only: both sides' entries must be kept in chronological order with their qualifications. (Correction after critique: `git merge-tree` reports this file auto-merges; any actual conflict still follows the retain-both rule.) No source conflict is expected.
* Main still holds the unfixed `paired_equity.py` blob `d29768d5` and `test_paired_equity.py` blob `432aef3e`; the parent holds the fix. Main did not change any module the diagnostic imports (`journey_register`, `ranking`, `rai_release`); the merge therefore brings the fix to main-bearing lineage without a coupling change.
* Document identities identical on main and parent: BRD-2026-AMA48-001 draft 0.21.0 (`34d88395`), PRD-2026-AMA48-001 in-review 0.21.0 (`c788b917`), ADR 0002 Proposed (`cbe21530`), ADR 0003 Accepted with amendment (`d6064539`).
* Original #128 plan (`issue-128-paired-cohort-comparability-plan.md`) declared tier FOCUSED: pure constructed diagnostic; no SQL, security, infrastructure or deployment change. The paired diagnostic imports only `journey_register`, `ranking` and `rai_release.digest` and keeps `fairness_evidence=False` and `activation_allowed=False`.
* Tier confirmation (prospective): FOCUSED holds only if the final fresh-main-relative scope stays this bounded metric tooling, test and documentation set plus main's already-merged gate-tooling changes, which arrive unchanged from main. No new runtime behaviour, SQL, security, infrastructure, deployment or finance feature is added by this preparation. Checkpoint prose that mentions those topics does not implement them. The recomputed final scope and tier are re-stated in the changes record; any mixed expansion stops for reclassification to FULL and new coordinator admission.
* No defect is confirmed by this research. Candidate observations (reviewer's optional seeded-defect-on-rejected-pair regression, strict `type(a) is type(b)`, no `paired_equity` to `cohort_eval` seam) remain unreproduced observations, not defects.

## Constraints

* LIGHT ONLY: no `tools/rpi-checks.py --all` or `--changed`, browser, SQL, Docker, scanner, cloud, broad test breadth or heavy lock. Smallest paired-equity unit tests and bounded static or document checks only, with explicit current-source imports, external caches and `PYTHONDONTWRITEBYTECODE=1`. The independent light tool environment `/tmp/ama-96-venv` may be reused read-only.
* Complete planned parent validation is PENDING coordinator admission and is not performed here. Child receipts and observations are historical context, not fresh parent results.
* No reset, rebase, force operation, main push or main merge. Append-only conflicts retain both sides; ambiguous intent stops the task.
* #123 whole-epic AC1 and AC2 stay unchecked and unproven; #440 criteria 7 and 8, company-owner and data prerequisites, actual-model, threshold and lawful-field approvals, resident and accessibility research and authorized Azure-only residuals stay outstanding. Use `Refs` only.

## Planning Readiness

Ready. Merge the fresh remote parent into the local topic, then the recorded fresh main; resolve only append-only log conflicts retaining both sides; append one dated integrated checkpoint to the evidence pack, one index link and one log entry; run the light observation; record changes and a single review.
