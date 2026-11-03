# Details: issue 233 stage map slice

* Phase 1: `journeyStages` lists the eight atlas stages with their screen id (stage 1 null) and boundary text, matching the trace walkthrough. `journeyStageMap(c)` uses `roleScreens` and `me.user.role` to link or explain, and `screenHref(id, c.id)` to keep the case.
* Phase 2: `test_same_home_stage_map_links_by_role_and_states_deferral` covers Programme Manager (links, deferral, contractor screen not installed) and Retrofit Coordinator (procurement not linked). Trace doc gains a paragraph and a limit bullet; log entry appended.
* Phase 3: unittest for programme screen, role-screen conformance and design-system, content-standard and accessibility baseline modules; atlas checker; ruff; mypy.
