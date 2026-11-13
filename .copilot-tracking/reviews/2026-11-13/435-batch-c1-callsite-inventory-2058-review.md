# Review: 435 C1 call-site inventory (2058)

Executed once by `code-review` on the uncommitted diff. Outcome: approve; one Medium wording finding, fixed in place.

* R1 (Medium, wording): the `INVENTORY` note said the runner "reserves and closes worst-case tokens and cost per call". In `heldout_batch.py` (about lines 291-335) the runner checks a worst-case reserve against the limits before each call, books measured usage on a usable reply, and books the worst case only for an unmeasured reply (then stops). Reworded accordingly; tests, ruff and both mypy runs re-run clean. The research note carries the same loose phrase ("reserves worst-case tokens and cost per call"); it is evidence history and the inventory note is the authoritative text.
* Classification `own-accounting` confirmed accurate; no admission call in `heldout_aoai.py`; invariants hold; direct-call bypass claim is correct.

Assessed boundary: diff of `src/api/tests/test_ai_call_site_inventory.py` plus RPI evidence. Not assessed: hosted CI, complete gate. No open findings; no routed work.
