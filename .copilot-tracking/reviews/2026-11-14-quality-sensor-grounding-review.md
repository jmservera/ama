# Review: retained sensor values and Quality AI flag grounding (Refs #1288)

Date: 2026-11-14. Execution: executed once. Outcome: conformant for scope.

* Values come only from retained rows already authorised and consent-gated; withheld or denied views yield no values.
* Origin labels are explicit: view and chat are `decision_rule`, the model finding is `generative_model`; the flag does not accept work or decide hazards.
* Dew point and mould risk index are stated as not retained rather than invented.
* Residuals: the `sensor` chat intent is keyword based and precedes other intents; chat text relies on the existing origin footer in `chat.js`; no browser run; independent human review and hosted CI remain required.
