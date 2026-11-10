<!-- markdownlint-disable-file -->
# Plan: bounded evidence corrections (issue 1204)

Written 2026-11-06 about 00:16Z UTC. Details: .copilot-tracking/details/2026-11-06/coordinator-evidence-corrections-1204-details.md. Critique: none separately; the one-pass gate is the planned independent Review. No source, frontmatter or tools edit.

* [ ] P1 Fresh generic design (content only) covering the actual AC1-AC6 behaviors and changed S01/S02 behavior, with mandatory expiry/revocation plus independent action, fresh quantified approval routing without re-asking, and R8 proof-absent case. Lead writes test-design.md and run-state.md with frozen expectations before execution.
* [ ] P2 Execute all accepted real-source scenarios freshly on `--model auto` in the existing method. Direct exits, strace identity, actual model per run. No controls repeat, no third batch.
* [ ] P3 Fresh independent grader (content only) grades all new evidence and required coverage; lead writes test-review.md.
* [ ] P4 Sidecars: corrected model-ID index for the 22 historical runs; m1.diff qualification and replay mapping.
* [ ] P5 Storage proof preparation (copy only): inventory, bounded credential-hygiene check, full snapshot archive outside checkout, readback, restore of the 68 selected members, protected-byte comparison, receipt; copy-only preservation of the 134-file run 002 set and new-run raw; tracked bundle only if the hygiene check passes.
* [ ] P6 Report 005, Changes, dedicated RPI Review, state, focused checks, new commit(s).

Stop rules: Partial on missing required scope or true failure; no automatic third batch, no source edit, no prune, no replacement; range `git diff --check` stays OPEN until approved replacement.
