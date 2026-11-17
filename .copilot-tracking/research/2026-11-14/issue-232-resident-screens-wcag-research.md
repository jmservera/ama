# Research: #232 resident screens WCAG
Disposition: executed. Planning Readiness: Ready.
* Resident choice and service issue screens in role-screens.js already used stateCue prefixes (Confirmed, Waiting for resident, Action needed).
* Missing: keyboard section links and focusable anchored headings; the screenPanel { anchor } and data-jump click handler from #226 can be reused.
* Constraint: literal screenPanel("...") calls must stay for test_connected_home_check.
