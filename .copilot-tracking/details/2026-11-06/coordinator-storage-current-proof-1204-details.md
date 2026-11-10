<!-- markdownlint-disable-file -->
# Details: current storage proof (issue 1204)

Written 2026-11-06 about 00:34Z UTC, before implementation.

* Output root: new unique owner-only directory ~/.local/share/ama/tracking-archives/2026-11-06-issue1204-current-proof-<UTC> (mode 0700, files 0600, exclusive create). Restore scratch: new empty /tmp/h1204-r6-restore-<UTC>.
* Script is external (in the output directory), uses lstat, never follows symlinks, refuses traversal, special files, and inputs whose size or mtime change during read.
* Archive: whole .copilot-tracking at the frozen head; members record type, mode, size, sha256. Readback compares each member to the inventory. Restore of the 68 selected plus comparison to the manifest rows, git blobs at f6b2984d9dabc181ef784caadcf045bcbb69a24a and current originals.
* B (400 members) and C (68): read the member bytes from the tracked bundles, check against bundle manifests (size, mode, sha256) and original sources; scan archived bytes with the bounded pattern set from the earlier hygiene script, printing names and counts only.
* Protected: sha256 and git blob of every unselected tracking file equal HEAD; refs; /tmp/h1204 listing hash; source blob; git status before and after.
