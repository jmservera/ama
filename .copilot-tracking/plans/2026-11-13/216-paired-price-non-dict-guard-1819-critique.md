# Critique (rubber-duck, one pass): Revise

Applied: reject negative values per field (non-negative check); overflow-safe validation and arithmetic (OverflowError caught, non-finite cost rejected); truthy non-Mapping gets "not a mapping" while falsy values keep the existing "missing" message (tested separately); add usage-field tests including model_calls and offsetting-negative case; assert no authority_decision on malformed input.
