# Plan critique: #134 extension E4

Author critique, one only, not independent. Verdict: Revise, applied.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | A single-pattern discover cannot reproduce the order; the regression must discover both files with one loader in a fresh process. | Applied in plan step 3. |
| 2 | The subprocess regression must not recurse into running the full suite. | Applied: it only loads two named files. |
| 3 | Append leaves core/tests last; a name in api/tests could shadow a helper in standalone runs. | Accepted: canonical layout already orders them; browser run covers standalone use. |
| 4 | Manifest digest claim must rest on a search, not assumption. | Applied: search recorded in research; no digest edit. |
| 5 | RED must use the unchanged 89a5 checker, not a reconstruction. | Applied: copy via git show of the 89a5 file. |
