---
title: Issue 149 UX parent integration plan research (2333)
description: Evidence gathered read-only to plan one coherent adoption of independently passed UX inputs into the declared UX parent; planning only
ms.date: 2026-11-12
---

## Scope and disposition

Prospective PLAN ONLY for the UX integration parent of #149. No source, publication, pack, ref or issue edit is made. Research disposition: `executed` (fresh read-only git, gh and evidence reads at the pins below). Planning Readiness: Ready for planning, NOT ready for implementation (gates in the plan).

## Pins observed 2026-11-12 (fresh fetch)

| Item | Value | Note |
| --- | --- | --- |
| origin/main | `8e6e554570f4075ff41ea130e29511455f57df2d` | contains #98 (`e155c88ed`), #1492 (`e4854bd7e`), #1491 (`8e6e55457`) |
| UX parent `feat/demo-ux-integration-1112` | `8f8be74e14c5fe1b6911a9493cd74d0750151085` | `43b2187b9` plus squash of #1487 (merged 2026-11-12T23:08:44Z) |
| parent versus main | left/right 1/5 | diverged, so the earlier parent fast-forward in the parent-base preflight no longer applies to the UX parent; main must be merged in |
| PR 1490 | OPEN, head `dc9fb68e0`, base UX parent | prior independent Pass (bounded); to be replaced by the combined head with force-with-lease by the coordinator |
| issue 149 | OPEN epic | earlier UX parent PR #1376 reached main 2026-11-10 (precedent: reviewed union diff, main merged into parent, hosted checks green) |

## Inputs and their actual lifecycle

| Id | Exact head | Tree | Base | Lifecycle at plan time |
| --- | --- | --- | --- | --- |
| 1490c (#82 funding) | `ff40e50c884b6ac85cecb99a71755e713b2be7d8` | `2e0bd970693ea2b4f7bab13124e53032a6b13870` | UX parent `8f8be74e1` | assembled in native task 2310 with one independent critique (PC-01..03 applied) and one independent Review (conformant, one low evidence gap resolved); coordinator exact-head assessment, force-with-lease publication, hosted CI and parent merge are STILL PENDING and gate all code assembly |
| 74 | `467a0cf5d108cd6b3f0111661facfc2e85a6ce8a` | `fd79cf6937b3e2b5af51e4fd510ec585dfe131a4` | `eac1206c6` | independent exact-head Pass (bounded test-only G1/G2/G3), 2312; unpublished |
| 176 | `da436be3e149f1e445440f16d5460edd590fefc3` | `0089dd5220dc8751ad65b1d93425af10d6592231` | `eac1206c6` | independent PASS_BOUNDED (40 canonical tests); unpublished |
| 134 | `cc7e3c3a9135b620035971d322d8875ba238be26` | `04c0c0ea8cd19b497729eb6d4b032e7f5a59ef13` | `43b2187b9` | correction 2 closure Pass (docs only); owner closure of its pending state not recorded; unpublished |
| 215 R1 | `6eacb4953534ab86416a65c337cb9c43bc5cb1f2` | `45fd37bc13c96f24716a4163365ef5faac7b69ea` | `eac1206c6` | independent exact-head Pass (bounded focus recovery), 2323; later-accepted wave |
| 233 programme row | `aebd381d9cdc405bcd14ef460ac1e8e5114fb792` | `377e032919bb96615a4fcf76abae472ef0a995c9` | `e4854bd7e` | implemented once (focused tier); independent assessment RUNNING (rpi-233-independent-2333); not accepted |
| 96 backend | `94760af7d274e1dc1d9ec8c37d76df85cbd46c28` | `46eb72d5249ce4d2bc3b40ef9afb3c5b5871feac` | `eac1206c6` | coordinator independent bounded M1 closure Pass (16 tests); earlier assessment Revise preserved; unpublished |
| 96 UI | `feat/demo-96-ui-implementation-2333` at `7f7a31ce6` (plan only) | not frozen | 96 backend | implementation RUNNING; no accepted head |

No input head is in the UX parent except 1487. The tree `2e0bd970...` equals the plan-time union of the parent and 1490c.

## Read-only merge simulations (dangling objects only, no refs)

* Parent + 1490c: clean. Parent + 1490c + main: clean.
* On parent + 1490c + main, each of 74, 176, 215, 233 and 96 backend merges clean alone.
* 134 alone against main CONFLICTS in `docs/architecture/cutover-evidence-pack.md` (one hunk, new sections appended on both sides: #1492 post-fix-wave checkpoint versus #134 disposition reconciliation) and `docs/reference/README.md` (one hunk, two adjacent paragraphs). `docs/reference/log.md` auto-merges with zero conflicts.
* All pairs among 74, 176, 215, 233, 96 backend (given the base) are clean. Every sequence containing 134 conflicts only in those two files.
* `test_home_case_api.py`: 1490c adds 7 lines at about line 90 (method `test_absent_funding_reads_as_not_confirmed_not_missing_case`); 74 appends 37 lines at about line 122 (two methods). Hunks are disjoint and merge clean in both orders at these pins (class count 3 on parent, 4 with 1490c, 5 with 74, expected 6 combined). The overlap remains a path-level risk if either head is rewritten or rebased.
* `test_mvp.py` and `store.py`: the 1487 versus 1490 conflict was already resolved inside 1490c (both complete methods; stage check before `gate_reasons`).

## Canonical changed-path selection (tools/rpi-checks.py `changed_groups`)

Per input: 1490c selects preflight, all five projects, namespace, static, mssql, four images, logo-0600. 74 selects project-api, browser. 215 and 233 select project-api, browser, image-api, logo-0600. 96 backend selects project-api, image-api, logo-0600. 176 selects all projects. 134 selects preflight, namespace, static. The union selects preflight, all five projects, namespace, static, browser, mssql, four images and logo-0600, effectively the whole matrix.

## Policy classification (basis)

The union contains a persisted SQL queue membership revision bump (`MEMBERSHIP_REVISION` 2 to 3) with a real-SQL regression, the funding gate that guards a human approval boundary, a Held-copy export check route and consent-adjacent web code. It selects mssql locally. Under the owner policy (D4, refined by #1294) SQL and security-sensitive changes and doubt take the FULL tier. The earlier precedent #1376 used focused checks; that is not a basis to downgrade this union.

## Spent history and human blocks carried (no new pool)

* #82/1490: original PR head plus one combined native correction (2310) spent; RV01 reader work adopted inside it; no further allowance; whole #82 stays open.
* #134: correction 1 (false closed-#83 wording) and correction 2 (`cc7e3c3a`) spent; original errors preserved.
* #96: saved-check correction 1 spent; M1 correction 2 spent and closed; sequencing defect of the self-performed first critique and Review preserved; UI under a separate plan with its own gates.
* #233: tensions-check corrections 1 to 4 spent and unrelated; the programme-row slice is a distinct admitted slice implemented once.
* #74, #176, #215: single implementation each, no correction spent.
* Human blocks: independent human exact-head review, hosted CI, owner merge decision; #134 owner closure of its pending state; #215 assistive technology, role keyboard and staff comprehension; #96 Held-copy human/Finance review and the R-UI-1 numeric fidelity decision; #82 real SQL acceptance and human approval of rules; none is inferred or ticked here.

## Environment facts

Python 3.12.3, node, docker 29.9.0, az, actionlint, shellcheck, trivy and bicep are present; no mssql image was listed among the first images, so SQL prerequisites remain UNVERIFIED. 72 GB free on `/`. Existing local venvs and the heavy lock `/tmp/ama-rpi-heavy.lock` are shared; no shared cleanup is planned.

## Open questions routed to the coordinator

* Which inputs form the cut line for the one assembly (wave A fixed; wave B conditional).
* Merge method of the assembly PR into the parent (merge commit recommended) and of the final parent to main PR (owner choice).
* Whether the 96 backend plus UI must travel together in the UX parent (recommended).

## A2 evidence update (2026-11-13)

Read-only re-check: origin/main `774a91e5f` (rubric delta only against `8e6e55457`); PR 1490 open at `ff40e50c8`, `src-api` in progress; `94760af7d` is an ancestor of `423517a71`; `aebd381d9` is an ancestor of `837da4fde`; merge-tree matrix recorded in the A2 section of the [policy amendment](../../plans/2026-11-12/issue-149-parent-plan-2333-policy-amendment.md). The earlier "233 page-context not accepted" and "96 UI unfrozen" facts above are superseded by the root-accepted final inputs; spent correction history carries unchanged.
