---
title: Climate child blocked at owner reuse decision
ms.date: 2026-10-27
---

Refs #178, parent #177. Branch: docs/climate-reuse-178-stack.
Common base: e7d531c789dbaafafc05fb4cacf7d851e188cd58.

## Research and Source Decision

The canonical existing comparison is
`docs/reference/research/iot-sensor-analytics-research-plan.md`, Historical
climate evidence (2026-10-17). It compares HadUK, MIDAS, Durham, ERA5 and CIBSE
on coverage/resolution/access/terms, with exact official URLs and retrieval
dates. Preserve its gaps; do not copy facts into a newly invented licence.

The conditional selected context source remains HadUK-Grid regional monthly
v1.3.2.ceda, DOI 10.5285/386b3c1ee2054ef5ae0d73060963a9f1, metadata/terms
retrieved 2026-10-17. Its exact regional catalogue declares OGL v3 with dataset
citation. This is a context recommendation, not an adopted paired hourly
temperature/humidity history. Records were login-blocked.

For executable exercises only, retain the explicitly synthetic seasonal
fallback permitted by the owner's 2026-10-15 comment. Its numbers are exercise
assumptions, not climate observations or a dataset under OGL. No external
record or licence was adopted in this child.

Open PR #425 already owns the paired 2023 Open-Meteo ERA5/NASA POWER MERRA-2
demonstrator. Read on 2026-10-27, it reports unresolved owner reuse,
underlying C3S terms and NASA licence text. It is not merged and one year is
not the required two-year history. Do not duplicate its acquisition or import
it without review. The documentation-only fetched API page exposed citations
only; no new complete licence retrieval is claimed.

## Plan and Implementation Disposition

Stop this child as instructed for an owner decision. No source adapter,
climate download, private source access, account registration or terms
acceptance occurs. One issue comment asks for the exact source/reuse scope.
Other exercise-only children may proceed.

## Acceptance Audit

| Original criterion | Evidence and result |
| --- | --- |
| Compare coverage, resolution, licence and reuse | Existing comparison substantive but exact alternative terms/site gaps remain; not complete. |
| Chosen source, retrieval date and licence; owner confirmation open | Conditional context choice and synthetic fallback recorded honestly; no paired source adopted; owner reuse UNMET. |
| Temperature and RH bounds from retrieved records | Existing Durham temperature-only evidence is not RH; #425 paired 2023 report is unmerged/unapproved; two-year replay bounds UNMET. |

No original checkbox ticked, no issue deferred/closed, no production permission.
Validation: Markdown/source-pointer and git diff review only. Parent's one
independent Review will assess this child with the other stack branches.
