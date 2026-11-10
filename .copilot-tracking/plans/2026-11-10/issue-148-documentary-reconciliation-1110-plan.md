# Plan: #148 documentary reconciliation (2026-11-10)

Research: `.copilot-tracking/research/2026-11-10/issue-148-documentary-reconciliation-1110-research.md`. Details: `.copilot-tracking/details/2026-11-10/issue-148-documentary-reconciliation-1110-details.md`.

* [ ] P1 Preserve originals: copy the original handoff to a `.original-9450959` file outside git; leave the bundle, `SHA256SUMS` and runner byte-for-byte unchanged (record hashes before and after).
* [ ] P2 Build the external final-snapshot manifest `ROOT/evidence-148-current-image-proof-1110.final-snapshot.sha256` and a reconciliation note beside it, by a single `sha256sum` over the exact finite bundle file list; verify with `sha256sum -c` before describing it as verified.
* [ ] P3 Correct wording in the parent changes, details, critique and handoff (RepoDigests present locally, not remote evidence; reproducibility not assessed; manifest reference to the new snapshot). The parent review is left unchanged.
* [ ] P4 Record changes, one review, state; witness events; commit dated records only.

Stop rules: no product/tooling edit, no build, smoke, Docker call, rerun, cloud or credential use; no issue tick; any doubt keeps the original claim limits.
