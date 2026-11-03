# Research: issue #228 correction and completion record slice (2026-11-03)

Disposition: executed. Planning Readiness: Ready.

Merged delivery (checked with gh): #655 (package queue and job pack screens), #782 (browser keyboard and axe evidence), #793 (tracking only), #496 (shared host). All Refs only; issue open.

Findings:
* `/api/workorders` returns corrections and history to managers only. The contractor projection (`_wo_view`) omits them; widening it would be a security-relevant change and is out of this slice.
* Complete and correct are manager-only actions (`WO_ACTIONS`). A contractor submit endpoint would be a provider portal and needs supplier-scoped access design and BRD OD-47, so it is not built.
* The manager screen hard-coded "Recorded outside this screen" for submission and review; it did not show recorded corrections or completion.

Smallest slice: show recorded corrections and completion from existing GET data, labelled as records not acceptance, with independent review Unknown. Contractor view derives only the Completed state it already receives.
