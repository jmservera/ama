---
title: Issue 104 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* Children: #105 and #106 closed. #107, #108, #432 and #435 open.
* Merged and relevant: #602, #660, #709, #765 (#432 metering and safety path), #863 (#107 model-call bounds), #405, #514, #515, #516 (evaluation, briefing, employee AI deployment). Open PR #875 (#435 pitch outline) is not in scope.
* Existing proofs: `test_assistants.py` shows the five assistants leave the domain unchanged; `test_ai_tasks.py` shows review keeps `cases` unchanged for a summary. No test covers the retained paths (briefing, message, summary, priority, funding draft) against hostile model output, nor accept, edit and reject across them.

## Findings (2026-11-03, origin/main b855aec86)

* `Store.funding_draft` writes the draft text to `funding.draft` and moves `funding.status` from Not started or To prepare to Draft ready. It never sets Approved, Submitted or Confirmed; `funding_step` approve still needs a named human with financial authority and an evidence reference. The same transition happens on the template path, so it is a drafting step, not an approval.
* `Store.read_document` writes the model description to `document.summary` (filing note; no extraction into the case).
* `ai_priority` and `resolve_priority` store proposals and decisions in `recommendations`; the ranking policy output is unchanged.

## Slice choice

Epic criterion 3 (AI never approves, executes, ranks or mutates controlled records) has no regression proof on the retained paths. Smallest coherent slice: a store-level boundary test with hostile scripted model output. Test-only plus one mypy override entry; no security, infrastructure, SQL or deployment surface, so the focused tier applies.

## Unmet after this slice

* Stabilization checkpoint (#440 is open): not done.
* All child features closed or deferred: #107, #108, #432, #435 open.
* Criterion 3: proved for the retained text, priority and funding paths on the JSON store only; read_document path and the SQL store are not covered; the Draft ready transition is an open design question for the owner.
* Tokenomics: #432 not complete (owner-gated criteria remain; price source and OD-51 open). Cost stays Unknown. Enablement-limit criterion unproven here.
