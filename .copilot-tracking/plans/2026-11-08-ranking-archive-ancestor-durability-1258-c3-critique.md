# Issue 1258 correction 3 critique and dispositions (2026-11-08)

Refs #1258. One independent prospective critique (rubber-duck agent, read-only, no files edited) of the c3 research and plan, run before any code or test edit. Verdict: Revise. Only this one critique is run in this cycle; the revised design below is NOT re-critiqued and the author's own dispositions are therefore unreviewed.

## Findings and dispositions

| ID | Severity | Finding (summary) | Disposition |
| --- | --- | --- | --- |
| PC3-1 | Blocking | ABA: the archive is moved out of its parent, the parent is synced, the archive is moved back before the second walk. Both walks match but the restored entry was created after the parent sync. | NOT resolved; returned to the owner as a platform-contract decision (see below). A timestamp comparison was assessed and rejected: kernel timestamps are coarse (a rename pair inside one tick escapes), and parents such as `/tmp` churn from unrelated activity, which would turn this into spurious unconfirmed results and flaky tests. No mechanism available to userspace without a contract choice closes the window, so the finding stays Blocking and the result is not declared conformant. |
| PC3-2 | Blocking | The link is path based, so a swap of the path before the link lands the record in another directory while the held directory is later checked. | Applied. Stage open, link, existing-record read, stage removal and the committed-name checks use the held directory descriptor and relative names (`dir_fd`). The record and the synced directory are then the same object by construction. Regression: path swapped before the link. |
| PC3-3 | High | The committed name is checked only before the syncs. | Applied. The record inode is captured when the record is written or validated and the name in the held directory must still resolve to that inode before and after the syncs; removal or replacement during confirmation is unconfirmed. Regressions: removal and replacement during a sync. |
| PC3-4 | High | Mount and platform claims exceed the evidence: the probe created no bind mount or Btrfs subvolume; chroot, container and overlayfs durability are unproved; `dir_fd` or `O_DIRECTORY` may be unavailable before the unconfirmed path is reached. | Applied to wording: all bind and subvolume cases are mocked at the mount-id seam and stated so. Where `dir_fd` is not supported the publication is refused before anything is written (truthful, nothing committed); this differs from the c2 "committed and unconfirmed" outcome on such platforms and is part of the unapproved platform contract below. Nothing is declared supported. |
| PC3-5 | Medium | Existing tests use the removed mountinfo seam and a source assertion constrains cleanup. | Applied. The mountinfo tests are migrated to a `_mount_id` seam keeping their behavioural assertions; the parser and hidden-mount tests are removed with the parser; the source assertion and any path-based fault injection are adjusted only as needed and each change is listed in Changes. Red runs must be behavioural, not helper absence alone (the `_parse_mount_id` and real fdinfo tests are the only ones that can fail by absence; the rest fail by wrong behaviour on the old code). |

## Revised design (supersedes the plan's items 1, 4 and the test table where they differ)

1. `publish` opens the archive directory once and uses `dir_fd` for every operation on the stage and the record. If `dir_fd` is unsupported or the directory cannot be opened, nothing is written.
2. Record inode captured at write (`fstat` of the stage descriptor) or at validation (`fstat` of the opened record); `_existing` reads through the held directory.
3. `_confirmed` order: verify path names the held directory and the name still holds the inode; walk with `..` and mount ids; fsync held then parents nearest first; walk again and compare `(st_dev, st_ino, mnt_id)`; verify the name and inode and the path again. Any mismatch or error is the existing unconfirmed path.
4. No timestamps, no retry loop, no `syncfs`.

## Blocking decision returned to the owner (not decided here)

Residual race: a concurrent actor that relocates a directory of the archive path chain (or changes mounts) inside one confirmation window can still produce a confirmation in which an entry was created after its parent's sync. Options and impact:

| Option | Effect | Cost or risk |
| --- | --- | --- |
| A. Contract precondition: the archive path chain is operator-owned and not relocated or remounted while the publisher runs, enforced by deployment control and documented | Smallest; current design is then sound within the precondition | Unenforced in code; needs a named platform or operations owner and deployment assurance |
| B. After the directory syncs, `syncfs(2)` on the held descriptor (via ctypes) | Flushes every entry on the archive's filesystem regardless of topology; closes ABA for entries created on that filesystem | Linux only, kernel 5.8 or later for reliable error reporting (older kernels can lose the error, a false confirmation), whole-filesystem cost on shared storage, new platform claim, ctypes use; not adopted without approval |
| C. Timestamp comparison of parents plus bounded retries | Narrows but cannot close the window (timestamp granularity) | Spurious unconfirmed results on busy parents; false assurance |
| D. Reject any archive whose confirmation cannot be proven (always unconfirmed) | Fail-closed | Defeats first-run behaviour; not acceptable under the existing requirement |

Recommendation for the human ledger: A with documented deployment control, optionally B after a named platform review. This is a recommendation, not an approval.
