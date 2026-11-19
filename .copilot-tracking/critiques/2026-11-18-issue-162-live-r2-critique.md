---
title: Critique of the #162 live isolation plan (r2)
ms.date: 2026-11-18
---

Executed once on the final candidate plan. Verdict: Approve with three compatible findings, applied directly.

| Finding | Disposition |
| --- | --- |
| A spoofed-header test could itself be a risk if direct ingress were open | Applied: it runs through the public Easy Auth URL only, with the staff cookie; if it ever succeeded it would be recorded as a finding, not hidden |
| Memory opt-in changes the test user's state | Applied: record status before, delete only the item created, opt out only when the user had no items and was not opted in |
| Two-user proof is overclaimed if only 404 on fake ids is shown | Applied: state that live cross-user read of a real foreign thread is unproven (one Entra identity); cite local tests as the proof for that part |
| Earlier cleanup deleted unrelated threads | Applied: the script deletes only ids it created and checks counts before and after |
