# Critique: issue 107 material-binding process plan

Date: 2026-11-12. Independent critic: `rubber-duck` subagent, model `claude-sonnet-5.5`, one pass on the final candidate plan. Verdict: Revise. Raw return preserved below without edits.

## Raw independent return

**Verdict: Revise.** The design is sound and the core semantics check out. A few assumptions are unverified, and several assertions need tightening.

**Checked against source and correct**
- `invalidate_changed` persistently revokes an active record on a trigger mismatch, with `system=True` and an `invalidated` cause (`assistant_release.py:85-99`).
- A `ReleaseDenied` denial still commits (`assistants.py:~668`).
- `disabled()` calls `admission` before the pool check (`assistants.py:829`), so `p` is denied before any allowance is reserved. "Attempts 0, no pool change" is therefore plausible.
- `RULES[cap]`, `REGISTRY[cap]["purpose"]` and `REGISTRY[cap]["roles"]` each feed only `policy_version`, `prompt_version` and `permission_version` for that capability (`assistants.py:415-425`).
- The existing revocation test is operator-driven (`test_assistant_release.py:1135-1175`), so the system-invalidation cause is genuinely new coverage.

**Findings**

1. **Medium, unverified premise: ZF-2 as a second stock proposal.**
   - The research does not show that `invoke(pm, "stock-prioritisation", "ZF-2")` returns a pending task. `snapshot` can return None for an ineligible case.
   - It also does not show that `c1`..`c3` (the "distinct unrelated capabilities") are invocable on ZF-1.
   - Existing tests only use `list(REGISTRY)[:3/4]` on ZF-1 (`:1080`, `:1119`) and `run_ready("stock-prioritisation")` on ZF-1.
   - Fix: do not invent ZF-2. Safer `held`: the same capability and the same ZF-1 case, if the dedup and schedule rules allow it. Otherwise, probe ZF-2 first and record the result. Choose `c1`..`c3` from `list(REGISTRY)` excluding stock. Confirm that the PM role is in each one's `roles` (all five include PM, `assistants.py:38-48`) and that each snapshot is non-None. Confirm that `p` and `held` do not collapse into one task.

2. **Medium, weak assertion on `held` in the fresh wave.**
   - `False` plus "disabled" would also pass for allowance exhaustion or an "activation release changed" denial (`assistants.py:1356`).
   - Fix: Assert `reason.startswith("Release admission denied")`. Assert that the denial names the invalidated fields, ideally via `rel.invalidation_cause`, with the expected trigger (`policy`, `prompt` or `permissions`) for each variation. Assert that `p`'s and `held`'s reasons differ in trigger text, not just in status. Check that the allowance in the fresh wave is not exhausted (`used_calls` 2 < the larger limit). The plan's "larger allowance" already helps here.

3. **Medium, the "revoked by a system invalidation" assertion must be specific.**
   - Assert the stock record's `revoked_by`/`system` marker, and that `invalidated.triggers` equals exactly the one expected trigger. The roles variation must yield `["permissions"]` only. The rule variation must yield `["policy"]` only. Do not assert a loose superset. Assert that the unrelated releases have no `invalidated` key, not just `active`.
   - Fix: parametrise the expected triggers per variation in the helper.

4. **Low, the "control" wave isolates less than claimed.**
   - It runs an original-binding worker on `c1`, but it does not show that the original worker would have run stock successfully.
   - Fix: either run the control wave on stock (`p`) and accept the extra consumption, or state that the premise rests on the existing fixture tests.

5. **Low, cost and flakiness.**
   - 3 variations x 3 child processes, each with the SQLite barrier startup, is about 9 spawns per run. The MSSQL inheritance multiplies this. `ProcessRaces` is a subclass of `UnleasedRevocation`, so the new methods are also inherited by `MssqlUnleasedRevocation` and skipped.
   - Fix: use a single helper with `subTest`, or limit to one or two variations in the MSSQL selector. Confirm the skip really applies.

6. **Low, the worker `variation` spec.**
   - The patching must be applied before the `Assistants` object is built and before any claim, and must be reverted or confined to the process. Do not patch `RULE_VERSION`/`SYSTEM`/`PROVENANCE`: they are global and would break `c2`. Verify that `REGISTRY[cap]["roles"]` is a tuple. Replace it, do not mutate it. Reject unknown kinds, as already planned.

7. **Scope and honesty (OK, with a caveat).**
   - There is no old-image claim. Keep every test name and docstring saying "constructed runtime-binding variation". Do not use "old image" or "stale image" in commit text or test names. The SQLite-only execution is correctly disclosed, with MSSQL labelled "not executed". The commit's `Refs #107` and `Refs #104` is fine. Make sure the message does not say the composite criterion is "closed".

**Required corrections:** items 1-3 before coding. The mutation proof should also cover item 2: it should fail if the fresh wave's `held` were denied for a non-revocation reason.

## Dispositions (author, no repeat critique)

* 1 accepted: ZF-2 is not assumed. The helper uses ZF-1 only. `held` is a second stock proposal if distinct on ZF-1 is possible; otherwise a proposal the changed worker never claims is obtained by invoking `p` while the changed worker's task list excludes it. The simplest compatible form: one stock proposal `p` is executed by the changed worker (denied and system-revoked); a second distinct stock task is not required because the fresh original-binding worker re-invokes nothing: instead the test calls `service.invoke(pm, stock, "ZF-1")` after the change from the test process (original binding) and runs it in the fresh worker. Probed and recorded before coding; fallback documented in the changes record. Unrelated capabilities are taken from `list(REGISTRY)` excluding stock, all with PM in roles.
* 2 accepted: reason prefix, per-variation invalidated trigger and not-exhausted allowance asserted; the mutation check also covers it.
* 3 accepted: exact trigger list per variation (`rule`->`policy`, `purpose`->`prompt`, `roles`->`permissions`), unrelated records without `invalidated`.
* 4 accepted: the premise that the original binding runs stock successfully rests on the existing `run_ready`/fixture tests and is also shown by the `fresh` wave positive control on an unrelated capability; stated, not over-claimed. The control wave is retained as the baseline pool.
* 5 accepted: one helper, three short methods; the MSSQL class inherits them and they skip without `ZF_TEST_MSSQL=1`.
* 6 accepted: variation applied in `main` before `Assistants` creation; process-confined; roles replaced by a tuple.
* 7 accepted: names and commit text use "constructed runtime-binding variation" and "changed-binding process"; no old-image, closure or acceptance language.

## Pre-implementation probe (finding 1)

Run from `src/api` in the worktree venv: the pm fixture invokes every registered capability on ZF-1, ZF-2 and ZF-3 and each returns a distinct `pending` task (stock-prioritisation ZF-1/ZF-2/ZF-3 ids 84ff89f3, 97ca2ba6, 40f11f6a). So `p` is stock on ZF-1 and `held` is stock on ZF-2; the fallback in disposition 1 is not needed. The probe module imported the whole release test module, so its output also ran those tests (55 tests, OK, 4 skipped). Probe file `/tmp/probe107.py` is deleted at close.
