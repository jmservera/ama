# Review: issue 344 live (2026-11-21), executed once

Outcome: conformant for the assessed boundary (diff of workflows.py, one test, research note, index, log, evidence).

* Fix is narrow; validation of as_of and limit still raises before the loop; `handoff_ageing` contract and its KeyError test are untouched.
* Test is red without the fix and green with it on both stores.
* The research note does not claim unproven items: criterion 1 browser redirect and criterion 5 stay open; the fix is not deployed.
* Routed follow-ups: owner decision on Return401 and redeploy; deploy this fix; blocked parity rows (#349, #350, #210).
