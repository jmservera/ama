<!-- markdownlint-disable-file -->
# Details: full behavior evidence at abd6b3f5f (issue 1204, pass 7)

* Sandbox: .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001 holds run-state.md, test-design.md, test-log.md, test-review.md (lead-written, retained). Executor working repos live in /tmp/h1204/native-*; raw outputs and share transcripts are copied byte-exact into the sandbox with sha256 manifest.
* Design: one generic task subagent, harness default model, given the target path to inspect, the requirement list, and the black-box rules; it returns scenarios S-01..; it must not read .copilot-tracking or prior tests.
* Execution: one `copilot --agent ama-backlog-delivery-coordinator --model auto` child per scenario, read-only tools, wrapper-only text stating that all actions are described not executed. Negative control: a /tmp copy with S01 pause/unknown and S02 gate clauses weakened, run on the scenarios they affect.
* Grading: fresh generic task subagent, given the log, design, requirements and rubric only.
* Checks: unittest 97 with direct exit capture, git diff --check, source blob hash, ASCII on added files not required for transcripts.
* Raw copies are byte-exact (no whitespace normalization).
