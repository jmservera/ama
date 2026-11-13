# Plan: #216 README field-count fix
1. Edit only `src/agents/README.md`: "nine" -> "ten"; state ids start with a letter or digit.
2. Validate against code (count OBSERVATION_KEYS) and run paired/regulatory suites, ruff, mypy.
3. Independent review, commit (Refs #216, Refs #208).
Critique (rubber-duck, once): Pass. Applied: ids start with letter or digit; pseudonymity format-checked only, not verified. Doc-only without RED test accepted.
