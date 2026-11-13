---
title: Issue 440 post-1500 checkpoint research (0240)
description: Research for the smallest merged-main provenance checkpoint after PR 1500, Refs #440
ms.date: 2026-11-13
ms.topic: reference
---

## Status

Research executed once (disposition: executed). Planning Readiness: Ready. Scope is a new bounded recurring stabilization checkpoint after the PR 1500 feature wave. It is not a source repair, not a correction-pool renewal and not a reopening of the exhausted coordinator campaign. Draft, local-only, not approved. No source, test, runtime, SQL, browser, Docker, provider or Azure action was taken in this stage; only repository reads, `git fetch` and read-only `gh` queries ran.

## Pinned identities (read 2026-11-13)

| Item | Value |
| --- | --- |
| Worktree and branch | `issue-440-post1500-plan-0240`, `research/demo-post1500-checkpoint-0240` |
| Base and head at start | `ad1a1722965e7943166e5d0018089b8d2dcd0316`, tree `f650b1ba936c7cd65442a4613eb43e071fb825df`, clean |
| `origin/main` after read-only fetch | `ad1a1722965e7943166e5d0018089b8d2dcd0316` (no movement) |
| PR 1500 | MERGED 2026-11-13T02:38:22Z, merge commit above, head `4961acbeca952f9e3f60a1c09905d4b7f8acce34`, closing references empty, #83 OPEN, #440 OPEN |
| Merged tree equality | main tree `f650b1ba...` equals the independently assessed candidate tree (given) and the hosted merge-ref tree (read below) |
| Hosted merge ref | `f1a5ebccd271b600ec9fe6ed53ef19d79930130e`, parents `c401e5d56446...` and `4961acbeca95...`, tree `f650b1ba936c7cd65442a4613eb43e071fb825df` (GitHub git API, read-only) |

## Source categories kept separate

### A. Parent-source observations (earlier, not at merged main)

* Eight validation lanes for the integrated source at `288b6a376` (`src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`): types, forms 74, home 28, roles 21, synthetic 51, AI 28 (11 scripted scenarios), integrated regulatory 12, browsers 88, 89, 24, 47 and 21 states. They are applied by exact named input equivalence only. They are in the existing pack section "Partial independent UX release affected-integration checkpoint" (pack line 7725 onwards).
* Core 72: explicit HISTORICAL REUSE from d790 by equality of three inputs, SQLite and static only.
* Original final UX Review `0104`: execution Partial, outcome conformant within a bounded partial scope, five Low findings, immutable.

### B. Fresh final C4 checks (at `4961`, `ROOT` records)

* C4 changed one baseline test, the WCAG record, the log and tracking. Product JS, CSS, backend and core did not change.
* Author: failing-first 12 tests with one failure (`8 != 7`), baseline 13 OK, role guards 21 OK, 7 scratch mutations fail the new test (author evidence only), noncanonical tool versions and explicit-file format failure preserved.
* Independent assessor (read-only): baseline 13 OK, role guards 21 OK, production-UX protocol 4 OK. The assessor's explicit read manifest is narrower than the original phases; root separately consumed the five original C4 phase files and the author log, so critique Revise (CR-1, CR-2) and the original Review (Conformant at `6a3f7a9e1`, one Low) are known to have occurred.
* Root canonical: API Ruff 0.17.1 lint pass, format pass (152 files), mypy 2.4.0 pass (236 files), unchanged configured exemptions. The baseline test stays an existing format exclusion and mypy `ignore_errors` override, so no typing acceptance is inferred.
* Not run: browser checks, AT, core 72, whole API, full gate.

### C. Hosted observations (new, read-only this stage)

Source CI run `43351173623` (event `pull_request`, created 2026-11-13T02:18:06Z, conclusion success, head SHA `4961...`, checked out as merge ref `f1a5ebcc...` whose tree equals merged main). Nineteen reported contexts, all SUCCESS: Source projects CI (`src-changes`, `src-no-working-data`, `image-paths`, `src-namespace`, `mssql`, `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`), Capstone Rubric Scorer (`pre_activation`, `activation`, `rubric_prepare`, `agent`, `detection`, `record_rubric_score`, `safe_outputs`, `conclusion`) and `rubric/score`.

Job and step detail read from the run metadata and the hosted log (counts only, no log copied):

| Job | Observed | Qualification |
| --- | --- | --- |
| `src-core` | `unittest discover -s tests -v`: 3148 tests OK, skipped 403; lint and type check steps success | Includes the 72 core selectors that were HISTORICAL REUSE: `test_sqlqueues.SqlQueueMembership.test_non_boolean_funding_refreshes_stale_revision_two_memberships` printed `ok`; `test_live_doc_links` ran. SQLite and static only; SQL Server twin classes show `skipped 'needs a SQL Server'` here. Hosted pull-request-merge-ref observation, not a local executed result |
| `src-api` | `unittest discover -s tests -v`: 2966 tests OK, skipped 629; lint, type check, design-system browser harness check, synthetic design-system browser checks (3 tests), image build, container security contract and startup, vulnerability gate, SBOM: all success | The hosted run also confirms the C4 baseline test: `test_every_invalid_field_is_tied_to_a_message` and `test_saved_held_copy_field_is_tied_to_its_visible_message` `ok`. The five role, held-copy, programme, home and regulatory browser walks named in the pack are NOT shown by these steps; the generic harness is a different check |
| `src-agents` | 336 tests, success | Whole-suite hosted observation; includes the AI lane's test modules, not an actual model run |
| `mssql` | Selectors from `.github/workflows/src-ci.yml`: `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, `test_assistants.Mssql{Contract,Review,Durability,Api,Ledger}Tests`, `test_resident_aoai_sql.AccountingSqlTests` with `ZF_TEST_MSSQL=1` against a `mcr.microsoft.com/mssql/server:2022-latest` service: 321 tests, `OK (skipped=1)` | Non-verbose step: individual test outcomes, and which single test skipped, are NOT identifiable. The module `test_mssqlstore` contains the SQL Server twin (`MssqlQueueMembership`) of the funding-membership regression, so module-level coverage is plausible, but per-test execution of that twin is unproven. Image tag is mutable; no immutable image id is claimed. Core `test_sqlqueues`, `test_taskqueues`, `test_gates` are not in the selectors |

The earlier hosted API failure (run `43347366743`, job `131630021882`, `8 != 7`) stays preserved as a genuine failure, not reclassified as flaky. A `push` run of Capstone Rubric Scorer on the merge commit was `in_progress` when read. No Source CI push-event run was listed for the merge commit; absence is not success.

### D. Actual merged-main provenance

* `git diff c401e5d56..ad1a17229` outside `.copilot-tracking` is 32 files, 1646 insertions: product `role-screens.js` (+91), API and core tests, four core source files, runbook, READMEs, synthetic-data README, profile review, WCAG record, log and the pack. The `src` tree equals the candidate plus nothing else (merge commit tree equals candidate tree).
* BRD, PRD and ADR blobs at main equal the blobs recorded in the existing pack section (`34d88395de86`, `c788b917bafa`, `f7f9b7675e60`, ADR 0001 `d42fa5c4615f`, 0002 `cbe21530043f`, 0003 `d60645397b20`, 0004 `9406c2e747ce`, 0005 `4d610335a5a1`, 0006 `956da1a3b804`, 0007 `541e0f72dd2c`). Document status is therefore unchanged: BRD draft, PRD in-review, ADR 0001, 0002 and 0007 Proposed (0002 with the bounded owner-accepted identity decision), ADR 0003 to 0006 Accepted with their stated scope. No requirement or ADR is approved by this wave.

## Gaps against the existing pack (reconciliation targets)

* G1. The existing 149 section is pre-C4 and pre-merge. It says no pull request exists, hosted CI is unobserved, `test_live_doc_links` was not run, and the head is `288b6a376` or `37e2715b5`. These statements were true when written and must stay; a later annex reconciles them, as the section already did for the original Review.
* G2. No pack text records the C4 correction, the hosted `8 != 7` failure, the nineteen SUCCESS contexts, the merge or the merged-tree equality.
* G3. Core 72 and "actual SQL Server" qualifiers in the pack can now be partly superseded by hosted observation: the 72 selectors are hosted-observed on the merged tree (SQLite and static), and a hosted SQL Server module run exists. Both need the qualifications above.
* G4. The pack's wave-level requirement trace (rows for 82, 74, 176, 215, 216, 96, C3, 156, 134, 1498) is unchanged by C4 because product source did not change; only the WCAG baseline row changes by one tied-field audit.

## Is a genuinely missing focused observation necessary?

No. Evidence:

* The only changed inputs after the eight lanes were the baseline test, WCAG record and log; those have fresh covering results (13, 21, 4) and hosted `ok` lines on the merged tree.
* Product bytes are unchanged versus the lane inputs, so lanes whose own named inputs are unchanged remain input-equivalent (the types lane does not: C4 changed an API test that Ruff lint covers, so final API static status rests on the fresh canonical C4 check); rerunning lanes would only produce counts, which the owner brief excludes.
* Attribution: the verified merge-ref checkout (tree equal to main) is Source CI evidence; Scorer and status contexts are PR rollup successes only, and the scorer run `43351173644` is a pull_request run whose checkout is unverified here. The post-merge push scorer run was in progress when read.
* The remaining unknown, per-test SQL Server outcome of `MssqlQueueMembership` and the single skip, cannot be resolved from the existing hosted step (non-verbose) without a hosted workflow change or a local Docker SQL Server run. A local SQL Server container is a full-tier or SQL-sensitive action under the repository validation policy, would repeat an unchanged-input selector, and the funding-membership regression is already covered by the SQLite twin and by the module-level hosted pass. It is recorded as an unproven limit, not a gap that blocks the checkpoint.
* The post-annex check is the one focused local check the change itself touches: `test_live_doc_links` reads the pack. It is an implementation-stage direct check, not a fresh-count claim about the wave.

Conditional, not recommended unless the owner or root later requires per-test SQL attribution: from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests ZF_TEST_MSSQL=1 python3 -m unittest -v test_mssqlstore.MssqlQueueMembership`, preconditions: separate root admission of a local-only disposable SQL Server container with immutable image id recorded, no Azure or provider credentials, exact merged tree `f650b1ba...`, clean worktree, constructed marker data, evidence kept external. Expected result unknown; skips must be reported, not hidden.

## Failure, manual and approval boundaries (unchanged, restated)

* All data constructed or synthetic. No resident consent, named human approval, Finance numeric-fidelity decision, legal review, live check, assistive-technology result or WCAG conformance is established.
* The saved Held copy path is a human-assisted comparison; unavailable-AI and unavailable-service paths remain manual. The AI harness is scripted offline.
* Original final UX Review stays Partial. C4 independent assessment is a bounded publication Pass, not a whole-product verdict.

## Backlog and holds (read from the brief, not re-derived)

* Entire 233 excluded (5 corrections spent, typing extension NO approval). Scoped 96 C4 of 5 spent, one remaining, no C5, older whole-96 history unknown.
* 203 retained candidate `2543` is locally held: positive correction authority unproved, owner extra-metadata cycle NO APPROVAL, and 1500 changed pack, log and tracking inventory inputs. This task does not regenerate or edit it.
* 184 minute/cohort candidate held (two formatter failures, extra formatting-only permission unavailable). Not repaired here.
* Allowances for 135, 132, 184, 144 and 146 are not borrowed.
* Issue 440 final two acceptance criteria stay unticked (verified: the triage criterion and the PR artifact criterion are `[ ]` in the issue body read 2026-11-13).

## Recommendation (proposed, not a decision)

CONTINUE, bounded, with a docs-only provenance annex in the existing pack. No fix, no new observation, no pivot. Affected closures held: #149 whole, A2 cut line, epic, #96 whole, #233, and criteria 2, 3 and 5 of #153 where unproven. Dependent gates: independent exact-head review and human approvals; hosted CI on the annex PR (path-filtering may skip Source CI for docs-only changes, which is not success); owner merge decision. Independent lanes: #203 and #184 holds, scoped 96 remaining allowance and #233 are untouched by the annex.

## Evidence read manifest

* Repository: `docs/reference/README.md` (index, scoped), `docs/reference/memory.md`, `docs/architecture/cutover-evidence-pack.md` lines 7725 to the 149 section end (partial, the Partial independent UX release checkpoint and final evidence assembly), BRD/PRD/ADR blob ids via `git rev-parse`, `.github/workflows/src-ci.yml` (`mssql` job and unit-test steps), `src/core/tests/test_sqlqueues.py` and `src/api/tests/test_mssqlstore.py` selectors, issue 440 body criteria. `docs/case_study_48_original.md` and the addendum are unchanged by this wave and were not re-read in full (this is a bounded evidence checkpoint; the 2026-11-13 wave touched neither).
* ROOT: `rpi-149-finalize-evidence-0131-result.json`, `rpi-149-independent-final-head-result.json`, `rpi-96-c4-ci-baseline-0208-result.json`, `rpi-96-c4-independent-result.json`, `96-c4-root-publication-assessment.json`, `pr1500-body-with-c4.md`, `demo-run-ledger.md` section "Actual hosted failure and scoped correction refill" and "C4 completion, independent assessment and one assessed publication".
* GitHub read-only: PR 1500 state and rollup, Source CI run `43351173623` jobs, steps and test-count lines, merge-ref commit tree, issue 83 and 440 state.
* Not read: `ROOT/rpi-149-final-ai-0104.log`, any private dataset, environment or credential output; raw native logs not copied.
* Limits: original C4 phase files were not opened here (the ROOT results summarise them); the ledger was read only for the two named sections.
