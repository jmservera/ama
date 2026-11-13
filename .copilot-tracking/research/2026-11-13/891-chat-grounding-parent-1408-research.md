# 891 chat grounding parent research

* Read case study, addendum, KB index and memory context (docs-only, no change).
* Child commits 1599446 (core), 4643283 (api web), e7daa01 (agents) share base dafed6a2.
* Source paths disjoint: src/core, src/api web+README, src/agents. Only src/api/tests/test_chat_panel.py is touched by the api child; the parent end-to-end test is added there after merge.
* Tracking files are uniquely named per child; no collisions.
* Planning Readiness: Ready.
