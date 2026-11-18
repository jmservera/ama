# Issue #164 Cycle 3: agent test wording alignment

* Cycle-2 independent review (`independent-rev-164-c2-2ecc7a12d.md`) found `test_sensor_question_uses_damp_hazard_and_draft_fields` still asserted "not a diagnosis".
* Changed `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` to assert "do not establish a root cause", matching the redaction-safe `_sensor()` wording.
* Validation: targeted unittest (16 tests) pass; `ruff check` and `ruff format --check` on src/core, src/agents, src/api pass.
* Tier: focused (test-only). Not pushed.
