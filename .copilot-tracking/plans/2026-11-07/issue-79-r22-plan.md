---
title: Issue 79 plan, r22 merge of main c1a16482
ms.date: 2026-11-07
---

Task `issue-79-r22-merge-main-1255`. Planning readiness: ready. Critique: one author-only prospective self-critique (not independent), below.

## Plan

* Commit research, plan, details. Re-fetch; stop unless main is `c1a164829`. One `git merge --no-ff`. Prove parents and blob/mode parity, then light checks, Changes, state, Review, log entry, commit.

## Acceptance

* Parents are the planning commit and `c1a164829`. All 17 incoming paths carry main's blobs and modes; all topic-changed paths keep pre-merge blobs; no `src/*/src` path differs from the pre-merge head.
* Scratch `/mnt/ama-gates/g79-main1255-preparation-1107`, `PYTHONDONTWRITEBYTECODE=1`, unmasked exits.

## Commands

* Origin proof with `/tmp/zf79venv/bin/python`; core 53 and API wiring 15; `test_assistant_release.py` 46 expected with the new class skipping or erroring only on missing SQL, recorded precisely; `tools/test_rpi_checks.py` unittest; CI-equivalent Ruff and mypy for tools (`--strict` on rpi-checks pair) as in `src-ci.yml`; ranking five-file Ruff and mypy `src tests`.

## Self-critique

* Risk: main moves (stop on drift). Risk: new SQL test needs a server (record skip/failure honestly, no fix). Excluded pre-existing formatter diagnostics are not reformatted.

## Follow-up

* Coordinator aligns child 1231; NEW parent FULL before main.
