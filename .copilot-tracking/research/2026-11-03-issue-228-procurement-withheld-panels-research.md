# Research: issue #228 withheld-items panels (2026-11-03)

Disposition: executed. Planning Readiness: Ready.

Merged delivery (checked with gh): #655 (package queue and job pack screens), #782 (browser keyboard and axe evidence), #820 (corrections and completion records), #793 (tracking only), #496 (shared host). All Refs only; issue open.

Findings:
* Criteria 1 and 2 are met on record by #655 and #782. Criterion 3 is advanced by #820; capture of submission, correction request and acknowledgement still needs supplier-scoped access and BRD OD-47 (security tier).
* Other role screens (#230, #233) render the shared `screenWithheld` "Not shown for this role" panel so absence is not read as nothing recorded. Neither procurement screen does. For criterion 4 the contractor screen only states one sentence about notice reasons.

Smallest slice: add the panel to both procurement screens, text only, from existing helpers. No API, projection or access change, so focused tier.
