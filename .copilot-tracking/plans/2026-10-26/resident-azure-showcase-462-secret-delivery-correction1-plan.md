# Secret-delivery helper correction 1 (issue 462)

Written 2026-10-26T07:16Z. Honest chronology: the small code edits (items 2 to 4) and the environment probe were made before this file was written; this plan and its dispositions record them, not prospective sequencing. The earlier plan, changes and review files are unchanged.

## Research: SH-001 (zava_forward not importable in gate namespace env)

* `/tmp/ama-462-local-final-gate4/venvs/namespace` has editable `.pth` entries pointing at `/tmp/ama-462-local-final-gate4/checkout/src/*`, a snapshot that no longer exists. The failure is that retained-env artefact.
* `tools/rpi-checks.py` `namespace_static_infra` installs `-e src/<project>` for all five `PROJECTS` from the live snapshot into `<out>/venvs/namespace`, then runs `unittest discover -s infra/tests` with that Python. Existing infra scripts (`initialize-workbench-staff.py`, `private-cutover-proof.py`) already import `zava_forward` in the same way.
* Conclusion: no runner, workflow or dependency change is needed; the repository rule (install the distributions, no source-path injection) already holds in the real gate. Not mocked, no shared validator duplicate, tests not skipped. Retained envs were not modified.
* Proof: new env `/mnt/ama-rpi-gates/issue462-helper-correction1/venv` with the five editable installs from this worktree (plus ruff 0.17.1) runs the selected suite.

## Changes

1. Low1: `O_NONBLOCK` on the verifier-file open; a FIFO is refused by the regular-file check. Test: bounded thread, 5 s join, exit 1, no CLI call. Mutation (remove the flag) fails the test.
2. Low3: malformed-value test now uses `assertNotIn(bad, output)` for non-empty values.
3. Low4: README states a dry run is not what-if proof.
4. Low2 (ARM race) stays a residual; no atomicity claim.

## Critique

Bounded: a single independent review of this delta (below) serves as the one post-implementation review; no separate critique pass was run for this small, non-architectural correction. Not a repeat of the earlier critique.
