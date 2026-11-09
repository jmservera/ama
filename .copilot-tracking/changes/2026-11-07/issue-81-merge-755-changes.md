---
title: Issue 81 fresh-main merge changes
description: Changes and evidence for the normal merge of origin/main 7551e50e into the parent
ms.date: 2026-11-07
task_slug: issue-81-merge-755
---

* Start `3e245e14f397305379d3c31a57fa596d751d8628` (ref `refs/ama/issue81-pre-755-merge`). PRE records commit `2b555169d5a26de5b988d15f954fdc856dd5c235` (four prospective files only). Normal `--no-ff` merge commit `8f0fc97fdace7781dd09742fe114f3f6468f94d8`, tree `1b702f7ceda25d42016515d1077b2fbea48fbd2e`; parents `2b555169d` and `7551e50e904cd4d696ed74ecd6fb1e0cb6be1ba8`. No conflicts, rebase, force or rewrite.
* Proof: `git diff --raw PRE HEAD` equals `git diff --raw 0f420dc9 7551e50e` (identical, including modes). Source change from main: only `src/api/checks/case_journey_browser_check.py`; no child-owned or appointment source touched.
* Local observed (no service), scratch `/mnt/ama-gates/g81-755-preparation-1107`, `env -i`, snapshot via git archive of the merged head, non-editable `--no-deps` install after a missing-import probe; import origin is the scratch venv and contains the capacity correction. Focused four modules (`test_quality_procurement test_gates test_hazard_referral test_resident_preview`): exit 0, 233 tests OK, 1 skip (JSON-only separate-file audit ordering). `ruff check`, `ruff format --check`, `mypy`: exit 0 (266 files). Queue benchmark excluded.
* Unverified: the incoming browser-check change is not browser-tested; MSSQL, Azure SQL, API, browser, FULL gate and hosted CI not run. Old receipts are historical. Child #86 untouched (remote branch observed at `6ff492adf`, differing from the coordinator's frozen `2eda7691`; not reconciled here).
