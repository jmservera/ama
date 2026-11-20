# Details: issue 73 requirement trace

Phase 1 matrix columns: Requirement, Status (Checked or Deferred), Check or reason. Check cells hold backtick `path::test_name`; several allowed separated by `;`.
Phase 2 test parses rows beginning with `| <ID> |` in the note; resolves paths from repo root.
Phase 3 commands: `python3 -m unittest tools.test_epic_73_requirement_trace`; cited src tests via `python3 -m unittest` with the PYTHONPATH from the repository instructions.
