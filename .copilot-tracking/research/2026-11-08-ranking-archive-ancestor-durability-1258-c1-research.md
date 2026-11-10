---
title: Ranking archive ancestor durability 1258 correction 1 research
description: Verification of independent functional findings H1 and M1 and readiness findings against head cbb1cc5b
ms.date: 2026-11-08
---

Refs #1258. Task `1258-ranking-archive-ancestor-durability`, correction 1. Research disposition: executed (code and contract read, findings verified by reading; no reproduction beyond the failing tests below). Planning Readiness: Ready.

## Start state

* Frozen head `cbb1cc5bbb415b7a74fea3b708fcb07b14b69d92`, tree `8277d9b48b4f902c1e4117e12e3b25c5ba5d3fb3`, ignored-inclusive clean. `origin/main` is `f548b65f4aa31eb92a2cc9cb801130e422daed7f` (fetched; unchanged, so no merge).
* The cbb1cc5b FULL receipt (sha256 `200135e156479b32dfa146e1a5d918747fcf43ae0207304e07a217276e9d07f2`, 17 groups, jobs 1) passed. It is historical evidence now. It does not resolve the findings below, and any correction invalidates it. Receipt, raw outputs, runtime and images stay retained and unmodified.
* Independent functional review: `request_changes`, H1 (High) and M1 (Medium). Independent readiness review: `approve_with_comments`, M1, L1, L2. Both are assistive, not qualified-human approval. Reports are session data under `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/` and were read as evidence only.

## Findings verified against code

Walker `_ancestors()` in `src/core/src/zava_forward/core/ranking_publication.py` (head cbb1cc5b lines 132-149) stopped before the first parent where `os.access(parent, os.W_OK)` was false, and checked `os.path.ismount` only after ascending.

* H1 confirmed by reading and by a failing test. Present non-writability says nothing about whether entries below it were ever synced. After a first publication fails syncing `a`, `chmod a 0555` makes the retry stop before `a`, so `_confirmed` returns success although the `b` entry in `a` and the `a` entry in its parent were never synced. The API then audits a success instead of `committed_unconfirmed`. Another creator or permission set has the same effect. My original D3 rationale ("a parent this process could not write is not one it created") was an unsupported inference. A directory is synced through a read-only handle, so write access is not needed to sync it.
* M1 confirmed by reading and by a failing test. For an archive that is itself a mount point, the walker added host parents outside the archive filesystem. An unreadable host parent then fails the extra `O_RDONLY` open and every publication reports unconfirmed.
* Readiness M1 and L1 confirmed: the session state and the original and FULL plans carry pre-gate snapshots (blocker B2, unchecked F1-F4) that read as current. L2 confirmed: criterion 4 text did not name a 503 test.

## Design options

| Option | Result |
| --- | --- |
| Keep the permission cutoff, add more checks | Rejected. Cannot establish a durably known boundary. |
| Sync every parent to the filesystem boundary, skip no folder | Chosen. Smallest change, fail closed, no new state. |
| Persist creation state to know a durable boundary | Rejected. New durable state and schema; out of scope. |
| Preprovisioned-only archive | Rejected. Needs owner approval (issue rule). |

Boundary: if the resolved archive is a mount point, there is no parent on its filesystem and the chain is empty. Otherwise parents nearest first, including the first mount point (its entries live on the archive's filesystem), or the root. An open or fsync error on any listed parent raises `DurabilityUnconfirmedError` (record kept, path-free message, unchanged runner and API handling).

Consequence, stated honestly: an ancestor that is not readable (mode without `r`) now yields `committed_unconfirmed` on every publication instead of being silently skipped. That is the fail-closed reading of the first criterion. It is an environment-visible behavior change from cbb1cc5b and is recorded as a limitation for the owner.

## Existing coverage reused

* `AncestorDurabilityTests` in `src/core/tests/test_ranking_publication.py` has `labelled()` (stat-identity labelled fsync and link events), retry, symlink and partial-creation cases. No new helper needed.
* Race-loser path: `test_publish_race_loser_confirms_durability_before_reporting_it` already fails every directory sync and `_confirmed` is the same function for winner and loser, so an ancestor-specific loser test adds no distinct behavior and is not added.
* API ancestor fault and retry: `test_parent_folder_sync_failure_is_audited_as_unconfirmed_and_retry_is_sound` (added in the earlier continuation) still applies.
* 503 evidence for criterion 4: `src/api/tests/test_ranking_publication_wiring.py` `test_unsupported_hard_links_are_a_storage_failure_not_an_authorization_one` and `test_link_and_cleanup_failure_is_logged_and_path_free` assert status 503 with path-free text. Both are re-run below.

## Limits

* Mocked and temporary-directory tests do not prove power-loss durability (R1) or the steady-state extra syncs' cost (R4). Real mounts were not created.
* The non-root permission case ran as uid 1000; the privileged and mount cases are mocked and labelled so.
