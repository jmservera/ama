# Research: provider input bounds for issue 116

Date: 2026-11-04. Disposition: executed. Planning Readiness: Ready.

## Delivered by merged PRs

* #275: role endpoint inventory and free-text note holding (ticks every-role-every-endpoint, contractor no-vulnerability-reason, free-text redaction decision).
* #205: RAI coverage record. #676, #277: contractor B2B design and identity as code.
* Closure audit 2026-10-31 (issue comment): C4 and C5 to C10 unmet.

## Unmet criteria

* OD-14/OD-19 role confirmation: human DPO/Legal decision; not an engineering slice.
* Provider-boundary criteria: partial; the single chokepoint is Ai._request in src/core/src/zava_forward/core/ai.py, used by run, _chat, evidence and look_at.

## Smallest slice

Unknown/excessive input and unapproved raw content (criterion 3): refuse oversized text before the meter or any provider call, and restrict look_at images to png/jpeg under 4 MiB. Manual route and storage unchanged. Not security, infra, SQL or deployment: focused tier.

## Stacked follow-on slices

1. Task/field allowlists and unknown-field refusal in ai_tasks.
2. Exact-payload provider-spy matrix per role and path.
3. Output, citation and error permission recheck.
4. Approved-derivative requirement for document AI.
