<!-- markdownlint-disable-file -->
# Issue 107 R2 usage attribution: details

* `src/core/src/zava_forward/core/ai_consumption.py`: `capability_usage(calls, completions, outputs, reviews, unresolved)`; reuses the report's acceptance rule. Tokens per accepted proposal is `Unknown` unless every accepted root has measured tokens.
* `src/core/tests/test_ai_consumption.py`: two tests.
* Cost per capability is not reported: price and billing stay report-level (BRD OD-51 open).
