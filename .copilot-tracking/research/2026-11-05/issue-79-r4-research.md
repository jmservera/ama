---
title: Issue 79 research, round 4 (local publication runner)
ms.date: 2026-11-05
---

## Identity and pins

* Task: `issue-79-r4-publication-runner`, parent task #73 (case workbench integration).
* Source branch `feat/ranking-publication-runner-79` at `ead177ef90d24666557708ea344848a1be43bdf8`.
* Target parent topic `feat/case-workbench-integration-73` and `origin/main` both resolved to the same SHA `ead177ef90d24666557708ea344848a1be43bdf8` on 2026-11-05 (fetched). Pinned as the base.
* Research disposition: `executed`. Planning Readiness: `Ready`.

## Literal issue #79 (read 2026-11-05)

* Criteria 1 and 2 are ticked (same data and policy give same order; policy files versioned and hash-verified).
* Criterion 3 unticked: named policy owner signs the first rule order. The shipped `ranking-v1.json` has owner `to be named` and status `Draft rule order, not yet signed off by an owner`.
* Criterion 4 unticked: ranking snapshot publication is scheduled and retained (ADR 0002 deviation).
* Parent #73. Open dependency: named owner of the ranking policy.

## Merged PRs read

| PR | Delivered | Relevance |
| --- | --- | --- |
| #896 | `ranking_publication`: immutable dated archive, `verify`, `overdue`, `SCHEDULE` contract | Reused unchanged |
| #1039 | Manager `publish` and `GET publication` store methods and routes, audited | Manual path; not edited |
| #1096 | `ranking.is_signed` and `signoff_problems` derive sign-off from a recorded owner sign-off | Reused as the approval gate |
| #1171 | Docs-only status record: criteria 3 and 4 unmet | Preserved; criteria stay open |

## Gap confirmed

`ranking_publication.SCHEDULE["runner"]` reads "deployment scheduler (not yet configured)". There is no callable invocation for schedule, publish or verify with explicit inputs, a window, refusal reasons or exit codes. The manager endpoint publishes the draft policy with today's server date and reports `policy_signed: false`, which suits a manual action but not an unattended job.

## Constraints carried forward

* No change to `store.py`, Store schema, workflow or gate families, API or web routes (#82 is changing controlled gates, #80 list exports). No overlap found in the files touched: only `ranking_publication_runner.py` (new), its test, `src/core/pyproject.toml` mypy override, `src/core/README.md` and the knowledge-base log.
* Open PRs on 2026-11-05 (#1206, #1205, #1203, #1141) touch none of these files by title; no real overlap flagged.
* No clock, environment variable, `ZF_DATA` or private data is read. Synthetic fixtures only.
* Prior adverse research and Review preserved: criteria 3 and 4 stay open; a mocked signed policy is a test-only registry copy and is never approval.
* No schedule, tolerance or retention period is invented: the cadence and 24-hour minimum already in `SCHEDULE` are reported as `proposed, not an approved operational rule`.

## Options considered

1. New thin module `ranking_publication_runner` over the existing functions (selected: smallest, no existing file changes).
2. Extend `store.py` with a scheduled publish method (rejected: store/route surface, #82 overlap, audit schema questions).
3. Deployment job or timer definition (rejected: infrastructure, out of scope).

## Environment note

Installed `zava-forward-*` packages pointed at another checkout; a temporary venv at `/tmp/zf79venv` was created with `pip install -e` of this worktree's `src/core`, `src/agents`, `src/api` and pinned-compatible `ruff` and `mypy`.
