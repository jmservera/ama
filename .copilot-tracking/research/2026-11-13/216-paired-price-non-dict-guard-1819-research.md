# Research: paired price non-Mapping guard (Refs #216)

* Disposition: executed (direct code read).
* `cost_per_accepted_check` does `inputs.get("price_source") or {}`; a truthy non-Mapping (str, list, True, 5) then fails on `.get` with AttributeError. Same for `usage`.
* Existing code catches TypeError for non-numeric rates, but bool and non-finite values pass or misbehave; `_number` helper already rejects bool/non-finite.
* Missing nested keys are already named (`price_source.as_of missing`).
* Planning Readiness: Ready.
