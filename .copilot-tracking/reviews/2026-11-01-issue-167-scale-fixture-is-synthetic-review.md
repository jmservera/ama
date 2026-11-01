# Review: issue 167, per-record is_synthetic on the scale fixture

Execution: executed once, direct review of the diff. Outcome: conformant for the slice; criterion 2 not fully closed.

* Additive key only; named-key consumers (sensor backfill, agents, api) pass.
* Re-pinned hashes were recomputed from the generator, not hand-edited; households golden unchanged confirms isolation.
* Version bump is consistent across code, registries and READMEs.

## Routed follow-ups

* Owner confirmation of the mapping and deferrals (criterion 2 decider is the owner).
* Whether the private SN-01 register regeneration sits in #168 or is deferred.
* Pre-existing format drift in scale_fixture.py and progress_browser_check.py.

PR therefore uses `Refs #167`.
