<!-- markdownlint-disable-file -->
# Research update: root decisions for the fresh full behavior run (issue 1204)

* Task: 1204-behavior-fresh-full, parent 1204-behavior-harness-diagnosis. Written 2026-11-05 before any scratch-copy, harness or model action. Prior research: [diagnosis](coordinator-behavior-harness-diagnosis-1204-research.md). HEAD 6a83e42235e489de228fcc285ec543248b430363, tree 57070e0fcafdea327d8a33b7a12bc88b1fd3af3b, source blob acefb44a4d254ede6d86413343127b763dec42cb (verified clean).
* Research disposition: reused (diagnosis) plus bounded known-target checks (strace presence, CLI help). The diagnosis is accepted by root as bounded facts and limitations, not a behavior Pass.
* Assignment accounting: 7 after the published-only pause of #440; this issue still counts and a worker exit frees no slot.

## Root decisions recorded (confirmed_decisions)

1. Fresh FULL canonical design and run; discriminating controls execute first as a precondition for the remaining real-source execution. Report 003 (Revise) is ineligible for reuse. Every real-source scenario in a new Complete/Pass must be freshly executed and independently graded; early failure is Partial, Deferred or Blocked, never an assumed old grade. No blind 21-case batch if identity or control fidelity fails.
2. No prompt asking the agent to quote its instructions. Identity evidence comes from CLI observability: a strictly exact-path-filtered own-child trace, `strace -f -e trace=openat -P <absolute owned agent copy> -o <external trace> <native argv>`, with fixed `--agent` name, minimal unique git cwd, before/after sha256 and blob, direct exit and the selected-model line. Trace only that non-secret owned file, no buffers. Limit: an open shows procedural loading, not tool workflow or native-host acceptance. A no-model metadata preflight is allowed; stop if the copy cannot be resolved safely.
3. Opaque cwd names; real copy is byte-exact acefb; mutants are coherent counterfactual copies with recorded diffs and remaining-clause checks. The executor receives only wrapper plus black-box scenario plus non-answer containment.
4. Designer and grader return content only; the lead writes the sandbox. Design covers the same 1204 requirements and gaps plus source-dependent pairs P1 (cap 8 vs 5), P2 (HVE gate inversion with backend control), P3 (Unknown-upstream inversion). Expectations are frozen before execution. Mutant outputs are graded against the original contract as separate negative-control findings. First execute only enough to confirm directional discrimination and identity; if none again, stop with usable evidence and exact cause, not another blind batch.
5. Originals, adverse outcomes, controls and the grader-role deviation stay unchanged. No SC-14 ceremonial requirement. A real-source failure becomes a separately planned correction. Scope changes are written prospectively before scratch edits; retain-sandbox=true.
6. Automatic profile already approved: `--model auto`, actual model per run, autoTier unknown; no pinned model, no invented tier, no native-host claim from text emulation. Designer and grader use harness defaults.
7. Executors run as normal monitored children (stdin /dev/null, direct exit and PID, no short top-level timeout), sequential or small bounded concurrency, no unbounded batch.

## Storage (not approved)

* Prior proposal was imprecise: 69 files exist under raw/ (68 transcripts plus exit-codes.json), and the earlier text mixed 69 and 68. Root requires an actual per-path manifest (path, type, mode, size, sha256, current blob, proposed action), a split of transcripts from exit-codes.json, protected records, and a raw-link and restore mapping, before any move.
* This phase writes the manifest as evidence only. No archive, normalization, deletion, suppression, gitattributes change or exemption. Range `git diff --check origin/main..HEAD` stays open and must not be masked by a clean-tree check.
* New run raw outputs go to a new external scratch by default; gradeable evidence needs durable promotion to the repo or an approved store, so external-only output is pending, not accepted. The VM is disposable, so nothing external-only is claimed persistent.

## Constraints

Lightweight remote-model, text and provenance only. No heavy gate, SQL, browser, Docker, scanner, build or cloud actions, no private data. Runner 2306020 owns the heavy lane. No push, PR, issue, schedule, global config or cleanup. New commits only, no amend.
