# Critique 2026-11-23, issue 116 live r11

Executed once. Verdict: proceed.

* Catch `UnicodeEncodeError` inside `approved_payload` and raise `InputRefused("input-type-not-approved")`: compatible, applied; avoids touching callers.
* Alternative of `errors="replace"` encoding would silently alter text; rejected.
* `provider_body` uses `ensure_ascii=True`, so it would serialize surrogates; the boundary check is therefore the right place.
