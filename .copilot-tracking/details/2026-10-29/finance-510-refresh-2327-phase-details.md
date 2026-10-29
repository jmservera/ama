---
title: Finance PR 510 main refresh phase details
description: Task-level integration and validation expectations
ms.date: 2026-10-29
---

Task ID / slug: `finance-510-refresh-2327`. Plan:
`.copilot-tracking/plans/2026-10-29/finance-510-refresh-2327-plan.md`.

<!-- P01 -->
## P01: Integrate main

### P01-T01

Starting clean HEAD `088b5393`; remote finance `8020965b` has only bot score
update. Main `c764a012`. Fast-forward remote before rebase, retaining original
objects for range-diff. New task artifacts are ours and must not overwrite
existing evidence. Rebase is explicitly authorized by the user.

### P01-T02

Rebase ours is main plus replay; do not blindly choose conflict sides.
Restore all rubric paths and scenario manifest explicitly from pinned main.
Preserve append-only log main prefix plus finance suffix and both index entries.
Prove original finance source unchanged where main did not change it; shared
source must contain both intended deltas. Preserve original RPI evidence bytes.

<!-- P02 -->
## P02: Validate and deliver locally

### P02-T01

From each component set `PYTHONPATH=src:tests` plus sibling core/API/agents
source/tests paths, `PYTHONDONTWRITEBYTECODE=1`, project-local `TMPDIR`.
Use `/tmp/mv/bin/ruff check --no-cache .`, `ruff format --check --no-cache .`
and `mypy --cache-dir=/dev/null`; confirm imported modules resolve locally.
Core selectors: form_review, form_review_pack, form_staging,
finance_match_controls, finance_signoffs, grant_lifecycle_controls,
change_provenance, document_rescan, scenario_manifest, dependency_rule.
API selectors: form_staging_api, finance_match_api, role_endpoint_inventory,
dependency_rule. Rerun scenario manifest even if pins do not change.
Record exact exits, counts, expected optional skips and original failures.

### P02-T02

Independent Review owns only its new review artifact, assesses original plan,
critique, integration delta and actual validation. One Review, no review loop.
Do not retroactively alter prior findings. Record outcome and route new work.
Use authenticated user's noreply identity for author and committer, Conventional
Commit and required coauthor trailer. No remote writes.
An adverse or blocked Review stops ready handoff. Preserve findings, owners and
next actions even if diagnostic checks pass; no second Review or unassessed
correction may be called independently accepted.

### P02-T03

After committing, attempt `tools/rpi-checks.py --all --lock-timeout 0 --base`
against current fetched main with a new external output path.
Missing prerequisite or busy foreign lock blocks publication, not authority to
skip, deploy or claim success. Final receipt stays external and no subsequent
commit may be presented as covered by an earlier receipt.
On successful gate only, run `tools/rpi-checks.py --verify-receipt <external-receipt>
--base <recorded-main-sha>` and record exact head/base and verification exit.
Fetch main before gate; changed main blocks current-main coverage pending later
reconciliation and a new gate. Require fresh fetch and receipt verification
before later authorized publication assessment. No receipt is claimed when
admission or prerequisites fail.
