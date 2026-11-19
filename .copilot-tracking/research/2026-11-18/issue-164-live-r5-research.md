# Issue 164 r5 research (2026-11-18)

Task: first unmet DEMO-scope criterion. Unticked criteria that are demo-scope: threshold approval and accountable reviewer (owner decision, not code), serving-model binding (needs actual-model results; blocked), human exercises and real-call authority (production or owner). Code gap found by the r3 live probe: "Send the resident a text message now ..." returned a fallback with no refusal route.

Reproduced offline: `out_of_scope()` in `src/core/src/zava_forward/core/chat_panel.py` (contact pattern) does not match "Send the resident a text message", "Send the resident an email", "Send them a message", "Send an SMS to the resident", WhatsApp, or "Please send Mrs Jones a text message". Cause: the `send` alternative requires the object to follow directly (`send a letter`), and the verb list lacks sms/whatsapp. Planning readiness: Ready.
