# Changes: #148 documentary reconciliation (2026-11-10)

Status: complete. Documentary/evidence only: no product or tooling file, no build, smoke, Docker call, rerun, cloud or credential use. Parent frozen head `9450959bacb0e0f1eff7238b749a5cb1108539d0`; source `64c3f9191a2ffa97ef2dc07245422333ad4d6585`; source counter 1 of 5 unchanged; no issue tick; #148 criterion 4 not claimed.

## Finding 1: RepoDigests wording (done)

* Observed: `inspect-{api,agents,orchestrator,importer}.json` each hold one `RepoDigests` entry `zava-forward-<p>@sha256:<image id>`, equal to the image ID. Local Docker metadata for locally built images; no push or pull, so no remote publication, resolution or deployment is evidenced.
* Corrected in place with dated notes: parent changes (heading and a new paragraph), details (digest and reproducibility bullet), critique F1, external handoff (original kept as `ROOT/handoff-148-current-image-proof-1110.original-9450959.md`). "Not reproducible" became "reproducibility not assessed".
* Parent review R4 ("not reproducible and have no registry digest") is preserved unchanged as the original review finding; this record supersedes its reproducibility wording. Original wording remains in git history at `9450959b`.

## Finding 2: manifest ordering (done)

* Preserved unchanged: bundle `ROOT/evidence-148-current-image-proof-1110/`, `SHA256SUMS` (sha256 `77a7fe62...9496`), `steps.tsv` (`068bec06...e788`), runner (`a337784b...4db7`); hashes before and after this work are identical.
* New external files: `ROOT/evidence-148-current-image-proof-1110.final-snapshot.sha256` (50 entries, not listing itself) and `...final-snapshot-note.md` (what changed: `DONE\n`, 5 bytes appended to `steps.tsv` after the manifest write at 16:13:49.349Z, at 16:13:49.350Z; hashes; limits).
* Verified before description: `sha256sum -c` of the new manifest in the bundle directory: 50 OK, 0 failed; original manifest minus the `steps.tsv` line: 48 OK; hash of `steps.tsv` without its last 5 bytes equals the original entry `200575e9...b91e`.
* Limits: a current-time observation of exactly those 50 files, not execution-time attestation; `fixture/`, `pkgsrc/`, `emptybin/`, `emptyhome/` and witness logs are not covered. The original manifest still fails for `steps.tsv` as adverse evidence.

## Unchanged limitations

Dry-run network use unobserved; container IDs not captured; default-network egress and no memory bound in the smoke; no registry, Azure, deployment, SQL, security or CI evidence.
