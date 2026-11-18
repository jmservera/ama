# Issue 164 r5 details
Change `contact` regex: verbs add sms, whatsapp; add `send\s+(?:{_PERSON}|{_NAMED_PERSON}|them)\s+(?:a|an|the)?\s*(?:text|sms|email|e-mail|message|letter|whatsapp)\b`. Keep the existing alternatives. Negative controls: "Send the report to the file", "What message was sent to the resident?" must not refuse.
