# Issue 1258 correction 3 research (2026-11-08)

Refs #1258. Read-only research before any plan, code or test edit. Original, c1 and c2 records are history and are not edited.

## Authority and scope

* Owner decision, issue comment 6722289866: ONE further narrow correction without relaxing durability. It lifts only the cycle limit. It does not approve a stable mount topology, a non-Linux contract, deployment assurance, privileged or shared-host mounts, power-loss testing, cloud actions, publication, acceptance or child 1259 retargeting.
* Coordinator comment 6718032322: the c2 critique PC-002 (topology may change between link, resolution and sync) stays Blocking; c2 assumed a stable topology without owner approval. Mountinfo ordering, non-Linux all-unconfirmed behaviour, execute-only ancestors and deployment assurance remain unapproved and unverified.
* Start: HEAD a0038709874ffdc3200b9ac9dc3fb074ce425c43, tree b3402b87842e9804ede53a304b724bc7ded62281, ignored-inclusive status clean. Fetched `origin/main` is 3c57a02d4d2ef61f6922436025b245c8a97e2694 (a descendant of f548b65f). `git diff f548b65f origin/main` is empty for `ranking_publication.py`, so no integration is needed for this correction; any ordinary merge is left to the coordinator and is not planned here.

## Documents read (honest range)

Repository instructions, branch and PR workflow, regulatory evidence conventions (not relevant to this code path); the issue 1258 body and the two comments above; the a0038709 source of `ranking_publication.py` lines 100-300 (`_fsync_dir`, `_read_mountinfo`, `_active_mounts`, `_ancestors`, `publish`, `_confirmed`); the test class list of `src/core/tests/test_ranking_publication.py` and the labelled-sync helper; the c2 critique and Review records through the coordinator summary. The case study original and addendum and `docs/reference` index and memory were not re-read in this cycle: no requirement, regulation or knowledge-base file is changed, so only the issue contract is used. This is a narrower read than a full entry read and is recorded as such.

## Actual call sequence at a0038709 and where topology can change

1. `os.makedirs(archive_dir)` resolves the path by name.
2. `os.open(stage)` and `os.link(stage, path)` resolve `archive_dir` by name each time.
3. `_confirmed` calls `_fsync_dir(archive_dir)`, which opens the archive by NAME again. If the path was renamed, replaced or mounted over after the link, the sync targets a different directory than the one that holds the committed entry, and success is reported.
4. `_ancestors` calls `os.path.realpath` then reads `/proc/self/mountinfo`, then each parent is opened by name. Three separate resolutions and one table read, with nothing tying them to one directory object or to one mount state.

So PC-002 is a real property of the code, not only a precondition: a path swap or a mount change between steps 2 and 4 yields a false confirmation. Directories are identified by inode, so a held descriptor cannot change identity.

## Kernel facts established by a real read-only probe (this host, unprivileged)

* `/proc/self/fdinfo/<fd>` has a `mnt_id:` line for an open directory descriptor. It identifies the mount instance of that open file, so a same-filesystem bind mount has a different `mnt_id` from its host parent, and a Btrfs subvolume that is not a mount has the same `mnt_id` as its parent. This is the distinction c2 used the mount table for.
* `openat(fd, "..")` returns the directory's parent in the current mount tree. Probe: starting at `/dev/shm` the ids were `[36, 30, 34]` (shm mount, /dev mount, root mount) with `..` crossing at the real mount roots; `/tmp` and `/home/azureuser` gave a single id (same mount as `/`). The walk ends at the root where `..` equals the directory itself (same device and inode).
* No mount was created or changed; the probe only opened existing directories read-only.

## Candidate corrections considered

| Option | Result |
| --- | --- |
| Keep mountinfo and add a re-read after the syncs | Still resolves by name, still depends on mountinfo ordering and parsing (the c2 PC-003 risk). Larger code. Rejected. |
| Hold descriptors and walk with `openat("..")`, boundary by `mnt_id`, sync the held descriptors, then re-verify | One set of directory objects for walk and sync, no mountinfo parsing, detects change by comparison. Smallest net code (removes about 40 lines of parser). Selected for planning. |
| Open the archive descriptor before staging and link through `dir_fd` | Ties the link and the sync to the same directory object. Needed so the committed entry's directory is the one synced. Selected. |
| Declare a stable topology, or declare supported platforms | Not permitted without owner approval. Not adopted. |

## Residual limits that remain regardless

* Between the final re-verification and the return, a mount change can still occur; no userspace check can close that window. The correction narrows false confirmation to: confirmed only when the held directory, the link target and the verified chain are identical before and after the syncs. Whether that remaining instant is acceptable is a platform-contract fact that stays an owner decision and is reported, not assumed.
* `mnt_id` requires Linux with `/proc`. Where it cannot be read the existing explicit unconfirmed path is used (the non-Linux all-unconfirmed behaviour is retained, not newly approved).
* Real bind mounts, Btrfs subvolumes, power loss (R1), sync overhead (R4), pre-existing operator symlinks and execute-only ancestors (PC-003 of c1) remain unproved. All new mount cases are mocked at the `_mount_id` seam; a real mount-root probe above is read-only observation only.
