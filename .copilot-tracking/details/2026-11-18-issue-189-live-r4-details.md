# Details r4

Checks (name, pass rule):

* owner_tag: hub tag `owner` is governed text.
* hub_tier: sku name and capacity present; equal to expected values when supplied.
* budget_cap: a Monthly budget with amount above 0.
* alert_actual and alert_forecast: enabled GreaterThan notifications with threshold 0 to 100 (actual) and forecast at or above the actual threshold.
* recipient_reachable: every enabled notification has a contact whose domain is not a noreply, `example.invalid`, `example.com` or `localhost` address; contact groups and roles count as reachable.
* Time limit and live run are out of scope for this verifier (code-proven in `RunMeter`).
