<!-- markdownlint-disable-file -->
# Research: PR 1295 stale resident-journey source references (2026-11-09)

* Task: `pr-1295-source-freshness` (parent `pr-1295-validation-correction`). Qualified native RPI agent, Claude Sonnet 5.5, worktree `docs/demo-recovery-pr1295-1109`.
* Research disposition: executed (fresh reproduction and a scratch dry run; C1 evidence is a pointer, not proof).
* Planning Readiness: Ready.
* Correction budget: cycle 2 of 5 total (C1 spent; no reset).

## Identities (read at start)

| Item | SHA |
| --- | --- |
| Frozen start HEAD (clean) | `6bcf10ee63518c0e157c73e42f574b1aae65b6d4` |
| Owner remote `origin/docs/capstone-cxo-story` (ls-remote) | `0bcf55da1d516c82567e6eb44357343054c69b76`, unchanged, ancestor of HEAD |
| `origin/main` (fresh fetch) | `d4d6827fe60be651cd922ab9656688c18c978e1d` (PR1222 merged) |
| Merge base HEAD / main | `b46a9ad9a9619db535368d1b2cbbddec8110e122` |

HEAD is not merged with main (not requested). No independent owner change, so no overlap to record.

## Reproduction

* `build-resident-journey.mjs --check` on this clean HEAD: exit 1, `Stale generated asset: resident-journey.excalidraw`.
* The same check on a `git archive` of `origin/main` `d4d6827f` (scratch `/tmp/ama-pr1295-c2/main`): exit 1, same assertion, recorded `"line": 21`. This is a baseline-red defect on current main, not a new application regression and not caused by this PR (C1 evidence retained: input changed by `ecb28815b`, #1283, before the merge base).
* `git diff HEAD origin/main -- docs/reference/research/company/agent-request-challenge.md` is empty, so the branch and main carry the identical changed input.

## Dry run (scratch copy of HEAD, generator without `--check`)

* Exit 0: 68 native elements, 15 two-line cells, five touchpoints, 22 source locators, 1600x560 bounds.
* Only `resident-journey.excalidraw` and `resident-journey.svg` are written by the generator. Changed lines in the native JSON are only `line` (48), `sha256` (98) and `localLink` (48) metadata fields for `agent-request-challenge.md` and `case_study_48_addendum.md`; the SVG differs only in its one `<metadata>` line. Element geometry, text and bindings are not in the diff set.
* The generator does not render the PNG. Rendering from native JSON is geometry/text only, so the PNG (`300656fc...`) should be byte-identical; this must be proven by an exact re-render, not assumed.

## Consumers of the two regenerated files

* `docs/capstone/source/assets/catalog.json` entry `resident-journey` pins `source_sha256` (SVG) and `source_native_sha256` (native); `sha256` pins the PNG (unchanged if the re-render is identical).
* `Invoke-Capstone.ps1 Build/Verify`, `Test-SourceHashes.ps1` and `validation.json` (catalog and candidate hashes) depend on the catalog and the PPTX. Whether PPTX bytes change is to be observed: only the PNG is embedded as `ppt/media/journey-resident.png`.

## Adjacent observation (not in scope)

* `docs/capstone/source/diagrams/discovery-journey/text-equivalent.md` row R09 links `agent-request-challenge.md#L21`, `#L241`, `#L315`; the headings are now at 33, 253 and 327. These hand-authored links are within file length, so no check fails. They are journey narrative/handoff text, not generated, and this cycle is generation-only. Recorded for the coordinator/owner; not edited.

## Smallest-fix check

* Alternatives rejected: editing `agent-request-challenge.md` (source content, not ours); changing the generator to ignore line numbers (weakens the freshness check, a design change); waiving the check (forbidden).
* Selected: run the existing generator, update only the SVG and native hashes in the catalog, rebuild the deck and receipt with existing tools, and prove the diff contains only intended metadata changes.

## Not established

* Native PowerPoint, AT, projector, rehearsal, whole-deck visual acceptance, notch semantic decision (owner).
