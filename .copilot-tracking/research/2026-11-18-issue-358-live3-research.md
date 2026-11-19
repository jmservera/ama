# Issue 358 live pass 3 research

Task: issue-358-live3. Mode: automatic. Research disposition: executed (reuse plus gap closure).

## Existing evidence

* `docs/reference/research/issue-358-live-evidence-2026-11-18.md` and `issue-358-live-recheck-2026-11-18.md`
  record criterion 1 (tests, mutation), criterion 2 (throwaway live round trip) and criterion 3 (delegating main).
* Gaps they state: the baseline test run, the mutation baseline and the deletion check have no retained raw output;
  the demo app Key Vault reference was observed but not retained.

## Planned evidence gaps to close

1. Retain raw `unittest` output for `infra/tests/test_setup_entra.py`.
2. Re-run the expiry-guard mutation on a scratch copy (no source edit in the worktree) and retain output.
3. Retain read-only ARM listing showing `ca-358-throwaway` absent and the demo API Key Vault reference (names only).
4. Retain delegation source lines and test result for criterion 3.

## Planning Readiness

Ready. No src change expected; any need is recorded as a full-tier follow-up.
