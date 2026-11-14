# 215 keyboard, focus and provenance critique

* Execution: once, independent (rubber-duck agent), on the test-only plan. Verdict: revise.
* Verified safeguards: docked Escape unhides the launcher before focusing it (chat-widget.js hide); the doubt button guards `aria-disabled` activation.
* Finding 1, outcome not attached per reply (chat.js ask handler passes no kind): applied directly. Each assistant reply now carries a persistent "Outcome: ..." line.
* Finding 2, "Answer added" announced for a fallback reply: applied directly. `statusFor` has an explicit fallback sentence.
* Finding 3, withheld label always says "source check" even when withholding came from an action claim or access change (chat.js:84): rejected for this task. The wording is pinned by test_chat_panel.py and the API README; changing it needs a backend reason field. Routed as follow-up.
* Finding 4, static checks are not behaviour: accepted as a stated limit; behavioural browser and assistive-technology checks routed as follow-up.
