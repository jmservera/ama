<!-- markdownlint-disable-file -->
# Issue 1818 live round 7: plan critique (single pass)

Verdict: proceed with amendments.

| ID | Finding | Disposition |
| --- | --- | --- |
| C1 | The round 6 fix is unmerged, so the proof relies on an image not built from main. | Applied: record the image, the branch commit `7bde5f149` and that merging it needs the full tier; do not claim main is ready. |
| C2 | A fresh reading expires after 15 minutes; screenshots must follow the send immediately. | Applied: browser phase runs straight after the job. |
| C3 | Resident home mapping from round 5 may have drifted. | Applied: confirm in the resident view; if absent record as unproven rather than reseeding beyond demo authority. |
| C4 | Ids in notes. | Applied: use home ids already synthetic (`ZF-2025-*`) only; redact object ids, tenant, subscription. |
