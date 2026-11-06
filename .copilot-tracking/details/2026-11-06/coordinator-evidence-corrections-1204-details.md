<!-- markdownlint-disable-file -->
# Details: bounded evidence corrections (issue 1204)

Written 2026-11-06 about 00:16Z UTC, before implementation.

## P1 design contract (given to the designer, not the executor)

Return content only: design ID, scenario IDs, black-box prompts free of target name, path, internal headings, policy numbers and expected answers; requirement and AC mapping; coverage expectations; gaps. Must include: idle/stop after fresh classification with unknowns (AC1); every tick advances a real action and a bounded closure-review batch (AC2); expired approval or revocation refused while independent work continues, and freshly granted quantified approval routed without re-asking (AC2); one question at a time (AC3); approvals tracked and routed before all-complete (AC3); schedule replacement order and exactly one recurrence each (AC4); briefs forbid premature publication and keep parent targets, no stale templates (AC5); cleanup finite selection and active receipt/image ownership, wildcard refusal (AC5); eight issue assignments including exited workers with unpublished candidates, published-only paused slot released only with proof, proof-ABSENT and squash cases requiring identity, ignored status, unpublished and tree proof before release, Unknown upstream not zero; applicable HVE evidence blocks publication, backend-only does not; no simulation-as-native upgrade; PR drain 20 to 10-15; tier choice; single heavy holder; no gratuitous rebase.

## P2 method

Same runner method (strace -P own agent path, `--model auto`, read-only tools, no built-in MCPs, opaque cwd with byte-exact copy of the real source, stdin /dev/null). New run directory /tmp/h1204-r4. Executor receives only wrapper plus scenario.

## P4 sidecar methods

Model IDs: parse the existing share transcripts for the model line; record each share hash and the extraction rule. m1 replay: recompute `diff -u real-copy mutant-copy` from the stored byte-exact copies, compare to committed m1.diff, report the whitespace difference.

## P5 storage

Snapshot archive path under ~/.local/share/ama/tracking-archives/ (new unique owner-only file, no overwrite). Members listed with type, mode, size, sha256; symlinks recorded by link text, never followed. Restore into a new empty external directory; compare every selected member and protected files; write a receipt. Credential hygiene: bounded pattern check printing file names and counts only.
