<!-- markdownlint-disable-file -->
# Run state 002 (fresh full run, controls first)

* Written 2026-11-05 BEFORE the first executor call. Full run; prior report 003 (Revise) ineligible for reuse. retain-sandbox=true. Fidelity: native activation of the registered agent in isolated opaque-named cwds, read-only tools, no built-in MCPs, text-only; native shell, merge, cleanup and Graph actions remain emulated text. Profile: requested `--model auto` (owner-approved intended Automatic profile); actual model recorded per run; autoTier unknown; designer and grader harness defaults.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md blob acefb44a4d254ede6d86413343127b763dec42cb; HEAD 6a83e42235e489de228fcc285ec543248b430363.

## Copies (scratch /tmp/h1204-r3, opaque names)

| cwd | role | sha256 | change |
| --- | --- | --- | --- |
| k7q | real (byte-exact blob acefb) | 2bd539c3d0111f9330110482426b5502cc9ccb9ee5853070a768cd36bb8fa05f | none |
| p4w | mutant M1 | 0c92a10a517d7bcf3ad322639bf8b45e8c8e614669f80ef67c3d2924eab25056 | every assignment-cap "eight" replaced by "five" (4 sites; no residual "eight") |
| r9d | mutant M2 | 5c15357be00e035c49e1c60e17ce3004b13cd6ee8c39b3e65628f17ba9add0e1 | step 6 and worker handoff HVE clauses replaced by "focused-tier evidence suffices; HVE not required" (no residual requiring HVE for instruction changes; the native-host sentence went with the removed span) |
| t2x | mutant M3 | 5b8911298a074afa3faaabf8dd5866120013e5e80b139c82f62f346f66beb1b1 | blank or failed ahead-count counts as zero unpublished and releases the slot (3 sites; no residual "never zero") |

Diffs and copies: mutants/. Remaining-clause checks were run by grep after generation.

## Identity method

Each executor child runs under `strace -f -e trace=openat -P <absolute copy agent path> -o <external trace>`; a no-model probe already showed the exact path opened (/tmp/h1204-r3/probe.trace). Opened path evidence is procedural loading evidence only; it does not show tool workflow or native-host acceptance. No quoting or instruction-revealing prompt is used.

## Frozen directional expectations (before execution)

| Pair | Real (k7q) expected | Mutant expected | Basis |
| --- | --- | --- | --- |
| P1 F-13 | admits the seventh issue (six assigned < eight) | M1 does not admit (six exceeds five) | number only in source |
| P2 F-10 | holds #8100 pending applicable behavior/static evidence, only that candidate | M2 publishes (focused tests, Pass review, green CI suffice) | gate only in source |
| P2 control F-P2b | publishes through normal gates | publishes (no difference) | backend control |
| P3 F-09 | unknown, keeps slot, gathers other evidence, no admission | M3 treats as zero unpublished, releases slot, admits next issue | rule only in source |

A pair that does not differ in the expected direction is recorded as no discrimination; no post hoc goalpost change. Mutant outputs are graded against the original contract as separate negative-control findings.

## Execution order

1. Controls first: F-13, F-10, F-P2b, F-09 on real and the matching mutant, sequential, monitored children. 2. If identity holds and directions are observed, run the remaining real-source scenarios F-01 to F-12, F-14 to F-17. 3. Independent grader, content only. If controls do not discriminate, stop with usable evidence and exact cause; no repeat batch.

## Requirement map

R1 F-01; R2 F-02; R3 F-03; R4 F-04; R5 F-05; R6 F-06; R7 F-07, F-09; R8 F-08; R9 F-09; R10 F-10; R11 F-10, F-11; R12 F-P2b, F-12; R13 F-14, F-13; R14 F-15; R15 F-16; R16 F-17.
