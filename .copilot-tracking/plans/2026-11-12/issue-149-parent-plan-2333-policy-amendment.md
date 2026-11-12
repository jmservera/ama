---
title: Issue 149 UX parent integration plan, policy amendment A1 (2347)
description: Prospective PLAN-ONLY amendment correcting the validation tier and merge-authority wording, recording the input cut line, wave A and B admission, valid dependencies and the pending amended critique; no assembly, source, pack or publication
ms.date: 2026-11-12
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
