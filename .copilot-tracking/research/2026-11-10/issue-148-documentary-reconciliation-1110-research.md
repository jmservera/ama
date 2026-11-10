# Research: #148 documentary reconciliation of two Medium findings (2026-11-10)

Task `issue-148-documentary-reconciliation-1110`, same issue and branch as `issue-148-current-image-proof-1110` (parent). Research disposition `executed`; Planning Readiness `Ready`. Documentary/evidence-only; frozen parent head `9450959bacb0e0f1eff7238b749a5cb1108539d0`; validated source `64c3f9191a2ffa97ef2dc07245422333ad4d6585`; source correction counter 1 of 5 unchanged.

## Reviewer findings read (readiness-findings.json, verdict approve_with_comments)

* M1: the four raw `inspect-<project>.json` hold nonempty `RepoDigests`; the changes, details, critique (and handoff) say none exist.
* M2: `SHA256SUMS` hashes `steps.tsv` before the runner appends `DONE`.

## Independent observations (read-only, 2026-11-10 16:3x UTC)

* `grep` of the raw inspect files: `RepoDigests` is `["zava-forward-<p>@sha256:<image id>"]` for all four, each digest equal to the image ID in the `.iid` file. This is local Docker 29.9 (containerd image store) metadata for locally built images; no push or pull occurred, so it is not remote registry publication, resolution or deployment evidence.
* Wording to reconcile: changes line 19; details line 30; critique F1; review R4 (preserved as an original finding, corrected only through the new records); handoff lines 22 and "checksummed".
* "Not reproducible" was an unsupported assertion: reproducibility was never tested. Only the in-image `apt-get upgrade` and `--no-cache` make a bit-identical rebuild uncertain.
* Manifest: `SHA256SUMS` (49 lines) verifies all files except `steps.tsv` (`sha256sum -c` FAILED, one mismatch). The recorded hash `200575e9...b91e` equals the hash of the current `steps.tsv` minus its final 5 bytes (`DONE\n`); the current file hash is `068bec06...e788`. The runner order is `sha256sum > SHA256SUMS` then `echo DONE >> steps.tsv` (mtimes 16:13:49.350 vs .349). The defect is deterministic.

## Constraints

Preserve the original bundle, `SHA256SUMS`, runner, frozen commit and review. The new manifest is separately named, outside the bundle, excludes itself, and covers only the exact finite files it lists; it does not attest original execution-time bytes. No rerun or Docker mutation. Read-only `docker image inspect` is not needed: the captured raw files are the evidence.
