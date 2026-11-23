# Research: issue 2311 aftercare concern pack contract

Disposition: executed. Planning Readiness: Ready.

Earlier workers delivered the registry (a04f370c40), `ai_prompts.render` enforcement and chat enforcement. The last review left "assistant and concern-pack builders unrouted" as later work.

Findings (code read):

* `aftercare.AftercareRegistry.propose_pack` builds `facts` from the concern record (raised_by, kind, owner, investigation, remedy) and never calls `task_contracts.enforce`, although `aftercare-concern-pack` declares `concern_id` (64) and `facts` (8000) with prohibited content.
* No model call is made in that builder; the pack is template built, so the contract guards the recorded facts a later AI summary relies on.
* Assistant tasks route through `ai_tasks.run_text_task` with a prebuilt prompt; separate, larger change, left as later work.

Angle chosen: enforce the concern-pack contract in `propose_pack`, refuse before the pack is stored.

Criteria: all four are already proven by earlier work (see changes record). Owner-only items (DPO/Legal approval) are not needed and not claimed. Live Azure is not relevant to this core code path; not used.
