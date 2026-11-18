# Research: case-domain chat grounding (Refs #164)

* Disposition: executed. Planning Readiness: Ready.
* `src/agents/.../regulatory_chat.py` is the offline regulatory source lookup and is unchanged. Case chat grounding lives in `src/core/.../chat_case_answers.py` and `chat_panel.py`.
* Gap: grant, PAS 2035 sign-off and damp/sensor questions had no rules-first intent. Grant wording fell to the generic `funding` answer or a model draft that could be withheld.
* Case packet keys used: `grants` (role-projected), `technical.signoffs` (PAS 2035 roles via `signoffs.SIGNOFFS`), `documents`/`checklist`, `hazards`, `sensor_review_drafts` (staff projection drops it, so sensor answers rely on damp hazards and survey documents).
* Decision: new rules-first intents `claim`, `pas2035`, `sensor` give `answer_origin=decision_rule` with a text `[Origin: decision_rule]` line. A claim question with no grant record falls through to the funding answer.
