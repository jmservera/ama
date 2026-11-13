---
title: Issue 149 UX parent integration plan, policy amendment A1 (2347)
description: Prospective PLAN-ONLY amendment correcting the validation tier and merge-authority wording, recording the input cut line, wave A and B admission, valid dependencies and the pending amended critique; no assembly, source, pack or publication
ms.date: 2026-11-13
---

## Status and honesty record

PLAN ONLY. No assembly, source, cutover pack, ref, PR, issue, tick or publication is changed by this amendment. The original plan, details, research, critique, state history and the 2333 result (which said FULL) are preserved unedited except for a pointer notice. This amendment supersedes only the items listed in the next section and states why. It does not accept any input as integrated.

## What the original 2333 plan got wrong

* It classified the whole assembly as the FULL tier "because of SQL queue membership revision, funding gate, mssql selected" and required `rpi-checks.py --all` plus an external receipt. The actual current owner policy (delivery schedule 13, recorded in the demo run ledger and the session `delivery_policy` concurrency rule; candidate text `delivery-schedule-session-cap-2220.txt`) says: prioritise existing PRs through focused impacted checks, original RPI evidence, independent exact-head review and guarded merge; implementation needs focused impacted checks; documentation-only work has no executable gate; "Do not default to full gates; preserve any applicable required gate". There is no blanket FULL default.
* It treated a Python constant bump as an SQL schema modification. `MEMBERSHIP_REVISION` (3) is a Python constant in `taskqueues.py`; `sqlstore.py:764` only passes it as a parameter when deciding whether cached queue memberships are stale. The 1490c diff (`8f8be74e1..ff40e50c8`) touches no `sqlstore.py`, DDL, schema or migration, and the independent 1490 assessment (2337) records no workflow, manifest, Dockerfile, SQL schema or gate-tool change. A funding reader that stays strict is a tightening, not a permission, secret, deployment or gate-semantics change.
* It described the merge as needing "the owner chooses the merge method" and "leave the merge to the owner", reading as a fresh owner permission. Merges into the parent and parent to main are coordinator-owned guarded actions under the existing standing delivery process. No fresh owner permission is a precondition of this plan and none is inferred or requested by it; equally nothing here grants authority. Superseded: plan G2 "merge methods" wording, Phase 8 "leave the merge to the owner", Topology "owner chooses its merge method".

## Corrected validation tier (supersedes plan "Validation tier", Phases 7 and 8 gate text, details Section 7, G4 SQL Server blocker)

Classification: FOCUSED modified and impacted checks. Basis: owner schedule 13 and the demo ledger focused-demo policy; no input at the recorded pins changes permissions, pinned actions or images, packages, secrets, deployment, SQL schema, a workflow, a gate tool, gate semantics or infrastructure (verified for 1490c above; every other input is re-verified from `git diff --name-only` at G3). The repository two-tier text (D4, issue 1294) is applied by actual impact, and its doubt clause is resolved here by the explicit owner policy, not by size.

* No default `rpi-checks.py --all`, no external full receipt, no `--verify-receipt` as a plan requirement. `rpi-checks.py --changed` is optional and never replaces a planned check.
* Required local direct checks (publication gates), each run from isolated pip-only venvs outside the repository, only the documented test-helper `PYTHONPATH` directories, no uv, pinned ruff 0.17.1 and mypy 2.4.0, pinned axe 4.10.3 hash recorded, heavy lock, results stored externally with the candidate SHA:

| Input | Impacted checks |
| --- | --- |
| 1490c | core `test_gates`, `test_home_case`, `test_chat_case_answers`, `test_sqlqueues`, `test_taskqueues` (SQLite regression `test_non_boolean_funding_refreshes_stale_revision_two_memberships` must RUN, not skip); API `test_home_case_api`, `test_mvp`; strict-reader and `MEMBERSHIP_REVISION = 3` invariants |
| 74 | the two over-HTTP cost tests; `home_case_browser_check` (24 PASS) because `home_case.py` changed |
| 176 | the two runbook five-home tests |
| 134 | docs only: namespace and static docs checks, link and diff review; no executable gate |
| 215 | `regulatory_ux_check` (21 states), regulatory and `chat.js` modules, `node --check` |
| 233 | its two unit tests, `programme_paging_browser_check`, `role_screens_browser_check 230` |
| 96 backend | the 16 Held-download methods, `test_form_export`, `test_role_endpoint_inventory` |
| 96 UI | defined by its own amended plan; its Held-download browser check |
| 156 docs | docs only: link and diff review, append-only log, one README row |

* Static: ruff, mypy, `node --check`, `git diff --check`, docs link review.
* SQL evidence is separated, not assumed. SQL Server tests that the above selectors gate on a docker/SQL Server prerequisite are run only if that prerequisite is actually present at assembly time (probe, no cloud fallback, no skip token); otherwise they are recorded as UNOBSERVED and the local publication claim says so. The SQLite regression covers the membership-revision logic locally. Real SQL Server acceptance of the 82 acceptance criteria is LATER LIVE ACCEPTANCE under issue 82, not a precondition of local publication, and is never claimed by this assembly.
* Escalation to stricter evidence for a specific input, with its stated reason, only when an actual change at G3 includes SQL DDL, schema or migration, a workflow, dependency manifest, Dockerfile, gate tool, permission, pinned action or image, secret, deployment or infrastructure file, a change to an existing authorisation, CSRF or consent control, or when impact is unresolved. Then the strictest applicable tier applies to that mixed change. Not triggered at the recorded pins.
* Open classification judgement for the amended critique: 96 backend adds a new access-controlled Held-copy GET route (default off, guard conditions, no body without all guards, 16 tests including unauthorised and revoked). It is a new route, not a change to an existing control, and is classified focused under the owner policy; the critique must challenge that explicitly and the coordinator records the answer.
* Hosted CI is read separately for the assembly PR head and the parent to main PR head; absent, skipped or path-filtered is not success; local-only coverage (browser checks) stays a direct local check. Current exact-head independent assessment by the coordinator, independent final Review (Phase 6), human exact-head review, consent, Finance, assistive-technology and legal approvals remain required and unrecorded. Passing local checks satisfy none of them.

## Corrected Phase 7 and 8 (supersedes the original text of those phases)

* Phase 7: commit dated assembly RPI evidence; run the focused checks above on the committed, clean candidate; coordinator exact-head independent assessment; publish the assembly PR; read hosted CI.
* Phase 8: after the assembly lands, the delivered candidate is the actual post-merge parent tip. Fast-forward of the parent to the assessed tip is preferred so the assessed head identity is kept. If the tip differs (merge commit, or main moved), record the tree-identity comparison, merge the fetched main, rerun only the impacted checks the delta touches, and have the coordinator assess that exact tip before the single parent to main PR; read hosted CI for that head. The guarded merge is a coordinator-owned action requiring all-green actual checks, MERGEABLE status, the exact-head assessment and any human review gate, and is not described as fresh owner permission.

## Input cut line and wave admission (G2 stays the coordinator or root decision)

Pins re-read now (read-only): main is `774a91e5f` (a rubric-score bot commit on the planned `8e6e55457`, changing only `.github/rubric/scores/latest.json`); parent is still `8f8be74e1`, so 1490c is NOT merged and G1 is open.

| Input | Pin | Admission state |
| --- | --- | --- |
| 1490c | `ff40e50c8` / tree `2e0bd9706` | Wave A prerequisite. Independent bounded Pass (2337). Needs G1 merge into the parent and hosted CI success. |
| 74 | `467a0cf5d` | Wave A, as recorded in research. |
| 176 | `da436be3e` | Wave A, as recorded in research. |
| 134 | `cc7e3c3a9` | Wave A. Only known conflict (union rule). Stays partial and deferred. |
| 215 | `6eacb4953` / tree `45fd37b` | Wave B. Independent Pass exists (2323), bounded to Refresh-alerts focus recovery; coordinator admission still recorded at G6. Assistive-technology and staff comprehension unproven. |
| 233 | `aebd381d9` / tree `377e0329` | Wave B. Independent CONFORMANT (2333) for the navigation slice; the tool 1.64.1 is qualified; admission waits for the canonical browser replay outcome, now underway and not yet recorded. |
| 96 backend | `94760af7d` / tree `46eb72d5` | Wave B. Coordinator independent Pass, M1 closed; prior Revise on `7f3386ddd` preserved. |
| 96 UI | unfrozen | Wave B, REAL dependency. Needs repin to the exact backend interface, an amended independent critique, implementation and independent acceptance. R-UI-1 was decided by the root in `96-independent-m1-closure-2332.json`: root backend contract; raw JSON text panel-local transport is authorised to keep numeric literals; the shared api helper is not broadened. That decision is NOT human Finance approval and authorises no publication. |
| 233 page-context | none | Separate optional slice, not accepted. NOT added silently; it needs its own acceptance and a coordinator decision. |
| 156 docs | `d8fe60017407f3f7df4b339dfa0bfaff06dfacbd` / tree `856766483` | Optional later DOCS input only, never a prerequisite. Independently accepted and directly reviewed by the root as a complete three-doc diff (`zava-forward-prototype-profile-review.md`, `docs/reference/README.md` index row, `docs/reference/log.md` append). Preserves dated snapshots and trace limits. Not a standalone main PR. No historical or criterion upgrade: 189 criterion 3 stays unticked, 187 stays unreconciled, no five-home claim. |

Read-only merge-tree at these pins: 156 against main `774a91e5f` is clean (tree `32f8ca7bf`); 156 against 233 is clean; 156 against 134 hits only the known 134-versus-main union files (`cutover-evidence-pack.md`, `docs/reference/README.md`), so the union rule applies and the README index row from 156 must survive once. Re-run at G3.

Admission rule (keeps critique PC-01): the single assembly proceeds only with a coordinator-declared cut line. Default is all of wave A plus the wave B members that individually reach G6; a reduced assembly is allowed only as an explicit recorded scope change with the remainder named for a later assembly. 96 UI never silently drops out. 156 docs may join only after a coordinator decision and only as docs input. Nothing is added after Phase 6.

## Valid dependencies

* G1: 1490c merged into the parent with SHA and hosted CI success. Assembly cannot start earlier.
* 96 UI depends on 96 backend (`94760af7d`), which depends on main `form_export` (#98); R-UI-1 is a contract decision, not an approval.
* 233 admission depends on the canonical browser replay result.
* 156 docs and 134 share `docs/reference/README.md` and `log.md` (union, append-only).
* 74 and 1490c share `test_home_case_api.py` (keep all six methods verbatim).
* Plan-ready: YES for the wave A skeleton and the contingent wave B steps. Implementation BLOCKED until G1 and G2, then G3 to G5; G6 per wave B member.

## Pending independent critique (not run here)

The amendment changes a decision (tier and merge-authority wording) and the cut line. A genuine independent read-only critique of the amended plan MUST execute once, before any assembly begins, with its verdict and dispositions recorded. It has not been run and no verdict is claimed. It must cover: the focused classification and the 96 route judgement, SQL evidence separation, merge-authority wording, cut line and PC-01, the 233 page-context and 156 docs boundaries, and the 96 UI dependency. The original adverse critique (Revise, PC-01 to PC-05) stays preserved and is not repeated.

## Budget and approvals

Unchanged: no new correction pool and no invented source budget; the spent history in the research file carries. No approval is invented. Refs, never closing keywords, for every PR.

## Amendment A1 correction notes (2353, after the independent critique)

The A1 text above is preserved unedited. These notes supersede it where they differ. PLAN ONLY; no assembly, source, pack or publication.

* 96 interface (supersedes "new default-off Held-copy GET route" and "new route, not a change to an existing control"). Read from `94760af7d` `server.py` and the frozen UI `423517a71`: the Held download GET `.../form-review/{draft}/held-export` and the additive `held_download_enabled` flag in the form-review GET view already exist on main `774a91e5f`. The 96 backend adds only the read-only POST `/api/cases/{case}/form-review/{draft}/held-export/freshness`: raw JSON body, `draft_id` must match, field ids must be text, `Cache-Control: private, no-store`, nothing written, both routes default off (`ZF_FORM_HELD_DOWNLOAD=synthetic-demo-only`, `ZF_DEPLOYMENT_PROFILE=demo`, never trusted-proxy), existing form routing and role projection `post` allowance reused. The UI sends the panel-local raw JSON text with `X-ZF-CSRF: 1`. No existing authorisation, CSRF or consent control is changed in the inspected inputs. Focused classification is kept on that corrected basis and re-checked from the actual diff at G3. The raw-text transport is a root contract decision (R-UI-1), not Finance approval.
* Escalation scope (supersedes the DDL-only reading). `MEMBERSHIP_REVISION = 3` changes when persisted SQL queue memberships are refreshed (`sqlstore.py:761`). The owner-focused classification stands, but actual SQL-affecting behaviour is assessed at G3, and a change to persisted SQL behaviour beyond the recorded 1490c diff escalates. Hosted `mssql` and the local SQL Server probe stay separate from human acceptance and from live SQL acceptance of 82.
* 96 UI checks (adds to the table). When admitted: `test_finance_grants_screens.py` (changed enabled and disabled control assertions), `held_form_download_browser_check`, the 16 backend Held-download methods, `test_form_export`, `test_role_endpoint_inventory`. UI is frozen at `423517a71` (parent of its review commit chain on `94760af7d`); independent assessment and execution are pending, so it is not admitted.
* Cut line (supersedes "wave B members that individually reach G6"). Every intended wave B member (215, 233, 96 backend, 96 UI) must be admitted, or named in a recorded coordinator deferral that states the remainder for a later assembly. No silent omission.
* Admission facts. 233: canonical Playwright 1.64.0 replay passed `programme_paging_browser_check` 99 and `role_screens_browser_check 230` 70; the queued heavy-lock deviation is retained and is not a compliant-admission claim; coordinator admission is still pending. 1490: PR open at `ff40e50c8`, hosted CI partly in progress, not merged, so G1 holds. 233 page-context stays not accepted. 156 docs stays optional later docs input; bounded Pass only, no 233 page context.

## Amendment A2 final-input plan (2026-11-13, root-accepted final inputs)

PLAN ONLY. A1 and its correction notes above are preserved unedited; A2 supersedes them only where stated. No assembly, source, cutover pack, ref, PR, issue, tick, approval or publication is changed. G1 holds, so DO NOT ASSEMBLE. The root approves preparing the revised cut line and phase checks now; that is not a bypass of any gate and is not coordinator admission of any member.

### Final inputs accepted by the root (supersede the 233 and 96 UI rows of the A1 table)

| Input | Final pin | Acceptance evidence (all external, read-only, qualified native RPI) |
| --- | --- | --- |
| 96 combined (backend plus UI) | `423517a71f2acb41baaa292cff08d3be7d32d995` / tree `0a28fe0e88302a756266538a043cbd52d95ca03e` | Fresh independent source/RPI Pass `96-ui-independent-2353` (bounded, no blocking or material defect; Low follow-ups: leading BOM wording, silent duplicate pending press, panel-local progress sentence). Separate canonical reproduction `96-ui-validation-2353`: Held-download API 16, form staging API 14, role endpoint inventory 24, finance screens 20, design system 8, content standard 19, browser check 88 PASS with pinned axe 4.10.3 (hash `880970c0...a68bb`), Playwright 1.64.0, non-queued heavy-lock admission. Reproduces the recorded 2333 results exactly. |
| 233 final (navigation plus queue page context) | `837da4fde4af955769f42b5e5fce4608a1ce8845` / tree `b12301ec54a81267998f55e20f0622a192084dae` | Fresh independent `rpi-233-page-independent-2358`: CONFORMANT for the bounded local boundary (IA-003), no Blocker, Major or Minor. 42 units across `test_programme_screen`, `test_role_screens_conformance`, `test_role_screens`; `programme_paging_browser_check` 107 PASS, 0 FAIL/SKIP, Playwright 1.64.0 manifest pin, pip only, non-queued `flock -n`. Fifth and final correction exhausted; no fresh pool. |

Facts verified read-only now: `94760af7d` is an ancestor of `423517a71` (six commits, no server or core change; the 96 UI diff touches only `role-screens.js`, `held_form_download_browser_check.py`, `test_finance_grants_screens.py`, `src/api/README.md` and RPI records); `aebd381d9` is an ancestor of `837da4fde` (diff touches only `role-screens.js`, `test_programme_screen.py`, `programme_paging_browser_check.py`, `atlas-screen-trace.md`, `log.md` and RPI records). Neither head changes a workflow, manifest, Dockerfile, infra, SQL, migration or gate tool. The 423 head CONTAINS the 947 backend: the assembly merges `423517a71` once and NEVER merges `94760af7d` separately (no double merge).

Disclosures kept, not rewritten:

* The original 96 UI missing green unit log stays disclosed; it is closed by the new independent execution (`96-ui-validation-2353`), not by editing the old record.
* The 233 `aebd381d9` replay's queued heavy-lock deviation stays recorded; for the final head it is superseded by the non-queued 2358 execution. The earlier 99 and 70 results belong to `aebd381d9` and are not carried as results for `837da4fde`.
* 233 `837da4fde` NOT done and not claimed: axe on page 2, 320 px scoped view (IA-002), assistive technology or WCAG acceptance, hosted CI, the role-screens 47-story run. The independent run reproduced the paging check only; `role_screens_browser_check 230` was not re-executed on the final head and must run at assembly. Carried Low RV-001: page-size literal duplicated.
* 233 page-context is now INCLUDED as part of the 233 final pin (supersedes "233 page-context not added"). Coordinator admission of 233 and 96 is still pending; root acceptance of the final inputs is not G2.

### Other pins (unchanged or deliberately not moved)

| Input | Pin | State |
| --- | --- | --- |
| 1490c | `ff40e50c884b6ac85cecb99a71755e713b2be7d8` | PR 1490 still OPEN, MERGEABLE; checks read now: `mssql`, `src-core` and eight others SUCCESS, `src-api` IN_PROGRESS. Not merged; G1 holds. |
| 74 | `467a0cf5d` | original accepted head, unchanged |
| 176 | `da436be3e` | original accepted head, unchanged |
| 134 | `cc7e3c3a9` | original accepted head, unchanged. A main-alignment candidate (`81c8bfae1c064f247fbb1472e9cda44bed53c8d4`, merge of main `774a91e5f`, task `rpi-134-main-alignment-2358`, own critique Revise applied and own Review Clean, asserted by that task) exists but is NOT auto-accepted and not an input. If the coordinator later accepts it after independent exact-head assessment, it replaces `cc7e3c3a9` as a recorded plan amendment and the M3 union resolution is already done inside it; read-only merge-tree of it against main is clean. Until then the union rule below applies. |
| 215 | `6eacb4953` | original accepted head, unchanged |
| 156 docs | `d8fe60017407f3f7df4b339dfa0bfaff06dfacbd` | optional, bounded accepted, later docs input only; no 233 page context claimed |
| 203 refresh | none recorded here | pending, EXCLUDED until independently accepted; no pin is invented; if accepted it is a new input needing its own plan amendment and critique scope |

### Rebinding to current main (rubric delta only)

`origin/main` is `774a91e5f09fa9db4f537494424efbd99be81826` (`chore(rubric): record score 79/100`), unchanged since A1. Against the originally planned `8e6e55457` the only difference is `.github/rubric/scores/latest.json`, a rubric-score bot file. No content, test, workflow or gate change; no plan binding other than the main SHA moves. G3 still re-fetches main and re-runs the matrix at assembly time.

Read-only `git merge-tree --write-tree` at these pins (no ref, worktree or index written):

* Against main `774a91e5f`: clean for `423517a71`, `837da4fde`, `467a0cf5d`, `da436be3e`, `6eacb4953`, `d8fe60017`, `81c8bfae1`; conflict only for `cc7e3c3a9` in `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md` (the known union files).
* Pairwise clean: `837da4fde` with `423517a71` (both edit `role-screens.js`, hunk-disjoint), `837da4fde` with `6eacb4953`, `423517a71` with `6eacb4953`, `467a0cf5d` and `cc7e3c3a9`, `ff40e50c8` with each of `423517a71` and `837da4fde`, `d8fe60017` with `837da4fde`.
* Conflict only in the same two known union files: `cc7e3c3a9` with `837da4fde`, and `cc7e3c3a9` with `d8fe60017` (resolved by keeping both sides verbatim, main's #1492 section first; the 156 README index row must survive once). This is pairwise evidence, not a sequential assembly result; the sequential result is a G3 and Phase 2 to 3 check.
* `log.md` is touched by 176, 134, 233 final, 96 UI and 156; append-only, zero deleted lines.

### Revised cut line and merge order (supersedes details Section 4 and A1 "Input cut line", plan only)

Wave A: 1490c (after G1 merge into the parent), 74, 176, 134 (`cc7e3c3a9`). Wave B: 215, 233 final `837da4fde`, 96 combined `423517a71`. All three wave B members are intended; each needs recorded coordinator admission at G6, or a named deferral listing the remainder for a later assembly. No silent omission; 156 docs optional, 203 excluded.

Order after M0 (fetched main merged into the assembly): M1 `467a0cf5d`, M2 `da436be3e`, M3 `cc7e3c3a9` (union), M4 `6eacb4953`, M5 `837da4fde`, M6 `423517a71`. Each is `git merge --no-ff`; no cherry-pick, squash or history rewrite; `94760af7d` is never merged separately. After every merge: `git diff --check`, no conflict markers, method-count assertions for touched tests, `role-screens.js` must contain both the 233 programme-page-context code and the 96 `fundingDraftPanel` Held-check code once each.

### Revised phase checks (focused impacted tier, A1 classification retained)

Dev checks are run on the assembled committed candidate from isolated pip-only venvs outside the repository; no uv; only the documented test-helper `PYTHONPATH` directories; ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0, pinned axe 4.10.3 hash recorded; non-queued `flock -n` heavy-lock admission; results external with the candidate SHA.

| Input | Checks (supersede the A1 233 and 96 rows) |
| --- | --- |
| 233 final | `test_programme_screen`, `test_role_screens_conformance`, `test_role_screens` (42 units at the pin), `programme_paging_browser_check` (107 PASS at the pin), `role_screens_browser_check 230` (not independently re-run on the final head; run it, record the number observed) |
| 96 combined | Held-download API 16, form staging API 14, `test_role_endpoint_inventory` 24, `test_finance_grants_screens` 20, `test_design_system` 8, `test_content_standard` 19, `held_form_download_browser_check` (88 PASS at the pin), `test_form_export` |
| Combined web | `role-screens.js` is edited by both 233 and 96: both browser checks and both unit groups must also pass on the assembled head, because separate passes at separate heads do not prove the union. `node --check`, fresh web-interface-guidelines fetch before any web review of `role-screens.js` |
| Others | unchanged from A1 (1490c, 74, 176, 134, 215, 156 rows) |

Phase 0 G3 also verifies by `git diff --name-only` that the actual assembled diff touches none of the escalation paths of A1 (workflow, manifest, Dockerfile, infra, SQL DDL, migration, gate tool, existing authorisation, CSRF or consent control); the recorded pins do not. SQL evidence stays separate (probe, UNOBSERVED if absent; no cloud fallback; real SQL acceptance of 82 is later live acceptance). No default full gate and no receipt are required; hosted CI is read separately for the assembly PR head and the parent to main PR head, and absent, skipped or path-filtered is not success. Exact-head independent assessment, the final independent Review (Phase 6), human exact-head review, consent, Finance, assistive-technology and legal approvals remain required and unrecorded. Nothing here is product behaviour change and no other correction allowance exists.

### Pending genuine independent critique (not run here, not claimed)

A2 changes the cut line, merge order, pins and checks, so a genuine independent read-only critique of A2 MUST execute once, with its verdict and dispositions recorded, before any future assembly. It must challenge: the double-merge prevention (423 contains 947), the both-files `role-screens.js` union evidence, the unreproduced `role_screens_browser_check 230` on the final 233 head, the 233 page-context inclusion, the unaccepted 134 alignment candidate and 156 and 203 boundaries, the unchanged focused classification, and whether root acceptance versus coordinator admission is stated correctly. The original adverse critique (Revise PC-01 to PC-05) and the A1 critique (Revise AC-01 to AC-05) stay preserved and are not repeated.

### Gates after A2

G1 HOLDS (1490c not merged; `src-api` in progress). G2 open (coordinator or root cut-line and authorisation; A2 only prepares it). G3 to G5 at assembly time. G6: 233 and 96 have independent acceptance at frozen final heads but coordinator admission is open, as is 215. R-UI-1 contract stays a root contract decision, not Finance approval. G4 SQL probe at assembly time. Resume at Phase 0 only after G1 and G2 and the A2 critique. DO NOT ASSEMBLE.

### A2 correction notes (after the independent critique, 2026-11-13)

The A2 text above is preserved unedited; these notes supersede it where they differ. PLAN ONLY.

* Rebind to current main (supersedes "Rebinding to current main (rubric delta only)"). `origin/main` is now `c58f87135` (`docs(infra): name Bicep secret parameter for redeploys (Refs #358) (#1493)`). The A2 statement was true only for `8e6e55457` to `774a91e5f` and did not cover this head. The delta `774a91e5f` to `c58f87135` is eight files: the #358 RPI tracking records, `docs/reference/log.md` and `infra/README.md`; no source, test, workflow, manifest, Dockerfile, SQL or gate-tool change. A read-only sequential simulation in a throwaway clone at `c58f87135` (run by the plan author, so not independent evidence) merged M1 `467a0cf5d`, M2 `da436be3e`, M4 `6eacb4953`, M5 `837da4fde` and M6 `423517a71` cleanly in order. M3 `cc7e3c3a9` conflicts only in `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md` (the known union files; skipped, not resolved in that run). G3 re-fetches main and repeats the matrix at assembly time.
* Per-merge check (supersedes "After every merge" for the web code). After each merge run `git diff --check`, look for conflict markers and assert method counts for touched tests. `role-screens.js` must contain the 233 programme-page-context code after M5 and the 96 `fundingDraftPanel` Held-check code after M6, each once; the combined union is required after M6 only when both are admitted. Only admitted members are merged.
* Diff inspection (supersedes the single G3 `--name-only` check). At G3 inspect the pinned input diffs, including hunks touching authorisation, CSRF, consent, SQL persistence or gate semantics. After assembly inspect the actual candidate diff and reassess the tier before publication. File names alone do not establish that a control is unchanged.
* Tier. The focused classification is kept (confirmed A1 decision, AC-02); the critique advice to apply the full tier was rejected as a conflict with it. Any further persisted-SQL, security-control, workflow, manifest, Dockerfile or gate change found at G3 or in the candidate escalates to the full tier, and doubt takes the full tier.
* Critique status. The A2 independent critique is executed (Revise, A2C-01 to A2C-04; see the critique file). It is not an assembly authorisation; G1 (1490 not merged), G2 and per-member G6 stay open. DO NOT ASSEMBLE.

## Amendment A5 independent-lane release without 233 (2026-11-13, prospective, written before any merge)

PLAN ONLY until the merges below run. A1, A2 and all earlier critiques are preserved unedited. This is a separately owned task (`issue-149-independent-ux-0042`, branch `feat/demo-149-independent-ux-0042`, exclusive worktree) that prepares an INDEPENDENT-LANE release from the original plan `c807923ec`. It does not change, adopt or supersede the separately owned original candidate `d790b6b45d31131f600414a2728af85ec5b5444f` (branch `feat/demo-149-ux-assembly-0017`), the original full-union Review `rpi-149-original-review-0031-result.json`, or the unmerged sibling `1498`. A3 and A4 live only on that original branch and are not part of this lineage.

### Root decision recorded (not an approval of 233)

* 233 is HUMAN-HELD: five corrections are spent, 15 new mypy errors remain, one extra typing-only correction was requested and the owner is UNAVAILABLE, which is NO APPROVAL. The hold stops 233 and its dependent closure and expansion only. It does not stop the independent lanes 96, 74, 176, 215, 134, 156 and 82.
* The root does NOT approve a 233 deferral, a requirement relaxation, epic closure or a new source pool. 233 stays open and held with its original candidate. This amendment is a work selection of independently admitted lanes (the A2 admitted-members-only merge rule), not acceptance of incomplete 233, and no failing 233 test is deleted, waived or silently fixed.
* The ENTIRE 233 new feature is excluded: `837da4fde` and `aebd381d9` are NOT merged and not in the candidate ancestry; no 233 code, helper or test change is carried. The programme paging code, `test_programme_screen.py` additions, `programme_paging_browser_check.py` additions and `atlas-screen-trace.md` edits from 233 are absent. The source-base programme features already on main stay the baseline.

### Frozen accepted inputs (exact SHAs)

| Input | Pin | Tree |
| --- | --- | --- |
| UX parent (includes 82 and the 1490 funding correction) | `318465aae0e484a5523fb37fda434714ca5200ab` | `2e0bd9706` |
| Fresh main (includes 1495 `e44de171e`) | `origin/main` at fetch time, at least `bb9f450fd0ad451a94d65f8cd683bf74f8975b2e` | recorded at merge |
| 74 | `467a0cf5d108cd6b3f0111661facfc2e85a6ce8a` | `fd79cf693` |
| 176 | `da436be3e149f1e445440f16d5460edd590fefc3` | `0089dd522` |
| 215 | `6eacb4953534ab86416a65c337cb9c43bc5cb1f2` | `45fd37bc1` |
| 96 combined (backend `94760af7d` carried once, never merged separately) | `423517a71f2acb41baaa292cff08d3be7d32d995` | `0a28fe0e8` |
| 156 docs | `d8fe60017407f3f7df4b339dfa0bfaff06dfacbd` | `856766483` |
| 134 main-aligned correction | `ca14b1523495c9304ecc076bd3fef7b4a43d19fa` | `5fd680566` |

203 stays excluded and no generated inventory is regenerated. 108 and its unmerged sibling `1498` are not adopted. The original 134 adverse amend process note and the root fresh assessment of 134 are preserved, not repeated or rewritten. The six partial and four deferred dispositions and open #83 wording in 134 stay exactly as in `ca14b1523`.

### Dependency verification (read-only, before any merge)

Shared-file overlap is not an implementation dependency. Facts read now:

* None of the six inputs has `aebd381d9` or `837da4fde` as an ancestor; `837da4fde` has `aebd381d9` as ancestor, and neither is an ancestor of the parent or main.
* Files touched against main: 74 `home_case_browser_check.py`, `test_home_case_api.py`; 176 runbook, `log.md`, retrofit README, `test_generated_dataset.py`; 215 `src/api/README.md`, `regulatory_ux_check.py`, `chat.js`; 96 `src/api/README.md`, `held_form_download_browser_check.py`, `server.py`, `role-screens.js`, `test_finance_grants_screens.py`, `test_form_held_download_api.py`, `test_role_endpoint_inventory.py`; 156 index row, `log.md`, one review document; 134 `cutover-evidence-pack.md`, README index, `log.md`.
* The only file in both 96 and 233 is `role-screens.js`: 96 adds two hunks in `fundingDraftPanel` and the Held-check code (about lines 1346 to 1452); 233 changes `screenTable`, `programmeRow`, `programmeQueue`, the programme overview and adds `screenPageSize` and `programmeCell`. The 96 hunks use no 233 symbol; read-only sequential `git merge-tree` of parent, main, 74, 176, 215, 96 and 156 is clean and a search of that tree finds no `screenPageSize`, `programmeCell` or "Open connected view" text. The only conflict in the full sequence is the known 134 `cutover-evidence-pack.md` keep-both case (original 134 plan and A4 rule).
* Therefore no real dependency of the independent lanes on 233 is found at plan time. The assembly re-verifies this on the actual merged tree (source search and import check). If a real dependency on 233 is found, no workaround is invented: the affected merge is not made, the route stops with the proof recorded, and the root is told.

### Merge order (normal `git merge --no-ff` only)

M0 actual UX parent `318465aae`; M1 fresh `origin/main`; M2 74; M3 176; M4 215; M5 96 combined; M6 156; M7 134 (keep-both on the pack if it conflicts, main's sections first, no wording edited). No cherry-pick, squash, amend, rebase, rewrite, product-code fix, new test, new issue, tick, publication, cloud, provider, deployment, spend or private working data. `git diff --check`, conflict-marker search, `node --check`, `compileall` and symbol-preservation checks only; that is the whole source-assembly check set.

### Boundary of the result

STOP at a clean, new SOURCE-FROZEN tree with an original source-assembly record (exact base, parent, head, `src` and module tree hashes, diff relative to fresh main). This is NOT acceptance. The new subset has no test evidence: it must undergo FRESH configured mypy, focused unit and browser checks and an original independent Review before any publication; the earlier Pass for the d790 candidate and any earlier per-input Pass are not reused as acceptance of the new head. The new record and any navigation or index text make no claim that 233 is delivered, accepted or deferred. Human, hosted CI, Finance, assistive-technology and legal approvals stay unrecorded. All actual source correction history and extensions are retained and unknown is not zero (research file, spent history: 82/1490 one combined correction; 134 corrections 1 and 2 and the later alignment process note; 96 corrections 1 and 2; 233 five spent, held; 74, 176, 215 none recorded).

### Pending genuine independent critique

A5 changes the cut line and routing, so one genuine independent read-only critique executes once before any merge. It must challenge: the dependency claim (no real 233 dependency), the exclusion completeness, the merge order and the single 134 conflict rule, the no-test-evidence boundary and the non-claim of 233 status. A verdict and dispositions are recorded in the critique file; it is not repeated.
