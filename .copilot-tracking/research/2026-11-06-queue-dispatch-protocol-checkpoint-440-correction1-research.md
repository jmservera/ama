---
title: Queue dispatch protocol checkpoint 440 correction 1 research
description: Research for correcting the fourteenth checkpoint's r8 chronology statement and parent-pin provenance
ms.date: 2026-11-06
---

## Identity and method

Correction cycle 1 of `queue-dispatch-protocol-checkpoint-440`. Start HEAD `e73733b98988b211a591edcace5f7d6070dbfaf5`, tree `fe548cafe2f0a6304baca49ac7f3f46c0fd23058`, ignored-clean (0 status lines). Fresh `git fetch` (exit 0): governance `119828353ccc1d678c1a4e9c1c67b621b0d263a0`, main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, candidate HEAD `4c878d664853074e9dec49e57d5c89c4cc9bf3a2` tree `978986c9374f6b1019136d121a4ee1f21be7941c`; all unchanged.

Method: the `rpi-research` skill was activated through the skill tool and its body was loaded before this phase. Posture focused (bounded internal correction with named evidence). Waves are inline and compact: wider (all places repeating the chronology and parent-pin claims), deeper (native event metadata), contrarian (could the order still be serial?). No subagent.

## Original r58 blobs (preserved, `git hash-object` at 08:54Z)

| Artifact | Blob |
| --- | --- |
| research | `f59f4ab5dbacef23f03b448311f6f197d4630f49` |
| plan | `a96e592aba3e804d6b11b2d326f7015db83ff8cd` |
| details | `8c6d3d79406199c5a0927903b1e01675e79e1016` |
| changes | `4a60c8e4145483805732b5260e6603ab9f536e1f` |
| review | `187b76fa44bdf59598a2c8f4c3c0f00a0a3bd15c` |
| state JSON | `a14e963166756813de857249dffb3830bf23179b` |

## Finding 1: r8 chronology (coordinator-corrected)

The coordinator's launch brief said the r8 creation order was Research, Details, Plan, and this cycle's original pack text repeated it (pack line 4361). The coordinator now states that inference came from the outer CLI log display and is wrong. Metadata read from the original native `events.jsonl` (session `0bd489d3-4546-4229-94f9-d1812eadef27`), only tool call IDs, event types, timestamps and success flags, no content:

| Call | Start | Complete | Success |
| --- | --- | --- | --- |
| Research create, first (`toolu_01Xo7PG9...`) | 08:17:18.098Z | 08:17:18.126Z | false |
| Research create, successful (`toolu_01CNbg7B...`) | 08:17:36.958Z | 08:17:36.985Z | true |
| Plan create (`toolu_016LrGET...`) | 08:18:22.940Z | 08:18:22.981Z | true |
| Details create (`toolu_015auJzP...`) | 08:18:22.940Z | 08:18:22.970Z | true |

Plan and Details started at exactly the same millisecond and overlapped, so they were parallel. Neither the CLI log display order nor the shared start time shows serial creation, so both "Research, Plan, Details" and "Research, Details, Plan" as a serial chain are unsupported. The failed first Research create is retained (the coordinator attributes it to a missing directory; the cause was not read by this author). State, log and commit creation order after these calls was not re-derived here and stays as supplied. The statement "creation order was Research, Details, Plan, state, log, commit" is therefore superseded for the Plan versus Details relation only.

## Finding 2: other r8 qualifications stand

Unread research skill body, no source edit, three original Markdown files without frontmatter, GitHub metadata retrieved (so "no network" is not literal), and no Azure, Graph, provider, SQL or browser run. Not changed. No serial phase chain is claimed and r8 is not presented as a completed full RPI.

## Finding 3: parent 136 provenance

Local `git rev-parse refs/heads/feat/infra-hosting-integration-136` in this worktree returned `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (equal to main). `git ls-remote origin 'refs/heads/feat/infra*'` returned 0 lines after the fresh fetch. So the ref is a local, unpublished integration branch at main. The earlier remote 404 stays true and historical. The pack row (line 4317) says "not observed" and that the brief's claim is "supplied, not observed", which is now superseded for the local ref: local observed `bb3a3b03`, remote absent as observed, intended code target. No remote branch is created and no branch-choice question is raised.

## Finding 4: unchanged holds

The second AgentsWorker route authority stays unresolved. The owner's reply, relayed by the coordinator, was a question about URL versus ACA environment or container, not an approval; the coordinator explained it is another URL on the existing proposed API integration. Clarification and the general background-processing scope are not role-code approval. The operator disposition for `liability-unknown` and all seven design gaps stay open. FIX recommendation unchanged.

## Contrarian

Could a serial order be proven from existing data? Start times are identical to the millisecond; completions differ by 11 ms (Details .970, Plan .981), which reflects completion not creation order. A Details-then-Plan completion does not establish serial starts. No evidence supports a serial chain.

## Planning readiness

Ready. Research disposition executed. Edits needed: the pack process sentence, the parent pin row, an additive correction subsection, a README sentence, a log entry. No source, requirement, ADR or approval change.
