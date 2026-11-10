<!-- markdownlint-disable-file -->
# Discovery CLI checkpoint 440 C4 qualification plan and details (2026-11-10)

Continuation of task `440-discovery-checkpoint-1110` (same session). Prospective, written before the pack edit. The original plan, details, critique, changes and review records are unchanged.

## Authority

Owner authorized one finite documentation qualification batch, C4 of five on the #440 ledger. C3 statements elsewhere stay history and are not edited. One correction remains afterwards; no reset, no new five.

## Trigger

Independent review of head `9b3f6ac64a894bc267ab65cddf31227302e19cac`: approve_with_comments, zero blocking, one Low. The D6 outside-source opens list omits `/usr/lib/ssl/openssl.cnf` (`openat` O_RDONLY, retained `D6b.strace` line 117). Document precision only; no connect or write-mode open contradiction; not a defect.

## Phases and details

* P1 Pack: qualify the D6 row additively (add the OpenSSL configuration read, state the list is from the retained trace limited to the selected syscalls (the independent review's reading that `socket` was not selected is incorrect: the producer command selected openat, connect, socket, execve, unlink, rename, mkdir and write)). No trace change, no new run.
* P2 New record `.copilot-tracking/reviews/2026-11-10-discovery-checkpoint-440-1110-c4-qualification.md`: independent review disposition, Root-executed identity and hash evidence (Root1323 verified all 26 members and manifest `c81aa583...3675`; Root1322 guard stopped on the wrong cwd before hashing), current main `4244e84e` with `src` and `infra` diff against `0d262beee` exit 0 (Root-confirmed), original native R1/R2, first mypy fault, tool-version mismatch retained.
* P3 State update and one concise appended log qualification. Earlier entries intact.
* P4 Review Markdown, links and exact diff; commit only this batch.

## Gates

Docs only. No product, config, agent or tool edit; no reruns, gates, installs, services, cloud, model, data or credentials; no merge, rebase, push, PR, issue or board write. Historical observation stays pinned at `0d262beee`. This launch's witness covers the continuation only.
