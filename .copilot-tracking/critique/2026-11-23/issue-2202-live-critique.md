# Critique: issue 2202 plan (one pass)

Verdict: approve with direct dispositions.

* Risk: counting `stale` and `offline` as "with readings" may overstate the owner's meaning. Disposition: report both `with_readings` and `recent`, state the definition.
* Risk: assuming unmeasured homes have readings. Disposition: `meets` uses the lower bound only.
* Risk: a tile over 100 homes silently drops homes. Disposition: dropped homes stay `not-loaded` and count as unmeasured; the probe refines tiles.
* Tools-only change, so no src tier escalation.
