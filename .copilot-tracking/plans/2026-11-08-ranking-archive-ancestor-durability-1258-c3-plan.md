# Issue 1258 correction 3 plan and details (2026-11-08)

Refs #1258. Planned before any code or test edit. Follows the c3 research record. Tier: FULL for final publication (persistence integrity); this cycle is LIGHT only (focused Core and API units, ruff, mypy; no gate, SQL, browser, Docker, scanner, model or cloud).

## Objective

Remove the silent stable-topology assumption behind c2 PC-002. A publication is confirmed only when the directory that holds the committed entry, the chain of parents that was synced and the mount boundary are the same objects before and after the syncs. Any difference, or any missing boundary information, uses the existing unconfirmed path (record kept, DurabilityUnconfirmedError, 409 with no path, committed_unconfirmed audit, sound retry). No relaxation of durability, no platform declared supported.

## Design (smallest evidence-backed change)

1. `publish` opens the archive directory once (`O_RDONLY|O_DIRECTORY`) after `os.makedirs` and before staging. Close it in a `finally`. Failure to open is an ordinary pre-commit OSError, as `makedirs` is today. Body moves to `_publish_held` unchanged otherwise (stage, link by path, loser and cleanup behaviour, original date).
2. `_mount_id(fd)` reads the `mnt_id:` line of `/proc/self/fdinfo/<fd>`; `_parse_mount_id(text)` is the pure parser. Absent or malformed data raises OSError.
3. `_walk(held)` replaces `_read_mountinfo`, `_active_mounts` and `_ancestors`: repeatedly `os.open("..", dir_fd=cur)`; stop at the filesystem root (parent identical to child) or at the first parent whose mount id differs from the child's (that parent is on another mount and is not included). A mount root is included as the last ancestor because its entries are on the archive's filesystem; an archive that is itself a mount root has no ancestors. Returns the open descriptors plus `(st_dev, st_ino, mnt_id)` identities. Any open or read error is raised.
4. `_confirmed(outcome, archive_dir, held)`: check that the archive path still names the held directory and that the committed name exists in it (`stat(name, dir_fd=held, follow_symlinks=False)`); walk; `fsync` the held directory then each parent descriptor (nearest first, as before); walk again and compare identities; check the path again. Any mismatch is `OSError(ESTALE)`. Everything is wrapped by the existing `DurabilityUnconfirmedError` conversion, and descriptors are closed in `finally`.
5. No `ismount`, no mountinfo, no `realpath`, no permission test. Symlinked parents are followed by the kernel's `..` and the real holder directories are synced, as before.

Deleted (c2 mountinfo parser and tests): they asserted a mechanism that is removed. They stay in git history and in the c2 records, which are not edited.

## Tests (existing files only; fail on a0038709 unless noted)

Core, `AncestorDurabilityTests`, with a `mount_ids(**by_name)` helper that patches `rp._mount_id` (create=True so the red run reaches the old code) keyed by directory identity:

| Test | Expected on a0038709 |
| --- | --- |
| archive path is swapped for another directory after the link: unconfirmed, record kept in the moved directory | FAIL (confirms the wrong directory) |
| mount id of a parent changes between the walk and the verification: unconfirmed | FAIL (confirmed) |
| bind-mount shape (archive mount id differs from parent): parent fault is not reached, written True | FAIL (unconfirmed from host parent) |
| mount root at `a` by mount id: syncs archive, b, a and not root | FAIL (syncs root) |
| unreadable mount id: unconfirmed, record kept, retry sound | FAIL (confirms) |
| `_parse_mount_id` rejects text without a valid mnt_id | FAIL (AttributeError) |
| real fdinfo returns an int for a real directory descriptor; skipped without /proc | FAIL (AttributeError) |
| required ancestor open failure (rewritten to fail the `..` open from b) | passes after rewrite |

API wiring: the c2 unreadable-mount-table test is rewritten to fault `_mount_id`; it asserts the committed record and original date, path-free 409, committed_unconfirmed audit and a sound unfaulted retry. The existing archive-directory and ancestor sync fault tests remain.

Retained unchanged: every first-run, retry, staging, concurrent loser, owner-only mode, original date and symlink test. Real (unmocked) walks run on this host, so the walk up to `/` and the fdinfo read are exercised for real; only the mount boundary shapes are mocked.

## Commands (LIGHT, one worker, synthetic temp data)

* Red: Core `cd src/core && PYTHONPATH=tests python -m unittest test_ranking_publication -q`; API `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py -q`, against the a0038709 source in the existing scratch venv `/home/azureuser/.local/share/ama/gates/g1258-c2-light-1108` (module origin and sha256 proven first).
* Green: new scratch `/home/azureuser/.local/share/ama/gates/g1258-c3-light-1108` (refuse if present), pip install of the edited local distributions, module sha256 equal to the edited source, same commands plus the runner publication selection if the coupled mapping exists, ruff and mypy on the two modules.
* Cleanup: only explicit paths proved generated by this run. Never `git clean`, glob or age removal.

## Out of scope and still unproved

Real power loss (R1), sync overhead (R4, now plus one `fdinfo` read and a second walk per confirmation), real bind mounts and Btrfs subvolumes, overlayfs and container layouts, pre-existing operator symlinks, execute-only ancestors and deployment permissions, and a mount change in the instant after the final check. Platform support and non-Linux behaviour (every publication unconfirmed) remain owner decisions. No chmod broadening. Child 1259 and its worktree untouched.

## Blocker rule

If the independent critique shows that the held-descriptor design cannot meet the existing requirement without a platform-contract choice, stop before code and return the options and impact.
