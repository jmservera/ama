# Critique: #152 manifest aftercare navigation (1433)

Execution: one independent `rubber-duck` pass before any edit. Verdict: Revise.

* Root cause confirmed: editable installs import `workbench.py` from the stale checkout `/home/azureuser/source/ama`; all workbench tests pass with the worktree on `PYTHONPATH`.
* Blocking: the proposed import-path guard would reject legitimate wheel-installed runs and would not detect stale `core` imports.
* Disposition: applied. Outcome is evidence only; no navigation, manifest or guard change.
