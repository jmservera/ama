<!-- markdownlint-disable-file -->
# Details: fresh full behavior run (issue 1204)

* Plan: [plan](../../plans/2026-11-05/coordinator-behavior-fresh-full-1204-plan.md). Written before any action.

## Phase 0 manifest

* A program lists every file under `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/` and writes a Markdown table with path, type, mode, size, sha256, git blob and proposed action (none until root approval), plus separate sections for the 68 transcript files vs exit-codes.json, protected records, and the restore mapping (source commit f6b2984d9dabc181ef784caadcf045bcbb69a24a). Output: `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-002/raw-storage-manifest.md` style evidence under a new run folder; raw files untouched.

## Phase 1 probe

* Scratch root `/tmp/h1204-r3/` (new). Opaque directory names. Copy agent byte-exact; verify sha256 2bd539c3d0111f9330110482426b5502cc9ccb9ee5853070a768cd36bb8fa05f.
* Try a no-model invocation first (for example an invalid model name, which should fail before inference) under `strace -f -e trace=openat -P <abs agent path> -o <trace>`; use `</dev/null`, capture exit directly. Parse the trace for the exact path only.
* If the agent file is opened only during a model-backed session, a single minimal native run is allowed under the approved Automatic profile; the trace is still filtered to the one path. If strace is blocked, stop and record it.

## Phase 2 to 4 details

* Designer prompt: return cases and coverage only, no file writes, cover R1 to R16 plus P1 to P3, scenario text must not name the target, rules or expected answers. Expectations (real vs mutant direction) are written by the lead into run-state before the first executor call.
* Mutants: M1 cap eight to five in every cap-bearing sentence; M2 coherent inversion of step 6 and handoff HVE clauses; M3 blank or failed ahead-count means zero and releases the slot. Each stored with a unified diff against the real copy and a grep proving no residual contradicting sentence.
* Executor argv: `copilot --agent ama-backlog-delivery-coordinator --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 60 --no-auto-update --log-dir <ext> --share <ext> -s -p <wrapper+scenario>` under the trace, stdin /dev/null, no timeout wrapper, direct exit.
* Raw outputs to `/tmp/h1204-r3/run/`; compact evidence plus manifest persisted in tracking.

## Phase 6 and 7 details

* Grader prompt: return content only; grade real-source results against the contract and mutant results against the original contract as negative controls, separately. Lead writes test-review.
* Review: one dedicated RPI review after phase completion; honest outcome, remaining gates (independent exact-head, published, hosted, owner approvals, storage approval, range diff check).
