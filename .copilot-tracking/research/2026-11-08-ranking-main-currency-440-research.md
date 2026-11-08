---
title: Issue 440 ranking main currency research
description: Research for the bounded current-main currency continuation of the ranking checkpoint
ms.date: 2026-11-08
---

## Scope and disposition

Bounded continuation of the original ranking main stabilization checkpoint (task 440-ranking-main-stabilization-checkpoint). Research disposition: executed (read-only git inspection). Planning Readiness: Ready. Focused tier, documentation and bookkeeping only. Refs only.

## Evidence

* Frozen head aa8f0d11baefab38e4d5e4dc4d9c6f55ed03d77b, tree afb700db98d5262950046ce6972e81fda95b8a97, branch docs/ranking-main-stabilization-440, ignored-inclusive status 0 lines (observed 2026-11-08T02:26Z).
* Original integration main a80acadaa1b7d96a10e71b246e297bc2825d3de5. Fresh origin/main 77fa5d35e915e524af9a5d536e3ae093b69c5807, subject "chore(rubric): record score 77/100", committed 2026-11-08T02:19:23Z.
* git diff --stat a80acada origin/main: one file, .github/rubric/scores/latest.json, 4 insertions, 4 deletions. Blob 6741ddd61aba2ff80cd8b7cb2f59e63cb1af7db3, mode 100644. No ranking source, test, tool or document changed.
* Native focused gate attempt for aa8f0d11 refused before execution, exit 1, "Candidate does not descend from the reviewed main base"; no receipt exists. Logs are in /mnt/ama-gates/ranking-main-440-1108 (gate-stdout.log, gate-stderr.log, handoff.txt) and stay unedited. This pre-execution ancestry refusal is distinct from the original socket-path preflight refusal and from the R35 adverse history.
* /mnt has about 6 GB free; /tmp/ama-rpi-heavy.lock exists as a zero-byte file and no holder is established until the gate takes it non-queued. Target gate directory /mnt/ama-gates/c440-currency-r2-1108 is absent.

## Conclusions

* a80acada and ac0f29f9 ranking evidence stays historical source evidence. 77fa5d35 is rubric-only and adds no model, deployment or acceptance evidence.
* The original selectors (core 76, API 53 on SQLite, cohort 20, retention 37) were run on source identical to current main for every non-rubric path, so they remain authoritative; they are refreshed once against the post-merge tree to record exact current identities.
* Decision from coordinator: normal merge of origin/main, no rebase, amend, reset or force push; original planning, authored Review and refusal evidence stay in ancestry.
* No new defect. #1258 and #1259 remain the owners.

## Omissions

No full gate, SQL Server, browser, Azure, model call, push or PR. Private data is not read.
