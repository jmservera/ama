---
title: Setup API selection changes
description: Source, regression and publication evidence for issue 360
ms.date: 2026-10-17
---

## Scope and Status

Full approved plan setup-api-selection-360, P01-T01 active. Research complete,
Plan Ready after one independent critique PC001-003 accepted/resolved directly.
No implementation review yet. Worktree source startd11c273, mainbbbc924 ancestor.

## Boundaries

Only safe compatibility selection/read-only guard and related tests/runbook/KB.
No live setup/private SQL/Graph/secret/cloud mutation. Historical ACR receipt,
prior review, sourcebab4bf3 and current integration heads remain distinct.

## P01-T01: Red-first regressions

Baseline setup101 passed under system Python. New actual deployed-pair test
failed twice with exact owner's ambiguity message; mixed modern/legacy direct
pool test failed because no refusal. Staff test initially could not import
zava_forward; created .venv and pip installed editable core/agents/api/orchestrator
only after missing-import failure. Real central guard test then failed six
check/list-staff payload/execute subcases as expected (dry-run already guarded).
Five new test methods total, no removals. No source edit before red captures.

## P01-T02: Implementation

Explicit ingress tag filter now supports absent-modern-role/workloadapi and
rejects conflicting modern role. Direct-pool cardinality before generic chooser
prevents mixed tag generation tie-break; exact override bypasses preference.
Central azure_staff refuses check/dry-run/list-staff before request payload or
execute; mutation-mode check operation unaffected. Green validation pending.

## P01-T03: Validation and documentation

Green combined command from infra/tests:
`../../.venv/bin/python -m unittest test_setup_entra test_staff_azure test_initialize_api_auth -q`
passed164 (104 setup,43 staff,17 legacy). Compileall passed. Ruff0.17.1 F-only
setup/script test; full existing E/F/I/B/UP staff-test lint/format passed.
Mypy2.4.0 `--follow-imports=silent --ignore-missing-imports infra/scripts/setup-entra.py`
passed. Tools installed via pip into task-local .venv after missing-tool errors.
Initial new callback closure lint warning corrected; an overbroad patch briefly
changed the pre-existing callback and caused NameError, immediately restored
with exact method context; final combined164 green. No test removed.

Runbook explains actual tag mismatch, safe compatibility, direct ambiguity and
exact override. Active check/list-staff advice corrected to private-host path;
KB route/log updated, documentation skill session recorded. Git diff whitespace
and five changed relative links passed; eight prior ACR artifacts/JSON exact
bytes retained and prior owned log is byte prefix.

## P02: Integration and Review preparation

Initial main bbbc924 was ancestor. Later prefix validation detected shared
origin/main advance; fresh fetch confirmed d400eb8d1d0d6567445b0fc11803260eab897a65
(#383 finance), no changes to selected infra source/tests. Do not claim fresh
main log prefix yet: authorized owned-topic rebase required. Commit current
owned work first, integrate while clean, preserve upstream full log prefix plus
all own appends and routes; exact old remote lease d11c273eb744c440965375c3638583565b28db6c.
Review/publication pending; prior ACR single Review remains residual, not rerun.
