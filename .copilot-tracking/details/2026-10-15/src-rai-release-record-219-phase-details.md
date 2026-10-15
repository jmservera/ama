---
title: Phase details - task-bound RAI release records
description: Issue 219 task ownership and completion evidence
ms.date: 2026-10-15
---

## Context

Task 219; same slug/date as the plan. Research C3-C7 confirms existing
assistant_releases SQL tables, admission checkpoints and JSON bypass.
No additional planning delegation: one coupled trace; independent critique only.
Implementation status: P01-T01/P01-T02 and P02-T01/P02-T02 complete.
Changes artifact holds all local commands/results and explicit unrun gates.
The single Review executed Complete with outcome Not accepted. Execution
markers describe performed work, not accepted engineering behavior:
RV-001/RV-002 block reliance guarantees and RV-003 blocks briefing recovery.
No second Review or source-fix cycle occurs within this completed RPI task.
Publish draft with these findings and unavailable human/live evidence explicit.

<!-- P01 -->
## P01 - Extend and wire the release contract

<!-- P01-T01 -->
### P01-T01 - Contract and matching

Extend existing record body, not SQL schema. An unexempt typed rai_release helper validates the
contract and hash the current registered task's use/impact/evaluation protocol
binding. Unknown owners or empty evidence cannot count as approval.
Actual evidence still needs explicit expected serving model configuration;
deployment aliases do not prove model identity. Constructed fixtures remain
clearly labelled. Record unavailable live holders, do not invent people.
Completion: all bound fields and contract omissions have negative controls.
Canonical ai_prompts templates own the actual static instructions (including
priority/document and citation suffix); their hash is shared by binding/output.
Supersession is task-wide, including routing changes. One release approves one
deployment; a task's fast/strong routing change requires renewed approval.

<!-- P01-T02 -->
### P01-T02 - Activation and invalidation

Reuse assistant admission at enqueue/claim/pre-dispatch/completion/review.
Bind selected record identity/digest, not merely any active release's returned
model. Superseding evidence/use records must invalidate dependent proposals
without losing old events. Legacy gates reuse shared selection and persist
denials. Outputs expose release ID/version; changes during calls quarantine.
JSON configured inference denies explicitly; manual/templates remain available.
Completion: zero-call tests for mismatch; revocation/supersession races;
cross-task isolation and unchanged controlled-domain state.
Include cached briefing reads, priority views and accept/edit, ordinary/document
accept/edit, and replacement during a call. New release IDs enter deterministic
assistant activation identity so renewal does not mutate old work.

<!-- P02 -->
## P02 - Evidence and documentation

<!-- P02-T01 -->
### P02-T01 - Local validation

Run smallest release tests first, then all src suites with documented fixture
paths. Use existing pip dev dependencies only if commands report missing tools.
Run ruff check/format and mypy per project, migration regression if relevant.
Run actual local App/HTTP over a wholly synthetic fixture with model test double,
assert denied calls=0 and allowed proposal is unapproved; never call it live AI.
Attempt Docker build, record actual permission/tool result. No deployment.
Record command, cwd, exit/result and limitations in the changes artifact and PR.
Strictly checked new files: src/core/src/zava_forward/core/rai_release.py and
ai_prompts.py, plus new typed tests. Run core ruff check/format and mypy with
existing config: these new modules have no migration exclusions. No broadening
exemptions; distinguish unchanged exempt integration glue.

<!-- P02-T02 -->
### P02-T02 - Documentation and Review

Document payload/configuration and live gaps in owning READMEs; update reference
index and append log without changing memory. Reconcile plan markers, changes,
validation and criteria; one post-implementation Review. Required human/live
approval remains unchecked. Commit all task artifacts, push only topic branch,
open main PR with Refs #219 and command evidence. No merge.
