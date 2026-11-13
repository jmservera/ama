---
title: Issue 157 memory-as-evidence boundary plan critique
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Execution and verdict

One independent critique (rubber-duck agent, claude-sonnet-5.5, read-only, with a throwaway in-memory feasibility run that wrote no file) of the final candidate plan, executed once. Original verdict: Revise. It confirmed the gap is real (no test reaches the chat `proposals` 202 success path), found no promotion path (`invoke` receives only capability and case id; `assistants.py` has no chat or memory reference; citations must be keys of `snapshot["citations"]`; `_clean_evidence` refuses `CM-` ids), and confirmed the path is feasible in `ApiTests` with no extra release record.

## Original findings and dispositions

* PC-001 (blocking): step 6 `domain()` equality fails because it includes the audit chain, which the chat route extends. Applied: compare only case-record slices (cases, procurement meta, recommendations, staff), not audit; also assert the proposal is `ready`, not accepted and not relied on.
* PC-002 (blocking): the `Provider` double cannot cite a memory id and records no prompts. Applied: wrap `provider.evidence` in the test to record system and prompt text and, for the citation case, return a proposal citing the memory id; assert not `ready` using the same fields the existing `bad="citation"` test checks; two provider calls in total.
* PC-003 (non-blocking): output-side canary absence is weak. Applied: scan the whole serialised task detail and the recorded prompt, keep the step 1 liveness assertion (memory is active and stored verbatim).
* PC-004 (non-blocking): `MssqlApiTests` inherits the method. Applied: use only `self.request`, `self.service` and `self.store` public calls; the inherited MSSQL variant is skipped without SQL Server and was not run.
* PC-005 (non-blocking): environment isolation and canary redaction. Applied: `patch.dict(os.environ)` around every request; canary with no phone or email shape; assert stored memory equals the canary. The venv installs this worktree's distributions in editable mode (path checked), so no source `PYTHONPATH` is used for the packages.

No user decision was required and the critique was not repeated.
