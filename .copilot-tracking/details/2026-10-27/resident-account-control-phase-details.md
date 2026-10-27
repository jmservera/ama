---
title: Resident account control phase details
ms.date: 2026-10-27
---

Task #467. Read with the matching plan and research artifacts.
Current state: P01 and P02 complete. Independent Review Complete / Conformant;
PR #471 open against feat/resident-interactive. Hosted/human approval pending.
No material divergence or implementation blocker.

<!-- P01 -->
## P01: Implementation and verification

<!-- P01-T01 -->
### P01-T01: Projection and account control

`ResidentDemo.view_for` already verifies token and authorises current case.
Only after that succeeds add `account.email` from `identity.email_for(case_id)`.
Do not disclose identity on `/demo/session` or change login/session contracts.
Move existing signout button into header details; reuse employee account class/
native interaction pattern, project tokens and text labels. Use flex wrap/
min-width constraints and right-anchored bounded panel. Reset open/identity
when hidden. No custom role=menu, icon dependency, storage or photo endpoint.

<!-- P01-T02 -->
### P01-T02: Coverage

Adapt existing exact projection test to permit precisely own email while still
excluding second resident and private IDs. Add account identity/session-denial
coverage. Browser runs against actual loopback server and existing constructed
fixture, with new throwaway fake credentials only. Include reload, anonymous,
two residents, keyboard toggle/dismissal/logout, long-email reflow, restored
session, failed logout and expiry. No database or deployed app access.
Existing `checks/resident_demo_browser_check.py` has four logout access sites
that also need to open the disclosure first. Adapt those interactions without
executing its SQL setup; include this changed file in Ruff/mypy. This is a
directly relevant compatibility update, not new infrastructure or wider scope.

<!-- P01-T03 -->
### P01-T03: Evidence and documentation

API README explains top-right account and own-email disclosure. Use a disposable
external virtualenv if system Python is externally managed. Missing dependencies
were confirmed by import failure; pip permitted. Record exact commands/results,
browser limitations and any implementation amendments in dated changes evidence.

<!-- P02 -->
## P02: Independent review and publication

<!-- P02-T01 -->
### P02-T01: Review

Fresh independent reviewer activates rpi-review, examines implementation and
evidence once, writes dated review. Refresh web rules before review and include
file:line findings. Preserve original verdict; do not loop review/fix silently.

<!-- P02-T02 -->
### P02-T02: Publication

Resolve gh account and repo-local noreply email for author/committer. Conventional
commit with required Copilot trailer. Push topic branch normally and open PR
base `feat/resident-interactive`, declaring stacking dependency and Refs #467/
Refs #466 only. Owner explicitly replaces full local gate with focused checks.
Do not merge; hosted checks/rubric/owner review remain separate pending gates.
