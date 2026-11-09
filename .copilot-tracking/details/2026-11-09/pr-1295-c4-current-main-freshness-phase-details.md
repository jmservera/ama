<!-- markdownlint-disable-file -->
# Phase details: PR 1295 C4 (2026-11-09)

## Phase 1

* Confirm clean tree, then `git merge --no-ff 23e944c1fccf0c4578e7beb0740ddd55c3f935b2 -m "chore: merge main into PR 1295 recovery branch"` with the repository-local noreply identity and Copilot trailer. If overlapping `docs/reference/README.md`, `docs/reference/log.md` or `docs/architecture/cutover-evidence-pack.md` conflict, keep both sides in order and record it. Confirm `0bcf55da1` and `292d0091a` remain ancestors.

## Phase 2

* From `docs/capstone/source/diagrams/architecture`: `node build-architecture.mjs --check`; from `docs/architecture`: `node update-architecture.mjs --check`; from the journey folder: `node build-resident-journey.mjs --check`. Then `node test-architecture.mjs` and `node test-geometry.mjs`, and `Test-SourceHashes.ps1` with an isolated PowerShell if present.
* Each command has its own log and exit code under the scratch folder `/tmp/ama-pr1295-c4`; the first failing run is kept as adverse evidence.
* Locator check: for each bound source of the architecture and journey generators, recompute the line of the anchor and the whole-file SHA-256 on the merged tree and compare with the stored metadata.

## Phase 3

* Run the generator without `--check` only for the diagram set that failed. Compare before and after: `.excalidraw` JSON element structure and text, SVG geometry attributes, PNG SHA-256. If only evidence locators and hashes changed, the diff is limited to those; PNG bytes equal means no rerender. If a PNG would need re-export, check whether the PNG is a deck input; deck inputs force a stop under the stop conditions, not an automatic rebuild.
* Update `text-equivalent.md` locators and `docs/architecture` metadata only where the generator output or hash check says so.
* Check whether `validation.json`, source hash receipt or catalog bind any refreshed file (grep for the path and hash); refresh only entries that no longer match.

## Phase 4

* Add a short dated qualification in the architecture guide only if the merged text now misstates the current-versus-baseline relation. Append one KB log entry and update the KB index only if a KB file changes materially.
* Write changes record, review record and state JSON under `.copilot-tracking/`.

## Phase 5

* Re-run all Phase 2 commands to green with separate logs; summarize counts and exits. No full gate.
