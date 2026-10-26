<!-- markdownlint-disable-file -->
---
title: Issue 349 image-scan correction 1 review (preserved return)
description: Documentary preservation of the already-executed independent review
ms.date: 2026-10-26
---

## Nature of this record

Preserves, verbatim, the return of the independent review executed once in
native session bfe8a55b-19b6-41a6-a0c7-c6c25bc06037 on 2026-10-26 (about
08:25 UTC, agent type code-review, read-only). It is not a new review, not a
retrospective plan and not a Pass. The disposition text already committed in the
changes record (issue349-image-scan-correction1-changes.md) is unchanged.

## Reviewed subject

Head 3d5b69d8fd1659cc4d32f9758320e13c91e6e726, an artifact-only commit
(.copilot-tracking research, plans, details, changes, 2026-10-26,
issue349-image-scan-correction1-*) on 0fe8c3be. Scope: scope of diff, absence of
Dockerfile/runner/scanner change, evidence under
/mnt/ama-rpi-gates/issue349-image-correction1, root-cause wording.

## Original return (verbatim)

**Verdict: acceptable with minor corrections.** The scope and the headline result hold. Several claims in the changes record are not backed by the retained files.

Verified:
- `git diff HEAD^ HEAD` touches only the four `issue349-image-scan-correction1-*` files, all under `.copilot-tracking/`.
- There is no non-tracking diff between `0fe8c3be` and `HEAD`, so no Dockerfile, runner or trivy config change.
- All four `*-gate.json` reports have 0 fixable HIGH/CRITICAL findings.
- The api and importer `versions-*.txt` show openssl and libssl3 at deb12u2, with installed equal to candidate.
- The plain-build logs show `CACHED` layers.
- The gate1 directory mtime is 08:20:11, before the correction run started at 08:23, and no later file is newer.
- I did not check that the candidate worktree was clean.

**Medium: some claims have no retained evidence**
- The Trivy exit statuses were only echoed to the console by `run*.sh`, and the `trivy-*.log` files contain no exit code. "Exit 0 for all four" is supported only by the zero-fixable JSON.
- There are no `versions-orchestrator.txt` or `versions-agents.txt` files. The "installed equals candidate" claim therefore has evidence for api and importer only, not for all four.
- The plain-build version outputs (deb12u1 versus deb12u2) were printed to the console and not saved. The orchestrator and agents "deb12u1 before refresh" and "deb12u2 after refresh" claims cannot be checked from the files. For the same reason, api and importer reusing deb12u2 cannot be confirmed.

**Low: the root cause is inferred**
"Frozen before Debian published" is a reasonable inference from a `CACHED` upgrade layer, a no-cache build fixing it, and installed equal to candidate. It was not shown directly, for example by comparing the old layer's creation date. The "all four" scope is covered only because the other two images were separately rebuilt.

No whole-issue acceptance claim is made.

## Preserver notes

The Medium and Low findings are accepted as recorded in the changes record. The
Medium gap stands: missing version files and exit codes are not retroactively
created. The coordinator also rejected cache warming as the durable correction;
the follow-up cycle is recorded in issue349-image-no-cache-correction2-*.
