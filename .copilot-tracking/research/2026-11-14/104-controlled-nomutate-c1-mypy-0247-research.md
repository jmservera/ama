<!-- markdownlint-disable-file -->
# Research: C1 mypy strict typing of the #104 non-mutation test

* Refs #104. Disposition: executed. Planning Readiness: Ready.
* Finding: `mypy` in `src/api` reports 74 strict errors, all in `src/api/tests/test_ai_controlled_record_non_mutation.py` (`no-untyped-def`, `var-annotated`, `no-any-return`, `no-untyped-call`, `attr-defined`).
* `tests/test_assistants.py` (`ta.Base`, `ta.Provider`, `ta.proposal`) and `zava_forward.api.server` are under `ignore_errors` overrides and untyped; sibling files must not change, so calls into them need targeted `# type: ignore[no-untyped-call]` and `cast`.
* `attr-defined` on `chat_text` comes from `self.provider` inferred as `ta.Provider`; a class-level `provider: ScriptedProvider` fixes it.
* Constraint: no weakening of `src/api/pyproject.toml`.
