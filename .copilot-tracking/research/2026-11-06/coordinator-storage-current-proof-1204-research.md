<!-- markdownlint-disable-file -->
# Research addition: current storage-proof readiness (issue 1204)

* Written 2026-11-06 about 00:34Z UTC, before any proof action. Start HEAD a4b6ab28d08baf56ab469c835687590f38fb99ca, tree f60f9b19930a0f63d9082590d1a73252a55be041, source blob acefb44a4d254ede6d86413343127b763dec42cb, clean. Parent: 1204-evidence-corrections. Earlier records unchanged.
* Gap 1: archive A (7559 members, sha256 767ba72f...) predates the final receipt, both tracked bundles, report 005, review and state. It is valid historical preservation, not the current a4b6ab28 tracking snapshot required immediately before any removal. Original A, its inventory, receipt.json and the receipt with the column-check bug stay byte-identical.
* Gap 2: the receipt says 396 files were scanned before the final run files were added, while bundle B has 400 members. "All 400 clean" is not established. Scan the exact archived member bytes of B (400) and C (68), names-only, no values printed.
* Selection stays exactly 68 files, 288862 bytes, manifest SHA256 643fb9ad14b44cf3e3b4e32d481c5646d8ff1c45f5d4527b259748375b309047; exit-codes.json unselected.
* Constraints: no new models or behavior runs; no prune, removal, replacement or normalization; after the commit of these three prospective records, no repository or tracking write; proof, script, inventory, hygiene and review outputs go external. Planning Readiness: Ready.
