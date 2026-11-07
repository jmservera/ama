---
title: Archive filesystem checkpoint research (Refs #440 #79 #1231)
description: Research for the twelfth stabilization checkpoint on the archive helper hard-link contract
ms.date: 2026-11-06
ms.topic: reference
---

Research disposition: executed (focused, inline, read-only; no delegation). Planning Readiness: Ready. Written before any plan, pack, index or log edit.

## Brief

* New bounded #440 checkpoint in the same native session. Not a regrade of earlier checkpoints. Child branch `docs/archive-filesystem-checkpoint-440` at governance `feat/discovery-assurance-integration-123` `dce6498cf850de9bdc79ecb1706f8491d75b2ea8`, tree `c7440e42226178d6967966b8003794c795a2c314`, ignored-clean at entry. Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, unchanged after fetch. Target is the governance parent, not main.
* Trigger: #1231 (open bug, linked to #79) changes the archive helper to need hard links and to remove its own staging file. Documentation only; no test, SQL, browser, install or cleanup. Disk is 98% used (5.1G free); nothing is deleted.

## Findings

* C1: #79 candidate `feat/ranking-publication-runner-79` head `397419724e68b24bce879512a24c7df430177f87`, tree `c728049e33a3a0e20d9a7bf16b3738fabfbc14d7`, read with `git rev-parse` only. It is not an ancestor of the governance parent (unmerged, local, unpublished).
* C2: child #1231 at `/home/azureuser/source/ama-wt/issue-1231-ranking-archive`, branch `fix/ranking-archive-concurrent-writer-metadata`, head `57b3b6a09f6ac5b77b37881e21447751a56be5ff`, tree `fea8273a05c2a42da3e127d77a2c4ad9377f365b`, read only. Commits: `748526484` (research, plan, details), `24cab4b60` (fix), `57b3b6a09` (changes, author review, state). Base is the #79 candidate.
* C3: `git diff 748526484~1 24cab4b60` is 8 files, +412/-15: helper `ranking_publication.py` (diffstat 40 changed lines), `src/core/README.md`, two test files (+191 and +29), and the child's research, plan, details and issue note.
* C4: source mechanism read in the diff. Existing pre-check and canonical text are kept. A unique same-directory stage is created with `os.open(O_WRONLY|O_CREAT|O_EXCL)`, written, then `os.link(stage, final)` (atomic, no overwrite). On `FileExistsError` the existing record is read back and its `published_on` returned with `written` False. A `finally` then calls `os.unlink(stage)` unconditionally, for the stage this call created. Other `OSError` (including no hard-link support) propagates; the runner reports `publish_failed`. No fallback. The old shared `<final>.tmp` and `os.replace` are removed.
* C5: README wording now says the helper never overwrites or deletes a record and removes only its own staging file, and that a local filesystem with hard links is needed; a folder without them refuses to publish.
* C6: the original #79 R11 diagnosis (issue #1231 body) is one deterministic two-thread, one-process, local-filesystem interleaving: A returned `published` 2026-11-05, retained bytes said 2026-11-06, B received a structured `publish_failed` from a real shared-temporary `FileNotFoundError`; verification still passed. No lost publication or overwrite of a finished record was demonstrated. Medium, inherited, not a production incident.
* C7: child evidence under `/tmp/1231-ranking-archive-r1-1106/` (read, not rerun): `red1.exit` 1 and red log ends `Ran 48 tests`, `FAILED (failures=4, errors=2)`; `green5.exit` 0 and log `Ran 48 tests in 0.628s`, `OK`; `api-wiring.exit` 0, `Ran 12 tests in 12.635s`, `OK`. `import-proof-final.txt` prints helper sha256 `4d222878a5031fbe04b69f7d2c063d2486daac6505483167eeefa94160544c2b` and the two test files `ab90c263...` and `9199cd95...`, all under the child worktree. The native log is `/tmp/rpi-1231-ranking-archive-r1-1106.log` (702 lines).
* C8: document identities (all equal on the governance parent and main): BRD `docs/brds/agentic-retrofit-programme-brd.md` 0.21.0 draft blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` 0.21.0 in-review blob `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0003 blob `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 blob `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft and in-review are not approval.
* C9: requirement trace. The archive helper is the demonstrator's ranking publication record (PRD PR-006 deterministic published policy version, with retention periods a defaults-not-approved item under PRD DH-002, PR-003 and DH-003). The legal retention period and scheduler are explicitly not set by the helper (helper docstring). ADR 0006 mounts runtime data at `/data` and state at `/state` but defines no hard-link or archive mount contract. A deployment filesystem decision is therefore unowned and unknown.
* C10: auth, identity, resident, AI and manual boundaries are unchanged by this contract: the helper takes dates as inputs, reads no clock and changes no ranking.

## Limitations and qualifications (originals preserved)

* L1: the child's tests used deliberate child source and test imports with a parent read-only environment; not an isolated installed-package or FULL gate.
* L2: the spawned-process smoke also passed the OLD helper, so it is not independent RED proof. The injected `PermissionError` is not a real unsupported-filesystem test.
* L3: newer Ruff 0.17.3 and mypy 2.4.1 than maintained 0.17.1 and 2.4.0 were used for the three-file checks.
* L4: the child's original details forecast a completed-record overwrite and tolerated a missing stage at cleanup; later actual results demonstrate neither. The unconditional `unlink` has no missing-stage tolerance. Originals stay unchanged; this is a qualification.
* L5: `import-proof-final.txt` was overwritten during successive green runs; the final proof matches the candidate, earlier printed metadata is preserved in the native event output, original raw proof files are not restored. First RED and static failures remain uniquely retained.
* L6: Linux development evidence does not establish Windows, SMB, network or production support or an approved deployment mount.
* L7: coordinator consumption of the native log and diff is not an independent publication Pass. Hard-link compatibility disposition, FULL, current independent review and publication are pending.

## Alternatives

* Silent fallback to rename or overwrite on a no-link filesystem: not recommended; it reopens the divergence and is not authorized.
* New issue: rejected; #1231 exists, is deduplicated and linked to #79.

## Decision state

* Recommendation for the record: HOLD the #79 archive delivery and #73 dependent expansion until compatibility disposition, relevant final validation and independent assessment hold; FIX route is #1231 on its own lane. Independent #96, #188, #80 lanes continue. No owner decision, supported filesystem, production acceptance, C7/C8 completion or closure is inferred.
