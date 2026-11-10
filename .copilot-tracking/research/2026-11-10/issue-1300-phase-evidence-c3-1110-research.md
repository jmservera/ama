# C3 research: derived evidence destination inside candidate (2026-11-10)

Disposition: executed (direct reading plus actual repro record).
* Actual repro (Root, session file `1300-c2-derived-ancestor-actual-repro-1110.json`): evidence root = owned root, candidate = `<root>/issue-1300`; derived `<root>/issue-1300/events.jsonl` and `events.lock` fall inside the candidate; record launch exit 0; git status shows both untracked.
* Cause: `log_contained` (tools/rpi_phase_witness.py) rejects a root equal to, or inside, the repo, and a derived path escaping the root, but never tests whether the derived directory, log or lock resolve inside the repo. `log_paths` appends `issue-{N}` to the root, so an ancestor root whose child name equals `issue-{N}` lands inside the candidate.
* Fix scope: add a derived-destination containment test for directory, log and lock against the resolved repo. No relocation, ignore rule or deletion.
* Existing tests: ExternalEvidenceTests (31 total) cover in-repo root, symlink substitution, other worktree binding.
Planning Readiness: Ready.
