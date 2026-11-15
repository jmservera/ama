---
title: Issue 165 api and agents branch coverage floor details
ms.date: 2026-11-14
---

## Phase 1 agents tests

`test_branch_floor.py` covers `_moment` non-text, naive and malformed inputs; each `valid_alert` rejection; `_threshold_gaps` malformed owner, date and numbers; minimum-sample reasons and invalid-record exclusion in `evaluate_alert_triage`; `agreement_gaps` for malformed fields and an empty agreement; `beat` on an unwritable path; and `install_signal_handlers` with `signal.signal` patched.

## Phase 2 api tests

`test_auth_branch_floor.py` covers password login rejection, tampered, undecodable, expired and malformed cookies, trusted-proxy construction refusals, role map override, bad principal headers, each denial reason, logout targets, account fallback and `make_provider` refusals. All identities are synthetic (`example.invalid`, placeholder GUIDs).

## Phase 3 validation

Commands run from each project with `PYTHONPATH` set to the worktree sources.
