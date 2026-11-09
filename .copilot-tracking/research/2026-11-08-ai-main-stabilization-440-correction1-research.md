---
title: AI and employee chat main stabilization 440 correction1 research
ms.date: 2026-11-08
---

## Purpose and relationship to the original record

New prospective corrective iteration on candidate `c96a32310466d4f39d31eed986489f44e0ab7c26` (tree `e824079515af425437f03b387e7a2a08b0f6de2e`), session `9dfa8bcc-4468-4888-be6a-d543c459c94f`, after the independent assessment `review-440-c96a` (request_changes: 4 Medium, 1 Low). The original research, critique, Review, plan, details, changes and state records of c96a are preserved unchanged, including every adverse claim. Nothing here backfills their phase history.

Research disposition: executed (genuine new reading and current-state refresh, 2026-11-08T11:45Z to 11:55Z).

## Amendment of the unsupported original claim (finding F3)

The original research file (lines 12-16) states that the case study, addendum, reference index, memory and component guides were read before planning. The independent transcript review found that the original session did not actually read addendum content or component-guide content before planning: it showed hashes, `wc` and a partial original read. That claim is unsupported and is amended here, in new evidence only. The original file is not edited. The original plan, critique, implementation and Review were therefore produced without those inputs; this iteration reads them now and corrects only where the reading changes an assertion.

## Mandated inputs genuinely read in this iteration

Read through the `view` tool or `sed` with the recorded ranges, 2026-11-08 (worktree at c96a):

| Input | Identity (sha256 prefix or blob) | Ranges read |
| --- | --- | --- |
| `docs/case_study_48_original.md` | blob `0aec2d80...`, sha256 `bf8f4462c41b58c8` | complete, 49 lines |
| `docs/reference/memory.md` | blob `e1268db9...`, sha256 `6c7d56639cf17a42` (context, not evidence) | complete, 67 lines |
| `docs/case_study_48_addendum.md` | blob `888d9ff7...`, sha256 `ca35dc94d1c74131`, 1,977 lines | 1-207 and 241-448 (lines 208-240, the EXA register tail, were truncated by the viewer and not read; purpose, 2026-10-23 resident proposal, exercise baseline, subsequent builds, deployment learning, budget start); 947-1100 (RAI release position, recovery, owner acceptance start); 1280-1345; 1471-1600 (where agents fit, brief, Decision 1); 1892-1977 (tokenomics, hypotheses, why now, recommendation). Headings of the whole file were listed. Lines 208-240, 449-946, 1100-1280, 1345-1470 and 1600-1891 were not read in full (cost, regulatory, sensor and platform appraisal sections); no claim here depends on them |
| `docs/reference/README.md` | worktree sha256 `2b4c07aec5116c26` (includes the c96a paragraph) | 1-60 and a targeted grep for ADR 0004, #157 and #440 (lines 378, 517, 807, 858, 984-1003). The full 1,003-line index was not read end to end |
| `docs/reference/method/tracking-retention-policy.md` | sha256 `e534783c040e7fe0` | complete, 6,081 bytes |
| `src/core/README.md` | 318,842 bytes | 4045-4195 (chat threads #160, chat and memory isolation #162, continuity #122 start) |
| `src/api/README.md` | 359,588 bytes | 707-810 (employee chat with bounded skills #530) and 4325-4400 (staff chat hardening #157) |
| `src/agents/README.md` | 69,579 bytes | 23-80 (chat provenance #175, consumption #164) and 679-740 (five assistants, review) |
| `src/README.md` | 35,656 bytes | 55-110 (local RPI gate and changed-path tier) |

BRD, PRD and ADR 0004 requirement text relied on by the pack was read in the original session (BRD FR-049, FR-050, RULE-025, RULE-026, NFR-010, NFR-011, OD-46 re-read earlier in this same session, before the c96a commit); this iteration did not re-read them in full and does not change their traceability rows beyond finding 4.

## Findings from the reading that bear on the corrections

* Addendum 1280-1345 and 1471-1600: the original case study agents are retained as history; the current proposal allows recommendations, drafts and flags only, and "AI must not ... approve professional work ... infer consent ... close complaints". This is consistent with the pack's authority ceiling rows. No change.
* Addendum 947-1100: RAI release position keeps real-data and operational activation BLOCKED until human owners approve; owner acceptance of the baseline report (2026-10-15) is not approval of live use. Consistent with the pack's statement that ADR 0004 adoption is not DPO, Legal, HR or control-owner acceptance. No change.
* Addendum 1892-1917: tokenomics is an owner-reported mentor line of challenge, hypothesis only; the pack already treats cost per accepted outcome as Unknown. No change.
* `src/api/README.md` 4325-4400 (#157): "No approved conversational task/release exists, so general staff model calls remain denied" and "All five issues remain Refs, including parent stabilization #440". Consistent with the pack.
* `src/agents/README.md` 679-740: "Quality review additionally uses the existing independence check against evidence submitters, recorders and fixers. This is independent proposal review, not competent technical sign-off." The README describes independence only for quality review. This supports finding 4: the pack's general "independent role review" overstated the enforcement. Direct source below confirms.
* Tracking retention policy: the original dated records are preserved, nothing is deleted, scratch output stays outside the checkout. This iteration adds new correction1 records and does not archive or prune.

## Direct source confirmation for finding 4

`src/core/src/zava_forward/core/assistants.py` `Assistants.review`, lines 1106-1173 (read 2026-11-08):

* `_view` and `authorize` enforce current role and case or area scope (`authorize(db, user, capability, case_id)`).
* `verify` requires `source_verified is True` and records `by`, `signature`, `note`, `at`.
* `accept` and `edit-accept` require a verification record whose `by` equals the accepting user and whose `signature` equals the current source signature.
* Only for `quality-evidence`: `self.store._independent(rec, current_actor, "review quality evidence")` checks the reviewer against active quality evidence submitters, recorders and fixers.
* There is no general rejection of the proposal requester as reviewer: the code compares the verifier to the accepter, not either to the requester.
* `reject` skips the verification and state checks, and writes `task["review"]`.
* No controlled record is written; task state, an event and a consumption review are the only writes.

## Current-state refresh (read-only, 2026-11-08T11:50Z to 11:55Z)

| Item | Observed |
| --- | --- |
| `origin/main` | `3c57a02d4d2ef61f6922436025b245c8a97e2694`, tree `3ed3dec05adbb7673515fbd90bd51791fd3b58a1`. It is the generated rubric score commit after #1278 |
| #1278 | MERGED into `main` as `e73d421046d00565f610fb671a80e683d2981874`, tree `feff48a485f0d1919698c08e3abd7d70af6a45d4`, 2026-11-08T11:37:10Z, head `6d7b52fdd9e55cd3a1f3a16d976d595bdc63dc88` |
| #1243 | MERGED into the declared parent branch `feat/controlled-lifecycle-integration-81` (not `main`) as `6ef6dc368ae3f8739095f740aa1e68634bd52922`, tree `0006f193b0fc459920f1fa3cf319d96c2a050c4a`, 2026-11-08T11:38:59Z, head `eddc7d715757a1cf2b50027471adcd9146dd08dd` |
| PR 1240 (parent) | OPEN, base `main`, head now `6ef6dc368ae3f8739095f740aa1e68634bd52922` (previously `c5edb320`). Not merged. The coordinator reports native integration of the parent is in progress locally; that is a coordinator statement, not observed here and not acceptance |
| #1275, #1271, #1273 | MERGED on main as recorded in the c96a pack (`4bc1e3f3`, `457a0c82`, `a5295c45`) |
| #1274 | OPEN (permanent AWF resilience not implemented) |
| Source movement 608c to current main | `git diff --name-only 608c98e6 origin/main` touches 11 files: #1278 sensor tests, `sensor_sql_check.py`, `src/api/README.md`, its RPI records and the rubric score. Zero files under the chat, assistant, isolation, privacy, thread, AI or registry modules, the agents `chat.py`, `server.py`, or any of the selected test files |
| Installed-source identity | sha256 (first 16 hex) of the venv `site-packages` files used by the original selectors equal the file content at `608c98e6` and at `origin/main`: `chat_panel` `bf6991cc547cbe94`, `chat_isolation` `7b8c009766ff6d9d`, `assistants` `80fb9a5fdb406158`, `chat_privacy` `ab30c5d022769534`, `chatthreads` `53d25ca09e82d20c`, `ai` `3593be1ea5cdb4e0`, `ai_registry` `cdac92bb3128ab1e` |

Therefore the original local selector results remain source-equivalent for the audited modules at current main. They remain observations at 608c on the installed packages; no selector is rerun in this iteration.

## AWF history for finding 1 (safe, source-qualified)

* Coordinator safe log `pr1275-awf-agent-recovery.log` (GitHub Actions run `42472167065`, Capstone Rubric Scorer, PR #1275 head `4db319288b837d7269f0e6cc19a309cd52b81b17`, 2026-11-08T10:38Z, no credentials read): `install_awf_binary.sh v0.28.23 --rootless` downloaded `checksums.txt` and `awf-bundle.js`, "Checksum verification passed for awf-bundle.js", installed the bundle, reported version 0.28.23 and "AWF installation complete".
* Coordinator reports (not independently re-run here) that later exact-head scorer retries and the #1278 scorer also passed.
* The historical 504 on the checksum retrieval is therefore a dated observation, recovered by the verified rootless checksums-plus-bundle route in #1275. Permanent AWF resilience (the retry, bounded and override design) is the separate open #1274 and is not implemented. It is not a currently observed installer outage.

## Planning readiness

Ready. Corrections 1 to 5 are bounded edits to this checkpoint's own pack section, index paragraph and a new log entry; no application, tool, test, workflow, agent, requirement or decision file changes. No source movement affects the audited modules.

## Follow-up candidates (unchanged ranking)

F1 clean-up (pending triage, proposed refactor, unfiled, unowned), F2 probe alignment, real-provider and SQL or browser evidence on a future head.
