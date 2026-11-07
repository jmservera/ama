<!-- markdownlint-disable-file -->
# Plan: current storage proof (issue 1204)

Written 2026-11-06 about 00:34Z UTC. Details in the matching details file.

* [ ] P1 Commit only these three prospective records; verify clean exact head.
* [ ] P2 Freeze inputs; inventory the whole .copilot-tracking (tracked, untracked, ignored, symlinks), size, ownership.
* [ ] P3 New unique owner-only external archive, streamed; full member readback; restore selected 68 to new empty scratch; compare manifest, f6b2984d blobs and current bytes; validate C and B (400) members against manifest.
* [ ] P4 Protected proof: all unselected current tracking bytes including report 005 and both tracked bundles, source blob, refs, /tmp/h1204; clean head/tree/status before and after.
* [ ] P5 Names-only credential hygiene over exact archived bytes of B (400) and C (68); list the four additional names.
* [ ] P6 Independent Review, external. All outputs external; no repository write after P1.

Stop rules: stop on uncertain credential match, changing or unreadable input; no prune, no self-approval.
