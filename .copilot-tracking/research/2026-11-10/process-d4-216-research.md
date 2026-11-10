---
title: Research - process D4 recovery after the refused D3 implement-start (Refs #216, #208)
description: Metadata-only research of the D3 state construction error and the serialization that prevents recurrence
ms.date: 2026-11-10
---

## Execution

* Research disposition: executed by read-only inspection of git, the D3 state file, the D3 witness log and the reviewer files. No source edit, runtime rerun or nested agent.
* Start identity observed: HEAD `46dfa75490a96f49dc89eab17fe72451320553ab`, tree `e1b6f51806ad1a0ec05ded63f389dff235ed1142`. The worktree holds exactly six untracked D3 files whose sha256 values equal the Root snapshot `216-d3-preservation-before-d4-1110.json`.
* Debits: D1, D2 and D3 are preserved spent debits. D4 is the fourth in this bounded recovery, not a new pool and not an automatic D5. Earlier whole-issue history stays qualified and unknown.

## Observations

* D3 witness log sha256 `40c73ea8663e7e3d55f4a2d7f6e0352baa100841ee896a65747bf93d0574feea`: seq 4 `implement-start` refused with "missing persisted artifact evidence: changes". The Root verifier reports four events and exit 1 although the CLI exited 0.
* Cause: the D3 state file contains two `changes` keys inside `artifact_paths`; the first holds the real path, the second is `null`, and JSON parsers keep the last. It arose from two text-replacement edits on a hand-written one-line JSON file. The malformed D3 state stays unchanged as a historical record and is not valid evidence of a successful phase.
* D2 plan is zero bytes in the committed tree (unchanged, historical). The D3 plan was not rewritten after its observation.
* Independent source assessment: reviewer `6339ad63-3729-49ea-924b-b9293482c70d`, `numeric-d1-final/functional-findings.json` sha256 `470a42896e3a959d46e1699f4b7b90ee3a9e27b9e2293ffd42eca6b601663d59`, ledger sha256 `ca3586dfd56fb42c16384c24f1a61ddea1bbbc71f40dfdd758ce0bd513ced560`. Verdict approve at `46dfa754`, no findings, both original Medium resolved, static only.

## Decision

Build the D4 state only with `json.dump` from a Python dictionary, never by editing text. Before every witness event, load it with an `object_pairs_hook` that rejects a repeated key at any depth and assert `artifact_paths.changes` is a single non-null existing non-empty path. Keep the plan unchanged after `plan-done`; record progress in the state and changes files instead of ticking boxes.

## Planning Readiness

Ready.
