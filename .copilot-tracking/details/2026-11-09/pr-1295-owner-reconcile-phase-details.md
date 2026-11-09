<!-- markdownlint-disable-file -->
# Phase details: PR 1295 owner-head reconciliation (2026-11-09)

## P1 Refresh

* `git fetch origin`; require `origin/docs/capstone-cxo-story` = `0bcf55da1d516c82567e6eb44357343054c69b76` and run HEAD `1d831ab3`. Observed equal at start.

## P3 Merge

* `git merge --no-ff origin/docs/capstone-cxo-story` with a Conventional Commit message and Copilot trailer. Dry run (`merge-tree`) was conflict-free. If a conflict appears, abort the merge and report the exact paths; do not drop owner source.

## P4 Proof

* Check merge parents are exactly `1d831ab3` and `0bcf55da1`; `git diff --name-status origin/docs/capstone-cxo-story HEAD` must list only `A .copilot-tracking/...` (12 recovery files plus new owner-reconcile records); `git ls-tree` blob IDs of every owner-changed path equal remote.
* `git merge-base --is-ancestor` for `292d0091a`, `0bcf55da1`, `1d831ab3`, `b671116d`.

## P5 Commands (from the component README at the remote head)

* `Invoke-Capstone.ps1 -Action Build` then `-Action Verify` on a copy; `Test-NativeShapes`, `Test-SourceHashes -SemanticOnly` and default, `Test-DeckInsertion -CandidatePath`, `Test-CostStatus -CandidatePath`; `pytest tools/capstone/test_render_preview.py` in a scratch venv installed from `tools/capstone/requirements.txt`; `build-resident-journey.mjs --check`, `build-architecture.mjs --check`, `docs/architecture/update-architecture.mjs --check`, `node --test` on `test-architecture.mjs` and `test-geometry.mjs` with `EXCALIDRAW_BROWSER_PATH`; `render_preview` for the Linux preview.
* Record each exit, counts and skips. Missing-tool failure: restore only isolated prerequisite.

## P6 to P8

* SHA-256 of Build PPTX against delivered PPTX and receipt. Visual check of preview PNGs. Evidence goes to changes and review records; no scratch files are committed.

## Critique amendments (2026-11-09, one pass)

* P5: also Verify the delivered PPTX itself, hash the delivered PDF against the receipt, and compare regenerated pitch files (speaker script, Q&A) with delivered files; compare changed diagram PNG/SVG hashes with `assets/catalog.json` (the generator `--check` covers editable sources only; unverified otherwise).
* P6: on a PPTX byte mismatch, diagnose ZIP metadata/compression versus member-content differences first; record as a reproducibility finding.
* P8: carry the PR 1301 / issue 1294 merge-first prerequisite into the handoff; no publication.
