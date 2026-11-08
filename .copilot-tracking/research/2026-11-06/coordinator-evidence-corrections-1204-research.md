<!-- markdownlint-disable-file -->
# Research update: bounded evidence corrections (issue 1204)

* Written 2026-11-06 about 00:16Z UTC (file mtime governs), before any new harness, scratch-copy, model or archive action. Starting state: HEAD b920c5a1d020fdc5be72f4b22250b767cdaed9d8, tree ad4df19dcae2f3c53a02a4e2e8f3fda6d0255a1a, source blob acefb44a4d254ede6d86413343127b763dec42cb, clean. Research disposition: reused plus bounded known-target reads.
* Parent: 1204-behavior-fresh-full (report 004, real source Pass, open B7). Report 004 and all 001/002 records stay byte-identical.

## Findings from known records

* Issue AC2 requires that expired approvals and freshly granted approvals are reconciled without a global stop. Report 004 left R3 expiry untested and R8 proof-supplied only. Both are real acceptance gaps. The design changes (new cases), so a correction run with reuse is ineligible: a full fresh design, full fresh real-source execution and full fresh grade are required (Flow step 3). Report 004 grades are historical.
* The 22-run controls (M1 cap, M2 HVE gate, M3 unknown upstream) established source-dependent discrimination for the unchanged source and unchanged runner. They are historical and qualified, not repeated unless the runner, dispatch or fidelity assumptions change. If the runner changes, reassess.
* run-index 002 truncates the model column ("GPT-6" for 20 runs). A sidecar index will be derived from the share transcripts and raw hashes; the original stays unchanged.
* The committed mutants/m1.diff differs from the generated diff: a whitespace-only context line was edited before commit (native log). m1.diff is a generated derivative, not executor output and not a source input. Source inputs are the byte-exact copies k7q/p4w/r9d/t2x (hashes in report 004). A replay mapping (diff of real copy to each mutant copy, recomputed and compared) will be added as a sidecar. No claim of "no artifact normalization" is made.
* Storage: root conditionally approved the finite 68-transcript selection (manifest SHA256 643fb9ad..., 288862 bytes; exit-codes.json 609 bytes unselected) for proof preparation only. The new-run manifest (SHA256 51af7cac...) is approved for copy-only preservation. No replacement or prune is approved. The full retention policy was read in full in the earlier pass: finite manifest, full snapshot including untracked and symlink identity not followed, readback, restore into new empty external scratch, hash and protected-byte comparison before any removal. Disk: 35G free; tracking dir about 108M; 7549 tracked files.
* Credential hygiene: CLI log directories may hold tokens or headers. A bounded text check must pass before any binary bundle is committed; uncertain files are named and not committed.

## Method constraints

* Executor: native `--model auto`, read-only tools, no built-in MCPs, opaque cwd, strace on the single agent path, stdin /dev/null, direct exits, no pinned tier. Designer and grader: generic subagents on harness defaults, content only, lead writes the sandbox. No quoting or extraction prompts.
* Limits: text-only emulation; autoTier unknown; canonical profile unresolved; one run per scenario.

## Planning Readiness

Ready.
