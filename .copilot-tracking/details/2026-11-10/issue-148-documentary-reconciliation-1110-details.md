# Details: #148 documentary reconciliation (2026-11-10)

Plan: `.copilot-tracking/plans/2026-11-10/issue-148-documentary-reconciliation-1110-plan.md`.

* Manifest selection: the files directly in the bundle listed in the original `SHA256SUMS` plus `SHA256SUMS` itself, `steps.tsv` and the original runner `ROOT/run-148-current-image-proof-1110.sh` (outside the bundle). The empty `emptybin`, `emptyhome`, `fixture/` and `pkgsrc/` directories are excluded and named as not covered. Written with relative-to-bundle names by `sha256sum` run in the bundle directory; the output file lives in ROOT, outside the bundle and outside its own selection.
* Reconciliation note (`ROOT/evidence-148-current-image-proof-1110.final-snapshot-note.md`): what changed (only `steps.tsv`, gaining `DONE\n`, 5 bytes), when (after the 16:13:49.349 manifest write, at 16:13:49.350), both hashes, how derived (hash of the first 5748 bytes equals the original entry), and that the new manifest is an observation made at the current time, not execution-time attestation.
* Verification: `sha256sum -c` on the new manifest and a second check that the 48 non-`steps.tsv` entries of the original `SHA256SUMS` still pass. The original manifest stays failing for `steps.tsv`, kept as adverse evidence.
* Wording: replace "no RepoDigests" with the observed local `RepoDigests` (each equals the image ID digest) and state no registry resolution or deployment; replace "not reproducible" with "reproducibility not assessed (in-image `apt-get upgrade` and `--no-cache` mean it is untested)".
