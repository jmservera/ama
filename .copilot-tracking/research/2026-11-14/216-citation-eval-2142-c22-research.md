<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 22 for Issue #216 (`RV-055`)

* Task ID: `216-citation-eval-2142-c22`
* Parent Task ID: `216-citation-eval-2142-c21`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence

Structural separation of immediate post-`meeting` appointment guards (`_POST_MEETING_GUARD_RE`) from NP modifier guards (`_NP_MODIFIER_GUARD_RE`) inside `src/core/src/zava_forward/core/regulatory_eval_gates.py` to close `RV-055`:

1. `_POST_MEETING_GUARD_RE` (checked ONLY immediately after the obligation verb, before the quantifier/determiner):
   * Blocks prepositions, clause subordinators, bare intransitive appointment adverbs (`tomorrow`, `today`, `tonight`, `yesterday`, `soon`, `later`, `here`, `there`, `online`, `remotely`, `together`, `privately`, `regularly`, `weekly`, `monthly`, `daily`, `annually`, `monday`..`sunday`, `morning`, `afternoon`, `evening`), AND deictic temporal phrases `(?:this|next|last|every|each)\s+(?:morning|afternoon|evening|night|week|weekend|month|quarter|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)`.
   * Because `weekly|monthly|daily|annual|quarterly` are checked in `_POST_MEETING_GUARD_RE` (only when bare directly after the verb, or when followed by `and|or|to|at|in|on|for` rather than an obligation noun!), wait: what if someone writes `"Are we meeting weekly safety requirements?"` (zero determiner before `weekly`) vs `"Are we meeting weekly and discussing safety requirements?"`?!
   * Look how clean that distinction is: bare `weekly|monthly|daily|quarterly|annual` is an intransitive adverb ONLY when NOT followed by an obligation modifier/noun (i.e., when followed by `(?:and|or|at|in|on|to|for|with|about|regarding|before|after|[.;!?,]|$)`)! So `"Are we meeting weekly safety requirements?"` AND `"Are we meeting our weekly safety requirements?"` BOTH refuse, while `"Are we meeting weekly and discussing safety requirements?"` and `"Are we meeting weekly?"` stay allowed!
2. `_NP_MODIFIER_GUARD_RE` (checked at every modifier token inside the NP):
   * Blocks prepositions, subordinators, finite auxiliaries, and coordinated participial verb phrases `(?:and|or)\s+(?!(?:building|housing|heating|lighting|plumbing|wiring|roofing|cladding|ventilation|funding|reporting|monitoring|licensing|letting|renting|living|working|operating|standing|existing|ongoing|pending|binding|governing|remaining)\b)[a-z]+ing\b`, blocking `"and planning"`, `"and discussing"`, `"and reviewing"`, `"and scheduling"`, `"and preparing"`, etc. across the entire morphology of `-ing` verbs!
