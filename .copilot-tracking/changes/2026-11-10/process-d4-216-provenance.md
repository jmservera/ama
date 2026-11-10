---
title: Provenance - D2 empty plan, D3 refusal and preserved partial records (Refs #216, #208)
description: Qualification of the numeric correction process chain after the D2 zero-byte plan and the refused D3 implement-start
ms.date: 2026-11-10
---

## Scope

Metadata only, at unchanged source HEAD `46dfa75490a96f49dc89eab17fe72451320553ab` (tree `e1b6f51806ad1a0ec05ded63f389dff235ed1142`). It cures no old chain and attests no older reasoning. D1, D2 and D3 are spent and preserved; D4 is the fourth debit in this bounded recovery, with no automatic D5 and no reset of earlier history.

## D1 (source numeric correction, commit `4e61626b`)

Preserved qualifications: `commit-complete` refused (omitted `--claim-commit`), verify exit 1, log sha256 `85c40318dd82f9f6c95e935c783774be1633e6a50deafe947e3b0a1593645c83`; `implement-done` observed a stub changes record; the review source was stale against the commit; the first derived-ratio red used unpaired participants and an early command hit an import-path fault.

## D2 (process, commit `46dfa754`)

Seven events were ok and verify exit 0, but `.copilot-tracking/plans/2026-11-10/process-d2-216-plan.md` is zero bytes in the committed tree. D2 `plan-done` observed 911 bytes, sha256 `60cb4035f369ec50e21d923853abc732b3101e8e138e5bf9a8c6d0059588ad32`; `implement-done` and `review-done` show the empty hash `e3b0c442...b855`. The truncation cause is inferred (a script that opened the file for writing before reading it) and was not witnessed. D2 is therefore not full unqualified evidence. The empty file is not repaired.

## D3 (refused partial attempt, never committed before D4)

D3 recorded `research-open` and `plan-done`, then `implement-start` was refused ("missing persisted artifact evidence: changes"). Cause: its state file has two `changes` keys in `artifact_paths`, the first a path and the second `null`, produced by hand text edits of one-line JSON. Root's verifier reports four events and exit 1 (log sha256 `40c73ea8663e7e3d55f4a2d7f6e0352baa100841ee896a65747bf93d0574feea`). D3 never reached implement, review or commit-complete. The malformed state is kept as a historical record and is not valid.

Six D3 files enter the D4 commit byte-identically (Root snapshot `216-d3-preservation-before-d4-1110.json`):

| File | sha256 |
| --- | --- |
| `.copilot-tracking/changes/2026-11-10/plan-d3-216-changes.md` | `96fc8cca84dcf073c8e7caf07733b1ee5f21d02f9539e24b05d46a6c77ea5b2b` |
| `.copilot-tracking/details/2026-11-10/plan-d3-216-details.md` | `3153dc73c985d7469c01edc868600da01d8ab3aff27c2dba075f574706c8edae` |
| `.copilot-tracking/plans/2026-11-10/plan-d3-216-plan.md` | `36f8a3255123adc8b01a1ca2ae17e403f666d10620d0146c31d9251d780b50f3` |
| `.copilot-tracking/research/2026-11-10/plan-d3-216-research.md` | `bb59356812cb3f65ae95db395e09c1d33b1056479d808b0e99fc99f6dff36546` |
| `.copilot-tracking/reviews/plans/2026-11-10/plan-d3-216-plan-critique.md` | `2bb83a72a240115d493f37e4b32dee47848388a30efb91c9840e65b936632cc1` |
| `.copilot-tracking/rpi-sessions/2026-11-10/issue-216-plan-d3-1110-state.json` | `171b801ad468998b2d51a0dbf202d198288fce728d880b3c63dc3208d3b9d5b0` |

## Recurrence prevention in D4

The D4 state is written only with `json.dump` from a dictionary and re-read with an `object_pairs_hook` that rejects duplicate keys at every depth, with an assertion that `artifact_paths.changes` is one non-null existing non-empty path, before each witness event.

## Source identity and checks

`git diff --name-only ab365e53 46dfa754 -- src` is exactly `src/agents/README.md`, `src/agents/evals/run_regulatory_gates.py` and `src/agents/tests/test_paired_report_command.py`. The earlier numeric red, green, Ruff and mypy results are carried by this unchanged identity only; nothing was rerun in D4. Whole #216 and #208 stay open.
