---
title: Issue 109 actual remote parent and main adoption research
ms.date: 2026-11-10
task_id: 109-actual-parent-main-1110
---

## Objective

Local-only adoption of the ACTUAL remote parent (PR #1395 squash) and fresh main (PR #1400 aftercare) into this topic, replacing the earlier prospective composition's dependence on the child head. Integration only: no source, test, config or policy authoring, no push, PR or GitHub write. The earlier preparation chain (3 events, verify exit 1) and prospective chain (HEAD `20addb9ae`) with their records and attribution correction are preserved unaltered. Brief: ROOT `brief-109-actual-parent-main-1958.txt`.

## Pinned identities (after `git fetch`, 2026-11-10 ~15:58Z)

| Ref | Identity |
| --- | --- |
| local HEAD (frozen start, clean) | `20addb9ae1d7c652ecf1882401e54523fee97ba0`, tree `ce82f2f65062807a829cb6b4c618f987343db4e4`; parents `a3d5e615`, main `1290aa557`, child `6b0ba7b14` |
| `origin/feat/demo-sensor-review-109-1110` (actual remote parent) | `bd2a6494464b451572fc3dc7c8d53c549e0f9dad`, squash of PR #1395 into the declared parent (not main); its first parent is `06374dfca` |
| exact reviewed child | `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2`; NOT an ancestor of the squash (squash merge), so the squash is adopted by its own commit |
| `origin/main` | `64c3f9191a2ffa97ef2dc07245422333ad4d6585`, tree `8fbdaec7d138e360e9e460ad714742cb78b4d621` (PR #1400 aftercare persistence; Root reports all 19 hosted checks passed) |

## Findings

* The squash's non-tracking content is identical to the reviewed child: `git diff --name-only <squash> 6b0ba7b14` outside `.copilot-tracking` is empty. HEAD already holds that content, and `git merge-tree` of HEAD with the squash gives tree `ce82f2f6...`, equal to HEAD's own tree: adopting the squash adds ancestry, no content.
* Dry run of HEAD with `origin/main` exits 0 (no conflict, tree `d45426bd28850d893622b48df1a2649a13135992`); this is the real source-affecting integration.
* Main-ahead of the previous prospective base (`1290aa557` to `64c3f9191`), non-tracking: aftercare Core (`aftercare_intake.py`, `aftercare_store.py`, `projection.py`, `sqlstore.py`, two tests), API (`server.py`, `workbench.py`, `aftercare.js`, `app.js`, `index.html`, `aftercare_browser_check.py`, `workbench-manifest.json`, four tests, README), `scenario-manifest.json`, WCAG baseline doc, `docs/reference/log.md`, and two pyproject edits (Core: aftercare store tests added to the existing `seed_merge` untyped-call group; API: new scoped override for `test_aftercare_served`).
* Overlap of sensor-review source with aftercare source: `server.py`, `projection.py`, `src/core/pyproject.toml`. The dry run merged them cleanly; semantic compatibility is established only by the planned checks, not by absence of a textual conflict. Candidates for interaction: API route inventory (`test_role_endpoint_inventory`), workbench manifest, scenario manifest integrity, `projection.py` and `sqlstore.py`.
* Rubric, registry, workspace and docs content already in HEAD from the previous prospective merge. Mediums #1401 and #1402 (aftercare) are open and inherited; they are not repaired here and no scoped mypy exemption is broadened by this lane.
* The earlier carried results (Core 65/22 skips, API 6, MSSQL 22, browser 33, mypy) were measured on a composition without PR #1400's source, so none carries; each affected check is refreshed (input-qualified refresh).

## Requirement status (document-qualified, unchanged)

BRD v0.21.0 (draft) FR-048, AC-090, OD-43; PRD v0.21.0 (in-review) FR-050, AC-066 to AC-068 all "Not run"; ADR 0003 decision 6 owner-accepted with no deployment or live approval. BRD FR-050 and AC-066 to AC-068 are unrelated requirements. Child actual merge and local tests are not integrated or live acceptance. All #109, #111, #110, #184 and #185 criteria remain unmet; `Refs` only. The #440 sensor-integration checkpoint remains for Root to route.

## Environment

Owned env `/tmp/z109-pi-1110/venv` exists with editable installs of this worktree, `azure-iot-hub==2.7.0`, `six==1.17.0`, mypy 2.4.0, ruff 0.17.1, mssql-python 1.15.0, playwright 1.64.0; actual import origins are re-verified after the merge. Scripts for the browser and MSSQL runs exist under ROOT `checks-109-prospective-integration-1110/`; new scripts will be adapted into a new checks directory. The heavy lock is attempted once per heavy check with `flock -n`; BUSY stops admission.

## Disposition

Research disposition executed; Planning Readiness Ready.
