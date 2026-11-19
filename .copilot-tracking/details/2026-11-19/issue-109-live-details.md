# Details

Gate fields are non-empty `_LABEL` references (no free text, no secrets). The guard checks presence, not truth: R1-R3 completion stays a human/research outcome and R2 reviewer sign-off is not inferred. No SQL, API, UI or infra change; store modules keep working because `research_gate` defaults to None.
