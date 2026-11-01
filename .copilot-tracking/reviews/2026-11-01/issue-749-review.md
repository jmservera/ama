# Review: issue 749 stored chat rules fallback

* Research: ChatPanel._ask (stored path) returned FALLBACK when model is None or fails; the rules answer (chat_case_answers.answer) was wired only in ask_unstored.
* Change: in _ask, a case thread whose reply would be FALLBACK now returns the rules-based grounded answer with case-fact citations, model workflow-only, plus a rules-only note. Out-of-scope refusals, limit-reached, withheld paths are unchanged. Explain-only; no record changes.
* Tests: StoredRulesFallbackTests (fails before fix); core chat tests 118 OK.
* Tier: focused; no SQL, infra or security surface change.
* Outcome: conformant; live redeploy verification remains for the owner.
